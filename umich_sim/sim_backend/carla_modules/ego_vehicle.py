#!/usr/bin/env python3
from time import time
import carla
from umich_sim.wizard.inputs import ClientMode, InputPacket, InputDevice, create_input_device
from umich_sim.sim_config import ConfigPool, Config
from umich_sim.sim_backend.helpers import VehicleType
from .vehicle import Vehicle


class EgoVehicle:
    """
    Vehicle class is a wrapper for carla vehicle apis and is combined
    with wizard switching functions. It also owns the drivers for the
    racing wheels. The class is a singleton.
    """
    __instance = None

    def __init__(self, blueprint=None, spawn_point=None):
        """
        Inputs:
            blueprint: the model for the vehicle to use
            spawn_point: initial transformation data of the vehicle
        for more information on the input, refer to Carla API documents
        """
        # Singleton
        if EgoVehicle.__instance is None:
            EgoVehicle.__instance = self
        else:
            raise Exception("Error: Reinitialization of Vehicle.")

        from . import World
        world = World.get_instance()
        config: Config = ConfigPool.get_config()
        # user mode, directly create vehicles
        if config.gui_mode:
            self.carla_vehicle = None
        elif config.client_mode == ClientMode.EGO:
            self.carla_vehicle: carla.Vehicle = \
                world.world.try_spawn_actor(blueprint, spawn_point)
        elif config.client_mode == ClientMode.WIZARD:
            vehicles = world.world.get_actors().filter('vehicle.*')
            self.carla_vehicle: carla.Vehicle = vehicles[0]

        # control info from agent racing wheel
        self._local_ctl: carla.VehicleControl = carla.VehicleControl()
        # control info from carla server
        self._carla_ctl: carla.VehicleControl = carla.VehicleControl()
        # rpc server
        self.enable_rpc = config.wizard.enable_rpc
        if self.enable_rpc:
            from umich_sim.wizard.rpc import RPC
            self._rpc: RPC = RPC.get_instance()
            # who is driving
            self.driver: ClientMode = self._rpc.get_driver()
        else:
            self.driver: ClientMode = ClientMode.EGO
        # TODO: change this
        self.joystick_wheel: InputDevice = create_input_device(
            config.wizard.dev_type, config.wizard.client_mode,
            config.wizard.dev_path)

        self.type_id: VehicleType = VehicleType.EGO_FULL_MANUAL

    @staticmethod
    def get_instance():
        "get the instance of the singleton"
        if EgoVehicle.__instance is None:
            return EgoVehicle()
        return EgoVehicle.__instance

    def set_vehicle(self, vehicle: carla.Vehicle):
        """
        set vehicle from outside
        """
        self.carla_vehicle = vehicle

    def start(self):
        self.joystick_wheel.start()

    def destroy(self):
        """
        destroy the vehicle
        TODO: change to destructor
        """
        self.carla_vehicle.destroy()
        self.joystick_wheel.stop()

    # TODO: recover this
    def change_vehicle(self, blueprint, spawn_point):
        "Using carla api to change the current vehicle"
        from . import World
        self.carla_vehicle.destroy()
        self.carla_vehicle: carla.Vehicle = \
            World.get_instance().world.try_spawn_actor(blueprint, spawn_point)

    def switch_driver(self):
        "Switch the current driver, wizard should be enabled"
        assert (data.dev == ClientMode.WIZARD or data.dev == ClientMode.EGO)
        if not self.enable_rpc:
            return
        # change user
        if self.driver == ClientMode.WIZARD:
            self.driver = ClientMode.EGO
        else:
            self.driver = ClientMode.WIZARD
        self._rpc.set_driver(self.driver)

    def get_transform(self) -> carla.Transform:
        """from carla Vehicle api"""
        return self.carla_vehicle.get_transform()

    def get_velocity(self) -> carla.Vector3D:
        """from carla Vehicle api"""
        return self.carla_vehicle.get_velocity()

    def update(self) -> None:
        """
        Update the vehicle status
        """
        if self.enable_rpc:
            self.driver = self._rpc.get_driver()
        if self.driver == ConfigPool.get_config().client_mode:
            # update control
            self.carla_vehicle.apply_control(self._local_ctl)
            self._carla_ctl = self._local_ctl
            if self.joystick_wheel.support_ff():
                # erase spring effect
                self.joystick_wheel.erase_ff_spring()
                # force feedback based on current states
                self.joystick_wheel.set_speed_feedback()

            # upload wheel position
            if self.enable_rpc:
                self._rpc.set_wheel(self._carla_ctl.steer)
        else:
            self._carla_ctl = self.carla_vehicle.get_control()
            if self.joystick_wheel.support_ff():
                # erase auto-center
                self.joystick_wheel.erase_ff_autocenter()
                # force follow
                self.joystick_wheel.SetWheelPos(self._rpc.get_wheel())

    def set_brake(self, data: InputPacket):
        """set the vehicle brake value"""
        self._local_ctl.brake = self.joystick_wheel.PedalMap(data.val)

    def kb_set_brake(self, val: float):
        """set the vehicle brake value"""
        self._local_ctl.brake = val

    def set_throttle(self, data: InputPacket):
        """set the vehicle throttle value"""
        self._local_ctl.throttle = self.joystick_wheel.PedalMap(data.val)

    def change_throttle(self, val: float = 0.05):
        """
        change current throttle by val
        :param val: value to change
        """
        self._local_ctl.throttle += val
        if self._local_ctl.throttle > 1:
            self._local_ctl.throttle = 1
        if self._local_ctl.throttle < 0:
            self._local_ctl.throttle = 0

    def set_steer(self, data: InputPacket):
        "set the vehicle steer value"
        self._local_ctl.steer = self.joystick_wheel.SteerMap(data.val)

    def kb_set_steer(self, val: float = 0):
        """
        set steer
        :param val: value to set
        """
        self._local_ctl.steer = val

    def change_steer(self, val: float = 0.05):
        """
        change steer by value
        :param val: value to change
        """
        self._local_ctl.steer += val
        if self._local_ctl.steer > 1:
            self._local_ctl.steer = 1
        if self._local_ctl.steer < -1:
            self._local_ctl.steer = -1

    def set_reverse(self, dev: ClientMode, val: bool):
        """Set the inverse mode of the vehicle"""
        self._local_ctl.reverse = val

    def toggle_reverse(self):
        """Toggle the reverse mode of the vehicle"""
        self._local_ctl.reverse = not self._local_ctl.reverse

    def get_control(self):
        """From carla api"""
        return self._carla_ctl

    def get_driver_name(self) -> str:
        """Get the current driver as string"""
        if self.driver == ClientMode.EGO:
            return "Human"
        else:
            return "Wizard"
