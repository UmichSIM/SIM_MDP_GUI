#!/usr/bin/env python3
import hydra
from omegaconf import DictConfig, OmegaConf, MISSING
from dataclasses import dataclass
from enum import IntEnum, auto, Enum
from typing import TypedDict, Tuple, List, Dict
from pathlib import Path
from typing import Union
from hydra.conf import ConfigStore
from umich_sim.wizard.inputs import ClientMode, InputDevType, ClientMode

# Enumerated class specifying the different types of Vehicles
class VehicleType(IntEnum):
    EGO = 0
    EGO_MANUAL_STEER = auto()
    EGO_FULL_MANUAL = auto()
    LEAD = auto()
    AHEAD_LEAD = auto()
    AFTER_FOLLOW = auto()
    ADJACENT_LEAD = auto()
    ADJACENT_FOLLOW = auto()
    AHEAD_ADJACENT_LEAD = auto()
    SPEED_BARRIER = auto()
    FOLLOWER = auto()
    GENERIC = auto()


# Enumerated class specifying the different directions in the World
class WorldDirection(IntEnum):
    FORWARD = 0
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()
    
Stop = Enum('Stop', ['NORMAL_STOP', 'ABRUPT_STOP', 'SLOW_INTRUDE', 'RUN_RED_LIGHT'])
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
    direction: WorldDirection
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

# Configs
@dataclass
class WizardConfig:
    client_mode: ClientMode = ClientMode.EGO
    dev_type: InputDevType = InputDevType.KBD
    dev_path: Union[Path, str] = ""
    enable_wizard: bool = False


@dataclass
class Config:
    debug: bool = True
    enable_sound: bool = False
    client_frame_rate: int = 60
    server_addr: str = "127.0.0.1"
    carla_port: int = 2000
    rpc_port: int = 2003  # rpc server port
    client_resolution: tuple = (1280, 720)
    client_mode: ClientMode = ClientMode.EGO
    gui_mode: bool = False
    cam_recording: bool = False  # whether to record experiment
    cam_record_dir: Union[Path, str] = Path("./_record")
    car_filter: str = "vehicle.*"
    wizard: WizardConfig = WizardConfig()


class ConfigPool:
    """
    class for storing configs
    """
    config: Config = Config()

    @staticmethod
    def load_config(config: Config):
        ConfigPool.config = config

    @staticmethod
    def get_config() -> Config:
        return ConfigPool.config
