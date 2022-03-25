"""
Backend - MapExplorationExperiment Class
Created on Tue February 22, 2022

Summary: The MapExplorationExperiment class is a class that derives from the base Experiment class. It
         provides a sandbox for exploring new maps and getting oriented with the map's layout and positions.

Usage: This file can be invoked as a regular python script to test out the experiment in the Carla
       environment. It can be invoked using "python MapExplorationExperiment.py"

References:
    Controller
    Experiment
    Helpers
    Threading

Referenced By:
    None

"""

# Local Imports
from Controller import WAYPOINT_SEPARATION
from Experiment import Experiment
from Helpers import ExperimentType, VehicleType, GREEN, YELLOW
from Threading import HeadlessWindow

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
import random
import sys
from typing import Dict, List


class MapExplorationExperiment(Experiment):

    def __init__(self, headless: bool) -> None:
        super(MapExplorationExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.INTERSECTION

    def initialize_experiment(self, configuration: Dict[str, str] = None) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        Adds a Manual Ego vehicle to the map for map exploration. Adds four other stationary vehicles around the map
        for testing purposes.

        :param configuration: a Dictionary containing the user defined settings for the experiment (exact properties
                              vary from experiment to experiment)
        :return: None
        """

        # Visualize each of the maps spawn points
        for spawn_point in self.spawn_points:
            self.world.debug.draw_point(spawn_point.location, size=0.05, color=GREEN, life_time=0.0)

        # Visualize each of the intersections of their waypoints
        all_intersection_waypoints = [waypoint
                                      for junction in self.junctions
                                      for waypoint_pair in junction.get_waypoints(carla.LaneType.Driving)
                                      for waypoint in waypoint_pair]
        for intersect_waypoint in all_intersection_waypoints:
            self.world.debug.draw_point(intersect_waypoint.transform.location, size=0.05, color=YELLOW, life_time=0.0)

        # Add a new test vehicle to the map
        spawn_location = self.spawn_points[2]
        self.add_vehicle(spawn_location, ego=True, type_id=VehicleType.EGO_FULL_MANUAL)

        # Add four other vehicles around the map
        for _ in range(4):
            spawn_location = random.choice(self.world.get_map().get_spawn_points())
            self.add_vehicle(spawn_location, ego=False, type_id=VehicleType.GENERIC)


def main() -> None:
    """
    Main Function to be run when the file is run as a standalone Python Script

    :return: None
    """

    # Create a new Experiment and initialize the server
    experiment = MapExplorationExperiment(True)
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
