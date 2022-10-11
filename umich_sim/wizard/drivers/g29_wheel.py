#!/usr/bin/env python3
from .base_wheel import BaseWheel
from . import InputDevType, WheelKeyType, ControlEventType

g29_key_map: dict = {
    # WheelKeyType.XBOX: ControlEventType.RESTART_WORLD, # TODO: recover this
    WheelKeyType.L2:
    ControlEventType.TOGGLE_INFO,
    WheelKeyType.R2:
    ControlEventType.TOGGLE_HELP,
    WheelKeyType.CROSS:
    ControlEventType.CLOSE,
    # WheelKeyType.LSB: ControlEventType.TOGGLE_SENSOR,
    WheelKeyType.L3:
    ControlEventType.SWITCH_DRIVER,
    WheelKeyType.R3:
    ControlEventType.TOGGLE_CAMERA,
    WheelKeyType.LSHIFT:
    ControlEventType.DEC_GEAR,
    WheelKeyType.RSHIFT:
    ControlEventType.INC_GEAR,
    WheelKeyType.HPAD:
    ControlEventType.CHANGE_WEATHER,
    WheelKeyType.STEER:
    ControlEventType.STEER,
    WheelKeyType.BRAKE:
    ControlEventType.BRAKE,
    WheelKeyType.ACC:
    ControlEventType.ACCELERATOR,
}


class G29(BaseWheel):
    # register keymap
    def __init__(self,
                 ev_path: str,
                 dev_type: InputDevType = InputDevType.WHEEL):
        # super class
        super().__init__(dev_type)
        self._ctl_key_map: dict = g29_key_map
        self.ev_key_map = {
            288: WheelKeyType.CROSS,
            289: WheelKeyType.SQUARE,
            290: WheelKeyType.CIRCLE,
            291: WheelKeyType.TRIANGLE,
            292: WheelKeyType.RSHIFT,
            293: WheelKeyType.LSHIFT,
            294: WheelKeyType.R2,
            295: WheelKeyType.L2,
            296: WheelKeyType.RSB,
            298: WheelKeyType.R3,
            299: WheelKeyType.L3,
        }
        self.ev_abs_map = {
            0: WheelKeyType.STEER,
            2: WheelKeyType.ACC,
            3: WheelKeyType.BRAKE,
            16: WheelKeyType.HPAD,
            17: WheelKeyType.VPAD
        }
        # 1 for key type and 3 for abs type
        self.ev_events: list = [None, self.ev_key_map, None, self.ev_abs_map]


if __name__ == "__main__":
    rw = G29(InputDevType.WHEEL)
