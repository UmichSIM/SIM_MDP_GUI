#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod
from . import InputDevType


class InputDevice(metaclass=ABCMeta):
    """
    base class for general input device
    """

    def __init__(self, dev_type: InputDevType):
        # thread
        self._thread = threading.Thread(target=self.events_handler)

        # stop thread
        self._thread_terminating: bool = False

        # type
        self.dev_type: InputDevType = dev_type

    @abstractmethod
    def events_handler() -> None:
        pass

    def start(self) -> None:
        "start the thread"
        self._thread.start()

    def stop(self) -> None:
        "stop the thread"
        self._thread_terminating = True
