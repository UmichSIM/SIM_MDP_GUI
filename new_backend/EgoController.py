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
from ApiHelpers import ExperimentType, ThrottleControlType
from Controller import Controller
from FreewayController import FreewayController
from IntersectionController import IntersectionController
from Vehicle import Vehicle, VehicleType

# Library Imports
import carla
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
        :return: None
        """

        # If the Ego vehicle is not manually driven, apply automatic control
        if current_vehicle.type_id == VehicleType.EGO_FULL_AUTOMATIC:
            if experiment_type == ExperimentType.FREEWAY:
                FreewayController.update_control(current_vehicle)
            elif experiment_type == ExperimentType.INTERSECTION:
                IntersectionController.update_control(current_vehicle)
            else:
                raise Exception("Invalid experiment type passed to update_control")
            return

        # Get the control that the manual input would predict
        manual_control: carla.VehicleControl = manual_control_callback()

        # Override the steering if necessary
        if current_vehicle.type_id == VehicleType.EGO_AUTOMATIC_STEER_MANUAL_THROTTLE:
            steering_angle = Controller.steering_control(Vehicle)
            manual_control.steer = steering_angle

        # Override the throttle if necessary
        if current_vehicle.type_id == VehicleType.EGO_MANUAL_STEER_AUTOMATIC_THROTTLE:
            throttle = Controller.throttle_control(current_vehicle, ThrottleControlType.TARGET_DISTANCE)

            # Apply the throttle for a positive throttle, and the brake for a negative throttle
            if throttle > 0:
                manual_control.throttle = throttle
            else:
                manual_control.brake = abs(throttle)

        current_vehicle.apply_control(manual_control)
