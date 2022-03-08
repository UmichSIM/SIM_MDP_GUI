"""
Backend - API Helpers
Created on Tue February 15, 2022

Summary: The API Helpers file defines and implements various helper functions that are needed
    throughout the backend. The creators of this file would like it to die, so please keep
    as much functionality in the classes as possible.

References:

Referenced By:

"""

# Library Imports
import carla
from datetime import datetime
from enum import Enum
import logging
import os
import sys


# Enumerated class specifying the different experiment types
class ExperimentType(Enum):
    INTERSECTION = 1
    FREEWAY = 2


# Enumerated class specifying the different directions in the World
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


def logging_setup(directory_name: str = "logs") -> None:
    """
    Configured the logging package to write out logs to the correct place under the correct filename.

    :param directory_name: the directory to which the logs will be written
    :return: None
    """

    current_directory = os.path.realpath(os.getcwd())
    logging_directory = current_directory + "/" + directory_name
    if not os.path.exists(logging_directory):
        os.makedirs(logging_directory)

    current_time = datetime.now().strftime("%m-%m-%Y.%H.%M.%S")
    log_file_name = sys.argv[0] + "." + current_time + ".log"

    logging.basicConfig(filename=logging_directory + "/" + log_file_name, level=logging.DEBUG)
