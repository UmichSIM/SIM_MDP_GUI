#!/usr/bin/env python3
import msgpackrpc
from sim_backend.wizard.drivers.inputs import InputDevType
from sim_backend.wizard import config


class RPC:
    """
    The RPC Client wrapper singleton class
    """
    _instance = None

    def __init__(self):
        self.client = msgpackrpc.Client(
            msgpackrpc.Address(config.server_addr, config.rpc_port))
        if RPC._instance == None:
            RPC._instance = self
        else:
            raise Exception("Error: Reinitialization of RPC")

    @staticmethod
    def get_instance():
        if RPC._instance == None:
            RPC._instance = RPC()
        return RPC._instance

    def set_driver(self, driver: InputDevType):
        """
        Set the current driver
        Inputs:
            driver: who is driving
        """
        self.client.call("set_driver", driver)

    def get_driver(self) -> InputDevType:
        "Get the current driver"
        return InputDevType(self.client.call("get_driver"))

    def set_wheel(self, pos: float):
        """
        upload the wheel position to the server
        Input: pos: position of the racing wheel
        """
        self.client.call("set_wheel", pos)

    def get_wheel(self) -> float:
        "get the wheel information"
        return self.client.call("get_wheel")
