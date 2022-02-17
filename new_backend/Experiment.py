"""
Backend - Experiment Class
Created on Tue February 15, 2022

Summary: The Experiment class is a base class that describes the high level interface that all
    derived experiments must implement. It provides all the functionality that is universal to all
    experiments and experiment types. Specific experiment types and specific maps must be represented
    as derived classes from this base class.

References:

Referenced By:

"""

import Vehicle
import Section
import carla
from typing import List


class Experiment:

    def __init__(self):
        self.vehicle_list: List[Vehicle] = []
        self.pedestrian_list: List[carla.Walker] = []
        self.section_list: List[Section] = []
        self.sensor_list: List[carla.Sensor] = []

    def destroy_actors(self) -> None:
        """
        Destroys all of the actors that have been spawned in the Carla simulation.

        :return: None
        """
        for vehicle in self.vehicle_list:
            vehicle.destroy()
        for pedestrian in self.pedestrian_list:
            pedestrian.destroy()
        for sensor in self.sensor_list:
            sensor.destroy()