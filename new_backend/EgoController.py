"""
Backend - EgoController Class
Created on Tue February 15, 2022

Summary: The EgoController class inherits from the base Controller class. It implements control
    specifically for the Ego vehicle. Ego vehicles must be able to be driven both autonomously
    and manually.

References:

Referenced By:

"""

# Local Imports
from ApiHelpers import ExperimentType
from Controller import Controller
from FreewayController import FreewayController
from IntersectionController import IntersectionController
from Vehicle import Vehicle, VehicleType

# Library Imports
from typing import Callable


class EgoController(Controller):

    @staticmethod
    def update_control(current_vehicle: Vehicle, manual_control_callback: Callable, experiment_type: ExperimentType) -> None:
        """
        Implementation of the update_control class for the Ego Vehicle type

        Applies control rules for the Ego Vehicle type. An Ego Vehicle can either be manually or
        automatically driven. A manual Ego Vehicle will be controlled by the user either using
        WASD or the arrow keys. An automatic Ego Vehicle will use either the Freeway or Intersection
        controller to control the Vehicle depending on the experiment type

        :param current_vehicle: the Vehicle object to which updated control needs to be applied
        :param manual_control_callback: a Callable object that should be called if manual control is needed
               by the Vehicle
        :param experiment_type: the current experiment type as a string, either "freeway" or "intersection"
        :param mode: a string representing whether the Vehicle should target a certain "speed" or a
                     certain "distance" behind the vehicle it is following
        :param avoid_collisions: whether the Vehicle should actively avoid collisions with nearby vehicles
        :return: None
        """

        # If the Ego vehicle is not manually driven, apply automatic control
        if current_vehicle.type_id != VehicleType.MANUAL_EGO:
            if experiment_type == ExperimentType.FREEWAY:
                FreewayController.update_control(current_vehicle)
            elif experiment_type == ExperimentType.INTERSECTION:
                IntersectionController.update_control(current_vehicle)
            else:
                raise Exception("Invalid experiment type passed to update_control")
            return

        # Otherwise apply manual control
        manual_control_callback()
