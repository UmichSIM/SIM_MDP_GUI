"""
Backend - API Helpers
Created on Tue February 15, 2022

Summary: The API Helpers file defines and implements various helper functions that are needed
    throughout the backend. The creators of this file would like it to die, so please keep
    as much functionality in the classes as possible.

References:

Referenced By:

"""

import carla
from enum import Enum


class ExperimentType(Enum):
    INTERSECTION = 1
    FREEWAY = 2


class WorldDirection(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4


def config_world(world: carla.World, synchrony: bool = True, delta_seconds: float = 0.02) -> None:
    """
    Configures the CARLA world to use certain synchrony and timestep settings.

    Carla Documentation:  https://carla.readthedocs.io/en/latest/adv_synchrony_timestep/

    :param world: a carld.World object representing the current simulation world
    :param synchrony: a bool representing whether synchrony should be applied to the world
    :param delta_seconds: a float representing the worlds timestep
    :return:
    """
    settings = world.get_settings()
    settings.synchronous_mode = synchrony
    settings.fixed_delta_seconds = delta_seconds
    world.apply_settings(settings)