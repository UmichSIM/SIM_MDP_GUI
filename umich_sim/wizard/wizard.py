#!/usr/bin/env python3
from threading import Lock
from queue import Queue
from typing import Callable
from umich_sim.sim_config import ConfigPool
from umich_sim.wizard.inputs import ControlEventType, ClientMode, InputPacket
import pygame
from umich_sim.base_logger import logger


def onpush(func: Callable) -> Callable:
    """
    Execute the function if the button is pushed,
    used in event handling
    """
    return lambda data: func() if data.val == 1 else None


class Wizard:
    """
    Main Controller of the wizard
    """
    __instance = None

    def __init__(self):
        # singleton
        if Wizard.__instance is None:
            Wizard.__instance = self
        else:
            raise Exception("Error: Reinitialization of Controller")
        # objects and references
        from umich_sim.sim_backend.carla_modules import World, HUD, EgoVehicle
        self.__world: World = World.get_instance()
        # TODO: change this
        if not ConfigPool.get_config().gui_mode:
            self.__world.restart()
        self.__hud: HUD = HUD.get_instance()

        self.__vehicle: EgoVehicle = EgoVehicle.get_instance()
        # vars
        self.driver: ClientMode = ClientMode.EGO
        self.__stopping = False

        # events handling
        self.__event_lock: Lock = Lock()
        self.__events_queue: Queue = Queue()
        self.__event_handlers: dict = {
            ControlEventType.CHANGE_WEATHER:
                onpush(self.__world.next_weather),

            ControlEventType.RESTART_WORLD:
                onpush(self.__world.restart),

            ControlEventType.TOGGLE_INFO:
                onpush(self.__hud.toggle_info),

            ControlEventType.TOGGLE_CAMERA:
                onpush(self.__toggle_cam),

            ControlEventType.TOGGLE_SENSOR:
                onpush(self.__toggle_sensor),

            ControlEventType.TOGGLE_HELP:
                onpush(self.__hud.help.toggle),

            ControlEventType.DEC_GEAR:
                lambda data: self.__vehicle.set_reverse(data.dev, True),

            ControlEventType.INC_GEAR:
                lambda data: self.__vehicle.set_reverse(data.dev, False),

            ControlEventType.GAS:
                self.__vehicle.set_throttle,

            ControlEventType.BRAKE:
                self.__vehicle.set_brake,

            ControlEventType.STEER:
                self.__vehicle.set_steer,

            ControlEventType.CLUTCH:
                lambda data: None,

            ControlEventType.KB_GAS:
                lambda data: self.__vehicle.change_throttle(1 if data.val else -1),

            ControlEventType.KB_BRAKE:
                lambda data: self.__vehicle.kb_set_brake(data.val),

            ControlEventType.KB_LEFT:
                lambda data: self.__vehicle.kb_set_steer(-1 if data.val else 0),

            ControlEventType.KB_RIGHT:
                lambda data: self.__vehicle.kb_set_steer(1 if data.val else 0),

            ControlEventType.KB_TOGGLE_REVERSE:
                onpush(self.__vehicle.toggle_reverse),

            ControlEventType.SWITCH_DRIVER:
                onpush(self.__vehicle.switch_driver),

            ControlEventType.CLOSE:
                onpush(self.stop),
        }
        # start multithreading
        self.__vehicle.start()

    @staticmethod
    def get_instance():
        if Wizard.__instance is None:
            Wizard.__instance = Wizard()
        return Wizard.__instance

    def register_event(self, event_type: ControlEventType, dev: ClientMode,
                       val: int) -> None:
        """
        Register the input event into the event queue
        Inputs:
            event_type: What type of actions is required to take
            dev: From which device
            val: Additional data field
        """
        with self.__event_lock:
            self.__events_queue.put_nowait(InputPacket(event_type, dev, val))

    def tick(self):
        """
        tick wizard controller
        """
        self.handle_events()
        self.__vehicle.update()

    def handle_events(self):
        """
        Handle events registered in the previous loop
        """
        while not self.__events_queue.empty():
            with self.__event_lock:
                pac: InputPacket = self.__events_queue.get_nowait()
                self.__event_handlers[pac.event_type](pac)

    def stop(self):
        """
        Stop the program by setting stopping flag
        """
        self.__stopping = True

    def is_stopping(self) -> bool:
        """see if the program is stopping"""
        return self.__stopping

    def __toggle_cam(self):
        """Toggle camera perspective"""
        self.__world.camera_manager.toggle_camera()

    def __toggle_sensor(self):
        """Toggle sensor used"""
        self.__world.camera_manager.next_sensor()