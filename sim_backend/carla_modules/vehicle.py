#!/usr/bin/env python3
from time import time
import carla
from sim_backend.wizard.drivers.inputs import InputDevType, InputPacket
from sim_backend.wizard import config
from sim_backend.wizard.rpc import RPC
from sim_backend.wizard.config import WheelType
from evdev import ecodes


class Vehicle:
    """
    Vehicle class is a wrapper for carla vehicle apis and is combined
    with wizard switching functions. It also owns the drivers for the
    racing wheels. The class is a singleton.
    """
    __instance = None

    def __init__(self, blueprint, spawn_point):
        """
        Inputs:
            blueprint: the model for the vehicle to use
            spawn_point: initial transformation data of the vehicle
        for more information on the input, refer to Carla API documents
        """
        # Singleton
        if Vehicle.__instance is None:
            Vehicle.__instance = self
        else:
            raise Exception("Error: Reinitialization of Vehicle.")

        from . import World
        world = World.get_instance()
        # user mode, directly create vehicles
        if config.client_mode == InputDevType.WHEEL:
            self.vehicle:carla.Vehicle = \
                world.world.try_spawn_actor(blueprint, spawn_point)
        else:  # wizard mode TODO: prompt to choose vehicle
            vehicles = world.world.get_actors().filter('vehicle.*')
            self.vehicle: carla.Vehicle = vehicles[0]

        # control info from agent racing wheel
        self._local_ctl: carla.VehicleControl = carla.VehicleControl()
        # control info from carla server
        self._carla_ctl: carla.VehicleControl = carla.VehicleControl()
        # rpc server
        self._rpc: RPC = RPC.get_instance()
        # who is driving
        self.driver: InputDevType = self._rpc.get_driver()
        self.joystick_wheel: WheelType = WheelType(config.client_mode,
                                                   config.user_input_event)

    @staticmethod
    def get_instance():
        "get the instance of the singleton"
        if Vehicle.__instance is None:
            raise Exception("Error: Class Vehicle not initialized")
        return Vehicle.__instance

    def start(self):
        self.joystick_wheel.start()

    def destroy(self):
        """
        destroy the vehicle
        TODO: change to destructor
        """
        self.vehicle.destroy()
        self.joystick_wheel.stop()

    # TODO: recover this
    def change_vehicle(self, blueprint, spawn_point):
        "Using carla api to change the current vehicle"
        from . import World
        self.vehicle.destroy()
        self.vehicle:carla.Vehicle = \
            World.get_instance().world.try_spawn_actor(blueprint, spawn_point)

    def switch_driver(self, data: InputPacket):
        "Switch the current driver, wizard should be enabled"
        assert (data.dev == InputDevType.WIZARD
                or data.dev == InputDevType.WHEEL)
        # react on push
        if data.val != 1: return
        # change user
        if self.driver == InputDevType.WIZARD:
            self.driver = InputDevType.WHEEL
        else:
            self.driver = InputDevType.WIZARD
        self._rpc.set_driver(self.driver)

        # should reinit the control TODO: why?
        # self._ctl = carla.VehicleControl()
        # self.vehicle.apply_control(self._ctl)

    def get_transform(self):
        "from carla Vehicle api"
        return self.vehicle.get_transform()

    def get_velocity(self):
        "from carla Vehicle api"
        return self.vehicle.get_velocity()

    def update(self):
        """
        Update the vehicle status
        """
        self.driver = self._rpc.get_driver()
        if self.driver == config.client_mode:
            # update control
            self.vehicle.apply_control(self._local_ctl)
            self._carla_ctl = self._local_ctl
            # erase spring effect
            self.joystick_wheel.erase_ff(ecodes.FF_SPRING)
            # force feedback based on current states
            self.joystick_wheel.SetSpeedFeedback()
            # upload wheel position
            self._rpc.set_wheel(self._carla_ctl.steer)
        else:
            self._carla_ctl = self.vehicle.get_control()
            # erase auto-center
            self.joystick_wheel.erase_ff(ecodes.FF_AUTOCENTER)
            # force follow
            self.joystick_wheel.SetWheelPos(self._rpc.get_wheel())

    def set_brake(self, data: InputPacket):
        "set the vehicle brake value"
        self._local_ctl.brake = self.joystick_wheel.PedalMap(data.val)

    def set_throttle(self, data: InputPacket):
        "set the vehicle throttle value"
        self._local_ctl.throttle = self.joystick_wheel.PedalMap(data.val)

    def set_steer(self, data: InputPacket):
        "set the vehicle steer value"
        self._local_ctl.steer = self.joystick_wheel.SteerMap(data.val)

    def set_reverse(self, dev: InputDevType, val: bool):
        "Set the inverse mode of the vehicle"
        self._local_ctl.reverse = val

    def get_control(self):
        "From carla api"
        return self._carla_ctl

    def get_driver_name(self) -> str:
        "Get the current driver as string"
        if self.driver == InputDevType.WHEEL:
            return "Human"
        else:
            return "Wizard"
