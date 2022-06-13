"""
Backend - Experiment Class
Created on Tue May 31, 2022

Summary: The Experiment class is a base class that describes the high level interface that all
    derived experiments must implement. It provides all the functionality that is universal to all
    experiments and experiment types. Specific experiment types and specific maps must be represented
    as derived classes from this base class.

Update: trying to add wizard support

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
# from CarlaModules.HUD import HUD
# from CarlaModules.World import World
from CarlaModules.KeyboardController import KeyboardControl
from CarlaModules.GlobalFunctions import DefaultSettings
from Controller import WAYPOINT_SEPARATION, Controller
from EgoController import EgoController
from FreewayController import FreewayController
from FreewaySection import FreewaySection
from Helpers import ExperimentType, VehicleType, project_forward, to_numpy_vector, smooth_path
from Intersection import Intersection
from IntersectionController import IntersectionController
from Threading import SIMThread, ThreadWorker
from Vehicle import Vehicle
from wizard.controller import Controller as WizardController
from wizard.hud import HUD
from wizard.world import World

# Library Imports
import carla
import logging
import pygame
import random
import sys
from typing import List, Dict, Union
import csv

# List of pseudo random numbers for speed generation
random_speed = [
    77, 80, 88, 82, 80, 91, 82, 87, 86, 91, 80, 84, 90, 87, 81, 85, 82, 87, 86,
    82, 90, 83, 82, 88, 80, 78, 84, 78, 85, 84, 79, 80, 80, 79, 83, 77, 87, 78,
    84, 87, 84, 85, 90, 77, 78, 86, 83, 78, 82, 90, 90, 80, 83, 82, 83, 87, 78,
    83, 85, 91, 88, 85, 83, 78, 89, 85, 78, 80, 83, 78, 85, 86, 89, 87, 83, 81,
    79, 85, 77, 91, 84, 79, 88, 83, 86, 81, 89, 80, 77, 79, 84, 90, 84, 83, 90,
    78, 89, 78, 77, 90, 77, 91, 87, 77, 88, 85, 90, 78, 87, 85, 81, 80, 83, 89,
    86, 81, 84, 78, 91, 88, 77, 78, 79, 88, 78, 89, 87, 84, 82, 79, 83, 84, 89,
    79, 89, 86, 88, 82, 80, 77, 86, 80, 90, 80, 82, 91, 77, 85, 80, 83, 80, 81,
    90, 89, 79, 90, 89, 77, 91, 84, 86, 78, 81, 87, 79, 78, 89, 86, 91, 78, 80,
    86, 78, 88, 90, 84, 82, 86, 82, 84, 77, 86, 91, 91, 79, 91, 87, 84, 85, 87,
    85, 82, 89, 77, 79, 87, 89, 87, 85, 77, 85, 80, 77, 87, 81, 91, 81, 91, 86,
    88, 85, 83, 77, 89, 85, 87, 83, 79, 88, 81, 90, 83, 88, 82, 85, 85, 87, 89,
    77, 88, 85, 91, 77, 78, 82, 86, 90, 82, 89, 82, 77, 84, 83, 84, 88, 80, 84,
    91, 78, 86, 77, 84, 90, 89, 88, 78, 81, 82, 86, 88, 89, 85, 89, 90, 90, 78,
    81, 77, 77, 83, 86, 81, 79, 81, 78, 89, 78, 88, 80, 87, 78, 80, 91, 87, 84,
    83, 82, 78, 77, 83, 87, 80, 79, 83, 83, 89, 83, 90, 82, 84, 87, 82, 79, 84,
    88, 81, 91, 83, 86, 87, 77, 79, 82, 78, 86, 87, 87, 90, 91, 83, 79, 83, 88,
    78, 91, 82, 82, 81, 82, 77, 87, 79, 83, 90, 84, 78, 86, 87
]

logarray= []

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

        # A carla.Map object that stores the current map loaded in the simulation
        self.map: carla.Map = None

        # A list of carla.Transform that stores every recommended spawn point in the map
        self.spawn_points: List[carla.Transform] = None

        # A list of carla.Waypoint representing every waypoint present in the simulation
        self.waypoints: List[carla.Waypoint] = None

        # A Dict mapping the OpenDrive junction id to the carla.Junction object
        self.junctions: Dict[int, carla.Junction] = None

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

        # List that holds all the intersections or freeway sections in the experiment
        self.section_list: List[Union[Intersection, FreewaySection]] = []

    def initialize_carla_server(self,
                                blocking: bool = False,
                                port: int = 2000) -> None:
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
        
        #Get available maps
        print(self.client.get_available_maps())

        
        # Set the world to have some default weather parameters
        weather = carla.WeatherParameters(cloudiness=10.0,
                                          precipitation=0.0,
                                          sun_altitude_angle=90.0)
        self.world.set_weather(weather)

        # Set the world spectator to some arbitrary position
        self.spectator = self.world.get_spectator()
        self.spectator.set_transform(
            carla.Transform(carla.Location(x=-170, y=-151, z=116.5),
                            carla.Rotation(pitch=-33, yaw=56.9, roll=0.0)))

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

        # Initialize the experiment properties that rely on the server
        self.map = self.world.get_map()
        self.waypoints = list(
            filter(lambda x: x.lane_type == carla.LaneType.Driving,
                   self.map.generate_waypoints(WAYPOINT_SEPARATION)))
        self.spawn_points = self.map.get_spawn_points()

        # Initialize the junctions from the map
        self.junctions = {}
        for waypoint in self.waypoints:
            if waypoint.is_junction:
                if waypoint.get_junction().id not in self.junctions:
                    self.junctions[
                        waypoint.get_junction().id] = waypoint.get_junction()

        # Give each controller a copy of the world to use
        Controller.world = self.world

        if status:
            self.server_initialized = True
            # TODO: display some message in the GUI when connected to the server
            logging.info(f"Successfully connected to the Carla Server")
            return

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

    def _generate_section_paths(
            self, configuration: Dict[int, Dict[int, str]]) -> None:
        """
        For each Vehicle, generate the path that will navigate them through each section in
        the experiment, following the commands provided for each section.

        :param configuration: a Dict of Dicts storing what each Vehicle should do at each section
        :return: None
        """

        for vehicle in [self.ego_vehicle] + self.vehicle_list:
            # Set the vehicle's first waypoint to their initial position
            vehicle.waypoints.append(
                self.map.get_waypoint(vehicle.get_current_location()))
            section_configuration = configuration[vehicle.id]["sections"]

            # Generate a path for the vehicles current last waypoint to the next intersection
            for (i, section) in enumerate(self.section_list):

                # Skip this intersection if the vehicle doesn't interact with it
                if i not in section_configuration:
                    continue

                # Generate the path from the vehicles current position to the start of the next section
                initial_waypoint = section.get_initial_waypoint(vehicle)
                waypoints, trajectory = Controller.generate_path(
                    vehicle, vehicle.waypoints[-1], initial_waypoint)
                vehicle.waypoints += waypoints
                vehicle.trajectory += trajectory

                # Add a new waypoint to move the vehicle through the intersection
                thru_waypoints = section.get_thru_waypoints(
                    self.map, vehicle, section_configuration[i])
                if thru_waypoints is not None:
                    vehicle.waypoints += thru_waypoints

                # If we've arrived at the last intersection, move forward some to clear the intersection
                # then stop
                if section.id == vehicle.ending_section.id:
                    vehicle.waypoints.append(
                        self.map.get_waypoint(
                            project_forward(vehicle.waypoints[-1].transform,
                                            15.0).location))
                    # Also, make sure to re-smooth the trajectory
                    vehicle.trajectory = smooth_path(vehicle.waypoints)
                    break

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
            (0, 0), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        display.fill((0, 0, 0))
        pygame.display.flip()

        # Initialize the objects that will be rendered by Pygame
        hud = HUD(display.get_size()[0], display.get_size()[1])
        world = World(self.client.get_world(), hud, 'vehicle.*')

        # Initialize the controller to handle user input
        controller = WizardController(self.ego_vehicle.carla_vehicle)

        count_time = 0
        count_array = 0
        try:
            # Loop continuously
            clock = pygame.time.Clock()
            while (1):
                count_time += 1
                # Tick the Carla Simulation
                # world.tick()
                clock.tick(60)
                #pygame.event.pump()

                # Update the state of each of the experiment sections (mainly applicable to intersection and
                # traffic lights)
                for section in self.section_list:
                    section.tick()

                # Update the relative locations of each vehicle
                for vehicle in self.vehicle_list + [self.ego_vehicle]:
                    vehicle.update_other_vehicle_locations(self.vehicle_list)

                          

                # Apply control to the Ego Vehicle
                if self.ego_vehicle is not None:
                    # Lambda used to avoid passing all the arguments into the update_control function
                    EgoController.update_control(
                        self.ego_vehicle,
                        lambda: controller.tick_no_control(clock),
                        self.experiment_type)
                # Apply control to every other Vehicle().render(display)
                pygame.display.flip()
                for vehicle in self.vehicle_list:
                    '''
                    if self.experiment_type == ExperimentType.INTERSECTION:
                        IntersectionController.update_control(vehicle)
                    elif self.experiment_type == ExperimentType.FREEWAY:
                    '''
                    if (count_time == 150):
                        vehicle.target_speed = random_speed[count_array]
                        count_array += 1
                        count_time = 0
                    FreewayController.update_control(vehicle)
                    
                    
                # tick wizard controller
                output = controller.tick(clock)
                output.append(pygame.time.get_ticks())
                
                logarray.append(output)   

                if (count_array == len(random_speed)):
                    count_array = 0

                # Update the UI elements
                World.get_instance().render(display)
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
            
        #Append log array to file
        with open('log_experiment.csv', 'w', newline='') as csvfile:
            #write header
            headers = ['TimeStamp', 'Speed', 'Distance','Collision','Leading Speed','Ticks']
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)
            writer.writeheader()
            #write rows
            log_writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            #shit_arr = ['time', 'speed', 'distance', 'collision']
            log_writer.writerows(logarray)

    def add_vehicle(self,
                    spawn_location: carla.Transform,
                    type_id: VehicleType,
                    ego: bool = False,
                    blueprint_id: str = None) -> Vehicle:
        """a
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
        blueprint_list = self.world.get_blueprint_library().filter(
            'vehicle.*.*')
        if blueprint_id is not None:
            blueprint = blueprint_list.find(blueprint_id)
            
        else:
            blueprint_list = [
                x for x in blueprint_list
                if int(x.get_attribute('number_of_wheels')) != 2
            ]
            blueprint = random.choice(blueprint_list)
            
        
        if ego:
            if self.ego_vehicle is not None:
                raise Exception("Unable to add multiple ego vehicles.")
            
            
            
            # Create a new ego vehicle in the Simulation
            new_carla_vehicle = self.world.spawn_actor(blueprint,
                                                       spawn_location)
            # Make vehicle have automatic lights
            new_carla_vehicle.set_light_state(carla.VehicleLightState.Position)
            '''
            #Physics of the ego car - can change the parameters of the car
            physics_control = new_carla_vehicle.get_physics_control()
            #Change the physics of the wheels
            front_left_wheel  = carla.WheelPhysicsControl(tire_friction=8.0, damping_rate=2.0, max_steer_angle=70.0, radius=25.0)
            front_right_wheel = carla.WheelPhysicsControl(tire_friction=8.0, damping_rate=2.0, max_steer_angle=70.0, radius=25.0)
            rear_left_wheel   = carla.WheelPhysicsControl(tire_friction=8.0, damping_rate=2.0, max_steer_angle=0.0,  radius=20.0)
            rear_right_wheel  = carla.WheelPhysicsControl(tire_friction=8.0, damping_rate=2.0, max_steer_angle=0.0,  radius=20.0)

            wheels = [front_left_wheel, front_right_wheel, rear_left_wheel, rear_right_wheel]
            physics_control.wheels = wheels
            #apply physics to vehicle
            new_carla_vehicle.apply_physics_control(physics_control)
            '''
            
            new_vehicle = Vehicle(new_carla_vehicle, "Ego", type_id)
            self.ego_vehicle = new_vehicle

            # Set the camera to be located at the Ego vehicle
            self.world.tick()
            self.spectator.set_transform(
                new_vehicle.carla_vehicle.get_transform())

        else:
            # Sets color of car (for other cars only)
            blueprint.set_attribute('color','255,255,255') # (8, 0, 0) is a black car
            # Create a new non-ego vehicle in the Simulation
            new_carla_vehicle = self.world.spawn_actor(blueprint,
                                                       spawn_location)
            new_vehicle = Vehicle(new_carla_vehicle, "temp_id",
                                  VehicleType.GENERIC)
            self.vehicle_list.append(new_vehicle)
            
        

        return new_vehicle

    def add_vehicles_from_configuration(self, configuration: Dict[int,
                                                                  Dict[int,
                                                                       str]]):
        """
        Adds vehicles to the Experiment according to the configuration dictionary.

        :param configuration:
        :return:
        """

        for i in range(configuration["number_of_vehicles"]):
            vehicle_configuration = configuration[i]

            # Set up the Vehicle's spawn point
            spawn_point = self.spawn_points[
                vehicle_configuration["spawn_point"]]
            if "spawn_offset" in vehicle_configuration and vehicle_configuration[
                    "spawn_offset"] != 0.0:
                spawn_point = project_forward(
                    spawn_point, vehicle_configuration["spawn_offset"])

            # Create the vehicle
            is_ego = vehicle_configuration["type"] in (
                VehicleType.EGO_FULL_AUTOMATIC, VehicleType.EGO_FULL_MANUAL,
                VehicleType.EGO_MANUAL_STEER_AUTOMATIC_THROTTLE,
                VehicleType.EGO_AUTOMATIC_STEER_MANUAL_THROTTLE)
            if (is_ego):
                #get blueprint_id
                car_blueprint_id = vehicle_configuration["car_name"]
                vehicle = self.add_vehicle(
                    spawn_point,
                    ego=is_ego,
                    type_id=vehicle_configuration["type"],
                    blueprint_id=car_blueprint_id)
            else:
                vehicle = self.add_vehicle(
                    spawn_point,
                    ego=is_ego,
                    type_id=vehicle_configuration["type"],
                    blueprint_id=car_blueprint_id)

            # Set which sections the vehicle will be active at
            starting_section = min(vehicle_configuration["sections"].keys())
            ending_section = max(vehicle_configuration["sections"].keys())
            vehicle.set_active_sections(self.section_list[starting_section],
                                        self.section_list[ending_section])
            

            # Set the initial lane index that the vehicle is starting in
            # (this currently doesn't exist in the IntersectionExperiment but it should be added)
            if "initial_lane_index" in vehicle_configuration:
                vehicle.current_lane = vehicle_configuration[
                    "initial_lane_index"]

    def add_section(self, new_section: Union[Intersection,
                                             FreewaySection]) -> None:
        """
        Adds a new section to the Experiment.

        Adds the section to the section_list. Also, handles setting the "next_section" property
        of the previous section to point to the newly added section.

        :param new_section: an Intersection or Freeway Section to add to the experiment
        :return: None
        """

        if len(self.section_list) > 0:
            self.section_list[-1].next_section = new_section

        self.section_list.append(new_section)
