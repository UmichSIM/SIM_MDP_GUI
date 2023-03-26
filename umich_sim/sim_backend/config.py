"""
Implementation of the configuration class according to "Configuration Class Proposal"
"""

from typing import TypedDict, Tuple, List, Dict
from enum import Enum
from dataclasses import dataclass

# ENUMs, for..
# Vehicle
VehicleType = Enum('Type', ['EGO', 'LEAD', 'FOLLOW',
                     'AHEAD_LEAD', 'AFTER_FOLLOW', 'ADJACENT_LEAD', 'ADJACENT_FOLLOW',
                            'AHEAD_ADJACENT_LEAD', 'SPEED_BARRIER'])
# Vehicle (intersection)
Direction = Enum('Direction', ['STRAIGHT', 'LEFT', 'RIGHT'])
Stop = Enum('Stop', ['NORMAL_STOP', 'ABRUPT_STOP', 'SLOW_INTRUDE', 'RUN_RED_LIGHT'])
# Vehicle (freeway)
Behavior = Enum('Behavior', ['KEEP_SAME_SPEED', 'AC_OR_DECELERATE', 'CHANGE_LANE',
                             'PULL_OFF_STOP', 'ENTER_ADJACENT'])
# Others
Task = Enum('Task', ['INTERSECTION', 'FREEWAY'])
Weather = Enum('Weather', ['SUNNY', 'CLOUDY', 'RAINY', 'SNOWY'])
Scene = Enum('Scene', ['DAY', 'NIGHT'])
TrafficLightColor = Enum('TrafficLightColor', ['GREEN', 'YELLOW', 'RED'])
TrafficLightTrigger = Enum('TrafficLightTrigger', ['TIME', 'DISTANCE'])

# Vehicle.exp_settings structure in TypedDict
@dataclass
class VehicleExpSettings:
    """Vehicle experiment-specific settings, applied to all types of experiments."""
    vehicle_type: VehicleType

@dataclass
class VehicleExpSettingsIntersection(VehicleExpSettings):
    """Vehicle experiment-specific settings, applied to intersection experiment."""
    follow_traffic_rule: bool
    direction: Direction
    stop: Stop

@dataclass
class VehicleExpSettingsFreeway(VehicleExpSettings):
    """Vehicle experiment-specific settings, applied to freeway experiment."""
    behavior: Behavior
    
@dataclass
class Vehicle:
    location: int  # integer that represents a specific location in a freeway or intersection
    gap: float  # gap of its front
    model: str
    color: Tuple[int, int, int]  # RGB
    speed: float
    acceleration: float
    exp_settings: VehicleExpSettings  # experiment-specific setting variables

@dataclass
class TrafficLight:
    state_durations: Dict[TrafficLightColor, float]
    trigger_type: TrafficLightTrigger
    trigger_val: float

@dataclass
class Intersection:
    subject_lane_traffic_light: TrafficLight
    subject_lane_vehicles: List[Vehicle]
    left_lane_vehicles: List[Vehicle]
    right_lane_vehicles: List[Vehicle]
    ahead_lane_vehicles: List[Vehicle]

@dataclass
class Freeway:
    left_lane_vehicles: List[Vehicle]
    subject_lane_vehicles: List[Vehicle]

# BASE CLASS
@dataclass
class ScenarioConfig:
    task: Task  # intersection or freeway
    map: str
    weather: Weather
    scene: Scene  # day or night
    intersections: List[Intersection]  # for intersection experiment
    freeways: List[Freeway]  # for freeway experiment
    ol_random_traffic: bool  # for freeway experiment (opposing lane random traffic)
    # other global settings
    allow_collision: bool
    max_speed: float
    min_speed: float
    safety_distance: float