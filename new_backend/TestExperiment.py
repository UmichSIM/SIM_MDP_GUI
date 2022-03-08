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
from ApiHelpers import logging_setup
from Experiment import Experiment, ExperimentType
from Threading import HeadlessWindow

# Library Imports
from PyQt5.QtWidgets import QApplication
from random import choice
import sys
from typing import Dict



class TestExperiment(Experiment):

    def __init__(self, headless: bool) -> None:
        super(TestExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.INTERSECTION

    def initialize_experiment(self, configuration: Dict[str, str]) -> bool:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        Adds a single vehicle to the map for testing purposes

        :param configuration: a Dictionary containing the user defined settings for the experiment (exact properties
                              vary from experiment to experiment)
        :return: a bool indicating if the experiment was configured correctly
        """

        # Add a new test vehicle to the map (probably dump this code into an Experiment class function)
        spawn_location = choice(self.world.get_map().get_spawn_points())
        blueprint = choice(self.world.get_blueprint_library().filter('vehicle.*.*'))
        new_vehicle = self.world.spawn_actor(blueprint, spawn_location)
        self.add_vehicle(new_vehicle, ego=True)


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
    # experiment.run_experiment()


if __name__ == "__main__":
    # logging_setup()
    app = QApplication(sys.argv)
    win = HeadlessWindow(main)
    win.show()
    sys.exit(app.exec())
