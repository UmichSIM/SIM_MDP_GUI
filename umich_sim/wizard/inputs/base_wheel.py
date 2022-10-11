#!/usr/bin/env python
from evdev import ecodes, InputDevice, ff
import math
import threading
from abc import ABC

from umich_sim.wizard.utils.map import LinearMap
from umich_sim.wizard.utils.limits import *
from umich_sim.wizard.drivers import InputDevType, WheelKeyType, ControlEventType


class BaseWheel(ABC):
    """
    Abstract wheel class to be inherited
    """

    # settings
    steer_max: int = iinfo(uint16).max  # max possible value to steering wheel
    pedal_max: int = iinfo(uint8).max  # max possible value of pedals

    def __init__(self,
                 ev_path: str,
                 dev_type: InputDevType = InputDevType.WHEEL):
        """
        :param ev_path: path to evdev device
        :dev_type: device type, racing wheel or wizard
        """
        # static variables
        self.ev_key_map: dict = {}
        self.ev_abs_map: dict = {}
        # 1 for key type and 3 for abs type
        self.ev_events: list = []
        self.ev_type_accepted: tuple = (1, 3)

        # evdev device
        self._ev = None
        self._ctl_key_map: dict = {}
        # data
        self.steer_val: int = 0  # steer input [0,65535]
        self.acc_val: int = 0  # accelarator input [0,255]
        self.brake_val: int = 0  # brake input [0,255]
        self.clutch_val: int = 0  # clutch input [0,255]
        # FF id
        self._ff_spring_id = None
        self._ff_autocenter_val: int = 0
        # stop thread
        self._thread_terminating: bool = False

        # connect evdev device
        self._ev_connect(ev_path)
        self._init()

    def __del__(self):
        "Destructor, used to erase ff settings"
        self._ev.close()

    def _init(self):
        # init with 75% autocenter force
        # self._setFFAutoCenter(49150)
        print("Racing wheel registered")

    def SetSpeedFeedback(self):
        '''
        Update the auto center force feedback using speed
        '''
        from sim_backend.carla_modules import Vehicle
        v = Vehicle.get_instance().get_velocity()
        speed = (3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2))

        # speed limit that influences the autocenter
        S2W_THRESHOLD = 90
        if (speed > S2W_THRESHOLD):
            speed = S2W_THRESHOLD
        # autocenterCmd  \in [0,65535]
        autocenterCmd: int = int(
            abs(math.sin(speed / S2W_THRESHOLD)) * iinfo(uint16).max)

        # send autocenterCmd to the steeringwheel
        self._setFFAutoCenter(autocenterCmd)

    def SetWheelPos(self, val: float):
        """
        Set the wheel position
        inputs:
        - val: float to indicate wheel position [-1,1]
        """
        # strongest force to maintain position
        self._setFFSpring(pos=int(val * iinfo(int16).max),
                          saturation=iinfo(uint16).max,
                          coeff=iinfo(int16).max)

    def start(self):
        "start the thread"
        self._thread.start()

    def stop(self):
        "stop the thread"
        self._thread_terminating = True

    def events_handler(self) -> None:
        '''
        Capture and handle events
        '''
        from sim_backend.wizard.controller import Controller
        for event in self._ev.read_loop():
            # return if terminated
            if self._thread_terminating: return
            if event.type in self.ev_type_accepted:
                # key based on raw code
                key_type: WheelKeyType = self.ev_events[event.type].get(
                    event.code)
                # controller event
                event_type: ControlEventType = self._ctl_key_map.get(
                    key_type, ControlEventType.NONE)
                if event_type is not ControlEventType.NONE:
                    Controller.get_instance().register_event(
                        event_type, self.dev_type, event.value)

    def _ev_connect(self, ev_path: str):
        "Connect to evdev device based on config file"
        self._ev: evdev.InputDevice = InputDevice(ev_path)

    def _setFFAutoCenter(self, val: int):
        """
        Set the auto center force
        Input: val - uint16_t indicates the intensity
        """
        assert (val >= 0 and val <= iinfo(uint16).max)
        self._ff_autocenter_val = val
        self._ev.write(ecodes.EV_FF, ecodes.FF_AUTOCENTER, val)

    def _setFFSpring(self,
                     pos: int,
                     saturation: int,
                     coeff: int,
                     deadband: int = 0) -> None:
        """
        Set the spring force feedback
        Input:
        - pos: position of the balance point
        - saturation: maximum level when wheel moved all way to end
        - coeff: controls how fast the force grows when the joystick
                 moves from center
        - deadband: size of the dead zone, where no force is produced
        """
        # create effect
        springs = (ff.Condition * 2)()
        for spring in springs:
            spring.right_saturation = saturation
            spring.left_saturation = saturation
            spring.right_coeff = coeff
            spring.left_coeff = coeff
            spring.deadband = deadband
            spring.center = pos

        # register effect
        spring_id = self._ev.upload_effect(
            ff.Effect(ecodes.FF_SPRING, -1, 16384, ff.Trigger(0, 0),
                      ff.Replay(iinfo(int16).max, 0),
                      ff.EffectType(ff_condition_effect=springs)))

        # apply
        self._ev.write(ecodes.EV_FF, spring_id, 1)

        # erase previous effect
        if self._ff_spring_id is not None:
            self._ev.erase_effect(self._ff_spring_id)

        self._ff_spring_id = spring_id

    # TODO: test if this work for all effects
    def erase_ff(self, ff_type: int):
        """
        Erase the specified force feedback type
        """
        if ff_type == ecodes.FF_SPRING:
            if self._ff_spring_id is not None:
                self._ev.erase_effect(self._ff_spring_id)
                self._ff_spring_id = None

        elif ff_type == ecodes.FF_AUTOCENTER:
            if self._ff_autocenter_val != 0:
                self._setFFAutoCenter(0)

    @classmethod
    def SteerMap(cls, val: int):
        """
        map the input of steering wheel to carla defined region [-1,1]
        """
        return LinearMap(val, cls.steer_max) * 2 - 1

    @classmethod
    def PedalMap(cls, val: int):
        """
        map the input of pedals to carla defined region [0,1]
        """
        # reverse the input because 255 is 0 in evdev
        return LinearMap(cls.pedal_max - val, cls.pedal_max)
