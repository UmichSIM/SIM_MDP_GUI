#!/usr/bin/env python3
import carla
import weakref
import collections
import math
from .world import World, get_actor_display_name
from .hud import HUD
from .ego_vehicle import EgoVehicle
# from wizard.helper import *


class CollisionSensor:
    """
    Sensor to get the car collision data with the environment
    """

    def __init__(self):
        self.sensor = None
        self.history = []
        self._parent = EgoVehicle.get_instance().carla_vehicle
        self.hud = HUD.get_instance()
        world = World.get_instance().world
        bp = world.get_blueprint_library().find('sensor.other.collision')
        self.sensor = world.spawn_actor(bp,
                                        carla.Transform(),
                                        attach_to=self._parent)
        World.get_instance().register_death(self.sensor)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(
            lambda event: CollisionSensor._on_collision(weak_self, event))

    def get_collision_history(self):
        history = collections.defaultdict(int)
        for frame, intensity in self.history:
            history[frame] += intensity
        return history

    @staticmethod
    def _on_collision(weak_self, event):
        self = weak_self()
        if not self:
            return
        actor_type = get_actor_display_name(event.other_actor)
        self.hud.notification('Collision with %r' % actor_type)
        impulse = event.normal_impulse
        intensity = math.sqrt(impulse.x**2 + impulse.y**2 + impulse.z**2)
        self.history.append((event.frame, intensity))
        if len(self.history) > 4000:
            self.history.pop(0)
        
        EgoVehicle.get_instance().set_collision()