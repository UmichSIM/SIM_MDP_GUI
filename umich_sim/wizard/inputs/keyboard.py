#!/usr/bin/env python3
from .base_input_dev import InputDevice
from .input_types import ClientMode, ControlEventType
import pygame
from umich_sim.wizard import Controller


class KeyboardInput(InputDevice):
    """
    keyboard input device type, use pygame api to get keyboard event
    """
    KB_EVENT_MAP: dict = {
        # wsad
        pygame.K_w: ControlEventType.KB_GAS,
        pygame.K_s: ControlEventType.KB_BRAKE,
        pygame.K_a: ControlEventType.KB_LEFT,
        pygame.K_d: ControlEventType.KB_RIGHT,
        # direction key
        pygame.K_UP: ControlEventType.KB_GAS,
        pygame.K_DOWN: ControlEventType.KB_BRAKE,
        pygame.K_LEFT: ControlEventType.KB_LEFT,
        pygame.K_RIGHT: ControlEventType.KB_RIGHT,
        # close program
        pygame.K_ESCAPE: ControlEventType.CLOSE
    }

    def __init__(self, client_type: ClientMode = ClientMode.EGO):
        super().__init__(client_type)

    def events_handler(self) -> None:
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event_key := KeyboardInput.KB_EVENT_MAP.get(event.key, None):
                    Controller.get_instance().register_event(
                        event_key, self.client_mode, 0)
