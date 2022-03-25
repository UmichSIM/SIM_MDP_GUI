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

# Library Imports
import carla
import numpy as np
from typing import Dict, List, Tuple


class Intersection:

    def __init__(self, junction: carla.Junction, traffic_lights: List[carla.TrafficLight]):

        # The carla.Junction object that this Intersection corresponds to
        self.junction = junction

        # Dictionary that stores the mapping from OpenDrive lane id to the carla.TrafficLight
        # that affects that OpenDrive lane
        self.lane_to_traffic_light: Dict[int, carla.TrafficLight] = {}

        # Create the mappings from OpenDrive lane to TrafficLight
        for traffic_light in traffic_lights:
            if traffic_light is not None:
                affected_waypoints = traffic_light.get_affected_lane_waypoints()
                for waypoint in affected_waypoints:
                    self.lane_to_traffic_light[waypoint.lane_id] = traffic_light

        print("Done")

    def stop_at_light(self, current_vehicle_waypoint: carla.Waypoint, braking_distance: float) -> Tuple[bool, carla.Location]:
        """
        Determines if the vehicle needs to stop at the light, and gives the vehicle a target location to stop at.

        :param current_vehicle_waypoint: a carla.Waypoint located at the vehicle's current location
        :param braking_distance: a float representing how long the car needs to break
        :return: a Tuple indicating if the vehicle needs to stop at the light and where it should stop
                 if needed
        """

        # Calculate the distance between the vehicle and the intersection
        current_separation = self._distance_between(current_vehicle_waypoint.transform.location)

        if current_separation < braking_distance:
            # Grab the traffic light affecting the current lane
            lane_light: carla.TrafficLight = self.lane_to_traffic_light[current_vehicle_waypoint.lane_id]

            # Check if the light is red
            if lane_light.get_state() in [carla.TrafficLightState.Red, carla.TrafficLightState.Yellow]:
                # Grab the possible stopping points in the vehicle's current lane
                possible_stop_points: List[carla.Waypoint] = [x for x in lane_light.get_affected_lane_waypoints()
                                                              if x.lane_id == current_vehicle_waypoint.lane_id]

                # If there are multiple stopping options, choose the one closer to the Vehicle
                if len(possible_stop_points) > 1:
                    print("Multiple stop points")
                    closest_index = np.argmin([np.linalg.norm(
                                                to_numpy_vector(current_vehicle_waypoint.transform.location) -
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
