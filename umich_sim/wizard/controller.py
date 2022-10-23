#!/usr/bin/env python3
from threading import Lock
from queue import Queue
from typing import Callable
from umich_sim.sim_config import ConfigPool
from umich_sim.wizard.inputs import ControlEventType, ClientMode, InputPacket
import pygame


def onpush(func: Callable) -> Callable:
    """
    Execute the function if the button is pushed,
    used in event handling
    """
    return lambda data: func() if data.val == 1 else None


class Controller:
    """
    Main Controller of the wizard
    """
    __instance = None

    def __init__(self):
        # singleton
        if Controller.__instance is None:
            Controller.__instance = self
        else:
            raise Exception("Error: Reinitialization of Controller")
        # objects and references
        from umich_sim.sim_backend.carla_modules import World, HUD, EgoVehicle
        self.__world: World = World.get_instance()
        self.__world.restart()
        self.__hud: HUD = HUD.get_instance()

        self.__vehicle: EgoVehicle = EgoVehicle.get_instance()
        # vars
        self.driver: ClientMode = ClientMode.EGO
        self.__stopping = False

        # events handling
        self.__event_lock: Lock = Lock()
        self.__eventsq: Queue = Queue()
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
                lambda data: self.__vehicle.change_throttle(1),
            ControlEventType.KB_RELEASE_GAS:
                lambda data: self.__vehicle.change_throttle(-1),
            ControlEventType.KB_BRAKE:
                lambda data: self.__vehicle.kb_set_brake(1),
            ControlEventType.KB_RELEASE_BRAKE:
                lambda data: self.__vehicle.kb_set_brake(0),
            ControlEventType.KB_LEFT:
                lambda data: self.__vehicle.kb_set_steer(-1),
            ControlEventType.KB_RIGHT:
                lambda data: self.__vehicle.kb_set_steer(1),
            ControlEventType.KB_CENTER_WHEEL:
                lambda data: self.__vehicle.kb_set_steer(0),
            ControlEventType.SWITCH_DRIVER:
                self.__vehicle.switch_driver,
            ControlEventType.CLOSE:
                lambda data: self.stop(),
        }
        # start multithreading
        self.__vehicle.start()

    @staticmethod
    def get_instance():
        if Controller.__instance is None:
            Controller.__instance = Controller()
        return Controller.__instance

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
            self.__eventsq.put_nowait(InputPacket(event_type, dev, val))

    def run(self, clock, display):
        """
        run the program main loop
        TODO: clean this
        """
        while True:
            if self.__stopping: return
            clock.tick_busy_loop(ConfigPool.get_config().client_frame_rate)
            self.tick(clock)
            self.__world.render(display)
            pygame.display.flip()

    def tick(self, clock):
        """
        Update all the stuffs in the main loop
        """
        self.handle_events()
        self.__vehicle.update()
        self.__hud.tick(clock)

    def handle_events(self):
        """
        Handle events registered in the previous loop
        """
        while not self.__eventsq.empty():
            with self.__event_lock:
                pac: InputPacket = self.__eventsq.get_nowait()

            self.__event_handlers[pac.event_type](pac)

    def __toggle_cam(self):
        "Toggle camera perspective"
        self.__world.camera_manager.toggle_camera()

    def __toggle_sensor(self):
        "Toggle sensor used"
        self.__world.camera_manager.next_sensor()

    def stop(self):
        """
        Stop the program by setting stopping flag
        """
        self.__stopping = True
