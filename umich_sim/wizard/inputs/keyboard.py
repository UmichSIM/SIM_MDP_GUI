#!/usr/bin/env python3
from .base_input_dev import InputDevice
from .input_types import ClientMode, ControlEventType
import pygame
from umich_sim.wizard import Wizard
from umich_sim.base_logger import logger


class KeyboardInput(InputDevice):
    """
    keyboard input device type, use pygame api to get keyboard event

    W            : throttle
    S            : brake
    A/D          : steer left/right
    Q            : toggle reverse
    Z/X          : toggle right/left blinker
    TAB          : toggle camera
    F1           : toggle HUD
    H/?          : toggle help
    ESC          : quit
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
        # reverse
        pygame.K_q: ControlEventType.KB_TOGGLE_REVERSE,
        # right/left blinker
        pygame.K_z: ControlEventType.LEFT_BLINKER,
        pygame.K_x: ControlEventType.RIGHT_BLINKER,
        # info panel
        pygame.K_F1: ControlEventType.TOGGLE_INFO,
        # camera
        pygame.K_TAB: ControlEventType.TOGGLE_CAMERA,
        # help
        pygame.K_h: ControlEventType.TOGGLE_HELP,
        pygame.K_QUESTION: ControlEventType.TOGGLE_HELP,
        pygame.K_SLASH: ControlEventType.TOGGLE_HELP,
        # close program
        pygame.K_ESCAPE: ControlEventType.CLOSE
    }

    def __init__(self, client_type: ClientMode = ClientMode.EGO):
        super().__init__(client_type)

    def events_handler(self) -> None:
        while True:
            # return if terminated
            if self._thread_terminating:
                return
            event = pygame.event.wait()

            # only handle keyboard event
            if event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
                continue

            # get event type based on key map and send to wizard controller
            if event_key := KeyboardInput.KB_EVENT_MAP.get(event.key, None):
                Wizard.get_instance().register_event(
                    event_key, self.client_mode,
                    1 if event.type == pygame.KEYDOWN else 0)
