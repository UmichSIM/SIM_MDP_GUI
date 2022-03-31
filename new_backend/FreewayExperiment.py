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

# Library Imports
import carla
from PyQt5.QtWidgets import QApplication
import random
import sys
from typing import Dict, List, Tuple

class FreewayExperiment(Experiment):

    def __init__(self) -> None:
        
        #test config dictioniary where key is the vehicle id and the value is a tuple/dict waypoints 
        config = {1: Tuple[w1, w2], 
                  2: Tuple[0, 1],
                  3: Tuple[0, 1]}
        # hardcode config dict for now (connect to gui later)
        # lanes - (lane #, starting waypoint, ending waypoint) (do we need to know lane numbers?)

    def initialize_experiment(self, config: Dict[int, Tuple[carla.Waypoint, carla.Waypoint]]) -> None:
        
        for vehicle in self.vehicle_list:
            # get start lane waypoint and end lane waypoint:
            starting_waypoint = config[vehicle][0]
            ending_waypoint = config[vehicle][1]
            Controller.generate_path(vehicle, starting_waypoint, ending_waypoint)

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
