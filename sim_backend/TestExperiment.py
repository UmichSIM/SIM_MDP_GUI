"""
Backend - TestExperiment Class
Created on Tue February 22, 2022

Summary: The TestExperiment class is a class that derives from the base Experiment class. It
         provides a sandbox for testing new backend functionality

Usage: This file can be invoked as a regular python script to test out the experiment in the Carla
       environment. It can be invoked using "python TestExperiment.py"

References:
    Controller
    Experiment
    Helpers
    Threading

Referenced By:

"""

# Local Imports
from Controller import Controller
from Experiment import Experiment
from Intersection import Intersection
from IntersectionExperiment import IntersectionExperiment
from Helpers import ExperimentType, VehicleType
from Threading import HeadlessWindow

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
import sys
from typing import Dict, List


class TestExperiment(IntersectionExperiment):

    def __init__(self, headless: bool) -> None:
        super(TestExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.INTERSECTION

    def initialize_experiment(self, configuration: Dict[str, str] = {}) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        Adds vehicles to the map in the needed configuration for testing. Please modify this class to meet
        your testing needs

        :param configuration: a Dictionary containing the user defined settings for the experiment (exact properties
                              vary from experiment to experiment)
        :return: None
        """

        # Add a new managed intersection to the map
        first_intersection = Intersection(self.junctions[838], self.world.get_traffic_lights_in_junction(838))
        second_intersection = Intersection(self.junctions[979], self.world.get_traffic_lights_in_junction(979))

        # Add the first intersection to the controller
        self.add_section(first_intersection)
        self.add_section(second_intersection)

        # Add a new vehicle at a subsequence intersection
        turning_spawn_location = self.spawn_points[253]
        turning_vehicle = self.add_vehicle(turning_spawn_location, ego=True, type_id=VehicleType.EGO_FULL_AUTOMATIC)

        # Set the vehicle's active intersections
        turning_vehicle.set_active_sections(second_intersection, second_intersection)

        # Configure what the turning vehicle will do at each intersection
        turning_configuration = {
            1: 'right'
        }
        configuration[turning_vehicle.id] = turning_configuration

        # Generate the paths for all the vehicles
        self._generate_intersection_paths(configuration)

        # Visualize the waypoints of the ego vehicle
        self.ego_vehicle.draw_waypoints(self.world)


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
