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
        pygame.KEYUP: {
            # wsad
            pygame.K_w: ControlEventType.KB_RELEASE_GAS,
            pygame.K_s: ControlEventType.KB_RELEASE_BRAKE,
            pygame.K_a: ControlEventType.KB_CENTER_WHEEL,
            pygame.K_d: ControlEventType.KB_CENTER_WHEEL,
            # direction key
            pygame.K_UP: ControlEventType.KB_RELEASE_GAS,
            pygame.K_DOWN: ControlEventType.KB_RELEASE_BRAKE,
            pygame.K_LEFT: ControlEventType.KB_CENTER_WHEEL,
            pygame.K_RIGHT: ControlEventType.KB_CENTER_WHEEL,
        },
        pygame.KEYDOWN: {
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
        },
    }

    def __init__(self, client_type: ClientMode = ClientMode.EGO):
        super().__init__(client_type)

    def events_handler(self) -> None:
        while True:
            event = pygame.event.wait()
            if event.type in KeyboardInput.KB_EVENT_MAP:
                if event_key := KeyboardInput. \
                        KB_EVENT_MAP[event.type].get(event.key, None):
                    Controller.get_instance().register_event(
                        event_key, self.client_mode, 0)
