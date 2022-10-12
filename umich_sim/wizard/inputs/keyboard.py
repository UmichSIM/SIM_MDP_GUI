#!/usr/bin/env python3
from .base_input_dev import InputDevice
from .input_types import InputDevType, ControlEventType
import pygame
from umich_sim.wizard import Controller

KB_EVENT_MAP: dict = {
    # wsad
    pygame.K_w: ControlEventType.KB_THRUST,
    pygame.K_s: ControlEventType.KB_BRAKE,
    pygame.K_a: ControlEventType.KB_LEFT,
    pygame.K_d: ControlEventType.KB_RIGHT,
    # direction key
    pygame.K_UP: ControlEventType.KB_THRUST,
    pygame.K_DOWN: ControlEventType.KB_BRAKE,
    pygame.K_LEFT: ControlEventType.KB_LEFT,
    pygame.K_RIGHT: ControlEventType.KB_RIGHT,
    # close program
    pygame.K_ESCAPE: ControlEventType.CLOSE
}


class KeyboardInput(InputDevice):

    def __init__(self, dev_type: InputDevType = InputDevType.EGO):
        super.__init__(dev_type)

    def events_handler(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    Controller.get_instance().register_event(
                        KB_EVENT_MAP[event.key], self.dev_type, 0)
