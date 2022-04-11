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

#Number of lanes in the freeway going in one direction. Able to change for future customizable maps / experiments
NUM_LANES = 4;

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
        self.starting_waypoints: List[carla.Waypoint] = starting_waypoints
        
        # List of waypoints that represent the end of this section. The index
        # in the list corresponds to the lane number
        self.ending_waypoints: List[carla.Waypoint] = ending_waypoints
        
        
    def get_waypoints(self, map: carla.Map, current_transform: carla.Transform,
                           direction: str) -> List[carla.Waypoint]:
        """
        Determines the waypoints that corresponds with a lane shift
        Runs before the experiment is running

        :param map: the carla.Map that the experiment is running on
        :param current_transform: the current transform of the Vehicle about to shift lanes
        :param direction: a string presenting the direction to shift lanes (left, right, straight)
        :return: a List of carla.Waypoints corresponding with the desired lane shift
        """

        minDist = float("inf");# get location from waypoint, find closest starting lane waypoint to it       
        for i in NUM_LANES:

        # find lane we are in given XXXXX[current_tranform or smth else](curr_lane)

        # new_lane = curr_lane
        # if direction == 'left':
        #   new_lane = curr_lane - 1
        # elif direction == 'right':
        #   new_lane = curr_lane + 1

        # starting_waypoint = starting_waypoints[curr_lane]
        # ending_waypoint = ending_waypoints[new_lane]
        
        # waypoints = [starting_waypoint, ending_waypoint]
        # find waypoints for that lane switch (not a gradual change over the section, but over
        # a given amount of path length)

        pass

# def car going straight -> starting waypoint of lane and ending waypoint of same lane
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
  