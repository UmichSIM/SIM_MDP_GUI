"""
Backend - FreewayExperiment Class
Created on Sun March 27, 2022

Summary: The FreewayExperiment class is a class that derives from the base Experiment class.

Usage: 

References:
    FreewayController
    FreewaySection

Referenced By:
    None

"""

# Local Imports
from WizardExperiment import Experiment
# from Controller import Controller
from FreewaySection import FreewaySection
from Helpers import ExperimentType, VehicleType, project_forward
from Vehicle import Vehicle
from Threading import HeadlessWindow

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
import sys
from typing import Dict, List, Tuple


# Sample configuration dictionary
# Notes: the vehicle with ID 0 must always be the ego vehicle,
# the vehicle's ID's must increase in consecutive order, otherwise later vehicles will be left out,
# the value of spawn_point corresponds with the spawn_point numbers found in the MapExplorationExperiment,
# spawn_offset shifts the spawn point forward or backward by x meters
configuration_dictionary = {
    "debug": False,
    "number_of_vehicles": 2,

    # Ego vehicle that simply goes straight through each Freeway section
    0: {
        "type": VehicleType.EGO_FULL_MANUAL,
        "spawn_point": 13,
        "spawn_offset": -10.0,
        "initial_lane_index": 1,
        "sections": {
            0: 'straight'
        },
        "car_name": 'vehicle.chevrolet.impala'
    },

    # Initial lead vehicle that turns right at the second intersection
    1: {
        "type": VehicleType.LEAD,
        "spawn_point": 13,
        "spawn_offset": 0.0,
        "initial_lane_index": 1,
        "sections": {
            0: 'straight'
        },
        "car_name": 'vehicle.mercedes.coupe_2020'
    }
}


class FreewayExperiment(Experiment):

    # Current map from the Freeway experiment
    MAP = "Town04"
    
    def __init__(self, headless: bool) -> None:
        super(FreewayExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.FREEWAY

    def initialize_experiment(self, configuration: Dict[int, Dict[int, str]] = {}) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        :param configuration: a Dictionary containing the user defined settings for the experiment
        :return: None
        """

        # Add the managed sections to the Experiment
        first_section = FreewaySection(
            [self.map.get_waypoint(x.location) for x in (self.spawn_points[14], self.spawn_points[13], self.spawn_points[1])],
            [self.map.get_waypoint(x.location) for x in (self.spawn_points[20], self.spawn_points[19], self.spawn_points[18])]
        )

        # Add the FreewaySections to the experiment (must be added in order)
        self.add_section(first_section)

        # Add the vehicles according to the configuration dictionary
        self.add_vehicles_from_configuration(configuration)

        # Generate the paths for all the vehicles
        self._generate_section_paths(configuration)

        # Visualize the waypoints of the vehicles
        if configuration["debug"]:
            for vehicle in [self.ego_vehicle] + self.vehicle_list:
                vehicle.draw_waypoints(self.world)


def main() -> None:
    """
    Main Function to be run when the file is run as a standalone Python Script

    :return: None
    """

    # Create a new Experiment and initialize the server
    experiment = FreewayExperiment(True)
    experiment.initialize_carla_server(blocking=True)

    # Set up the experiment
    experiment.initialize_experiment(configuration_dictionary)

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
