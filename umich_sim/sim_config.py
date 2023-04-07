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

# FREEWAY SAMPLE
# configuration_dictionary = {
#     "debug": True,
#     "number_of_vehicles": 2,
#     # Ego vehicle that simply goes straight through each Freeway section
#     0: {
#         "type": VehicleType.EGO_FULL_MANUAL,
#         "spawn_point": 13,
#         "spawn_offset": -10.0,
#         "initial_lane_index": 1,
#         "sections": {0: "straight"},
#     },
#     # Initial lead vehicle that turns right at the second intersection
#     1: {
#         "type": VehicleType.LEAD,
#         "spawn_point": 13,
#         "spawn_offset": 0.0,
#         "initial_lane_index": 1,
#         "sections": {0: "straight"},
#     },
# }
# INTERSECTION SAMPLE
# configuration_dictionary = {
#     "debug": True,
#     "number_of_vehicles": 5,
#     # Ego vehicle that simply goes straight through each intersection
#     0: {
#         "type": VehicleType.EGO_FULL_MANUAL,
#         "spawn_point": 188,
#         "spawn_offset": 0.0,
#         "sections": {
#             0: 'straight',
#             1: 'straight',
#             2: 'straight',
#             3: 'straight'
#         }
#     },
#     # Initial lead vehicle that turns right at the second intersection
#     1: {
#         "type": VehicleType.LEAD,
#         "spawn_point": 188,
#         "spawn_offset": 10.0,
#         "sections": {
#             0: 'straight',
#             1: 'right'
#         }
#     },
#     # Vehicle that turns right at initial intersection
#     2: {
#         "type": VehicleType.GENERIC,
#         "spawn_point": 59,
#         "spawn_offset": 0.0,
#         "sections": {
#             0: 'right'
#         }
#     },
#     # Vehicle that turns right at the second intersection
#     3: {
#         "type": VehicleType.GENERIC,
#         "spawn_point": 253,
#         "spawn_offset": 0.0,
#         "sections": {
#             1: 'right'
#         }
#     },
#     # Vehicle that turns left at the third intersection
#     4: {
#         "type": VehicleType.GENERIC,
#         "spawn_point": 277,
#         "spawn_offset": 0.0,
#         "sections": {
#             2: 'left',
#             3: 'left'  # Current this is left due to some weirdness with Carla lanes, it actually goes straight
#         }
#     }
# }

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
    # direction: WorldDirection
    stop: Stop
    #sections: List[WorldDirection]
    sections: Dict[int, str]

@dataclass
class VehicleExpSettingsFreeway(VehicleExpSettings):
    """Vehicle experiment-specific settings, applied to freeway experiment."""
    behavior: Behavior

@dataclass
class Vehicle:
    spawn_point: int # integer that represents a specific location in a freeway or intersection
    spawn_offset: float
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
    # subject_lane_vehicles: List[Vehicle]
    # left_lane_vehicles: List[Vehicle]
    # right_lane_vehicles: List[Vehicle]
    # ahead_lane_vehicles: List[Vehicle]
    # 0: subject_lane, 1: ahead_lane, 2: left_lane, 3: right_lane
    vehicles: List[List[Vehicle]]

@dataclass
class Freeway:
    # left_lane_vehicles: List[Vehicle]
    # subject_lane_vehicles: List[Vehicle]
    # 0: left_lane, 1: subject_lane
    vehicles: List[List[Vehicle]]

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
