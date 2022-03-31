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
# from Controller import Controller
# from Vehicle import Vehicle
#
# # Library Imports
# import carla

# get list of vehicles inside of freeway section -> get starting and ending waypoints of the vehicles to manage their movements
# 2 lane highway (can get left/right lane separately -> start/end waypoints of the lanes) (we build experiement section by section)
# sections facilitate path generation
# generate paths for all vehicles ahead of time (b4 experiment runs)
# for each car, we do shit ???? 
# def car going straight -> starting waypoint of lane and ending waypoint of same lane
# def lane change -> starting waypoint in one and ending waypoint of other lane
# only generating path -> dont fuck with controller
# self.waypoints  (generate path and write waypoints into this (auto?)) / self.trajectory
class FreewaySection:

    def __init__(self, starting_waypoint, ending_waypoint):
        self.starting_waypoint = starting_waypoint
        self.ending_waypoint = ending_waypoint

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
  