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
from Controller import Controller
from Experiment import Experiment
from Vehicle import Vehicle
from Threading import HeadlessWindow
from Helpers import ExperimentType, VehicleType

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
import random
import sys
from typing import Dict, List, Tuple


class FreewayExperiment(Experiment):

    # The map for the Freeway Experiment
    MAP = "Town04"

    def __init__(self, headless: bool) -> None:
        super(FreewayExperiment, self).__init__(headless)
        self.experiment_type = ExperimentType.FREEWAY
       
    def initialize_experiment(self, configuration: Dict[int, Tuple[carla.Waypoint, carla.Waypoint]]) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        Adds vehicles to the map in the needed configuration for testing. Please modify this class to meet
        your testing needs

        :param configuration: a Dictionary containing the user defined settings for the Freeway experiment (exact properties
                              vary from experiment to experiment)
        :return: None
        """
        #Add the four freeways to the experiment TODO: figure out the freeway location
        first_freeway = None
        second_freeway = None
        third_freeway = None
        fourth_freeway = None 
        fifth_freeway = None

        #Add the freeways to the controller
        self.add_section(first_freeway)
        self.add_section(second_freeway)
        self.add_section(third_freeway)
        self.add_section(fourth_freeway)
        self.add_section(fifth_freeway)

         # Add a new test vehicle to the map TODO: figure out ego spwan point 
        ego_spawn_location = None 
        ego_vehicle = self.add_vehicle(ego_spawn_location, ego=True, type_id=VehicleType.EGO_FULL_AUTOMATIC)

        # Set the vehicle's initial section
        ego_vehicle.set_active_sections(first_freeway, fifth_freeway)

        # Config what the ego vehicle will do at each FreewaySection
        ego_configuration = {
            0: 'straight',
            1: 'left',
            2: 'right',
            3: 'straight',
            4: 'left'
        }
        configuration[ego_vehicle.id] = ego_configuration

        ######################################
        # add other vehicles if desired here #
        ######################################

        # Generate the paths for the vehicles
        self._generate_freeway_paths(configuration)

        # Visualize the waypoints of the ego vehicle
        self.ego_vehicle.draw_waypoints(self.world)



    def _generate_freeway_paths(self, configuration: Dict[int, Dict[int, str]]) -> None:
        """
        For each Vehicle, generate the path that will navigate them through each FreewaySection in
        the experiment, following the commands provided for each FreeWayIntersection.

        :param configuration: a Dict of Dicts storing what each Vehicle should do at a given point
        (left, right, straight)
        :return: None
        """
        for vehicle in [self.ego_vehicle] + self.vehicle_list:
            # Set the vehicle's first waypoint to their initial position
            vehicle.waypoints.append(self.map.get_waypoint(vehicle.get_current_location()))
            vehicle_configuration = configuration[vehicle.id]
            
            # Generate a path for the vehicles current last waypoint to the next lane TODO: FIX 
            for (i, lane) in enumerate(self.section_list):

                # Skip this lane if the vehicle doesn't interact with it
                if i not in vehicle_configuration:
                    continue

                # Add a new waypoint to move the vehicle through the lane
                thru_waypoints = lane.get_waypoints(self.map,
                                                                 vehicle.carla_vehicle.get_transform(),
                                                                 vehicle_configuration[i])
                if thru_waypoints is not None:
                    vehicle.waypoints += thru_waypoints
                

            None

def main() -> None:
    """
    Main Function to be run when the file is run as a standalone Python Script

    :return: None
    """

    # Create a new Experiment and initialize the server
    experiment = FreewayExperiment(True)
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
