#!/usr/bin/env python3
import msgpackrpc
from umich_sim.wizard.inputs import ClientMode
from umich_sim.sim_config import ConfigPool, Config


class RPC:
    """
    The RPC Client wrapper singleton class
    """
    _instance = None

    def __init__(self):
        config: Config = ConfigPool.get_config()
        self.client = msgpackrpc.Client(
            msgpackrpc.Address(config.server_addr, config.rpc_port))
        if RPC._instance is None:
            RPC._instance = self
        else:
            raise Exception("Error: Reinitialization of RPC")

    @staticmethod
    def get_instance():
        if RPC._instance is None:
            RPC._instance = RPC()
        return RPC._instance

    def set_driver(self, driver: ClientMode):
        """
        Set the current driver
        Inputs:
            driver: who is driving
        """
        self.client.call("set_driver", driver)

    def get_driver(self) -> ClientMode:
        "Get the current driver"
        return ClientMode(self.client.call("get_driver"))

    def set_wheel(self, pos: float):
        """
        upload the wheel position to the server
        Input: pos: position of the racing wheel
        """
        self.client.call("set_wheel", pos)

    def get_wheel(self) -> float:
        "get the wheel information"
        return self.client.call("get_wheel")
