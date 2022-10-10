#!/usr/bin/env python3
import hydra
from omegaconf import DictConfig, OmegaConf
from dataclasses import dataclass
from pathlib import Path
from typing import Union
from hydra.conf import ConfigStore
from sim_backend.wizard.drivers import InputDevType, WheelType


# Configs
@dataclass
class WizardConfig:
    control_mode: InputDevType = InputDevType.WHEEL
    wheel_type: WheelType = G920
    dev_path: Union[Path, str]


@dataclass
class Config:
    client_frame_rate: int = 60
    server_addr: str = "127.0.0.1"
    carla_port: int = 2000
    rpc_port: int = 2003  # rpc server port
    client_resolution: tuple = (1280, 720)
    cam_recording: bool = False  # whether to record experiment
    cam_record_dir: Union[Path, str] = Path("./_record")
    wizard: WizardConfig


if __name__ == "__main__":
    cs = ConfigStore.instance()
