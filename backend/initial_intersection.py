#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:12:58 2020

@author: shijiliu
"""
import sys
sys.path.append("..")

import carla
import time

from backend.generate_path_omit_regulation import generate_path
from backend.intersection_definition import Intersection, get_traffic_lights, get_trajectory, smooth_trajectory
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


# Really not sure if this needs to be a separate intersection class
class Init_Intersection(Intersection):
    def __init__(self, env, world_pos, traffic_light_list, waypoint_list, subject_traffic_light_list, navigation_speed = 10.0):
        super().__init__(env, world_pos, traffic_light_list,navigation_speed = navigation_speed)
        self.waypoint_list = waypoint_list
        self.start_sim = True # the init intersection will start as soon as the simulation begins
        self.subject_traffic_light_list = subject_traffic_light_list
        self.subject_traffic_light_list.insert(0,self.subject_light)
        
        # 3 special vehicles
        self.ego_vehicle = None
        self.lead_vehicle = None
        self.follow_vehicle = None
        
        # generate the full path that's going to be shared between the ego, lead and follow vehicles
        self._generate_intersection_path()

    # Intersection Class
    def add_ego_vehicle(self, gap = 10.0,model_name = "vehicle.tesla.model3", stop_choice = "abrupt", penetrate_distance = None, obey_traffic_lights = True, run = True, safety_distance = 0.0, vehicle_color = None):
        
        self._add_full_path_vehicle("ego",gap = gap, model_name = model_name, obey_traffic_lights = obey_traffic_lights, run = run, safety_distance = safety_distance, vehicle_color = vehicle_color)
        self.ego_vehicle["lead_distance"] = 0.0
        self.ego_vehicle["follow_distance"] = 0.0
        self.ego_vehicle["index"] = len(self.subject_vehicle) - 1 # the index of the ego vehicle in the subject
        self.ego_vehicle["vehicle_type"] = "ego"
        self.ego_vehicle["stop_choice"] = stop_choice
        self.ego_vehicle["penetrate_distance"] = penetrate_distance
        self.ego_vehicle["stop_ref_point"] = self._generate_full_path_stop_ref(stop_choice,penetrate_distance)
        
        return self.ego_vehicle['uniquename']

    # Intersection class
    def add_lead_vehicle(self, lead_distance ,gap = 10.0,model_name = "vehicle.tesla.model3", stop_choice = "abrupt", penetrate_distance = None, obey_traffic_lights = True, run = True, safety_distance = 15.0, vehicle_color = None):
        # get all the vehicles that's going to be after the lead vehicle
        ego_index = self.ego_vehicle["index"]
        vehicle_after_lead = self.subject_vehicle[ego_index : ]
        self.ego_vehicle["lead_distance"] = lead_distance
        shift_distance = -(gap + 5) # should be gap + model length
        
        # shift all vehicles starting from the ego vehicle
        self._shift_vehicles(shift_distance,index = ego_index)
        
        # only keep the vehicle before the ego 
        self.subject_vehicle = self.subject_vehicle[:ego_index] 
        
        # add the lead vehicle
        self._add_full_path_vehicle("lead",gap = gap, model_name = model_name, obey_traffic_lights = obey_traffic_lights, run = run, safety_distance = safety_distance, vehicle_color = vehicle_color)
    
        # put back ego and vehicles after ego
        self.subject_vehicle += vehicle_after_lead
        
        # generate path for ego vehicle
        start_waypoint = self.ego_vehicle["ref_waypoint"]
        trajectory, ref_speed_list = self._generate_full_path(start_waypoint)
        self.ego_vehicle["trajectory"] = trajectory
        self.ego_vehicle["ref_speed_list"] = ref_speed_list
    
        self.lead_vehicle["vehicle_type"] = "lead"
        self.ego_vehicle["index"] = ego_index + 1 # add one car in front of ego vehicle
        
        # stop settings for lead
        self.lead_vehicle["stop_choice"] = stop_choice
        self.lead_vehicle["penetrate_distance"] = penetrate_distance
        self.lead_vehicle["stop_ref_point"] = self._generate_full_path_stop_ref(stop_choice,penetrate_distance)
        return self.lead_vehicle['uniquename']

    # Intersection Class
    def add_follow_vehicle(self, follow_distance ,gap = 10.0,model_name = "vehicle.tesla.model3", stop_choice = "abrupt", penetrate_distance = None, obey_traffic_lights = True, run = True, safety_distance = 15.0, vehicle_color = None):
        # get all the vehicles that's going to be after the lead vehicle
        ego_index = self.ego_vehicle["index"]
        vehicle_after_ego = self.subject_vehicle[ego_index + 1 : ]
        self.ego_vehicle["follow_distance"] = follow_distance
        shift_distance = -(gap + 5) # should be gap + model length
        
        # shift all vehicles starting after the ego vehicle
        self._shift_vehicles(shift_distance,index = ego_index + 1)
        
        # only keep the vehicle until the ego 
        self.subject_vehicle = self.subject_vehicle[:ego_index + 1]
        
        # add the follow vehicle
        self._add_full_path_vehicle("follow",gap = gap, model_name = model_name, obey_traffic_lights = obey_traffic_lights, run = run, safety_distance = safety_distance, vehicle_color = vehicle_color)
        
        # put back vehicles after follow
        self.subject_vehicle += vehicle_after_ego
        
    
        self.follow_vehicle["vehicle_type"] = "follow"
        
        # stop settings for follow vehicle
        self.follow_vehicle["stop_choice"] = stop_choice
        self.follow_vehicle["penetrate_distance"] = penetrate_distance
        self.follow_vehicle["stop_ref_point"] = self._generate_full_path_stop_ref(stop_choice,penetrate_distance)
        return self.follow_vehicle['uniquename']


    # Intersection Class (figure out if full_path vehicles need to be separated out)
    def _add_full_path_vehicle(self, vehicle_type, gap = 10.0,model_name = "vehicle.tesla.model3", obey_traffic_lights = True, run = True, safety_distance = 0.0, vehicle_color = None):
        '''
        

        Parameters
        ----------
        vehicle_type : string
            the type of the vehicle, valid input values are "ego","lead","follow"
        
        gap : float, optional
            initial distance between this vehicle and the vehicle in front of it/ border. The default is 10.0.
        model_name : string, optional
            vehicle model. The default is "vehicle.tesla.model3".
        obey_traffic_lights : bool, optional
            whether ego vehicle obeys traffic light. The default is True.
        run : bool, optional
            whether ego vehicle starts immediately. The default is True.
        safety_distance : float, optional
            safety distance between ego vehicle and other vehicle. The default is 0.0 since ego vehicle is allowed to crash

        Returns
        -------
        None.

        '''
        right_shift_value = 0.0#1.6
        
        vehicle = ConfigObj()
        
        if vehicle_type == "ego":
            self.ego_vehicle = vehicle
        elif vehicle_type == "lead":
            self.lead_vehicle = vehicle
        elif vehicle_type == "follow":
            self.follow_vehicle = vehicle
        
        
        vehicle["model"] = model_name
        vehicle["gap"] = gap
        vehicle["obey_traffic_lights"] = obey_traffic_lights
        vehicle["run"] = run
        vehicle["safety_distance"] = safety_distance
        vehicle["command"] = "straight"
        vehicle["traffic_light"] = self.subject_traffic_light_list
        ref_waypoint = self.subject_lane_ref
        vehicle_set = self.subject_vehicle
        
        if len(vehicle_set) != 0:
            ref_waypoint = vehicle_set[-1]["ref_waypoint"]
            #previous_uniquename = vehicle_set[-1]["uniquename"]
            #bb = self.env.get_vehicle_bounding_box(previous_uniquename)
            bb = vehicle_set[-1]["bounding_box"]
            
            right_shift_value = right_shift_value #- bb.y / 2
            
            
            
            curr_length = self.env.get_vehicle_model_length(model_name)
            
            gap += bb.x / 2 + curr_length / 2
        

        # use the original reference point to get the new reference point
        # reference point is in the middle of the lane
        # function same as self._get_next_waypoint
        forward_vector = ref_waypoint.transform.get_forward_vector()

        location = ref_waypoint.transform.location
        raw_spawn_point = carla.Location(x = location.x - gap * forward_vector.x  , y = location.y - gap * forward_vector.y , z = location.z + 0.1)
        
        new_ref_waypoint = self.carla_map.get_waypoint(raw_spawn_point)
        
        # right shift the spawn point
        # right is with respect to the direction of vehicle navigation
        ref_yaw = new_ref_waypoint.transform.rotation.yaw
        
        right_vector = self._get_unit_right_vector(ref_yaw)
        
        new_location = new_ref_waypoint.transform.location
        
        spawn_location = carla.Location(x = new_location.x - right_shift_value * right_vector[0], y = new_location.y -  right_shift_value * right_vector[1], z = new_location.z + 0.2)
        spawn_rotation = new_ref_waypoint.transform.rotation
        
        uniquename = self.env.spawn_vehicle(model_name = model_name,spawn_point = carla.Transform(spawn_location,spawn_rotation), color = vehicle_color) 
        vehicle["uniquename"] = uniquename
        vehicle["ref_waypoint"] = new_ref_waypoint
        vehicle["location"] = spawn_location
        vehicle["rotation"] = spawn_rotation
        if vehicle_color == None:
            vehicle["vehicle_color"] = vehicle_color
        else:
            vehicle["vehicle_color"] = vehicle_color.replace(',',';') # replace , by ; to avoid error when importing from file
        
        # generate the full path
        trajectory, ref_speed_list = self._generate_full_path(new_ref_waypoint)
        
        vehicle["trajectory"] = trajectory
        vehicle["ref_speed_list"] = ref_speed_list
        
        # get the bounding box of the new vehicle
        
        new_bb = self.env.get_vehicle_bounding_box(uniquename)
        vehicle["bounding_box"] = new_bb
        
        vehicle_set.append(vehicle)

    # Controller class
    def _generate_full_path_stop_ref(self, stop_choice, penetrate_distance):
        '''
        generate the reference point for stoping the vehicle

        Returns
        -------
        stop_ref_list : list [(float,float),(float,float),...]
            a list of stop reference points

        '''
        
        
        stop_ref_waypoint = []
        stop_ref_waypoint.append(self.subject_lane_ref)
        
        stop_ref_list = []
        
        for ii in range(0,len(self.waypoint_list),3):
            stop_ref_waypoint.append(self.waypoint_list[ii]) # the first point of each intersection
        
        if stop_choice == "normal":
            for ref_waypoint in stop_ref_waypoint:
                stop_point = self._get_next_waypoint(ref_waypoint,distance = -3.0)
                stop_ref_list.append(stop_point.transform)
        elif stop_choice == "penetrate":
            for ref_waypoint in stop_ref_waypoint:
                stop_point = self._get_next_waypoint(ref_waypoint,distance = penetrate_distance)
                stop_ref_list.append(stop_point.transform)
        else:
            for ref_waypoint in stop_ref_waypoint:
                stop_ref_list.append(ref_waypoint.transform)
        
        return stop_ref_list

    # Controller class
    def _generate_intersection_path(self):
        '''
        generate the path from the initial intersection to the end intersection

        Returns
        -------
        None.

        '''
        first_waypoint = self.subject_lane_ref
        second_waypoint = self.ahead_in[0] # can also be [1], choosing the left lane
        third_waypoint = self._get_next_waypoint(second_waypoint,30)
        waypoint_list = copy.copy(self.waypoint_list)
        waypoint_list.insert(0,third_waypoint)
        waypoint_list.insert(0,second_waypoint)
        waypoint_list.insert(0,first_waypoint)
        
        full_trajectory = generate_path(self.env, waypoint_list[0] , waypoint_list[1], waypoint_separation = 4)
        for ii in range(1,len(waypoint_list) - 1):
            trajectory = generate_path(self.env, waypoint_list[ii] , waypoint_list[ii + 1], waypoint_separation = 4)
            full_trajectory += trajectory[1:]
            
        self.intersection_trajectory = full_trajectory
        
    # Controller class
    def _generate_full_path(self,start_waypoint):
        '''
        

        Parameters
        ----------
        start_waypoint : carla.Waypoint
            initial waypoint of the vehicle.

        Returns
        -------
        None.

        '''
        color = cyan
        
        trajectory = generate_path(self.env,  start_waypoint, self.subject_lane_ref, waypoint_separation = 4)
        
        full_trajectory = trajectory + self.intersection_trajectory[1:]
        
        whole_trajectory = [((pt[0],pt[1]),10.0) for pt in full_trajectory]
        
        smoothed_full_trajectory, ref_speed_list = get_trajectory(whole_trajectory) 
        
        if self.DEBUG_TRAJECTORY:
            for ii in range(1,len(smoothed_full_trajectory)):
                loc1 = carla.Location(x = smoothed_full_trajectory[ii - 1][0], y = smoothed_full_trajectory[ii - 1][1], z = 0.0)
                loc2 = carla.Location(x = smoothed_full_trajectory[ii][0], y = smoothed_full_trajectory[ii][1], z = 0.0)
                self.env.world.debug.draw_arrow(loc1, loc2, thickness = 0.05, arrow_size = 0.1, color = color, life_time=0.0, persistent_lines=True)
                
        return smoothed_full_trajectory, ref_speed_list
    
    # Intersection class
    def export_settings(self):
        '''
        export all settings for a specific intersection
        note: this method overrides the method in Intersection
              by not exporting the settings for subject lane


        Returns
        -------
        intersection_settings : ConfigObj
            settings of the intersection

        '''
        intersection_settings = ConfigObj()
        
        # general
        intersection_settings["navigation_speed"] = self.navigation_speed
        
        # vehicles
        intersection_settings["subject_vehicle"] = []
        intersection_settings["left_vehicle"] = []
        intersection_settings["right_vehicle"] = []
        intersection_settings["ahead_vehicle"] = []
        
        # do not export subject lane settings
        '''
        for vehicle in self.subject_vehicle:
            # deep copy the vehicle settings
            new_vehicle = self._copy_vehicle_settings(vehicle)
            intersection_settings["subject_vehicle"].append(new_vehicle)
        '''
        
        for vehicle in self.left_vehicle:
            # deep copy the vehicle settings
            new_vehicle = self._copy_vehicle_settings(vehicle)
            intersection_settings["left_vehicle"].append(new_vehicle)
            
        for vehicle in self.right_vehicle:
            # deep copy the vehicle settings
            new_vehicle = self._copy_vehicle_settings(vehicle)
            intersection_settings["right_vehicle"].append(new_vehicle)
            
        for vehicle in self.ahead_vehicle:
            # deep copy the vehicle settings
            new_vehicle = self._copy_vehicle_settings(vehicle)
            intersection_settings["ahead_vehicle"].append(new_vehicle)
        
        # lights
        intersection_settings["subject_light"] = copy.copy(self.light_config["subject"])
        intersection_settings["subject_light_time"] = copy.copy(self.light_config["subject_time"])
        
        intersection_settings["left_light"] = copy.copy(self.light_config["left"])
        intersection_settings["left_light_time"] = copy.copy(self.light_config["left_time"])
        
        intersection_settings["right_light"] = copy.copy(self.light_config["right"])
        intersection_settings["right_light_time"] = copy.copy(self.light_config["right_time"])
        
        intersection_settings["ahead_light"] = copy.copy(self.light_config["ahead"])
        intersection_settings["ahead_light_time"] = copy.copy(self.light_config["ahead_time"])
        
        return intersection_settings

    # Intersection class
    def import_settings(self,intersection_settings):
        '''
        note: this method overrides the import_settings in Intersection
              by add the part of removing the ego, lead and follow vehicle
        
        Parameters
        ----------
        intersection_settings : ConfigObj
            the intersection settings we want to import

        Returns
        -------
        new_intersection_setting : ConfigObj
            settings of the intersection
            this will be generated by call self.export_settings() after finishing import
            output these settings are for the purpose of creating the front-end gui
        '''
        
        # remove ego, lead and follow settings 
        self.ego_vehicle = None
        self.lead_vehicle = None
        self.follow_vehicle = None
        
        # remove all vehicle in this intersection 
        # if any vehicle has been added
        for ii in range(len(self.subject_vehicle) - 1, -1, -1): # go through the array in reverse order
            uniquename = self.subject_vehicle[ii]['uniquename']
            self.remove_vehicle(uniquename)
        
        for ii in range(len(self.left_vehicle) - 1, -1, -1): # go through the array in reverse order
            uniquename = self.left_vehicle[ii]['uniquename']
            self.remove_vehicle(uniquename)
            
        for ii in range(len(self.right_vehicle) - 1, -1, -1): # go through the array in reverse order
            uniquename = self.right_vehicle[ii]['uniquename']
            self.remove_vehicle(uniquename)
            
        for ii in range(len(self.ahead_vehicle) - 1, -1, -1): # go through the array in reverse order
            uniquename = self.ahead_vehicle[ii]['uniquename']
            self.remove_vehicle(uniquename)
        
        # import all settings
       
        self.navigation_speed = float(intersection_settings["navigation_speed"])
       
        '''
        for vehicle_config in intersection_settings["subject_vehicle"]:
            # add vehicles according to imported settings
            self.add_vehicle(gap = vehicle_config["gap"], 
                             model_name = vehicle_config["model"], 
                             choice = vehicle_config['choice'], 
                             command = vehicle_config['command'],
                             stop_choice = vehicle_config['stop_choice'],
                             penetrate_distance = vehicle_config['penetrate_distance'],
                             obey_traffic_lights = vehicle_config['obey_traffic_lights'],
                             run = vehicle_config['run'],
                             safety_distance = vehicle_config['safety_distance'],
                             vehicle_color = vehicle_config['vehicle_color'].replace(';',','))
        '''
        
        for vehicle_config in intersection_settings["left_vehicle"]:
            # add vehicles according to imported settings
            if vehicle_config['vehicle_color'] != None:
                vehicle_config['vehicle_color'] = vehicle_config['vehicle_color'].replace(';',',')
            
            self.add_vehicle(gap = vehicle_config["gap"], 
                             model_name = vehicle_config["model"], 
                             choice = vehicle_config['choice'], 
                             command = vehicle_config['command'],
                             stop_choice = vehicle_config['stop_choice'],
                             penetrate_distance = vehicle_config['penetrate_distance'],
                             obey_traffic_lights = vehicle_config['obey_traffic_lights'],
                             run = vehicle_config['run'],
                             safety_distance = vehicle_config['safety_distance'],
                             vehicle_color = vehicle_config['vehicle_color'])
            
        for vehicle_config in intersection_settings["right_vehicle"]:
            # add vehicles according to imported settings
            if vehicle_config['vehicle_color'] != None:
                vehicle_config['vehicle_color'] = vehicle_config['vehicle_color'].replace(';',',')
            
            self.add_vehicle(gap = vehicle_config["gap"], 
                             model_name = vehicle_config["model"], 
                             choice = vehicle_config['choice'], 
                             command = vehicle_config['command'],
                             stop_choice = vehicle_config['stop_choice'],
                             penetrate_distance = vehicle_config['penetrate_distance'],
                             obey_traffic_lights = vehicle_config['obey_traffic_lights'],
                             run = vehicle_config['run'],
                             safety_distance = vehicle_config['safety_distance'],
                             vehicle_color = vehicle_config['vehicle_color'])
            
        for vehicle_config in intersection_settings["ahead_vehicle"]:
            # add vehicles according to imported settings
            if vehicle_config['vehicle_color'] != None:
                vehicle_config['vehicle_color'] = vehicle_config['vehicle_color'].replace(';',',')
            
            self.add_vehicle(gap = vehicle_config["gap"], 
                             model_name = vehicle_config["model"], 
                             choice = vehicle_config['choice'], 
                             command = vehicle_config['command'],
                             stop_choice = vehicle_config['stop_choice'],
                             penetrate_distance = vehicle_config['penetrate_distance'],
                             obey_traffic_lights = vehicle_config['obey_traffic_lights'],
                             run = vehicle_config['run'],
                             safety_distance = vehicle_config['safety_distance'],
                             vehicle_color = vehicle_config['vehicle_color'])
    
        self.light_config['subject'] = intersection_settings['subject_light']
        self.light_config['subject_time'] = intersection_settings['subject_light_time']
        
        self.light_config['left'] = intersection_settings['left_light']
        self.light_config['left_time'] = intersection_settings['left_light_time']
        
        self.light_config['right'] = intersection_settings['right_light']
        self.light_config['right_time'] = intersection_settings['right_light_time']
        
        self.light_config['ahead'] = intersection_settings['ahead_light']
        self.light_config['ahead_time'] = intersection_settings['ahead_light_time']
        
        new_intersection_setting = self.export_settings()
        return new_intersection_setting
    
    # Experiment class
def create_intersections(env, number_of_intersections, traffic_light_list, navigation_speed):
    '''
    

    Parameters
    ----------
    env : CARLA_ENV
        sself-written simulation help class.
    number_of_intersections : int
        number of intersection.
    navigation_speed : float
        the navigation speed of the vehicle

    Returns
    -------
    Intersections : list of intersections, [Init_Intersection,Intersection,Intersection,...,Intersection]

    '''
    
    # note: due to the limit of map, number_of_intersections can be at most 4 at present
    world_pos_list = [(-190.0,0.0),(-133.0,0.0),(-55.0,0.0),(25.4,0.0)] # Hardcoded intersection list
    number_of_intersections = min(4,number_of_intersections)
    waypoint_list = [] # way points that form the full path
    subject_traffic_light_list = [] # all subject traffic lights along the full path 
    intersection_list = []
    
    for ii in range(1,number_of_intersections):
        normal_intersection = Intersection(env,world_pos_list[ii],traffic_light_list,navigation_speed = navigation_speed)
        waypoint_list += normal_intersection.get_subject_waypoints() # get the three points representing the path
        subject_traffic_light_list.append(normal_intersection.get_subject_traffic_light())
        intersection_list.append(normal_intersection)
        
    
    
    init_intersection = Init_Intersection(env,world_pos_list[0],traffic_light_list,waypoint_list,subject_traffic_light_list, navigation_speed = navigation_speed)
    intersection_list.insert(0,init_intersection)
    return intersection_list

    # Vehicle class
def get_ego_spectator(ego_transform,distance = -10):
        '''
        

        Parameters
        ----------
        ego_transform : carla.Transform
            transform for the ego vehicle.
        distance : float, optional
            "distance" between  ego vehicle and spectator. The default is -10.

        Returns
        -------
        next_waypoint : carla.Waypoint
            next waypoint, "distance" away from curr_waypoint, in the direction of the current way point
        '''
        forward_vector = ego_transform.get_forward_vector()

        location = ego_transform.location
        spectator_location = carla.Location(x = location.x + distance * forward_vector.x  , y = location.y + distance * forward_vector.y , z = location.z + 5.0)
        spectator_transform = carla.Transform(spectator_location,ego_transform.rotation)
        
        return spectator_transform
    
    # Vehicle Class
def get_ego_left_spectator(ego_transform,distance = -20):
    forward_vector = ego_transform.get_forward_vector()

    location = ego_transform.location
    spectator_location = carla.Location(x = location.x + distance * forward_vector.y  , y = location.y + distance * forward_vector.x , z = location.z + 5.0)
    spectator_rotation = carla.Rotation(roll = ego_transform.rotation.roll,pitch = ego_transform.rotation.pitch, yaw = (ego_transform.rotation.yaw + 90) % 360)
    
    spectator_transform = carla.Transform(spectator_location,spectator_rotation)
    return spectator_transform

    # Vehicle Class
def get_ego_driving_spectator(ego_transform, bounding_box):
    
    distance = bounding_box.x
    left_shift = -bounding_box.y * 0.3
    
    forward_vector = ego_transform.get_forward_vector()

    location = ego_transform.location
    spectator_location = carla.Location(x = location.x + distance * forward_vector.x + left_shift * forward_vector.y , y = location.y + distance * forward_vector.y + left_shift * forward_vector.x, z = location.z + bounding_box.z * 1.5)
    spectator_transform = carla.Transform(spectator_location,ego_transform.rotation)
        
    return spectator_transform

    # Redundant, please delete
def IntersectionBackend(env,intersection_list):
    vehicle_list = []
    started_intersection_list = []
    ego_vehicle = intersection_list[0].ego_vehicle #init_intersection.ego_vehicle
    lead_vehicle = intersection_list[0].lead_vehicle
    follow_vehicle = intersection_list[0].follow_vehicle
    
    spectator = env.world.get_spectator()
    
    # assign the first full path vehicle, to determine whether 
    # each intersection should start
    if not lead_vehicle == None:
        first_full_path_vehicle_name = lead_vehicle["uniquename"]
    else:
        first_full_path_vehicle_name = ego_vehicle["uniquename"]
    
    # assign the vehicle for the spectator to follow
    if follow_vehicle != None:
        spectator_vehicle = follow_vehicle
    else:
        spectator_vehicle = ego_vehicle
    # get the init intersection
    init_intersection = intersection_list.pop(0)
    
    for vehicle_config in init_intersection.subject_vehicle:
        # initialize vehicles by different type (ego,lead,follow,other)
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
        vehicle_list.append(vehicle)
    
    for vehicle_config in init_intersection.left_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
        vehicle_list.append(vehicle)
                    
    for vehicle_config in init_intersection.right_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
        vehicle_list.append(vehicle)
        
    for vehicle_config in init_intersection.ahead_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
        vehicle_list.append(vehicle)
    

    while True:
        env.world.tick()
        
        # update the distance between vehicles after each tick
        env.update_vehicle_distance()
        
        # update the ego spectator
        if env.vehicle_available(spectator_vehicle["uniquename"]):
            spectator_vehicle_transform = env.get_transform_3d(spectator_vehicle["uniquename"])
            spectator_transform = get_ego_spectator(spectator_vehicle_transform,distance = -10)
            spectator.set_transform(spectator_transform)
        
        #else:
        #    spectator_transform = carla.Transform(carla.Location(x= 25.4, y=1.29, z=75.0), carla.Rotation(pitch=-88.0, yaw= -1.85, roll=1.595))
        #spectator.set_transform(spectator_transform)
        
        
        for ii in range(len(intersection_list)-1,-1,-1):
            # check whether the intersection should start
            intersection_list[ii].start_simulation(first_full_path_vehicle_name)
            if intersection_list[ii].start_sim:
                for vehicle_config in intersection_list[ii].subject_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
                    vehicle_list.append(vehicle)
                    
                for vehicle_config in intersection_list[ii].left_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
                    vehicle_list.append(vehicle)
                    
                for vehicle_config in intersection_list[ii].right_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
                    vehicle_list.append(vehicle)
        
                for vehicle_config in intersection_list[ii].ahead_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
                    vehicle_list.append(vehicle)
                
                # move the intersection to started intersection list
                intersection = intersection_list.pop(ii)
                started_intersection_list.append(intersection)
                
        if len(vehicle_list) == 0:
            break        
                
        for jj in range(len(vehicle_list) -1, -1, -1):
            vehicle = vehicle_list[jj]
            if vehicle.run:
                end_trajectory = vehicle.pure_pursuit_control_wrapper()
                if end_trajectory:
                    vehicle_list.pop(jj)

def main():
    try:
        client = carla.Client("localhost",2000)
        client.set_timeout(10.0)
        world = client.load_world('Town05')
         
        # set the weather
        weather = carla.WeatherParameters(
            cloudiness=10.0,
            precipitation=0.0,
            sun_altitude_angle=90.0)
        world.set_weather(weather)
        
        # set the spectator position for demo purpose
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(carla.Location(x=-190, y=1.29, z=75.0), carla.Rotation(pitch=-88.0, yaw= -1.85, roll=1.595))) # top view of intersection
        
        env = CARLA_ENV(world) 
        time.sleep(2) # sleep for 2 seconds, wait the initialization to finish
        
        traffic_light_list = get_traffic_lights(world.get_actors())
        
        intersection_list = create_intersections(env, 4, traffic_light_list)
        init_intersection = intersection_list[0]
        normal_intersections = intersection_list[1:]
        init_intersection.add_ego_vehicle(safety_distance = 15.0 )
        init_intersection.add_follow_vehicle(follow_distance = 20.0)
        init_intersection.add_lead_vehicle(lead_distance = 20.0)
        init_intersection.add_vehicle(choice = "left")
        init_intersection.add_vehicle(choice = "right",command="left")
        init_intersection.add_vehicle(choice = "ahead",command="left")
        init_intersection.add_vehicle(choice = "ahead",command = "right")
        
        intersection_list[1].add_vehicle(choice = "ahead")
        intersection_list[1].add_vehicle(choice = "left",command="left")
        intersection_list[1].add_vehicle(choice = "right",command = "left")
        intersection_list[1].add_vehicle(choice = "right",command = "right")
        intersection_list[1]._shift_vehicles(-10, choice = "right",index = 0)
        
        intersection_list[2].add_vehicle(choice = "ahead")
        intersection_list[2].add_vehicle(choice = "left",command="left")
        intersection_list[2].add_vehicle(choice = "right",command = "left")
        intersection_list[2].add_vehicle(choice = "right",command = "right")
        
        intersection_list[3].add_vehicle(command = "left")
        intersection_list[3].add_vehicle()
        
        
        IntersectionBackend(env,intersection_list)
    finally:
        time.sleep(10)
        env.destroy_actors()
        
if __name__ == '__main__':
    main()