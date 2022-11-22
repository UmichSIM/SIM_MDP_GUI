#!/usr/bin/env python3
from time import time
import carla
from umich_sim.wizard.inputs import ClientMode, InputPacket, InputDevice, create_input_device
from umich_sim.sim_config import ConfigPool, Config
# from umich_sim.sim_backend.helpers import VehicleType
from .vehicle import Vehicle
from .hud import HUD
from umich_sim.sim_backend.helpers import (WorldDirection, VehicleType,
                                           to_numpy_vector, rotate_vector,
                                           ORANGE, RED)
from pygame import mixer
from datetime import datetime, timedelta


class EgoVehicle(Vehicle):
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
            carla_vehicle = None
        elif config.client_mode == ClientMode.EGO:
            carla_vehicle: carla.Vehicle = \
                world.world.try_spawn_actor(blueprint, spawn_point)
        elif config.client_mode == ClientMode.WIZARD:
            vehicles = world.world.get_actors().filter('vehicle.*')
            carla_vehicle: carla.Vehicle = vehicles[0]
        else:
            raise Exception("Error: Invalid client mode.")

        super().__init__(carla_vehicle, "Ego Vehicle", VehicleType.EGO)

        # control info from agent racing wheel
        self._local_ctl: carla.VehicleControl = carla.VehicleControl()
        # control info from carla server
        self._carla_ctl: carla.VehicleControl = carla.VehicleControl()

        # whether to enable wizard
        self.enable_wizard = config.wizard.enable_wizard
        if self.enable_wizard:
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

        # Rumble Strips
        self.mapp = World.get_instance().world.get_map()
        self.is_rumbling: bool = False
        self.rumble_lane_type = {carla.LaneMarkingType.Solid}

        # LDW System
        self._is_ldw_on = False
        self._last_ldw_ts = datetime.now()
        self._ldw_time_interval = timedelta(seconds=3) # time interval between two triggered warning, in seconds
        self.ldw_lane_type = {carla.LaneMarkingType.Solid,
                              carla.LaneMarkingType.Broken,
                              carla.LaneMarkingType.SolidSolid,
                              carla.LaneMarkingType.SolidBroken,
                              carla.LaneMarkingType.BrokenSolid,
                              carla.LaneMarkingType.BrokenBroken}

        # Sound Effect
        # TODO: move this part to HUD module
        mixer.init()  # Initialzing pyamge mixer
        mixer.pre_init(44100, 16, 2, 4096)
        self._sound_rs = mixer.Sound(
            'umich_sim/sim_backend/media/rs_cut.mp3')  # Loading Music File
        self._sound_ldw = mixer.Sound(
            'umich_sim/sim_backend/media/warning_2.mp3')  # Loading Music File TODO
        

    @staticmethod
    def get_instance():
        "get the instance of the singleton"
        if EgoVehicle.__instance is None:
            return EgoVehicle()
        return EgoVehicle.__instance

    def set_vehicle(self, vehicle: carla.Vehicle):
        """
        set vehicle from outside
        :param vehicle: carla vehicle to set
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
        """Switch the current driver, wizard should be enabled"""
        if not self.enable_wizard:
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
        if self.enable_wizard:
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
            if self.enable_wizard:
                self._rpc.set_wheel(self._carla_ctl.steer)
        else:
            self._carla_ctl = self.carla_vehicle.get_control()
            if self.joystick_wheel.support_ff():
                # erase auto-center
                self.joystick_wheel.erase_ff_autocenter()
                # force follow
                self.joystick_wheel.SetWheelPos(self._rpc.get_wheel())

        if_rumble, if_ldw = self.lane_effect_update()
        if self.is_rumbling and not if_rumble:
            self.stop_rumble()
            self.is_rumbling = False
        elif not self.is_rumbling and if_rumble:
            self.start_rumble()
            self.is_rumbling = True
        
        self.ldw_handler(if_ldw)


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
        """change current throttle by val
        :param val: value to change
        """
        self._local_ctl.throttle += val
        if self._local_ctl.throttle > 1:
            self._local_ctl.throttle = 1
        if self._local_ctl.throttle < 0:
            self._local_ctl.throttle = 0

    def set_steer(self, data: InputPacket):
        """set the vehicle steer value"""
        self._local_ctl.steer = self.joystick_wheel.SteerMap(data.val)

    def kb_set_steer(self, val: float = 0):
        """set steer
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
        self._light ^= carla.VehicleLightState.Reverse
        self.carla_vehicle.set_light_state(carla.VehicleLightState(self._light))

    def get_control(self):
        """From carla api"""
        return self._carla_ctl

    def get_driver_name(self) -> str:
        """Get the current driver as string"""
        if self.driver == ClientMode.EGO:
            return "Human"
        else:
            return "Wizard"
    
    def toggle_ldw(self):
        """Toggle the lane departure warning system"""
        self._is_ldw_on = not self._is_ldw_on
        hud = HUD.get_instance()
        if self._is_ldw_on:
            hud.notification('Lane Departure Warning On')
        else:
            hud.notification('Lane Departure Warning Off')
    
    def ldw_handler(self, if_ldw):
        if if_ldw and self._is_ldw_on and not self._is_left_blinking and not self._is_right_blinking:
            curr_time = datetime.now()
            if curr_time - self._last_ldw_ts >= self._ldw_time_interval:
                hud = HUD.get_instance()
                hud.notification('Warning: Lane Departure!')
                print("warn", curr_time)
                self._sound_ldw.play(loops=0)  # loops=0 for playing once
                self._last_ldw_ts = curr_time


    # Force feedback

    def set_collision(self):
        if self.joystick_wheel.support_ff():
            self.joystick_wheel.collision_effect()

    def start_rumble(self):
        print("[INFO] Start rumbling...")
        self._sound_rs.play(loops=-1)  # Playing Music with Pygame
        if self.joystick_wheel.support_ff():
            self.joystick_wheel.start_rumble()

    def stop_rumble(self):
        print("[INFO] Stop rumbling")
        self._sound_rs.stop()
        if self.joystick_wheel.support_ff():
            self.joystick_wheel.stop_rumble()

    def lane_effect_update(self):
        """
        1. Calculate the distance from four wheels to the center of the lane
        2. Update rumbling and lane-departure-warning status
        Return:
            if_rumble: True if rumbling is needed
            if_ldw: True if ldw is needed
        """

        def distance_to_segment_2d(point, seg_start, seg_end):
            """
            Calculate the distance from point to a segment defined by "seg_start" and "seg_end"
            Note: only works for 2D
            """
            point.z = 0
            cross_product = (point.x - seg_start.x) * (seg_end.y - seg_start.y) \
                            - (point.y - seg_start.y) * (seg_end.x - seg_start.x)
            distance = abs(cross_product) / seg_start.distance_2d(seg_end)
            return distance

        def is_on_lane(distance, lane_width, low=0.43, high=0.55):
            """
            Define whether the wheel lies in the range of the lane
            Input:
                distance: distance between the wheel and the center of the lane
                lane_width: width of the lane
                low: the inner edge of the lane, in percentage of the lane width
                high: the outer edge of the lane, in percentage of the lane width
            """
            return (distance / lane_width > low) and (distance / lane_width <
                                                      high)

        ### Return false if the velocity is zero
        if self.carla_vehicle.get_velocity().length() == 0:
            return False, False

        ### get the closest waypoint (a point in the center of the lane)
        ### carla.Location, see https://carla.readthedocs.io/en/latest/python_api/#carla.Location
        vehicle_location = self.carla_vehicle.get_location()
        waypoint: carla.Location = self.mapp.get_waypoint(
            vehicle_location,
            project_to_road=True,
            lane_type=(carla.LaneType.Driving | carla.LaneType.Sidewalk))
        waypoint_loc = waypoint.transform.location
        next_waypoint_loc = waypoint.next(
            0.5)[0].transform.location  # next waypoint
        lane_width = waypoint.lane_width

        ### get the location of wheels, in the order of front left, front right, back left, back right
        ### convert from cm to m since the vehicle position is in meters
        wheels = self.carla_vehicle.get_physics_control().wheels
        wheels_loc: carla.Vector3D = [x.position / 100 for x in wheels]
        wheels_dist = [
            distance_to_segment_2d(x, waypoint_loc, next_waypoint_loc)
            for x in wheels_loc
        ]

        ### Determine if the vehicle goes the wrong way
        lane_direction = next_waypoint_loc - waypoint_loc
        vehicle_direction = wheels_loc[0] - wheels_loc[2]
        is_reverse: bool = lane_direction.dot_2d(vehicle_direction) < 0

        ### Determine overlap with lane
        if_rumble: bool = False
        if_ldw: bool = False
        for idx, distance in enumerate(wheels_dist):
            # print(idx, distance / lane_width)
            ### invade right lane
            if is_on_lane(distance, lane_width) and (
                (idx % 2 and not is_reverse) or (idx % 2 == 0 and is_reverse)):
                # print("right", distance, waypoint.right_lane_marking.type)
                if waypoint.right_lane_marking.type in self.rumble_lane_type:
                    if_rumble = True
                if waypoint.right_lane_marking.type in self.ldw_lane_type:
                    if_ldw = True
            ### invade left lane
            elif is_on_lane(distance, lane_width):
                # print("left", distance, waypoint.left_lane_marking.type)
                if waypoint.left_lane_marking.type in self.rumble_lane_type:
                    if_rumble = True
                if waypoint.left_lane_marking.type in self.ldw_lane_type:
                    if_ldw = True

        ### DEBUG: visualize wheel locations and the closest waypoint
        # from . import World
        # world = World.get_instance().world
        # world.debug.draw_point(waypoint_loc, size=0.15, color=ORANGE, life_time=1.0)
        # world.debug.draw_point(next_waypoint_loc, size=0.15, color=RED, life_time=1.0)
        # for i in wheels_loc:
        #     world.debug.draw_point(i, size=0.15, color=RED, life_time=0.5)

        return if_rumble, if_ldw
