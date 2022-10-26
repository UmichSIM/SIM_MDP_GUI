#!/usr/bin/env python3
import carla
import weakref
from .world import World
from .hud import HUD
from .ego_vehicle import EgoVehicle
import time

class LaneInvasionSensor(object):
    """
    Sensor to detect Lane Invasion
    """

    def __init__(self):
        self.sensor = None
        self._parent = EgoVehicle.get_instance().carla_vehicle
        self.hud = HUD.get_instance()
        world = World.get_instance().world
        bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
        is_modifiable = bp.get_attribute("sensor_tick") #.is_modifiable()
        print("sensor tick modifiable: ", is_modifiable)
        # bp.set_attribute("sensor_tick", 0.1)




        self.sensor = world.spawn_actor(bp,
                                        carla.Transform(),
                                        attach_to=self._parent)
        World.get_instance().register_death(self.sensor)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(
            lambda event: LaneInvasionSensor._on_invasion(weak_self, event))

    @staticmethod
    def _on_invasion(weak_self, event):
        self = weak_self()
        if not self:
            return
        lane_types = set(x.type for x in event.crossed_lane_markings)
        print(time.time(), "lane invasion: ", lane_types)
        text = ['%r' % str(x).split()[-1] for x in lane_types]
        self.hud.notification('Crossed line %s' % ' and '.join(text))
