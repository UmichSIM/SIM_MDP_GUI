#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:15:47 2020

@author: shijiliu
"""

import sys
sys.path.append("..")

import carla
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time
import math

import control # the python-control package, install first

from backend.intersection_definition import Intersection, get_traffic_lights
from backend.carla_env import CARLA_ENV # self-written class that provides help functions, should be in the same folder
from configobj import ConfigObj
from backend.multiple_vehicle_control import VehicleControl

import copy


# color for debug use
red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)


class VehicleControlFreeway(VehicleControl):
    def __init__(self, env, vehicle_config, delta_seconds, allow_collision = True):
        super().__init__(env, vehicle_config, delta_seconds, allow_collision = True)
        
    def _obey_safety_distance(self, current_ref_speed):
        # override the _obey_safety_distance method
        has_vehicle_in_front, distance = self.env.check_vehicle_in_front_freeway(self.model_uniquename, self.safety_distance) #self.env.check_vehicle_in_front_freeway(self.model_uniquename, self.safety_distance)
        
        if has_vehicle_in_front and abs(distance) < self.L / 2 + 1.0 and not self.allow_collision:
            # if vehicle is about to collide with other vehicle and collision is not allowed
            # set the vehicle velocity to 0
            abrupt_stop_vel = carla.Vector3D(x = 0,y = 0,z = 0)
            self.env.set_vehicle_velocity(self.model_uniquename, abrupt_stop_vel) # set the velocity of vehicle
        
        
        if has_vehicle_in_front: 
            #print("---")
            #print("safety_distance: ", self.safety_distance)
            #print("distance with previous vehicle ", distance)
            return 0.0
        
        return current_ref_speed
    




class FullPathVehicleControl(VehicleControlFreeway):
    def __init__(self, env, vehicle_config, delta_seconds, allow_collision = True):
        super().__init__(env,vehicle_config,delta_seconds, allow_collision = True)
        
        # store the subject trajectory and left trajectory
        self.subject_trajectory = copy.copy(self.vehicle_config["subject_trajectory"])
        self.subject_ref_speed = copy.copy(self.vehicle_config["subject_ref_speed_list"])
        self.subject_max_ref_speed = copy.copy(self.vehicle_config["subject_max_speed_list"])
        self.subject_min_ref_speed = copy.copy(self.vehicle_config["subject_min_speed_list"])
        
        self.left_trajectory = copy.copy(self.vehicle_config["left_trajectory"])
        self.left_ref_speed = copy.copy(self.vehicle_config["left_ref_speed_list"])
        self.left_max_ref_speed = copy.copy(self.vehicle_config["left_max_speed_list"])
        self.left_min_ref_speed = copy.copy(self.vehicle_config["left_min_speed_list"])
        
        # store the current lane of the vehicle
        self.current_lane = copy.copy(self.vehicle_config["current_lane"])
        
        # store the local time of the section the vehicle is in
        self.local_time = 0.0
        
        # store the time the vehicle is going to take command, (command should be "lane")
        self.command_start_time = self.vehicle_config["command_start_time"]
        
        # store time steps after executing the change lane command
        self.lane_change_step = 0
        
        # store variable for deciding whether the vehicle should change lane
        self.lane_change_available = False
        
    def _change_lane(self):
        '''
        order the vehicle to change its lane

        Returns
        -------
        None.

        '''
        # check whether the vehicle is safe to change lane
        if not self.lane_change_available:
            if self.current_lane == "subject":
                has_vehicle_in_left, distance = self.env.check_vehicle_in_left(self.model_uniquename, safety_distance = 20)
                
                print("--------")
                print("has_vehicle_in_left : ", has_vehicle_in_left)
                print("distance: ", distance)
                if has_vehicle_in_left:
                    if distance < 0:
                        self.ref_speed_list = copy.copy(self.subject_max_ref_speed) # accelerate to max speed if the close vehicle is behind
                                                                                    # the current vehicle
                    else:
                        self.ref_speed_list = copy.copy(self.subject_min_ref_speed) # deccelerate to min speed if the close vehicle is in
                                                                                    # front of the current vehicle
                    return # only change speed, don't change lane
                else:
                    self.lane_change_available = True # no close vehicle in left lane, enable lane change
            else:
                # vehicle currently in right lane
                has_vehicle_in_right, distance = self.env.check_vehicle_in_right(self.model_uniquename, safety_distance = 20)
                
                print("--------")
                print("has_vehicle_in_right : ", has_vehicle_in_right)
                print("distance: ", distance)
                
                if has_vehicle_in_right:
                    if distance < 0:
                        self.ref_speed_list = copy.copy(self.left_max_ref_speed) # accelerate to max speed if the close vehicle is behind
                                                                                    # the current vehicle
                    else:
                        self.ref_speed_list = copy.copy(self.left_min_ref_speed) # deccelerate to min speed if the close vehicle is in
                                                                                 # front of the current vehicle
                    return # only change speed, don't change lane                                                   
                else:
                    self.lane_change_available = True # no close vehicle in left lane, enable lane change
        
        
        
        if self.lane_change_step == 0:
            if self.current_lane == "subject":
                self.trajectory = copy.copy(self.left_trajectory)
                self.ref_speed_list = copy.copy(self.left_ref_speed)
                self.current_lane = "left"
            else:
                self.trajectory = copy.copy(self.subject_trajectory)
                self.ref_speed_list = copy.copy(self.subject_ref_speed)
                self.current_lane = "subject"
            self.lane_change_step += 1
            self.Lfc = 15.0 # set a large look ahead distance when changing the lane
        elif self.lane_change_step > 0 and self.lane_change_step < 15:
            self.lane_change_step += 1
        else:
            self.command = "speed" # have changed the lane, change the mode to speed
            self.lane_change_step = 0
            self.Lfc = 4.0 # change the look ahead distance back to its original value
            self.lane_change_available = False
        
    def update_local_time(self, local_time):
        # update the local time of the section the vehicle is in
        # the time is used to decide whether the vehicle is going to 
        # change direction
        self.local_time = local_time
        if self.command == "lane" and self.command_start_time <= self.local_time:
            self._change_lane()

        elif self.command == "distance" and self.command_start_time <= self.local_time:
            self._keep_distance()
            
        else:
            self._keep_speed()
            
    def _keep_speed(self):
        if self.current_lane == "subject":
            self.ref_speed_list = copy.copy(self.subject_ref_speed) # accelerate to the max speed
        elif self.current_lane == "left":
            self.ref_speed_list = copy.copy(self.left_ref_speed) # accelerate to the max speed
    
    def _keep_distance(self):
        pass

class LeadFollowVehicleControl(FullPathVehicleControl):
    def __init__(self, env, vehicle_config, delta_seconds, allow_collision = True):
        super().__init__(env, vehicle_config, delta_seconds, allow_collision = True)
        
        # store the vehicle type
        self.vehicle_type = self.vehicle_config["vehicle_type"]
    
        
        # store the constant distance
        self.lead_follow_distance = self.vehicle_config["lead_follow_distance"]
        if self.vehicle_type == "lead":
            self.lead_follow_distance = - self.lead_follow_distance # if the vehicle is of "lead" type, the lead distance is negative
        self.lead_follow_far_limit = 1.05 * self.lead_follow_distance
        self.lead_follow_close_limit = 0.95 * self.lead_follow_distance
    
    
        # store variable indicating whether the current vehicle and the ego vehicle are within desired range
        self.within_desired_range = False
    
    def update_distance_with_ego(self, ego_transform):
        ego_location = ego_transform.location
        
        # get local location
        local_transform = self.env.get_transform_3d(self.model_uniquename)
        local_location = local_transform.location
        forward_vector = local_transform.get_forward_vector()
        forward_vector_2d = np.array([forward_vector.x,forward_vector.y])
        unit_forward_vector_2d =  forward_vector_2d / np.linalg.norm(forward_vector_2d)
        
        vec_loc_target = np.array([ego_location.x - local_location.x,ego_location.y - local_location.y])
        distance = np.dot(vec_loc_target,unit_forward_vector_2d)
        
        self.distance_with_ego = distance
    
    def _keep_distance(self):
        # keep constant distance between the current vehicle and the ego vehicle
        if self.vehicle_type == "lead":
            # for lead vehicle, check if there exists vehicle in the back
            has_vehicle_in_back, distance = self.env.check_vehicle_in_back_freeway(self.model_uniquename,abs(self.lead_follow_distance) * 4 + self.safety_distance * 4) # use a large distance
            #print("---lead---")
            #print("distance with back vehicle ", distance)
            if has_vehicle_in_back:
                if abs(self.distance_with_ego) > abs(distance) + 1.0: # there exists at least one vehicle between current vehicle and lead vehicle
                    self.command = "speed"                            # give up keeping constant distance, keep constant speed
                    print("give up distance mode")
                    if self.current_lane == "subject":
                        self.ref_speed_list = copy.copy(self.subject_ref_speed) # keep constant speed
                    elif self.current_lane == "left":
                        self.ref_speed_list = copy.copy(self.left_ref_speed) # keep constant speed
                     
                    # set the vehicle speed
                    local_transform = self.env.get_transform_3d(self.model_uniquename)
                    forward_vector = local_transform.get_forward_vector()
                    vehicle_velocity = carla.Vector3D(x = forward_vector.x * self.subject_ref_speed[0], y = forward_vector.y * self.subject_ref_speed[0], z = forward_vector.z * self.subject_ref_speed[0])
                    self.env.set_vehicle_velocity(self.model_uniquename , vehicle_velocity) # set the velocity
                    return
            
            if self.distance_with_ego <= self.lead_follow_far_limit: # the vehicle is leading the ego vehicle and far away
                # deccelerate
                if self.current_lane == "subject":
                    self.ref_speed_list = copy.copy(self.subject_min_ref_speed) # decelerate to the min speed
                elif self.current_lane == "left":
                    self.ref_speed_list = copy.copy(self.left_min_ref_speed) # decelerate to the min speed
                    
                self.within_desired_range = False
            
            elif self.distance_with_ego > self.lead_follow_close_limit and self.distance_with_ego < 0: # the vehicle is leading 
                                                                                                       # and close to ego
                # accelerate
                if self.current_lane == "subject":
                    self.ref_speed_list = copy.copy(self.subject_max_ref_speed) # accelerate to the max speed
                elif self.current_lane == "left":
                    self.ref_speed_list = copy.copy(self.left_max_ref_speed) # accelerate to the max speed
            
                self.within_desired_range = False
            
            else:
                # vehicle within expected range or lead vehicle behind the ego vehicle, which could happen due to change lane
                # keep normal navigation speed
                if self.current_lane == "subject":
                    self.ref_speed_list = copy.copy(self.subject_ref_speed) # keep constant speed
                elif self.current_lane == "left":
                    self.ref_speed_list = copy.copy(self.left_ref_speed) # keep constant speed
            
                if self.within_desired_range == False: # just come into the desired range, set the speed
                    local_transform = self.env.get_transform_3d(self.model_uniquename)
                    forward_vector = local_transform.get_forward_vector()
                    vehicle_velocity = carla.Vector3D(x = forward_vector.x * self.subject_ref_speed[0], y = forward_vector.y * self.subject_ref_speed[0], z = forward_vector.z * self.subject_ref_speed[0])
                    self.env.set_vehicle_velocity(self.model_uniquename , vehicle_velocity) # set the velocity
                
                self.within_desired_range = True
            
            

            
        else: # "follow" vehicle
           # for follow vehicle, check if there exists vehicle in the front
            has_vehicle_in_front, distance = self.env.check_vehicle_in_front_freeway(self.model_uniquename, abs(self.lead_follow_distance))
            if has_vehicle_in_front: # has vehicle in front that is not the ego vehicle
                if abs(self.distance_with_ego) > abs(distance) + 1.0: # there exists at least one vehicle between current vehicle and lead vehicle
                    self.command = "speed"                            # give up keeping constant distance, keep constant speed
                    
                    if self.current_lane == "subject":
                        self.ref_speed_list = copy.copy(self.subject_ref_speed) # keep constant speed
                    elif self.current_lane == "left":
                        self.ref_speed_list = copy.copy(self.left_ref_speed) # keep constant speed
                    return
        
            if self.distance_with_ego >= self.lead_follow_far_limit: # the vehicle is following the ego vehicle and far away
                # accelerate
                if self.current_lane == "subject":
                    self.ref_speed_list = copy.copy(self.subject_max_ref_speed) # accelerate to the max speed
                elif self.current_lane == "left":
                    self.ref_speed_list = copy.copy(self.left_max_ref_speed) # accelerate to the max speed
                self.within_desired_range = False
            
            elif self.distance_with_ego < self.lead_follow_close_limit and self.distance_with_ego > 0: # the vehicle is following 
                                                                                                       # and close to ego
                # deccelerate
                if self.current_lane == "subject":
                    self.ref_speed_list = copy.copy(self.subject_min_ref_speed) # decelerate to the min speed
                elif self.current_lane == "left":
                    self.ref_speed_list = copy.copy(self.left_min_ref_speed) # decelerate to the min speed
                self.within_desired_range = False
            
            else:
                # vehicle within expected range or follow vehicle before the ego vehicle, which could happen due to change lane
                # keep normal navigation speed
                if self.current_lane == "subject":
                    self.ref_speed_list = copy.copy(self.subject_ref_speed) # keep constant speed
                elif self.current_lane == "left":
                    self.ref_speed_list = copy.copy(self.left_ref_speed) # keep constant speed
    
                if self.within_desired_range == False: # just come into the desired range, set the speed
                    local_transform = self.env.get_transform_3d(self.model_uniquename)
                    forward_vector = local_transform.get_forward_vector()
                    vehicle_velocity = carla.Vector3D(x = forward_vector.x * self.subject_ref_speed[0], y = forward_vector.y * self.subject_ref_speed[0], z = forward_vector.z * self.subject_ref_speed[0])
                    self.env.set_vehicle_velocity(self.model_uniquename , vehicle_velocity) # set the velocity
                
                self.within_desired_range = True
            
    
    
        #print("distance with ego == ", self.distance_with_ego)