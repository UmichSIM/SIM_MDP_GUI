# Python Version: 3.9

from typing import *
from enum import Enum

# Enums (Auto-assign integer values starting with 1)
Task = Enum('Task', ['INTERSECTION', 'EXPRESSWAY'])
Weather = Enum('Weather', ['SUNNY', 'CLOUDY', 'RAINY', 'SNOWY'])
Scene = Enum('Scene', ['DAY', 'NIGHT'])
TrafficLightColor = Enum('TrafficLightColor', ['GREEN', 'YELLOW', 'RED'])
TrafficLightTrigger = Enum('TrafficLightTrigger', ['TIME', 'DISTANCE'])
Direction = Enum('Direction', ['STRAIGHT', 'LEFT', 'RIGHT'])
Accident = Enum('Accident', ['NORMAL_STOP, ABRUPT_STOP', 'SLOW_INTRUDE', 'RUN_RED_LIGHT'])
VehicleType = Enum('VehicleType', ['LEAD', 'AHEAD_LEAD', 'ADJACENT_LEAD', 'FOLLOW', 'SPEED_BARRIER'])
FreewayVehicleBehavior = Enum('FreewayVehicleBehavior', ['KEEP_SAME_SPEED', 'AC_OR_DECELERATE', 'CHANGE_LANES', 'PULL_OFF_STOP', 'ENTER_ADJACENT'])
VehicleColor = Enum('VehicleColor', []) # to be specified
BehaviorRoute = Enum('BehaviorRoute', []) # to be specified

# BASE CLASSES
class Position:
    def __init__(self):
        # To be specified
        pass

# Environment -> intersection_settings (list of Intersection) -> Intersection -> traffic_light
class TrafficLight:
    def __init__(self):
        self.state_durations: dict[TrafficLightColor, float] = {}
        self.trigger_type: TrafficLightTrigger = None
        self.trigger_val: float = 0.0

# Environment -> intersection_settings (list of Intersection) -> Intersection -> vehicles (list of IntersectionVehicle)
class IntersectionVehicle:
    def __init__(self):
        self.init_position: Position = None
        self.model: str = ''
        self.direction: Direction = None
        self.accident: Accident = None

# Environment -> intersection_settings (list of Intersection)
class Intersection:
    def __init__(self):
        self.traffic_light: TrafficLight = None
        self.vehicles: list[IntersectionVehicle] = []

# Environment -> freeway_settings (list of Freeway) -> Freeway -> vehicles (list of FreewayVehicle)
class FreewayVehicle:
    def __init__(self):
        self.init_position: Position = None
        self.type: VehicleType = None
        self.behavior: FreewayVehicleBehavior = None
        self.ol_random_traffic: bool = False # Opposing Lanes Random Traffic

# Environment -> freeway_settings (list of Freeway)
class Freeway:
    def __init__(self):
        self.speed_limit: float = 0.0
        self.vehicles: list[FreewayVehicle] = []

# Environment
class Environment:
    def __init__(self):
        self.map: str = ''
        self.task_type: Task = None
        self.weather: Weather = None
        self.scene: Scene = None
        self.num_intersections: int = 0
        self.intersection_settings: list[Intersection] = []
        self.freeway_settings: list[Freeway] = []

# vehicles (list of Vehicle) -> Vehicle -> VehicleBehavior
class VehicleBehavior:
    def __init__(self):
        self.is_ego: bool = False
        self.is_leading: bool = False
        self.is_following: bool = False
        self.speed: int = 0
        self.acceleration: int = 0
        self.follow_traffic_rules: bool = False
        self.route: BehaviorRoute = None

# vehicles (list of Vehicle) -> Vehicle
class Vehicle:
    def __init__(self):
        self.init_position: Position = None
        self.type: VehicleType = None
        self.color: VehicleColor = None
        self.behavior: VehicleBehavior = None # VehicleBehavior is a class, not an Enum

class Config:
    def __init__(self, env_in: Environment, vehicles_in: list[Vehicle]):
        self.env: Environment = env_in
        self.vehicles: list[Vehicle] = vehicles_in