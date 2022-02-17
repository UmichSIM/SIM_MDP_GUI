"""
Backend - Vehicle Class
Created on Tue February 15, 2022

Summary: The Vehicle class represents a single vehicle in the CARLA simulation environment. It stores
    all relevant information for a single instance. Provides a high level interface for controlling a
    vehicle's motion through a Controller class.

References:
    Carla Python API

Referenced By:

"""

import carla
from typing import List


class Vehicle(carla.Vehicle):

    def __init__(self, id_number: int, name: str):
        super().__init__()
        self.id: int = id_number     # The unique internal ID for each vehicle
        self.name: str = name        # The user specified name for each vehicle

        # List of the carla.Transforms for every other vehicle in the Simulation.
        # Tracking both the position and forward facing vector is necessary to calculate
        # distance between vehicles and relative positioning between vehicles
        self.other_vehicle_transforms: List[carla.Transform] = []

    def move_vehicle_location(self, new_position: carla.Transform) -> None:
        """
        Updates the position of the Vehicle to a new position.

        :param new_position: a carla.Transform representing the new location of the vehicle
        :return: None
        """
        self.set_transform(new_position)

    def get_vehicle_size(self) -> (float, float):
        """
        Gets the size of the vehicle's bounding box as a width, length tuple.

        If this function doesn't work as intended, blame Austin
        :return: the width and length of the vehicle as a tuple
        """
        return self.bounding_box.extent[0], self.bounding_box.extent[1]

    def get_current_speed(self) -> float:
        """
        Gets the current forward speed of the Vehicle.

        :return: the current forward speed of the Vehicle as a float
        """
        velocity = self.get_velocity()
        return (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5

    def get_current_position(self) -> (float, float):
        """
        Gets the current position of the vehicle.

        :return: the current position of the Vehicle as an (x,y) tuple
        """
        transform = self.get_transform()
        return transform.location.x, transform.location.y

    def get_current_rotation(self) -> float:
        """
        Gets the current rotation of the vehicle (yaw).

        :return: the current rotation of the vehicle as a float
        """
        transform = self.get_transform()
        return transform.rotation.yaw

    def update_other_vehicle_transforms(self, other_vehicles: List[Vehicle]) -> None:
        """
        Updates the internal list with the transforms of all other Vehicles in the simulation

        :param other_vehicles: a List of all other Vehicles in the Simulation
        :return: None
        """
        pass