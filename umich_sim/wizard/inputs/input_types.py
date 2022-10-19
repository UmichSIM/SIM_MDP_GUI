#!/usr/bin/env python3
from enum import IntEnum, auto
from dataclasses import dataclass


class InputDevType(IntEnum):
    """
    Type of input device
    """
    G920 = 0
    G29 = auto()
    G27 = auto()
    KBD = auto()


class ControlEventType(IntEnum):
    """
    Enum indicating the event requested for controller to handle
    """
    # User Interface
    CHANGE_WEATHER = 0
    RESTART_WORLD = auto()
    TOGGLE_INFO = auto()
    TOGGLE_CAMERA = auto()
    TOGGLE_SENSOR = auto()
    TOGGLE_HELP = auto()
    # Racing wheel
    DEC_GEAR = auto()
    INC_GEAR = auto()
    GAS = auto()
    BRAKE = auto()
    STEER = auto()
    CLUTCH = auto()
    # Keyboard specific
    KB_GAS = auto()
    KB_BRAKE = auto()
    KB_RELEASE_GAS = auto()
    KB_RELEASE_BRAKE = auto()
    KB_LEFT = auto()
    KB_RIGHT = auto()
    KB_CENTER_WHEEL = auto()
    # Controls
    SWITCH_DRIVER = auto()
    CLOSE = auto()  # close the program
    NONE = auto()  # do nothing


class ClientMode(IntEnum):
    """
    Enum indicating input device type
        EGO: Driver input
        WIZARD: Wizard input as autopilot
    """
    EGO = 0
    WIZARD = 1


class WheelKeyType(IntEnum):
    "Enum indicating the keys on the racing wheel"
    XBOX = 0
    LSB = auto()
    RSB = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    L2 = auto()
    L3 = auto()
    R2 = auto()
    R3 = auto()
    VIEW = auto()
    MENU = auto()
    # control buttons
    A = auto()
    B = auto()
    X = auto()
    Y = auto()
    CROSS = auto()
    CIRCLE = auto()
    SQUARE = auto()
    TRIANGLE = auto()
    # pads in horizon and vertical
    VPAD = auto()
    HPAD = auto()
    STEER = auto()
    CLUTCH = auto()
    BRAKE = auto()
    ACC = auto()
    LTOP = auto()
    LMID = auto()
    LBOT = auto()
    RTOP = auto()
    RMID = auto()
    RBOT = auto()


@dataclass
class InputPacket:
    """
    dataclass carrying data to controller
    """
    event_type: ControlEventType
    dev: ClientMode
    val: int
