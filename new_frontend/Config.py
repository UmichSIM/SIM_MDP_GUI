
freeway_dict = {
    "allow_collision": False,
    "num_freeway_section": 1,
    "max_speed": 0.0,
    "min_speed": 0.0,
    "safety_distance": 0.0,
    "lane1": {
        "subject_lane_vehicle": [],
        "left_lane_vehicle": []
    },
    "lane2": {
        "subject_lane_vehicle": [],
        "left_lane_vehicle": []
    },
    "lane3": {
        "subject_lane_vehicle": [],
        "left_lane_vehicle": []
    },
    "lane4": {
        "subject_lane_vehicle": [],
        "left_lane_vehicle": []
    },
    "lane5": {
        "subject_lane_vehicle": [],
        "left_lane_vehicle": []
    }
}

intersection_dict = {
    "allow_collision": False,
    "num_freeway_section": 1,
    "max_speed": 0.0,
    "safety_distance": 0.0,
    "intersection1": {
        "subject_lane_vehicles": [],
        "left_lane_vehicles": [],
        "ahead_lane_vehicles": [],
        "right_lane_vehicles": [],
        "traffic_light1": [],
        "traffic_light2": [],
        "traffic_light3": [],
        "traffic_light4": [],
    },
    "intersection2": {
        "subject_lane_vehicles": [],
        "left_lane_vehicles": [],
        "ahead_lane_vehicles": [],
        "right_lane_vehicles": [],
        "traffic_light1": [],
        "traffic_light2": [],
        "traffic_light3": [],
        "traffic_light4": [],
    },
    "intersection3": {
        "subject_lane_vehicles": [],
        "left_lane_vehicles": [],
        "ahead_lane_vehicles": [],
        "right_lane_vehicles": [],
        "traffic_light1": [],
        "traffic_light2": [],
        "traffic_light3": [],
        "traffic_light4": [],
    },
    "intersection4": {
        "subject_lane_vehicles": [],
        "left_lane_vehicles": [],
        "ahead_lane_vehicles": [],
        "right_lane_vehicles": [],
        "traffic_light1": [],
        "traffic_light2": [],
        "traffic_light3": [],
        "traffic_light4": [],
    },
    "intersection5": {
        "subject_lane_vehicles": [],
        "left_lane_vehicles": [],
        "ahead_lane_vehicles": [],
        "right_lane_vehicles": [],
        "traffic_light1": [],
        "traffic_light2": [],
        "traffic_light3": [],
        "traffic_light4": [],
    },
    "intersection6": {
        "subject_lane_vehicles": [],
        "left_lane_vehicles": [],
        "ahead_lane_vehicles": [],
        "right_lane_vehicles": [],
        "traffic_light1": [],
        "traffic_light2": [],
        "traffic_light3": [],
        "traffic_light4": [],
    }
}

"""
Template for traffic light object
traffic_light_dict = {
    "red_light_duration" = 0,
    "yellow_light_duration" = 0,
    "green_light_duration" = 0
}
"""

""""
This is the template for vehicle object
vehicles_dict = {
    "gap": 0.0,
    "model": "",
    "color": (0,0,0),
    "position": "", #Position of vehicle with repect to the ego vehicle -- lead, ego, follow
}
"""

# import Config.py


if __name__ == "__main__":
    #print(freeway_dict["allow_collision"])
    #print(freeway_dict["max_speed"])
    print(freeway_dict.items())
