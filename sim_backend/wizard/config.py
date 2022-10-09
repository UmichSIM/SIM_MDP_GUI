#!/usr/bin/env python3
from sim_backend.wizard.drivers.inputs import InputDevType, WheelKeyType, ControlEventType
from sim_backend.wizard.drivers import G920, G27, G29
# frame rate for client
client_frame_rate: int = 60
# server address
server_addr: str = "127.0.0.1"
rpc_port: int = 2003
# indicate whether to record the game onto the disk
cam_recording: bool = False
cam_record_dir: str = "./_out"

# this client runs in which mode
client_mode: InputDevType = InputDevType.WHEEL

# The wheel model to use
WheelType = G920
# WheelType = G27
# WheelType = G29

# device event file
user_input_event: str = "/dev/input/event7"
