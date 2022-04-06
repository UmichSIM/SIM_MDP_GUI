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


class IntersectionExperiment(Experiment):

    def __init__(self, headless: bool) -> None:
        super(IntersectionExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.INTERSECTION

    def initialize_experiment(self, configuration: Dict[int, Dict[int, str]] = {}) -> None:
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
        ego_vehicle.set_active_sections(first_intersection, fourth_intersection)

        # Config what the ego vehicle will do at each intersection
        ego_configuration = {
            0: 'straight',
            1: 'straight',
            2: 'straight',
            3: 'straight'
        }
        configuration[ego_vehicle.id] = ego_configuration

        # Add a new vehicle directly in front of the initial vehicle
        lead_spawn_location = project_forward(ego_spawn_location, 10.0)
        lead_vehicle = self.add_vehicle(lead_spawn_location, ego=False, type_id=VehicleType.LEAD)

        # Set the vehicle's initial section
        lead_vehicle.set_active_sections(first_intersection, second_intersection)

        # Configure what the lead vehicle will do at each intersection
        lead_configuration = {
            0: 'straight',
            1: 'right'
        }
        configuration[lead_vehicle.id] = lead_configuration

        # Generate the paths for all the vehicles
        self._generate_intersection_paths(configuration)

        # Visualize the waypoints of the lead and ego vehicles
        self.ego_vehicle.draw_waypoints(self.world)
        self.vehicle_list[0].draw_waypoints(self.world)

    def _generate_intersection_paths(self, configuration: Dict[int, Dict[int, str]]) -> None:
        """
        For each Vehicle, generate the path that will navigate them through each intersection in
        the experiment, following the commands provided for each intersection.

        :param configuration: a Dict of Dicts storing what each Vehicle should do at each light
        :return: None
        """

        for vehicle in [self.ego_vehicle] + self.vehicle_list:
            # Set the vehicle's first waypoint to their initial position
            vehicle.waypoints.append(self.map.get_waypoint(vehicle.get_current_location()))
            vehicle_configuration = configuration[vehicle.id]

            # Generate a path for the vehicles current last waypoint to the next intersection
            for (i, intersection) in enumerate(self.section_list):
                current_location = vehicle.waypoints[-1].transform.location
                _, next_waypoint = intersection.get_stop_location(to_numpy_vector(current_location))
                Controller.generate_path(vehicle, vehicle.waypoints[-1], next_waypoint)

                # Add a new waypoint to move the vehicle through the intersection
                if vehicle_configuration[i] == 'straight':
                    vehicle.waypoints.append(
                        self.map.get_waypoint(project_forward(vehicle.waypoints[-1].transform, 15.0).location)
                    )
                else:
                    next_waypoint = intersection.get_turn_waypoint(vehicle.carla_vehicle.get_transform(),
                                                                   vehicle_configuration[i])
                    if next_waypoint is not None:
                        vehicle.waypoints.append(next_waypoint)

                # If we've arrived at the last intersection, move forward some to clear the intersection
                # then stop
                if intersection.id == vehicle.ending_section.id:
                    vehicle.waypoints.append(
                        self.map.get_waypoint(project_forward(vehicle.waypoints[-1].transform, 25.0).location)
                    )
                    # Also, make sure to re-smooth the trajectory
                    vehicle.trajectory = smooth_path(vehicle.waypoints)
                    break


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
