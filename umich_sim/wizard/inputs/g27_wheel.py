#!/usr/bin/env python
from .base_wheel import BaseWheel
from . import ClientMode, WheelKeyType, ControlEventType

g27_key_map: dict = {
    WheelKeyType.LTOP: ControlEventType.CLOSE,
    WheelKeyType.RTOP: ControlEventType.SWITCH_DRIVER,
    WheelKeyType.LMID: ControlEventType.TOGGLE_CAMERA,
    WheelKeyType.RMID: ControlEventType.CHANGE_WEATHER,
    WheelKeyType.LSHIFT: ControlEventType.DEC_GEAR,
    WheelKeyType.RSHIFT: ControlEventType.INC_GEAR,
    WheelKeyType.STEER: ControlEventType.STEER,
    WheelKeyType.BRAKE: ControlEventType.BRAKE,
    WheelKeyType.ACC: ControlEventType.GAS,
}


class G27(BaseWheel):
    # register keymap
    def __init__(self, ev_path: str, client_mode: ClientMode = ClientMode.EGO):
        # super class
        super().__init__(ev_path, client_mode)
        self._ctl_key_map: dict = g27_key_map
        self.ev_key_map = {
            292: WheelKeyType.RSHIFT,
            293: WheelKeyType.LSHIFT,
            294: WheelKeyType.RTOP,
            295: WheelKeyType.LTOP,
            706: WheelKeyType.RMID,
            707: WheelKeyType.RBOT,
            708: WheelKeyType.LMID,
            709: WheelKeyType.LBOT,
        }
        self.ev_abs_map = {
            0: WheelKeyType.STEER,
            2: WheelKeyType.ACC,
            5: WheelKeyType.BRAKE,
        }
        # 1 for key type and 3 for abs type
        self.ev_events: list = [None, self.ev_key_map, None, self.ev_abs_map]
