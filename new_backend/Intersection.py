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
from Helpers import to_numpy_vector
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
            current_vehicle.current_section = current_vehicle.current_section.next_section
            return False, None

        # If it's time to brake
        if current_separation < braking_distance:
            # Select the traffic light that has a stop waypoint that is nearest to the vehicle
            # This assumes that the controlled vehicles are acting rationally, and it may break in some niche cases.
            # Please just trust me that this list comprehension does what it's supposed to
            correct_light_index = min([(i, np.linalg.norm(current_vehicle.get_location_vector() - to_numpy_vector(waypoint.transform.location)))
                                      for (i, light) in enumerate(self.traffic_lights)
                                      for waypoint in light.get_stop_waypoints()], key=lambda x: x[1])[0]
            lane_light = self.traffic_lights[correct_light_index]

            # Check if the light is red
            if lane_light.get_state() in [carla.TrafficLightState.Red, carla.TrafficLightState.Yellow]:

                # Mark the vehicle as stopped at the selected light
                self.vehicles_at_lights[correct_light_index].append(current_vehicle)

                # Grab the possible stopping points in the vehicle's current lane
                possible_stop_points: List[carla.Waypoint] = lane_light.get_stop_waypoints()

                # If there are multiple stopping options, choose the one closer to the Vehicle
                if len(possible_stop_points) > 1:
                    print("Multiple stop points")
                    closest_index = np.argmin([np.linalg.norm(
                                                current_vehicle.get_location_vector() -
                                                to_numpy_vector(x.transform.location))
                                               for x in possible_stop_points])
                    return True, possible_stop_points[closest_index].transform.location

                return True, possible_stop_points[-1].transform.location

        return False, None

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
                            vehicle.current_section = self.next_section
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
