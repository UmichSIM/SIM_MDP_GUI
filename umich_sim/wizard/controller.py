#!/usr/bin/env python3
from threading import Lock
from queue import Queue
from typing import Callable
from umich_simsim_backend.carla_modules import World, HUD, Vehicle
from umich_sim.wizard.rpc import RPC
from umich_sim.wizard.inputs import ControlEventType, InputDevType, InputPacket
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
        self.__world: World = World.get_instance()
        self.__world.restart()
        self.__hud: HUD = HUD.get_instance()

        self.__vehicle: Vehicle = Vehicle.get_instance()
        # vars
        self.driver: InputDevType = InputDevType.WHEEL
        self.__stopping = False

        # events handling
        self.__event_lock: Lock = Lock()
        self.__eventsq: Queue = Queue()
        self.__event_handlers: list = [
            onpush(self.__world.next_weather),  # change weather
            onpush(self.__world.restart),  # restart world
            onpush(self.__hud.toggle_info),  # toggle info
            onpush(self.__toggle_cam),  # toggle camera
            onpush(self.__toggle_sensor),  # toggle sensor
            onpush(self.__hud.help.toggle),  # toggle help
            lambda data: self.__vehicle.set_reverse(data.dev, True
                                                    ),  # Decrease Gear
            lambda data: self.__vehicle.set_reverse(data.dev, False
                                                    ),  # Increate Gear
            self.__vehicle.set_throttle,  # Accelerator
            self.__vehicle.set_brake,  # Brake
            self.__vehicle.set_steer,  # Steer
            lambda data: None,  # Clutch
            self.__vehicle.switch_driver,  # switch driver
            lambda data: self.stop(),  # Close program
        ]
        # start multithreading
        self.__vehicle.start()

    @staticmethod
    def get_instance():
        if Controller.__instance is None:
            Controller.__instance = Controller()
        return Controller.__instance

    def register_event(self,
                       event_type: ControlEventType,
                       dev: InputDevType = InputDevType.KBD,
                       val: int = 0) -> None:
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
            clock.tick_busy_loop(config.client_frame_rate)
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
