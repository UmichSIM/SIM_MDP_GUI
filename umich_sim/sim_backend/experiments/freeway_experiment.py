#!/usr/bin/env python3
"""
Backend - FreewayExperiment Class
Created on Sun March 27, 2022

Summary: The FreewayExperiment class is a class that derives from the base Experiment class.
"""

# Local Imports
from umich_sim.sim_backend.helpers import VehicleType, ExperimentType
from umich_sim.sim_backend.vehicle_control import freeway_control
from umich_sim.sim_backend.carla_modules import Vehicle
from .experiment import Experiment
from umich_sim.sim_backend.sections import FreewaySection

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
import sys
from typing import Dict, List, Tuple


class FreewayExperiment(Experiment):

    # Current map from the Freeway experiment
    MAP = "Town04"

    def __init__(self, headless: bool) -> None:
        super(FreewayExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.FREEWAY

    def initialize_experiment(self,
                              configuration: Dict[int,
                                                  Dict[int,
                                                       str]] = {}) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        :param configuration: a Dictionary containing the user defined settings for the experiment
        :return: None
        """

        # Add the managed sections to the Experiment
        first_section = FreewaySection([
            self.map.get_waypoint(x.location)
            for x in (self.spawn_points[14], self.spawn_points[13],
                      self.spawn_points[1])
        ], [
            self.map.get_waypoint(x.location)
            for x in (self.spawn_points[20], self.spawn_points[19],
                      self.spawn_points[18])
        ])

        # Add the FreewaySections to the experiment (must be added in order)
        self.add_section(first_section)

        # Add the vehicles according to the configuration dictionary
        self.add_vehicles_from_configuration(configuration)

        # Generate the paths for all the vehicles
        self._generate_section_paths(configuration)

        # Visualize the waypoints of the vehicles
        if configuration["debug"]:
            for vehicle in [self.ego_vehicle] + self.vehicle_list:
                vehicle.draw_waypoints()

    def update_control(self, vehicle: Vehicle) -> None:
        freeway_control(vehicle)
