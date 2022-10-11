#!/usr/bin/env python3
import hydra
from omegaconf import DictConfig, OmegaConf, MISSING
from dataclasses import dataclass
from pathlib import Path
from typing import Union
from hydra.conf import ConfigStore
from umich_sim.wizard.inputs import InputDevType, WheelType


# Configs
@dataclass
class WizardConfig:
    control_mode: InputDevType = InputDevType.WHEEL
    wheel_type: WheelType = MISSING
    dev_path: Union[Path, str] = MISSING


@dataclass
class Config:
    client_frame_rate: int = 60
    server_addr: str = "127.0.0.1"
    carla_port: int = 2000
    rpc_port: int = 2003  # rpc server port
    client_resolution: tuple = (1280, 720)
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
