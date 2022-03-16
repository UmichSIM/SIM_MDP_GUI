"""
Backend - TestExperiment Class
Created on Tue February 22, 2022

Summary: The TestExperiment class is a class that derives from the base Experiment class. It
         provides a sandbox for testing new backend functionality

Usage: This file can be invoked as a regular python script to test out the experiment in the Carla
       environment. It can be invoked using "python TestExperiment.py"

References:

Referenced By:

"""

# Local Imports
import random

from ApiHelpers import ExperimentType, VehicleType
from Controller import Controller, WAYPOINT_SEPARATION
from Experiment import Experiment
from Threading import HeadlessWindow

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
from random import choice
import sys
from typing import Dict, List


# Global colors
GREEN = carla.Color(0, 255, 0)
YELLOW = carla.Color(255, 255, 0)


class TestExperiment(Experiment):

    def __init__(self, headless: bool) -> None:
        super(TestExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.INTERSECTION

    def initialize_experiment(self, configuration: Dict[str, str] = None) -> bool:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        Adds a single vehicle to the map for testing purposes

        :param configuration: a Dictionary containing the user defined settings for the experiment (exact properties
                              vary from experiment to experiment)
        :return: a bool indicating if the experiment was configured correctly
        """

        # Initialize the waypoints
        sim_map: carla.Map = self.world.get_map()
        waypoints: List[carla.Waypoint] = filter(lambda x: x.lane_type == carla.LaneType.Driving, sim_map.generate_waypoints(WAYPOINT_SEPARATION))

        # Visualize each of the maps spawn points
        all_spawn_points: List[carla.Transform] = self.world.get_map().get_spawn_points()
        for spawn_point in all_spawn_points:
            self.world.debug.draw_point(spawn_point.location, size=0.05, color=GREEN, life_time=0.0)

        # Visualize each of the intersections of their waypoints
        all_intersection_waypoints = filter(lambda x: x.is_junction, waypoints)
        for intersect_waypoint in all_intersection_waypoints:
            self.world.debug.draw_point(intersect_waypoint.transform.location, size=0.05, color=YELLOW, life_time=0.0)

        # Add a new test vehicle to the map
        spawn_location = self.world.get_map().get_spawn_points()[2]
        blueprint = choice(self.world.get_blueprint_library().filter('vehicle.*.*'))
        new_vehicle = self.world.spawn_actor(blueprint, spawn_location)

        self.add_vehicle(new_vehicle, ego=True, type_id=VehicleType.MANUAL_EGO)

        # Add four other vehicles around the map
        for _ in range(4):
            spawn_location = random.choice(self.world.get_map().get_spawn_points())
            blueprint = random.choice(self.world.get_blueprint_library().filter('vehicle.*.*'))
            new_vehicle = self.world.try_spawn_actor(blueprint, spawn_location)

            self.add_vehicle(new_vehicle, ego=False, type_id=VehicleType.GENERIC)



def main() -> None:
    """
    Main Function to be run when the file is run as a standalone Python Script

    :return: None
    """

    # Create a new Experiment and initialize the server
    experiment = TestExperiment(True)
    experiment.initialize_carla_server(blocking=True)

    # Set up the experiment
    experiment.initialize_experiment()

    # Start the main simulation loop
    try:
        experiment.run_experiment()
    finally:
        experiment.clean_up_experiment()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HeadlessWindow(main)
    win.show()
    sys.exit(app.exec())
