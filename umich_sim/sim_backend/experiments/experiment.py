#!/usr/bin/env python3
"""
Backend - Experiment Class
Created on Tue February 15, 2022

Summary: The Experiment class is a base class that describes the high level interface that all
    derived experiments must implement. It provides all the functionality that is universal to all
    experiments and experiment types. Specific experiment types and specific maps must be represented
    as derived classes from this base class.
"""

# Local Imports
from umich_sim.sim_backend.carla_modules import (HUD, World, Vehicle, EgoVehicle, )
from umich_sim.sim_backend.vehicle_control.base_controller import WAYPOINT_SEPARATION
from umich_sim.sim_backend.vehicle_control import (VehicleController, EgoController)
from umich_sim.sim_backend.sections import Section
from umich_sim.sim_backend.helpers import (smooth_path, project_forward)
from umich_sim.sim_config import Task, VehicleType
from umich_sim.sim_config import ConfigPool, Config, ScenarioConfig
from umich_sim.wizard import Wizard

# Library Imports
import carla
import pygame
import random
from typing import List, Dict
from abc import ABCMeta, abstractmethod


# noinspection PyTypeChecker
class Experiment(metaclass=ABCMeta):
    # Static variable denoting which map this experiment takes place on
    # Can be overridden by derived classes
    MAP = "Town05"

    # The Type of Experiment that is currently running
    experiment_type: Task = None

    def __init__(self, headless: bool):

        # Indicates whether the experiment is being run with a GUI or standalone
        self.display = None
        self.wizard = None
        self.server_initialized: bool = False
        self.headless = headless

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

        # Store the specific vehicle that is the Ego vehicle
        self.ego_vehicle: Vehicle = None

        # List of all vehicles in the Simulation
        self.vehicle_list: List[Vehicle] = []

        # List that holds all the intersections or freeway sections in the experiment
        self.section_list: List[Section] = []

    def init(self) -> None:
        """
        Connects to the Carla server.

        :returns: None
        """
        config: Config = ConfigPool.get_config()
        pygame.init()
        pygame.font.init()

        self.display = pygame.display.set_mode(config.client_resolution,
                                               pygame.HWSURFACE | pygame.DOUBLEBUF)
        try:
            client = carla.Client(config.server_addr, config.carla_port)
            client.set_timeout(4.0)

            hud = HUD(*config.client_resolution)
            world: World = World(client, hud, config.car_filter, self.MAP)
            self.wizard = Wizard.get_instance()

            self.spectator = world.world.get_spectator()
            self.spectator.set_transform(
                carla.Transform(carla.Location(x=-170, y=-151, z=116.5),
                                carla.Rotation(pitch=-33, yaw=56.9, roll=0.0)))

            self.map = world.world.get_map()
            self.waypoints = list(
                filter(lambda x: x.lane_type == carla.LaneType.Driving,
                       self.map.generate_waypoints(WAYPOINT_SEPARATION)))
            self.spawn_points = self.map.get_spawn_points()

            # Initialize the junctions from the map
            self.junctions = {}
            for waypoint in self.waypoints:
                if waypoint.is_junction:
                    if waypoint.get_junction().id not in self.junctions:
                        self.junctions[waypoint.get_junction().
                        id] = waypoint.get_junction()

            self.server_initialized = True
        finally:
            pass
            # print("aba")

    @abstractmethod
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
                waypoints, trajectory = VehicleController.generate_path(
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

        config: Config = ConfigPool.get_config()

        world: World = World.get_instance()
        hud: HUD = HUD.get_instance()
        world.restart()

        try:
            # Loop continuously
            clock = pygame.time.Clock()
            while True:
                # check if program need to stop
                if self.wizard.is_stopping():
                    break

                # Tick the clock
                clock.tick(config.client_frame_rate)
                # clock.tick_busy_loop(config.client_frame_rate) # use more cpu for accuracy

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
                    EgoController.update_control(self.ego_vehicle,
                                                 self.experiment_type)

                # Apply control to every other Vehicle
                for vehicle in self.vehicle_list:
                    self.update_control(vehicle)

                # Update the UI elements
                hud.tick(clock)
                world.render(self.display)
                # Do you call the event queue every tick? If not pygame may become unresponsive.
                # See: https://www.pygame.org/docs/ref/event.html#pygame.event.pump
                pygame.event.pump()
                pygame.display.flip()
        finally:
            world.destroy()
            pygame.quit()

    @abstractmethod
    def update_control(self, vehicle: Vehicle) -> None:
        """
        update control based on specific experiment type
        :param vehicle: the vehicle to update control
        """
        pass

    def clean_up_experiment(self) -> None:
        """
        Destroys all the actors that have been spawned in the Carla simulation.

        :return: None
        """
        for vehicle in self.vehicle_list:
            vehicle.carla_vehicle.destroy()

    def add_vehicle(self,
                    spawn_location: carla.Transform,
                    type_id: VehicleType,
                    ego: bool = False,
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

        world = World.get_instance()
        # Grab the selected blueprint if one was provided, otherwise select a random non-bike blueprint
        blueprint_list = world.world.get_blueprint_library().filter(
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
            new_carla_vehicle = world.world.spawn_actor(
                blueprint, spawn_location)
            self.ego_vehicle = EgoVehicle.get_instance()
            self.ego_vehicle.set_vehicle(new_carla_vehicle)

            # Set the camera to be located at the Ego vehicle
            self.spectator.set_transform(
                self.ego_vehicle.carla_vehicle.get_transform())

            return self.ego_vehicle

        else:
            # Create a new non-ego vehicle in the Simulation
            new_carla_vehicle = world.world.spawn_actor(
                blueprint, spawn_location)
            new_vehicle = Vehicle(new_carla_vehicle, "temp_id",
                                  VehicleType.GENERIC)
            self.vehicle_list.append(new_vehicle)

            return new_vehicle

    def add_vehicles_from_configuration(self, sconfig: ScenarioConfig):
        """
        Adds vehicles to the Experiment according to the configuration dictionary.
        :param configuration:
        :return:
        """
        units = sconfig.intersections if sconfig.task == Task.INTERSECTION else sconfig.freeways
        for unit in units:
            # unit is either intersection or freeway
            for lane_vehicles in unit.vehicles:
                for vehicle in lane_vehicles:
                    # set up spawn points
                    spawn_point = self.spawn_points[vehicle.spawn_point]
                    if vehicle.spawn_offset != 0.0:
                        spawn_point = project_forward(spawn_point, vehicle.spawn_offset)

                    # create vehicle
                    is_ego = vehicle.exp_settings.vehicle_type in (VehicleType.EGO, VehicleType.EGO_FULL_MANUAL, VehicleType.EGO_MANUAL_STEER)
                    vehicle_created: Vehicle = \
                        self.add_vehicle(spawn_location = spawn_point, ego=is_ego, type_id=vehicle.exp_settings.vehicle_type)

                    # Set which sections the vehicle will be active at
                    starting_section = min(vehicle.sections.keys())
                    ending_section = max(vehicle.sections.keys())
                    vehicle_created.set_active_sections(self.section_list[starting_section], self.section_list[ending_section])

                    # Set the initial lane index that the vehicle is starting in
                    # (this currently doesn't exist in the IntersectionExperiment but it should be added)
                    # if "initial_lane_index" in vehicle:
                    #     vehicle.current_lane = vehicle["initial_lane_index"]
                    pass

    def add_section(self, new_section: Section) -> None:
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
