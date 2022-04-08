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
        "type": VehicleType.EGO_FULL_AUTOMATIC,
        "spawn_point": 188,
        "spawn_offset": 0.0,
        "intersections": {
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
        "intersections": {
            0: 'straight',
            1: 'right'
        }
    },

    # Vehicle that turns right at initial intersection
    2: {
        "type": VehicleType.GENERIC,
        "spawn_point": 59,
        "spawn_offset": 0.0,
        "intersections": {
            0: 'right'
        }
    },

    # Vehicle that turns right at the second intersection
    3: {
        "type": VehicleType.GENERIC,
        "spawn_point": 253,
        "spawn_offset": 0.0,
        "intersections": {
            1: 'right'
        }
    },

    # Vehicle that turns left at the third intersection
    4: {
        "type": VehicleType.GENERIC,
        "spawn_point": 277,
        "spawn_offset": 0.0,
        "intersections": {
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

        for i in range(configuration["number_of_vehicles"]):
            vehicle_configuration = configuration[i]

            # Set up the Vehicle's spawn point
            spawn_point = self.spawn_points[vehicle_configuration["spawn_point"]]
            if vehicle_configuration["spawn_offset"] > 0.0:
                spawn_point = project_forward(spawn_point, vehicle_configuration["spawn_offset"])

            # Create the vehicle
            is_ego = vehicle_configuration["type"] in (VehicleType.EGO_FULL_AUTOMATIC, VehicleType.EGO_FULL_MANUAL,
                                                       VehicleType.EGO_MANUAL_STEER_AUTOMATIC_THROTTLE,
                                                       VehicleType.EGO_AUTOMATIC_STEER_MANUAL_THROTTLE)
            vehicle = self.add_vehicle(spawn_point, ego=is_ego, type_id=vehicle_configuration["type"])

            # Set which intersections the vehicle will be active at
            starting_section = min(vehicle_configuration["intersections"].keys())
            ending_section = max(vehicle_configuration["intersections"].keys())
            vehicle.set_active_sections(self.section_list[starting_section], self.section_list[ending_section])

        # Generate the paths for all the vehicles
        self._generate_intersection_paths(configuration)

        # Visualize the waypoints of the vehicles
        if configuration["debug"]:
            for vehicle in [self.ego_vehicle] + self.vehicle_list:
                vehicle.draw_waypoints(self.world)

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
            intersection_configuration = configuration[vehicle.id]["intersections"]

            # Generate a path for the vehicles current last waypoint to the next intersection
            for (i, intersection) in enumerate(self.section_list):

                # Skip this intersection if the vehicle doesn't interact with it
                if i not in intersection_configuration:
                    continue

                # Generate the path from the vehicles current position to their next intersection
                current_location = vehicle.waypoints[-1].transform.location
                _, next_waypoint = intersection.get_stop_location(to_numpy_vector(current_location))
                Controller.generate_path(vehicle, vehicle.waypoints[-1], next_waypoint)

                # Add a new waypoint to move the vehicle through the intersection
                thru_waypoints = intersection.get_thru_waypoints(self.map,
                                                                 vehicle.carla_vehicle.get_transform(),
                                                                 intersection_configuration[i])
                if thru_waypoints is not None:
                    vehicle.waypoints += thru_waypoints

                # If we've arrived at the last intersection, move forward some to clear the intersection
                # then stop
                if intersection.id == vehicle.ending_section.id:
                    vehicle.waypoints.append(
                        self.map.get_waypoint(project_forward(vehicle.waypoints[-1].transform, 15.0).location)
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
