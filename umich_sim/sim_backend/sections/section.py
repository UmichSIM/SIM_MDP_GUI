"""
Backend - Section Class
Created on Mon May 9th, 2022

Summary: The Section class provides the base functionality that exists in both the FreewaySection
    and the Intersection classes. Both of these classes derive from this base class.

"""

# Local Imports
from umich_sim.sim_backend.carla_modules import Vehicle
from abc import ABCMeta, abstractmethod

# Library Imports
import carla
import numpy as np
from typing import List


class Section(metaclass=ABCMeta):

    # Static ID variable used as a last number to assign Section IDs
    id = 0

    def __init__(self):

        # Give the section a unique id
        self.id = Section.id
        Section.id += 1

        # Vehicles that start at this section
        self.initial_vehicles: List[Vehicle] = []

        # Section that follows sequentially after this one (this is set by the Experiment::add_section method)
        self.next_section = None

    @abstractmethod
    def get_initial_waypoint(self, vehicle: Vehicle) -> carla.Waypoint:
        """
        Gets the waypoint at the start of the Section.

        This is an abstract function that must be implemented by the derived types.
        As the vehicle approaches the section, get the waypoint that the Vehicle will start the
        section at.

        :param vehicle: the current Vehicle
        :return: a carla.Waypoint representing where the Vehicle will enter the section
        """
        pass

    @abstractmethod
    def get_thru_waypoints(self, carla_map: carla.Map, current_vehicle: Vehicle, direction: str) -> List[carla.Waypoint]:
        """
        Determines the waypoints that correspond with a particular maneuver through the Section.

        This is an abstract function that must be implemented by the derived types. This function
        will take in the currently running carla.Map, the vehicle's current transform, and a string
        representing the desired maneuver direction through the section. This function will then
        return a List of carla.Waypoints that corresponds with the correct maneuver through this
        particular section

        :param carla_map: the carla.Map that the experiment is running on
        :param current_vehicle: the current Vehicle
        :param direction: a string presenting the direction to maneuver (either "left" or "right" or "straight")
        :return: a List of carla.Waypoints corresponding with the desired maneuver
        """
        pass

    @abstractmethod
    def _distance_between(self, current_location: carla.Location) -> float:
        """
        Calculates the distance between the current vehicle and the Section.

        This is an abstract function that must be implemented by the derived types. This function will
        take in the carla.Location of the current vehicle and calculate how far away the vehicle
        is from the intersection

        :param current_location: a carla.Location corresponding to the location of the current vehicle
        :return: a float representing the vehicle's distance from the section
        """
        pass

    @abstractmethod
    def tick(self) -> None:
        """
        Updates the section with each tick of the world.

        This is an abstract function that must be implemented by the derived types. This function will
        update the section on every tick of the world. If the section has become active, then the
        vehicles waiting to start at this section will become active as well.

        :return:
        """
        pass
