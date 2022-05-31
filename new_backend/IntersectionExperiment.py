"""
Backend - IntersectionExperiment Class
Created on Monday, April 4th, 2022

Summary: The IntersectionExperiment class is a class that derives from the base Experiment class. It
         runs the Intersection experiment type

Usage: This file can be invoked as a regular python script to test out the experiment in the Carla
       environment. It can be invoked using "python IntersectionExperiment.py"

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
from Helpers import ExperimentType, VehicleType, project_forward, to_numpy_vector, smooth_path
from Threading import HeadlessWindow

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
import sys
from typing import Dict, List

# Sample configuration dictionary
# Notes: the vehicle with ID 0 must always be the ego vehicle,
# the vehicle's ID's must increase in consecutive order, otherwise later vehicles will be left out,
# the value of spawn_point corresponds with the spawn_point numbers found in the MapExplorationExperiment,
# spawn_offset shifts the spawn point forward or backward by x meters
configuration_dictionary = {
    "debug": True,
    "number_of_vehicles": 5,

    # Ego vehicle that simply goes straight through each intersection
    0: {
        "type": VehicleType.EGO_FULL_MANUAL,
        "spawn_point": 188,
        "spawn_offset": 0.0,
        "sections": {
            0: 'straight',
            1: 'straight',
            2: 'straight',
            3: 'straight'
        }
    },

    # Initial lead vehicle that turns right at the second intersection
    1: {
        "type": VehicleType.LEAD,
        "spawn_point": 188,
        "spawn_offset": 10.0,
        "sections": {
            0: 'straight',
            1: 'right'
        }
    },

    # Vehicle that turns right at initial intersection
    2: {
        "type": VehicleType.GENERIC,
        "spawn_point": 59,
        "spawn_offset": 0.0,
        "sections": {
            0: 'right'
        }
    },

    # Vehicle that turns right at the second intersection
    3: {
        "type": VehicleType.GENERIC,
        "spawn_point": 253,
        "spawn_offset": 0.0,
        "sections": {
            1: 'right'
        }
    },

    # Vehicle that turns left at the third intersection
    4: {
        "type": VehicleType.GENERIC,
        "spawn_point": 277,
        "spawn_offset": 0.0,
        "sections": {
            2: 'left',
            3: 'left'  # Current this is left due to some weirdness with Carla lanes, it actually goes straight
        }
    }
}


class IntersectionExperiment(Experiment):

    def __init__(self, headless: bool) -> None:
        super(IntersectionExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.INTERSECTION

    def initialize_experiment(self, configuration: Dict[int, Dict[int, str]] = {}) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        :param configuration: a Dictionary containing the user defined settings for the experiment
        :return: None
        """

        # Add the four managed intersections to the experiment
        first_intersection = Intersection(self.junctions[838], self.world.get_traffic_lights_in_junction(838))
        second_intersection = Intersection(self.junctions[979], self.world.get_traffic_lights_in_junction(979))
        third_intersection = Intersection(self.junctions[1427], self.world.get_traffic_lights_in_junction(1427))
        fourth_intersection = Intersection(self.junctions[1574], self.world.get_traffic_lights_in_junction(1574))

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
        if configuration["debug"]:
            for vehicle in [self.ego_vehicle] + self.vehicle_list:
                vehicle.draw_waypoints(self.world)


def main() -> None:
    """
    Main Function to be run when the file is run as a standalone Python Script

    :return: None
    """

    # Create a new Experiment and initialize the server
    experiment = IntersectionExperiment(True)
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
