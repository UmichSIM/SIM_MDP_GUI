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
from enum import IntEnum
import logging
import math
import numpy as np
import os
import sys
from typing import List


# Enumerated class specifying the different types of Vehicles
class VehicleType(IntEnum):
    MANUAL_EGO = 1
    AUTOMATIC_EGO = 2
    LEAD = 3
    FOLLOWER = 4
    GENERIC = 5


# Enumerated class specifying the different experiment types
class ExperimentType(IntEnum):
    INTERSECTION = 1
    FREEWAY = 2


# Enumerated class specifying the different directions in the World
class WorldDirection(IntEnum):
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


def to_numpy_vector(carla_vector: carla.Vector3D, dims=3):
    """
    Converts a carla.Vector3d into a numpy.array with length three

    :param carla_vector: the carla.Vector3d to convert
    :param dims: number of dimensions in the returned vector (defaults to 3)
    :return: a numpy.array of length 3 representing the Carla vector
    """
    if dims == 3:
        return np.array([carla_vector.x, carla_vector.y, carla_vector.z])
    return np.array([carla_vector.x, carla_vector.y])


def rotate_vector(vector: np.array, degrees: float) -> np.array:
    """
    Rotates the provided vector around the z-axis by the specified number of degrees

    :param vector: a np.array representing the vector to rotate
    :param degrees: a float representing the number of degrees to rotate by
    :return: a np.array containing the rotated vector
    """

    radians = degrees * math.pi / 180
    rotation_matrix = np.array([
        [math.cos(radians), -1 * math.sin(radians), 0],
        [math.sin(radians), math.cos(radians),      0],
        [0,                 0,                      1]
    ])

    return np.matmul(rotation_matrix, vector)


def smooth_path(current_path: List[carla.Transform], num_passes=1) -> List[carla.Transform]:
    """
    Function that smooths the provided path by adding intermediate points between all neighboring points.

    :param current_path: a List of carla.Transforms representing the path to be smoothed
    :param num_passes: an int representing the number of smoothing passes to make
    :return: a List of carla.Transforms representing the newly smoothed path
    """

    starting_path: List[carla.Transform] = current_path
    for _ in range(num_passes):
        smoothed_path: List[carla.Transform] = []
        smoothed_path.append(starting_path[0])
        for i in range(1, len(starting_path), 1):

            # Calculate the intermediate point by averaging together the neighbor points
            intermediate_point = carla.Transform()
            intermediate_point.location.x = (starting_path[i].location.x + smoothed_path[-1].location.x) / 2
            intermediate_point.location.y = (starting_path[i].location.y + smoothed_path[-1].location.y) / 2
            intermediate_point.location.z = (starting_path[i].location.z + smoothed_path[-1].location.z) / 2

            # Add both the intermediate point and the current point to the smoothed path
            smoothed_path.append(intermediate_point)
            smoothed_path.append(starting_path[i])

        starting_path = smoothed_path

    return smoothed_path
