#!/usr/bin/env python3
import re
import carla
import random
from .module_helper import find_weather_presets, get_actor_display_name
from .hud import HUD
from typing import Optional, List, Tuple, Dict, Any, Union
from umich_sim.wizard.inputs import ClientMode


class World(object):
    """
    Carla world object
    """
    __instance = None

    def __init__(self, client: carla.Client, hud, actor_filter,
                 map_name: Optional[str] = None):
        # Singleton check
        if World.__instance is None:
            World.__instance = self
        else:
            raise Exception("Error: Reinitialization of World")
        self.client: carla.Client = client
        if map_name is not None:
            self.world: carla.World = client.load_world(map_name)
        else:
            self.world: carla.World = client.get_world()
        self.hud: HUD = hud
        self.vehicle = None
        self.collision_sensor = None
        self.lane_invasion_sensor = None
        self.gnss_sensor = None
        self.imu_sensor = None
        self.camera_manager = None
        self.__weather_presets = find_weather_presets()
        self.__weather_index = 0
        self.__actor_filter = actor_filter
        # list of actors to be destroyed
        self.__destroy_actors: list = []
        self.world.on_tick(hud.on_world_tick)

        # default weather
        weather = carla.WeatherParameters(cloudiness=10.0,
                                          precipitation=0.0,
                                          sun_altitude_angle=90.0)
        self.world.set_weather(weather)

    @staticmethod
    def get_instance():
        if World.__instance is None:
            raise Exception("Class World not initialized")
        return World.__instance

    def restart(self):
        from umich_sim.sim_backend.carla_modules import CollisionSensor, LaneInvasionSensor, GnssSensor, IMUSensor, \
            CameraManager, EgoVehicle
        # Keep same camera config if the camera manager exists.
        cam_index = self.camera_manager.index if self.camera_manager is not None else 0
        cam_pos_index = self.camera_manager.transform_index if self.camera_manager is not None else 0
        # Get a random blueprint.
        #blueprint = random.choice(self.world.get_blueprint_library().filter(
            #self.__actor_filter))
        blueprint = self.world.get_blueprint_library().filter(self.__actor_filter)[0]
        blueprint.set_attribute('role_name', 'hero')
        if blueprint.has_attribute('color'):
            color = random.choice(
                blueprint.get_attribute('color').recommended_values)
            blueprint.set_attribute('color', color)
        # Spawn the vehicle.
        from umich_sim.sim_config import ConfigPool, Config
        if self.vehicle is not None:
            spawn_point = self.vehicle.get_transform()
            spawn_point.location.z += 2.0
            spawn_point.rotation.roll = 0.0
            spawn_point.rotation.pitch = 0.0
            self.destroy()
            self.vehicle.change_vehicle(blueprint, spawn_point)
        if self.vehicle is None:
            if ConfigPool.get_config().gui_mode:
                self.vehicle: EgoVehicle = EgoVehicle.get_instance()
            else:
                spawn_points = self.world.get_map().get_spawn_points()
                spawn_point = random.choice(
                    spawn_points) if spawn_points else carla.Transform()
                self.vehicle: EgoVehicle = EgoVehicle(blueprint, spawn_point)
            self.register_death(self.vehicle)
        # Set up the sensors.
        self.collision_sensor = CollisionSensor()
        self.lane_invasion_sensor = LaneInvasionSensor()
        self.gnss_sensor = GnssSensor()
        self.imu_sensor = IMUSensor()
        self.camera_manager = CameraManager()
        self.camera_manager.transform_index = cam_pos_index
        self.camera_manager.set_sensor(cam_index, notify=False)
        actor_type = get_actor_display_name(self.vehicle.carla_vehicle)
        self.hud.notification(actor_type)

    def next_weather(self, reverse=False):
        self.__weather_index += -1 if reverse else 1
        self.__weather_index %= len(self.__weather_presets)
        preset = self.__weather_presets[self.__weather_index]
        self.hud.notification('Weather: %s' % preset[1])
        self.world.set_weather(preset[0])

    def render(self, display):
        self.camera_manager.render(display)
        self.hud.render(display)

    def register_death(self, actor):
        """ Register the actors to be destroyed, actor should have destroy method"""
        self.__destroy_actors.append(actor)

    def destroy(self):
        "TODO: change to destructor"
        for actor in self.__destroy_actors:
            if actor is not None:
                try:
                    actor.destroy()
                except NameError:
                    print("actor does not have destroy method!")
        self.__destroy_actors.clear()
