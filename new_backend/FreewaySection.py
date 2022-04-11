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

        # List of Vehicles that start at this section (TODO: move this to base section class)
        self.initial_vehicles: List[Vehicle] = []

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
        Determines the waypoints that corresponds with a lane shift
        Runs before the experiment is running

        :param map: the carla.Map that the experiment is running on
        :param curr_vehicle: the current transform of the Vehicle about to shift lanes
        :param direction: a string presenting the direction to shift lanes (left, right, straight)
        :return: a List of carla.Waypoints corresponding with the desired lane shift
        """

        # get location from waypoint, find closest starting lane waypoint to it
        curr_lane = self.get_lane(curr_vehicle, True)

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
        if not self.has_started:
            self.has_started = True

        for vehicle in self.initial_vehicles:
            curr_location = vehicle.get_current_location()
            for ending_waypoint in self.ending_waypoints:
                distance = curr_location.distance(ending_waypoint.transform.location)
                if distance < 0.01:
                    vehicle.target_location = None 
                    vehicle.advance_section()
                    break

        return
    
    #Helper function that calculates  the  curr_lane of vehicle
    def get_lane(self, curr_vehicle: carla.Vehicle, start: bool) -> int:
        minDist = float("inf")
        curr_lane = -1
        lane_loc = None

        for i in range(len(self.starting_waypoints)):

            if start:
                lane_loc = self.starting_waypoints[i].transform.location
            else:
                lane_loc = self.ending_waypoints[i].transform.location
    
            self_loc = curr_vehicle.get_location()
            dist = self_loc.distance(lane_loc)

            if dist < minDist:
                curr_lane = i
                minDist = dist

        return curr_lane 
        
#waypoint of lane and ending waypoint of same lane
# -- configuration: Dict[str, str] in TestExperiment to tell whether a vehicle ging straight or changing
# def lane change -> starting waypoint in one and ending waypoint of other lane
# freewayexperiement -> read dicts and call straight path/change lanes 
#                       (in config dict determine start lane, ending lane[int])
#                       create instance of freeway section (has start/end waypoints of every lane)
#            # in what situations do we want to change lanes: lead car in front moves too slow
#             for every vehicles we find config (which has start and ending lane):
#                 get start lane waypoint and end lane waypoint:
#                     generate path
            # Controller.generate_path(curr_vehicle, starting_waypoint, ending_waypoint)
    #generate path from controller .... 
  