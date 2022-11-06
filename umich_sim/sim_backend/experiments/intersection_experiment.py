"""
Backend - IntersectionExperiment Class
Created on Monday, April 4th, 2022

Summary: The IntersectionExperiment class is a class that derives from the base Experiment class. It
         runs the Intersection experiment type

"""

# Local Imports
from .experiment import Experiment
from umich_sim.sim_backend.sections import Intersection
from umich_sim.sim_backend.helpers import (ExperimentType, VehicleType, project_forward, smooth_path)
from umich_sim.sim_backend.carla_modules import World
from umich_sim.sim_config import ConfigPool, Config

# Library Imports
from typing import Dict, List


class IntersectionExperiment(Experiment):
    MAP = "Town05"

    def __init__(self, headless: bool) -> None:
        super(IntersectionExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.INTERSECTION

    def initialize_experiment(self, configuration: Dict[int, Dict[int, str]] = None) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        :param configuration: a Dictionary containing the user defined settings for the experiment
        :return: None
        """
        world = World.get_instance().world
        # Add the four managed intersections to the experiment
        first_intersection = Intersection(self.junctions[838], world.get_traffic_lights_in_junction(838))
        second_intersection = Intersection(self.junctions[979], world.get_traffic_lights_in_junction(979))
        third_intersection = Intersection(self.junctions[1427], world.get_traffic_lights_in_junction(1427))
        fourth_intersection = Intersection(self.junctions[1574], world.get_traffic_lights_in_junction(1574))

        # Add the intersections to the experiment (must be added in order)
        self.add_section(first_intersection)
        self.add_section(second_intersection)
        self.add_section(third_intersection)
        self.add_section(fourth_intersection)

        # Add the vehicles according to the configuration dictionary
        self.add_vehicles_from_configuration(configuration)

        # Generate the paths for all the vehicles
        self._generate_section_paths(configuration)

        # Visualize the waypoints of the vehicles
        if ConfigPool.get_config().debug:
            for vehicle in [self.ego_vehicle] + self.vehicle_list:
                vehicle.draw_waypoints()
