"""
Backend - Experiment Class
Created on Tue February 15, 2022

Summary: The Experiment class is a base class that describes the high level interface that all
    derived experiments must implement. It provides all the functionality that is universal to all
    experiments and experiment types. Specific experiment types and specific maps must be represented
    as derived classes from this base class.

References:

Referenced By:

"""

# Local Imports
import Section
from Threading import SIMThread, ThreadWorker
import Vehicle


# Library Imports
import carla
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from typing import List, Dict


class Experiment:

    # Static variable denoting which map this experiment takes place on
    # Must be overridden by derived classes
    MAP = "Town10"

    def __init__(self, headless: bool):

        # Indicates whether the experiment is being run with a GUI or standalone
        self.headless = headless

        # A single SIMThread to handle all threaded execution
        self.sim_thread: SIMThread = None

        # List of all vehicles in the Simulation
        self.vehicle_list: List[Vehicle] = []

        # List of all pedestrians/walkers in the Simulation
        self.pedestrian_list: List[carla.Walker] = []

        # List of all Sections (Intersections / Freeway Sections) in the Simulation
        self.section_list: List[Section] = []

        # List of all sensors in the Simulation
        self.sensor_list: List[carla.Sensor] = []



    def initialize_carla_server(self, blocking: bool = True, port: int = 2000) -> None:
        """
        Connects to the Carla server.

        :param blocking: a Bool indicated whether the connection should be made concurrently on a
                         separate thread or if the application should block until completed (defaults to True)
        :param port: an int specifying the network port to connect to (defaults to 2000)
        :return: a bool indicating if the server connection was made successfully
        """

        worker = ThreadWorker(self._initialize_server_private, port)
        worker.call_when_finished(self._finish_server_connection)
        print("Starting connection thread")
        self.sim_thread = SIMThread(worker)


    def _initialize_server_private(self, port: int = 2000) -> None:
        """
        Private function that handles the bulk of connecting to the Carla server.

        Separate private function is necessary to take advantage of QThreads. Designed to be run on
        a worker thread (non-main thread)

        :param port: an int specifying the network port to connect to (defaults to 2000)
        :return: None
        """

        print(f"Connecting to the Server on port {port}")

    def _finish_server_connection(self, status: bool) -> None:
        """
        Private function that handles updating the GUI after the connection to the Carla server is made.

        Should be connected to the worker thread's "Finished" signal. Must be run on the main thread
        in order to update the GUI. On successful connection, will display a toast style notification
        indicating that the connection succeeded. On failure, will display an error message and close
        the GUI. If the experiment is currently headless, only command line output will be created.

        :param status: a bool indicating if connection to the Carla server was successful
        :return: None
        """

        print(f"Connected to the Server: {status}")

    def initialize_experiment(self, configuration: Dict[str, str]) -> bool:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        THIS FUNCTION IS ABSTRACT, IT MUST BE IMPLEMENTED BY THE DERIVED EXPERIMENT CLASS. OTHERWISE,
        NOTHING WILL HAPPEN WHEN YOU GO TO RUN THE EXPERIMENT.
        Adds vehicles in the places specified in the GUI, generates paths for all non-Ego vehicles,
        specifies traffic light settings.

        :param configuration: a Dictionary containing the user defined settings for the experiment (exact properties
                              vary from experiment to experiment)
        :return: a bool indicating if the experiment was configured correctly
        """
        pass

    def run_experiment(self) -> None:
        """
        Runs a basic main simulation loop to drive the experiment.

        Any additional functionality can be added by overloading this function in a derived class.
        Spawns a new thread to control each manually driven vehicle. Each tick, updates the positions of
        each vehicle and applies autonomous control to each vehicle.

        :return: None
        """
        pass

    def clean_up_experiment(self) -> None:
        """
        Destroys all the actors that have been spawned in the Carla simulation.

        :return: None
        """
        for vehicle in self.vehicle_list:
            vehicle.destroy()
        for pedestrian in self.pedestrian_list:
            pedestrian.destroy()
        for sensor in self.sensor_list:
            sensor.destroy()