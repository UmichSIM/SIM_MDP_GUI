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
import Section

# Library Imports
import carla
from typing import Dict


class Intersection(Section):

    def __init__(self, junction: carla.Junction, first_traffic_light: carla.TrafficLight = None,
                 second_traffic_light: carla.TrafficLight = None, third_traffic_light: carla.TrafficLight = None,
                 fourth_traffic_light: carla.TrafficLight = None):

        # The carla.Junction object that this Intersection corresponds to
        self.junction = junction

        # Dictionary that stores the mapping from OpenDrive lane id to the carla.TrafficLight
        # that affects that OpenDrive lane
        self.lane_to_traffic_light: Dict[int, carla.TrafficLight] = {}

        # Create the mappings from OpenDrive lane to TrafficLight
        for traffic_light in [first_traffic_light, second_traffic_light, third_traffic_light, fourth_traffic_light]:
            if traffic_light is not None:
                affected_waypoints = traffic_light.get_affected_lane_waypoints()
                for waypoint in affected_waypoints:
                    self.lane_to_traffic_light[waypoint.lane_id] = traffic_light
