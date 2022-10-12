#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod
from . import ClientMode
import threading


class InputDevice(metaclass=ABCMeta):
    """
    base class for general input device
    """
    # device attributes
    has_ff: bool = False # force feedback

    def __init__(self, client_mode: ClientMode):
        # thread
        self._thread = threading.Thread(target=self.events_handler)

        # stop thread
        self._thread_terminating: bool = False

        # type
        self.client_mode: ClientMode = client_mode

    @abstractmethod
    def events_handler(self) -> None:
        pass

    def start(self) -> None:
        """
        start the thread
        """
        self._thread.start()

    def stop(self) -> None:
        """
        stop the thread
        """
        self._thread_terminating = True

    @classmethod
    def support_ff(cls) -> bool:
        return cls.has_ff
