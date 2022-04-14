"""
Backend - FreewaySection Class
Created on Tue February 15, 2022

Summary: The FreewaySection class represents a single road section in the Freeway experiment
    type. It is derived from the base Section class. This class is responsible for managing all the
    vehicle that interact along this freeway section, along with their specific movements as they
    enter and exit the section.

References:
    Controller 

Referenced By:
    Experiment 

"""

# Local Imports
from Controller import Controller
from Vehicle import Vehicle

# Library Imports
import carla
from typing import List

class FreewaySection:

    # Static ID variable used as a last number to assign Intersection Ids
    id = 0

    def __init__(self, starting_waypoints: List[carla.Waypoint], ending_waypoints: List[carla.Waypoint]):
        
        # Store a local id number identifying the order of the FreewaySection in this experiment
        self.id = FreewaySection.id
        FreewaySection.id += 1

        # Vehicles that start at this section (TODO: move this to the base section class)
        self.initial_vehicles: List[Vehicle] = []

        # List of Vehicles active in this section
        self.active_vehicles: List[Vehicle] = []
        
        # Boolean to init active_vehicles to initial_vehicles at beginning of tick
        self.start = True

        # Store the next intersection that follows sequentially after this one (this will be set by
        # the Experiment::add_section method)
        self.next_section = None

        # List of waypoints that represent the start of this section. The index
        # in the list corresponds to the lane number
        # in order from left to right
        self.starting_waypoints: List[carla.Waypoint] = starting_waypoints
        
        # List of waypoints that represent the end of this section. The index
        # in the list corresponds to the lane number
        self.ending_waypoints: List[carla.Waypoint] = ending_waypoints
        
        
    def get_waypoints(self, curr_vehicle: carla.Vehicle,
                           direction: str) -> List[carla.Waypoint]:
        """
        Determines the starting and ending waypoints that corresponds with a lane shift
        Runs before the experiment is running

        :param curr_vehicle: the current vehicle about to shift lanes
        :param direction: a string presenting the direction to shift lanes (left, right, straight)
        :return: a List of carla.Waypoints corresponding with the desired lane shift
        """

        # get location from waypoint, find closest starting lane waypoint to it
        minDist = float("inf")
        curr_lane = -1
        lane_loc = None
        self_loc = curr_vehicle.get_location()

        for (i, waypoint) in enumerate(self.starting_waypoints):
            lane_loc = waypoint.transform.location
            dist = self_loc.distance(lane_loc)

            if dist < minDist:
                curr_lane = i
                minDist = dist

        new_lane = curr_lane
        if direction == 'left':
           new_lane = curr_lane - 1
        elif direction == 'right':
           new_lane = curr_lane + 1

        starting_waypoint = self.starting_waypoints[curr_lane]
        ending_waypoint = self.ending_waypoints[new_lane]
        
        waypoints = [starting_waypoint, ending_waypoint]

        return waypoints

    def tick(self) -> None :
        if self.start:
            self.active_vehicles = self.initial_vehicles
            self.start = False
        for (i, vehicle) in enumerate(self.active_vehicles):                   
            curr_location = vehicle.get_current_location()
            for ending_waypoint in self.ending_waypoints:
                distance = curr_location.distance(ending_waypoint.transform.location)
                if distance < 1.0:
                    self.vehicles_in_freeway.pop(i)
                    vehicle.advance_section()
                    break