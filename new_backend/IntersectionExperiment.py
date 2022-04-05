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
from Helpers import ExperimentType, VehicleType, project_forward
from Threading import HeadlessWindow

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
import sys
from typing import Dict, List


class IntersectionExperiment(Experiment):

    def __init__(self, headless: bool) -> None:
        super(IntersectionExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.INTERSECTION

    def initialize_experiment(self, configuration: Dict[str, str] = None) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        Adds vehicles to the map in the needed configuration for testing. Please modify this class to meet
        your testing needs

        :param configuration: a Dictionary containing the user defined settings for the experiment (exact properties
                              vary from experiment to experiment)
        :return: None
        """

        # Add the four managed intersections to the experiment
        first_intersection = Intersection(self.junctions[838], self.world.get_traffic_lights_in_junction(838))
        second_intersection = Intersection(self.junctions[979], self.world.get_traffic_lights_in_junction(979))
        third_intersection = Intersection(self.junctions[1427], self.world.get_traffic_lights_in_junction(1427))
        fourth_intersection = Intersection(self.junctions[1574], self.world.get_traffic_lights_in_junction(1574))

        # Add the first intersection to the controller (must be added in order)
        self.add_section(first_intersection)
        self.add_section(second_intersection)
        self.add_section(third_intersection)
        self.add_section(fourth_intersection)

        # Add a new test vehicle to the map
        ego_spawn_location = self.spawn_points[188]
        ego_vehicle = self.add_vehicle(ego_spawn_location, ego=True, type_id=VehicleType.EGO_FULL_AUTOMATIC)

        # Set the vehicle's initial section
        ego_vehicle.current_section = first_intersection

        # Generate a straight forward path for the ego vehicle
        Controller.generate_path(ego_vehicle, self.map.get_waypoint(ego_spawn_location.location),
                                 self.map.get_waypoint(carla.Location(x=90, y=2, z=0)))

        # Add a new vehicle directly in front of the initial vehicle
        lead_spawn_location = project_forward(ego_spawn_location, 10.0)
        lead_vehicle = self.add_vehicle(lead_spawn_location, ego=False, type_id=VehicleType.LEAD)

        # Set the vehicle's initial section
        lead_vehicle.current_section = first_intersection

        # Generate a straight forward path for the vehicle in front
        Controller.generate_path(lead_vehicle, self.map.get_waypoint(lead_spawn_location.location),
                                 self.map.get_waypoint(carla.Location(x=90, y=2, z=0)))

        # Visualize the waypoints of the lead vehicle
        self.vehicle_list[0].draw_waypoints(self.world)


def main() -> None:
    """
    Main Function to be run when the file is run as a standalone Python Script

    :return: None
    """

    # Create a new Experiment and initialize the server
    experiment = IntersectionExperiment(True)
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
