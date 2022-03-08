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
from ApiHelpers import ExperimentType
from Section import Section
from Threading import SIMThread, ThreadWorker
from Vehicle import Vehicle


# Library Imports
import carla
import logging
from pygame.time import Clock
from PyQt5.QtCore import QWaitCondition, QMutex
from typing import List, Dict
import sys


class Experiment:

    # Static variable denoting which map this experiment takes place on
    # Must be overridden by derived classes
    MAP = "Town05"

    # Pygame clock to control FrateRate dependant physics
    clock: Clock = Clock()

    # The Type of Experiment that is currently running
    experiment_type: ExperimentType = None

    # Single static wait condition to synchronize between threads if needed
    wait_condition: QWaitCondition = QWaitCondition()


    def __init__(self, headless: bool):

        # Indicates whether the experiment is being run with a GUI or standalone
        self.headless = headless

        # A Carla.Client object that stores the current connection to the server
        self.client: carla.Client = None

        # A Carla.World object that stores the current world the simulation is running in
        self.world: carla.World = None

        # A Carla.Action that represents the spectator in the Simulation
        self.spectator: carla.Actor = None

        # A single SIMThread to handle all threaded execution
        self.sim_thread: SIMThread = None

        # Track whether the connection to the server has been initialized
        self.server_initialized = False

        # Store the specific vehicle that is the Ego vehicle
        self.ego_vehicle: Vehicle = None

        # List of all vehicles in the Simulation
        self.vehicle_list: List[Vehicle] = []

        # List of all pedestrians/walkers in the Simulation
        self.pedestrian_list: List[carla.Walker] = []

        # List of all Sections (Intersections / Freeway Sections) in the Simulation
        self.section_list: List[Section] = []

        # List of all sensors in the Simulation
        self.sensor_list: List[carla.Sensor] = []

    def initialize_carla_server(self, blocking: bool = False, port: int = 2000) -> None:
        """
        Connects to the Carla server.

        :param blocking: a bool representing whether connecting to the server should block the GUI
                         or allow it to continue
        :param port: an int specifying the network port to connect to (defaults to 2000)
        :return: a bool indicating if the server connection was made successfully
        """

        if blocking:
            try:
                self._initialize_server_private(port)
                self._finish_server_connection(True)
            except Exception as e:
                logging.error(e)
                self._finish_server_connection(False)
            return

        worker = ThreadWorker(self._initialize_server_private, port)
        worker.call_when_finished(self._finish_server_connection)
        self.sim_thread = SIMThread(worker, "single")

    def _initialize_server_private(self, port: int = 2000) -> None:
        """
        Private function that handles the bulk of connecting to the Carla server.

        Separate private function is necessary to take advantage of QThreads. Designed to be run on
        a worker thread (non-main thread)

        :param port: an int specifying the network port to connect to (defaults to 2000)
        :return: None
        """

        logging.info(f"Connecting to the Server on port {port}")

        self.client = carla.Client("localhost", port)
        self.client.set_timeout(10.0)
        self.world = self.client.load_world(self.MAP)

        # Update this stuff later
        weather = carla.WeatherParameters(
            cloudiness=10.0,
            precipitation=0.0,
            sun_altitude_angle=90.0)
        self.world.set_weather(weather)

        self.spectator = self.world.get_spectator()
        self.spectator.set_transform(
            carla.Transform(carla.Location(x=-170, y=-151, z=116.5), carla.Rotation(pitch=-33, yaw=56.9, roll=0.0)))

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

        # Allow any threads waiting on a connection to continue
        self.wait_condition.wakeAll()

        if status:
            self.server_initialized = True
            logging.info(f"Successfully connected to the Carla Server")
            return

        logging.error("Unable to connect to Carla Server")
        sys.exit(-1)

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

        # Updates the global clock
        self.clock.tick()

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

    def add_vehicle(self, new_vehicle: Vehicle, ego: bool = False) -> None:
        """
        Adds a new Vehicle to the experiment.

        This function may be relocated later, but it currently exists here for testing purposes. Please
        delete this function if it gets relocated.

        :param new_vehicle: the Vehicle object to be added to the experiment
        :param ego: a bool representing whether the new Vehicle is the Ego Vehicle or not
        :return: None
        """

        if ego:
            if self.ego_vehicle is not None:
                raise Exception("Unable to add multiple ego vehicles.")
            self.ego_vehicle = new_vehicle

            # Set the camera to be located at the Ego vehicle
            self.world.tick()
            print(new_vehicle.get_transform())
            self.spectator.set_transform(new_vehicle.get_transform())

        else:
            self.vehicle_list.append(new_vehicle)
