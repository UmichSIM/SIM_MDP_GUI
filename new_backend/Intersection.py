"""
Backend - Intersection Class
Created on Tue February 15, 2022

Summary: The Intersection class represents a single intersection in the Intersection experiment
    type. It is derived from the base Section class. This class is responsible for managing all the
    vehicle that interact in this intersection, along with their specific movements as they
    enter and exit the intersection.

References:
    Section

Referenced By:

"""

# Local Imports
from Helpers import to_numpy_vector, project_forward, angle_difference
from Vehicle import Vehicle

# Library Imports
import carla
import numpy as np
from time import perf_counter
from typing import Dict, List, Tuple


class Intersection:

    # Static ID variable used as a last number to assign Intersection Ids
    id = 0

    def __init__(self, junction: carla.Junction, traffic_lights: List[carla.TrafficLight],
                 green_time: float = 10.0, yellow_time: float = 3.0, first_pair: Tuple = (0, 2),
                 second_pair: Tuple = (1, 3)):

        # Store a local id number identifying the order of the intersection in this experiment
        self.id = Intersection.id
        Intersection.id += 1

        # Vehicles that start at this section (TODO: move this to the base section class)
        self.initial_vehicles: List[Vehicle] = []

        # Store the next intersection that follows sequentially after this one (this will be set by
        # the Experiment::add_section method)
        self.next_section = None

        # The carla.Junction object that this Intersection corresponds to
        self.junction = junction

        # List of all the carla.TrafficLights that affect this intersection
        self.traffic_lights = traffic_lights
        self.has_started = False

        # Dictionary storing the index of each light in the traffic_lights light and a list of
        # all vehicles that are stopped at that traffic light.
        self.vehicles_at_lights: Dict[int, List[Vehicle]] = {}
        for (i, _) in enumerate(self.traffic_lights):
            self.vehicles_at_lights[i] = []

        # Store the light timings in a dictionary for easy retrieval
        self.light_timings: Dict[carla.TrafficLightState, float] = {
            carla.TrafficLightState.Green: green_time,
            carla.TrafficLightState.Yellow: yellow_time,

            # This only defines the overlap where both sets of lights will be red. Otherwise, one
            # pair of lights will remain red until the active pair of lights has finished their cycle
            carla.TrafficLightState.Red: 1.0
        }

        # Store the indexes of the traffic light that make up opposite pairs (opposite pairs of
        # traffic lights will be synced up, the first pair will always start on green)
        self.first_pair: Tuple = first_pair
        self.second_pair: Tuple = second_pair

        # The active pair refers to which pair of traffic lights is currently active. The inactive
        # pair will remain red until the active pair has moved from green -> yellow -> red
        self.active_pair = 'first'

        # Start time used to track how long a light has been in a particular state
        self.start_time: float = None

        # Set the timings for each of the traffic lights
        for (i, light) in enumerate(self.traffic_lights):
            light.freeze(True)
            if i in self.first_pair:
                light.set_state(carla.TrafficLightState.Green)
            else:
                light.set_state(carla.TrafficLightState.Red)

    def stop_at_light(self, current_vehicle: Vehicle, braking_distance: float) -> Tuple[bool, carla.Location]:
        """
        Determines if the vehicle needs to stop at the light, and gives the vehicle a target location to stop at.

        :param current_vehicle: a Vehicle representing the current vehicle
        :param braking_distance: a float representing how long the car needs to break
        :return: a Tuple indicating if the vehicle needs to stop at the light and where it should stop
                 if needed
        """

        # Calculate the "distance" between the vehicle and the intersection, use the L1 norm so we have
        # some sense of direction
        current_separation = self._distance_between(current_vehicle.get_current_location())

        # If the current_separation is negative, then the vehicle is already in the intersection.
        # Simple advance the vehicle to the next section
        if current_separation < 0:
            current_vehicle.advance_section()
            return False, None

        # If it's time to brake
        if current_separation < braking_distance:

            # Determine what light is controlled the current vehicle's lane and the carla.Waypoint
            # that the vehicle needs to stop at
            light_index, stop_waypoint = self.get_stop_location(current_vehicle.get_location_vector())

            debug = self.traffic_lights[light_index].get_state()

            # Check if the light is red
            if self.traffic_lights[light_index].get_state() in [carla.TrafficLightState.Red, carla.TrafficLightState.Yellow]:
                # Mark the vehicle as stopped at the selected light
                self.vehicles_at_lights[light_index].append(current_vehicle)
                return True, stop_waypoint.transform.location

        # Otherwise, it's not time to brake
        return False, None

    def get_stop_location(self, location_vector: np.array) -> Tuple[int, carla.Waypoint]:
        """
        Determines the traffic light that the vehicle should stop at given its current location and lane.

        :param location_vector: the current position of the Vehicle as a np.array
        :return: the index corresponding to the lane's traffic light in the self.traffic_lights list and
                 the carla.Waypoint that the vehicle should stop at when they arrive at the intersection

        """

        # Select the traffic light that has a stop waypoint that is nearest to the vehicle
        # This assumes that the controlled vehicles are acting rationally, and it may break in some niche cases.
        # Please just trust me that this list comprehension does what it's supposed to
        correct_light_index = \
            min([(i, np.linalg.norm(location_vector - to_numpy_vector(waypoint.transform.location)))
                 for (i, light) in enumerate(self.traffic_lights)
                 for waypoint in light.get_stop_waypoints()], key=lambda x: x[1])[0]
        lane_light = self.traffic_lights[correct_light_index]

        # Grab the possible stopping points in the vehicle's current lane
        possible_stop_points: List[carla.Waypoint] = lane_light.get_stop_waypoints()

        # If there are multiple stopping options, choose the one closest to the Vehicle
        if len(possible_stop_points) > 1:
            closest_index = np.argmin([np.linalg.norm(location_vector - to_numpy_vector(x.transform.location))
                                       for x in possible_stop_points])
            return correct_light_index, possible_stop_points[closest_index]

        # If there's only one stopping option, just return that
        return correct_light_index, possible_stop_points[-1]

    def get_thru_waypoints(self, map: carla.Map, current_transform: carla.Transform,
                           direction: str) -> List[carla.Waypoint]:
        """
        Determines the waypoints that corresponds with a particular turn at the intersection

        :param map: the carla.Map that the experiment is running on
        :param current_transform: the current transform of the Vehicle about to turn
        :param direction: a string presenting the direction to turn (either "left" or "right" or "straight")
        :return: a List of carla.Waypoints corresponding with the desired turn
        """

        # Grab all possible pairs of starting -> ending waypoints
        possible_waypoint_pairs: List[Tuple[carla.Waypoint, carla.Waypoint]] = self.junction.get_waypoints(carla.LaneType.Driving)
        possible_starting_waypoints: List[carla.Waypoint] = [pair[0] for pair in possible_waypoint_pairs]

        # Find the closest starting intersection waypoint
        current_location = to_numpy_vector(current_transform.location)
        closest_starting_waypoint_index = np.argmin([
            np.linalg.norm(current_location - to_numpy_vector(waypoint.transform.location))
            for waypoint in possible_starting_waypoints
        ])

        # Reduce the possible number of pairs down to only those that start as the closest waypoint
        starting_waypoint = possible_starting_waypoints[closest_starting_waypoint_index]
        possible_waypoint_pairs = list(
            filter(lambda x: np.linalg.norm(to_numpy_vector(x[0].transform.location) - to_numpy_vector(starting_waypoint.transform.location)) < 1.0,
                   possible_waypoint_pairs)
        )

        # Now determine the target yaw (add the change in angle caused by the maneuver and mod by 360)
        target_yaw = current_transform.rotation.yaw +\
            (90 if direction == "right" else -90 if direction == "left" else 0) % 360

        # Convert negative angles into their positive equivalent
        if target_yaw < 0:
            target_yaw += 360

        # Now, out of the possible pairs, choose the ending waypoint with the yaw closest to the target
        closest_yaw = np.argmin([angle_difference(x[1].transform.rotation.yaw, target_yaw) for x in possible_waypoint_pairs])

        # Make sure that the chosen waypoint has a correct yaw
        thru_waypoint = possible_waypoint_pairs[closest_yaw][1]
        # Absolute values are necessary since Carla uses positive and negative yaws interchangeably for same angle
        yaw_difference = angle_difference(thru_waypoint.transform.rotation.yaw, target_yaw)
        if yaw_difference > 5:
            return None

        # Grab the starting and ending intersection waypoints
        waypoints = [starting_waypoint, thru_waypoint]

        # If the maneuver is a turn,then add a waypoint at the midpoint of the turn to smooth it out and
        # some closely spaced waypoints after the turn to stabilize the vehicle's direction in the new lane
        if direction in ("left", "right"):

            # Midpoint waypoint
            waypoints.insert(1, map.get_waypoint(carla.Location(
                x=starting_waypoint.transform.location.x + ((thru_waypoint.transform.location.x - starting_waypoint.transform.location.x) / 2),
                y=starting_waypoint.transform.location.y + ((thru_waypoint.transform.location.y - starting_waypoint.transform.location.y) / 2),
                z=0.0
            )))

            # Closely spaced waypoints after turn
            for dist in range(4, 20, 2):
                waypoints.append(
                    map.get_waypoint(project_forward(thru_waypoint.transform, dist).location)
                )

        # Then return the waypoints
        return waypoints

    def _distance_between(self, current_location: carla.Location) -> float:
        """
        Calculates the distance between the current_vehicle and the intersection.

        :param current_location: a np.array representing the current location of the Vehicle
        :return: the distance from the Vehicle to the intersection
        """

        # Get the two position vectors
        current_location_vector = to_numpy_vector(current_location)
        junction_location_vector = to_numpy_vector(self.junction.bounding_box.location)

        # Calculate the distance and offset of the size of the intersection
        distance = np.linalg.norm(current_location_vector - junction_location_vector)
        distance -= self.junction.bounding_box.extent.x

        return distance

    def tick(self) -> None:
        """
        Updates the Intersection with each tick of the world.

        Checks the state of each traffic light in the Intersection. For all the lights that are
        currently green, checks if there are any vehicles waiting at that light. If there are waiting
        vehicles, then remove their target location and advance them to the next section to allow them to proceed.
        :return: None
        """

        if not self.has_started:
            self.has_started = True
            self._reset_light_timer()
            # for light in self.traffic_lights:
            #     light.freeze(False)

        # Get a reference to the current pair of lights that are active
        if self.active_pair == 'first':
            current_pair = self.first_pair
            inactive_pair = self.second_pair
        else:
            current_pair = self.second_pair
            inactive_pair = self.first_pair

        # Check to see if the light's state needs to change
        current_state = self.traffic_lights[current_pair[0]].get_state()
        if self._get_elapsed_time() > self.light_timings[current_state]:

            # If the active lights are green, move them to yellow
            if current_state == carla.TrafficLightState.Green:
                for light in [self.traffic_lights[index] for index in current_pair]:
                    light.set_state(carla.TrafficLightState.Yellow)

            # If the active lights are yellow, move them to red
            if current_state == carla.TrafficLightState.Yellow:
                # Set the currently active lights to red
                for light in [self.traffic_lights[index] for index in current_pair]:
                    light.set_state(carla.TrafficLightState.Red)

            # If the active lights are red, activate the next group
            if current_state == carla.TrafficLightState.Red:
                for index, light in [(index, self.traffic_lights[index]) for index in inactive_pair]:
                    light.set_state(carla.TrafficLightState.Green)
                    # When setting a light to green, update the vehicles waiting at that light
                    if len(self.vehicles_at_lights[index]) > 0:
                        for vehicle in self.vehicles_at_lights[index]:
                            vehicle.target_location = None
                            vehicle.advance_section()
                        self.vehicles_at_lights[index] = []
                self.active_pair = 'first' if self.active_pair == 'second' else 'second'

            # Reset the timer
            self._reset_light_timer()

    def _reset_light_timer(self) -> None:
        """
        Resets the start_time whenever the light's change state

        :return: None
        """
        self.start_time = perf_counter()

    def _get_elapsed_time(self) -> float:
        """
        Gets the number of seconds that have elapsed since _reset_light_timer() was last called

        :return: the number of seconds as a float
        """
        return perf_counter() - self.start_time
