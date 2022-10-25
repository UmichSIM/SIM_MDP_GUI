"""
Backend - FreewaySection Class
Created on Tue February 15, 2022

Summary: The FreewaySection class represents a single road section in the Freeway experiment
    type. It is derived from the base Section class. This class is responsible for managing all the
    vehicle that interact along this freeway section, along with their specific movements as they
    enter and exit the section.
"""

# Local Imports
from umich_sim.sim_backend.vehicle_control import VehicleController
from .section import Section
from umich_sim.sim_backend.carla_modules import Vehicle

# Library Imports
import carla
from typing import List


class FreewaySection(Section):

    def __init__(self, starting_waypoints: List[carla.Waypoint], ending_waypoints: List[carla.Waypoint]):
        super(FreewaySection, self).__init__()

        # Set the starting and ending waypoints of this FreewaySection
        self.starting_waypoints = starting_waypoints
        self.ending_waypoints = ending_waypoints

    def get_initial_waypoint(self, vehicle: Vehicle) -> carla.Waypoint:
        """
        Gets the waypoint at the start of the FreewaySection in the Vehicle's current lane.

        :param vehicle: the current Vehicle
        :return: a carla.Waypoint representing where the Vehicle will enter the section
        """
        return self.starting_waypoints[vehicle.current_lane]

    def get_thru_waypoints(self, carla_map: carla.Map, current_vehicle: Vehicle, direction: str) -> List[
        carla.Waypoint]:
        """
        Determines the waypoints that correspond with a particular lane change through this FreewaySection.

        :param carla_map: the carla.Map that the experiment is running on
        :param current_vehicle: the current Vehicle
        :param direction: a string presenting the direction to take (either "left" or "right" or "straight")
        :return: a List of carla.Waypoints corresponding with the desired lane change
        """

        # Determine which ending waypoint the vehicle is going toward
        if direction == 'straight':
            ending_waypoint = self.ending_waypoints[current_vehicle.current_lane]
        elif direction == 'left':
            ending_waypoint = self.ending_waypoints[max(current_vehicle.current_lane - 1, 0)]
        elif direction == 'right':
            ending_waypoint = self.ending_waypoints[min(current_vehicle.current_lane + 1, len(self.ending_waypoints))]
        else:
            raise Exception("Invalid direction passed into FreewaySection Get_Thru_Waypoints")

        # Generate the path between the vehicles initial waypoint in the FreewaySection and their ending waypoint
        waypoints, trajectory = VehicleController.generate_path(current_vehicle, current_vehicle.waypoints[-1],
                                                                ending_waypoint)
        return waypoints

    def _distance_between(self, current_location: carla.Location) -> float:
        """
        Calculates the distance between the current vehicle and the Section.

        :param current_location: a carla.Location corresponding to the location of the current vehicle
        :return: a float representing the vehicle's distance from the section
        """
        pass

    def tick(self) -> None:
        """
        Updates the section with each tick of the world.

        :return:
        """
