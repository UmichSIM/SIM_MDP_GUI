"""
Implementation of the configuration class according to "Configuration Class Proposal"
https://docs.google.com/document/d/12WPOGTSmqdKhLk_f6ysbAbLGbMhUN15yMLg7rpNrrJY/
"""

from typing import *
from enum import Enum
from dataclasses import dataclass

# Enums (Auto-assign integer values starting with 1)
# Environment
Task = Enum('Task', ['INTERSECTION', 'EXPRESSWAY'])
Weather = Enum('Weather', ['SUNNY', 'CLOUDY', 'RAINY', 'SNOWY'])
Scene = Enum('Scene', ['DAY', 'NIGHT'])
TrafficLightColor = Enum('TrafficLightColor', ['GREEN', 'YELLOW', 'RED'])
TrafficLightTrigger = Enum('TrafficLightTrigger', ['TIME', 'DISTANCE'])
Direction = Enum('Direction', ['STRAIGHT', 'LEFT', 'RIGHT'])
Accident = Enum('Accident', ['NORMAL_STOP, ABRUPT_STOP', 'SLOW_INTRUDE', 'RUN_RED_LIGHT'])
FreewayVehicleType = Enum('FreewayVehicleType', ['LEAD', 'AHEAD_LEAD', 'ADJACENT_LEAD', 'FOLLOW', 'SPEED_BARRIER'])
FreewayVehicleBehavior = Enum('FreewayVehicleBehavior', ['KEEP_SAME_SPEED', 'AC_OR_DECELERATE', 'CHANGE_LANES', 'PULL_OFF_STOP', 'ENTER_ADJACENT'])
# Vehicle
VehicleType = Enum('VehicleType', [])  # to be specified
VehicleColor = Enum('VehicleColor', [])  # to be specified
TrafficRule = Enum('TrafficRule', ['FOLLOW', 'INTRUDE', 'IGNORE'])
Route = Enum('Route', ['CHANGE_LANE', 'TURN_AT_INTERSECTION'])  # more to be specified

@dataclass
class Location:
    # To be specified
    pass

# Environment -> intersections (list of Intersection) -> Intersection -> traffic_light
@dataclass
class TrafficLight:
    state_durations: Dict[TrafficLightColor, float]
    trigger_type: TrafficLightTrigger
    trigger_val: float

# Environment -> intersections (list of Intersection) -> Intersection -> vehicles (list of IntersectionVehicle)
@dataclass
class IntersectionVehicle:
    init_location: Location
    model: str
    direction: Direction
    accident: Accident

# Environment -> intersections (list of Intersection)
@dataclass
class Intersection:
    traffic_light: TrafficLight
    # based on the front-end review
    subject_lane_vehicles: List[IntersectionVehicle]
    left_lane_vehicles: List[IntersectionVehicle]
    right_lane_vehicles: List[IntersectionVehicle]
    ahead_lane_vehicles: List[IntersectionVehicle]

# Environment -> freeways (list of Freeway) -> Freeway -> vehicles (list of FreewayVehicle)
@dataclass
class FreewayVehicles:
    init_location: Location
    type: FreewayVehicleType
    behavior: FreewayVehicleBehavior

# Environment -> freeways (list of Freeway) -> Freeway -> vehicles (list of FreewayVehicle) -> FreewayVehicle -> lane_sections (list of LaneSection)
@dataclass
class LaneSection:
    left_lane_vehicles: List[FreewayVehicles]
    subject_lane_vehicles: List[FreewayVehicles]

# Environment -> freeways (list of Freeway)
@dataclass
class Freeway:
    speed_limit: float
    # based on the front-end review
    lane_sections: List[LaneSection]
    ol_random_traffic: bool  # Opposing Lanes Random Traffic

# Environment
@dataclass
class Environment:
    map: str
    task_type: Task
    weather: Weather
    scene: Scene
    num_intersections: int
    intersections: List[Intersection]
    freeways: List[Freeway]
    # based on the front-end review
    allow_collision: bool
    max_speed: float
    min_speed: float
    safety_distance: float

# vehicles (list of Vehicle) -> Vehicle -> VehicleBehavior
@dataclass
class VehicleBehavior:
    is_ego: bool
    is_lead_or_follow: bool
    speed: float
    acceleration: float
    traffic_rule: TrafficRule
    route: Route

# vehicles (list of Vehicle) -> Vehicle
@dataclass
class Vehicle:
    init_location: Location
    type: VehicleType
    color: VehicleColor
    behavior: VehicleBehavior  # VehicleBehavior is a class, not an Enum
    # based on the front-end review
    gap: float
    model: str

# BASE CLASS
@dataclass
class ScenarioConfig:
    env: Environment
    vehicles: List[Vehicle]