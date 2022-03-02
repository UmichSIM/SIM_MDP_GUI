"""
Backend - TestExperiment Class
Created on Tue February 22, 2022

Summary: The TestExperiment class is a class that derives from the base Experiment class. It
         provides a sandbox for testing new backend functionality

Usage: This file can be invoked as a regular python script to test out the experiment in the Carla
       environment. It can be invoked using "python TestExperiment.py"

References:

Referenced By:

"""

# Local Imports
from Experiment import Experiment
from Threading import HeadlessWindow
from ApiHelpers import logging_setup

# Library Imports
import sys
from PyQt5.QtWidgets import QApplication


class TestExperiment(Experiment):

    def __init__(self, headless: bool) -> None:
        super(TestExperiment, self).__init__(headless)


def main() -> None:
    """
    Main Function to be run when the file is run as a standalone Python Script

    :return: None
    """
    experiment = TestExperiment(True)
    experiment.initialize_carla_server()


if __name__ == "__main__":
    logging_setup()
    app = QApplication(sys.argv)
    win = HeadlessWindow(main)
    win.show()
    sys.exit(app.exec())
