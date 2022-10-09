#!/usr/bin/env python
from .base_wheel import BaseWheel
from .inputs import InputDevType, WheelKeyType, ControlEventType

g920_key_map: dict = {
    # WheelKeyType.XBOX: ControlEventType.RESTART_WORLD, # TODO: recover this
    WheelKeyType.VIEW:
    ControlEventType.TOGGLE_INFO,
    WheelKeyType.MENU:
    ControlEventType.TOGGLE_HELP,
    WheelKeyType.X:
    ControlEventType.CLOSE,
    # WheelKeyType.LSB: ControlEventType.TOGGLE_SENSOR,
    WheelKeyType.LSB:
    ControlEventType.SWITCH_DRIVER,
    WheelKeyType.RSB:
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


class G920(BaseWheel):
    # register keymap
    def __init__(self,
                 ev_path: str,
                 dev_type: InputDevType = InputDevType.WHEEL):
        # super class
        super().__init__(dev_type)
        self._ctl_key_map: dict = g920_key_map
        self.ev_key_map = {
            288: WheelKeyType.A,
            289: WheelKeyType.B,
            290: WheelKeyType.X,
            291: WheelKeyType.Y,
            292: WheelKeyType.RSHIFT,
            293: WheelKeyType.LSHIFT,
            294: WheelKeyType.MENU,
            295: WheelKeyType.VIEW,
            296: WheelKeyType.RSB,
            297: WheelKeyType.LSB,
            298: WheelKeyType.XBOX,
        }
        self.ev_abs_map = {
            0: WheelKeyType.STEER,
            1: WheelKeyType.ACC,
            2: WheelKeyType.BRAKE,
            5: WheelKeyType.CLUTCH,
            16: WheelKeyType.HPAD,
            17: WheelKeyType.VPAD
        }
        # 1 for key type and 3 for abs type
        self.ev_events: list = [None, self.ev_key_map, None, self.ev_abs_map]


if __name__ == "__main__":
    rw = G920(InputDevType.WHEEL)
