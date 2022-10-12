#!/usr/bin/env python3

from .input_types import *
from .base_input_dev import InputDevice
from typing import Optional


def create_input_device(dev_type: InputDevType,
                        client_mode: ClientMode,
                        dev_path: Optional[str] = None) -> InputDevice:
    """
    create input device based on dev_type passed
    :param dev_type: device type
    :param client_mode: client mode (wizard or host)
    :param dev_path: optional argument passed to joystick devices
    """
    from .g27_wheel import G27
    from .g29_wheel import G29
    from .g920_wheel import G920
    from .keyboard import KeyboardInput
    wheel_map: dict = {
        InputDevType.G29: G29,
        InputDevType.G920: G920,
        InputDevType.G27: G27,
    }

    if dev_type == InputDevType.KBD:
        return KeyboardInput(client_mode)
    else:
        return wheel_map[dev_type](dev_path, client_mode)

