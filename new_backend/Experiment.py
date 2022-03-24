"""
Backend - Experiment Class
Created on Tue February 15, 2022

Summary: The Experiment class is a base class that describes the high level interface that all
    derived experiments must implement. It provides all the functionality that is universal to all
    experiments and experiment types. Specific experiment types and specific maps must be represented
    as derived classes from this base class.

References:
    CarlaModules
    EgoController
    FreewayController
    Helpers
    IntersectionController
    Section
    Threading
    Vehicle

Referenced By:
    MapExplorationExperiment
    TestExperiment

"""

# Local Imports
from CarlaModules.HUD import HUD
from CarlaModules.World import World
from CarlaModules.KeyboardController import KeyboardControl
from CarlaModules.GlobalFunctions import DefaultSettings
from EgoController import EgoController
from FreewayController import FreewayController
from Helpers import ExperimentType, VehicleType
from IntersectionController import IntersectionController
from Section import Section
from Threading import SIMThread, ThreadWorker
from Vehicle import Vehicle

# Library Imports
import carla
import logging
import pygame
import random
import sys
from typing import List, Dict


# noinspection PyTypeChecker
class Experiment:

    # Static variable denoting which map this experiment takes place on
    # Can be overridden by derived classes
    MAP = "Town05"

    # The Type of Experiment that is currently running
    experiment_type: ExperimentType = None

    def __init__(self, headless: bool):

        # Indicates whether the experiment is being run with a GUI or standalone
        self.headless = headless

        # A Carla.Client object that stores the current connection to the server
        self.client: carla.Client = None

        # A Carla.World object that stores the current world the simulation is running in
        self.world: carla.World = None

        # TODO: Implement these four attributes (initialize them at the end of connect to server)
        # A carla.Map object that stores the current map loaded in the simulation
        self.map: carla.Map = None

        # A list of carla.Transform that stores every recommended spawn point in the map
        self.spawn_points: List[carla.Transform] = None

        # A list of carla.Waypoint representing every waypoint present in the simulation
        self.waypoints: List[carla.Waypoint] = None

        # A list of carla.Junction represent every junction present in the simulation
        self.junctions: List[carla.Junction] = None

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

        # List of all Sections (Intersections / Freeway Sections) in the Simulation
        self.section_list: List[Section] = []

    def initialize_carla_server(self, blocking: bool = False, port: int = 2000) -> None:
        """
        Connects to the Carla server.

        :param blocking: a bool representing whether connecting to the server should block the GUI
                         or allow it to continue
        :param port: an int specifying the network port to connect to (defaults to 2000)
        :returns: None
        """

        # If blocking, just directly call the connection functions
        if blocking:
            try:
                self._initialize_server_private(port)
                self._finish_server_connection(True)
            except Exception as e:
                logging.error(e)
                self._finish_server_connection(False)
            return

        # If non-blocking, call the connection functions in a separate thread
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

        # Connect to the Carla server
        self.client = carla.Client("localhost", port)
        self.client.set_timeout(20.0)
        self.world = self.client.load_world(self.MAP)

        # Set the world to have some default weather parameters
        weather = carla.WeatherParameters(
            cloudiness=10.0,
            precipitation=0.0,
            sun_altitude_angle=90.0)
        self.world.set_weather(weather)

        # Set the world spectator to some arbitrary position
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

        if status:
            self.server_initialized = True
            # TODO: display some message in the GUI when connected to the server
            logging.info(f"Successfully connected to the Carla Server")
            return

        # Initialize the experiment properties that rely on the server
        self.map = self.world.get_map()
        self.waypoints

        # Exit the GUI if unable to connect to server
        logging.error("Unable to connect to Carla Server")
        sys.exit(-1)

    def initialize_experiment(self, configuration: Dict[str, str]) -> None:
        """
        Uses an existing connection to the Carla server and configures the world according to the experiment design.

        THIS FUNCTION IS ABSTRACT, IT MUST BE IMPLEMENTED BY THE DERIVED EXPERIMENT CLASS. OTHERWISE,
        NOTHING WILL HAPPEN WHEN YOU GO TO RUN THE EXPERIMENT.
        Adds vehicles in the places specified in the GUI, generates paths for all non-Ego vehicles,
        specifies traffic light settings.

        :param configuration: a Dictionary containing the user defined settings for the experiment (exact properties
                              vary from experiment to experiment)
        :return: None
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

        # Initialize Pygame to handle user input
        pygame.init()

        # Initialize the Pygame display
        display = pygame.display.set_mode(
            (0, 0),
            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        display.fill((0, 0, 0))
        pygame.display.flip()

        # Initialize the objects that will be rendered by Pygame
        hud = HUD(display.get_size()[0], display.get_size()[1])
        world = World(self.ego_vehicle.carla_vehicle, self.world, hud, DefaultSettings())

        # Initialize the controller to handle user input
        controller = KeyboardControl(world, False)

        try:
            # Loop continuously
            clock = pygame.time.Clock()
            while True:

                # Tick the Carla Simulation
                self.world.tick()
                clock.tick(60)
                pygame.event.pump()

                # Update the relative locations of each vehicle
                for vehicle in self.vehicle_list + [self.ego_vehicle]:
                    vehicle.update_other_vehicle_locations(self.vehicle_list)

                # Apply control to the Ego Vehicle
                if self.ego_vehicle is not None:
                    # Lambda used to avoid passing all the arguments into the update_control function
                    EgoController.update_control(self.ego_vehicle,
                                                 lambda: controller.parse_events(self.client, world, clock, True),
                                                 self.experiment_type)

                # Apply control to every other Vehicle
                for vehicle in self.vehicle_list:
                    if self.experiment_type == ExperimentType.INTERSECTION:
                        IntersectionController.update_control(vehicle)
                    elif self.experiment_type == ExperimentType.FREEWAY:
                        FreewayController.update_control(vehicle)

                # Update the UI elements
                world.tick(clock, self.ego_vehicle)
                world.render(display)
                pygame.display.flip()

        finally:
            world.destroy()

    def clean_up_experiment(self) -> None:
        """
        Destroys all the actors that have been spawned in the Carla simulation.

        :return: None
        """
        for vehicle in self.vehicle_list:
            vehicle.carla_vehicle.destroy()

    # TODO: add new parameters to this function as needed
    def add_vehicle(self, spawn_location: carla.Transform, type_id: VehicleType, ego: bool = False,
                    blueprint_id: str = None) -> Vehicle:
        """
        Adds a new Vehicle to the experiment.

        The new vehicle will be added at the location specified by spawn_location. The specific type of the vehicle
        must be specified so the correct type of control is applied to the vehicle.

        :param spawn_location: a carla.Transform representing where the Vehicle should spawn in the world
        :param type_id: the VehicleType of the carla.Vehicle to specify the type of the Vehicle
        :param ego: a bool representing whether the new Vehicle is the Ego Vehicle or not
        :param blueprint_id: a str representing the specific name of the Vehicle blueprint to use. If not provided,
                          a random blueprint is used
        :returns: the created Vehicle object
        """

        # Grab the selected blueprint if one was provided, otherwise select a random non-bike blueprint
        blueprint_list = self.world.get_blueprint_library().filter('vehicle.*.*')
        if blueprint_id is not None:
            blueprint = blueprint_list.find(blueprint_id)
        else:
            blueprint_list = [x for x in blueprint_list if int(x.get_attribute('number_of_wheels')) != 2]
            blueprint = random.choice(blueprint_list)

        if ego:
            if self.ego_vehicle is not None:
                raise Exception("Unable to add multiple ego vehicles.")

            # Create a new ego vehicle in the Simulation
            new_carla_vehicle = self.world.spawn_actor(blueprint, spawn_location)
            new_vehicle = Vehicle(new_carla_vehicle, "Ego", type_id)
            self.ego_vehicle = new_vehicle

            # Set the camera to be located at the Ego vehicle
            self.world.tick()
            self.spectator.set_transform(new_vehicle.carla_vehicle.get_transform())

        else:
            # Create a new non-ego vehicle in the Simulation
            new_carla_vehicle = self.world.spawn_actor(blueprint, spawn_location)
            new_vehicle = Vehicle(new_carla_vehicle, "temp_id", VehicleType.GENERIC)
            self.vehicle_list.append(new_vehicle)

        return new_vehicle

    def get_vehicles_current_waypoint(self, vehicle: Vehicle) -> carla.Waypoint:
        """
        Gets an OpenDrive waypoint located at the Vehicle's current location.

        :param vehicle: the Vehicle whose current waypoint is desired
        :return: a carla.Waypoint located at the vehicle's current location
        """
        return self.world.get_map().get_waypoint(vehicle.carla_vehicle.get_location())