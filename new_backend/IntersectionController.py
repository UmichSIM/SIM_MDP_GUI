"""
Backend - IntersectionController Class
Created on Tue February 15, 2022

Summary: The IntersectionController class inherits from the base Controller class. It implements control
    from all the non-ego vehicles that are operating in a Intersection experiment type. These vehicles
    do need to manage traffic lights, and they must also manage distance to the vehicles in-front
    and to the side of them.

References:

Referenced By:

"""

# Local Imports
from ApiHelpers import VehicleType
from Controller import Controller
from Vehicle import Vehicle

# Library Imports
from carla import VehicleControl

class IntersectionController(Controller):

    @staticmethod
    def update_control(current_vehicle: Vehicle) -> None:
        """
        Updates the control for a vehicle that is operating in an Intersection experiment.

        Update this documentation once the function is better written.

        :param current_vehicle:
        :return:
        """

        # Just constantly accelerate forward for now
        control = VehicleControl()
        control.throttle = 1
        # current_vehicle.carla_vehicle.apply_control(control)
