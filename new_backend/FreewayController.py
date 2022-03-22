"""
Backend - FreewayController Class
Created on Tue February 15, 2022

Summary: The FreewayController class inherits from the base Controller class. It implements control
    from all the non-ego vehicles that are operating in a Freeway experiment type. These vehicles
    do not need to manage traffic lights, however they must manage distance to the vehicles in-front
    and to the side of them.

References:

Referenced By:

"""

# Local Imports
from Vehicle import Vehicle

# Library Imports


class FreewayController:

    @staticmethod
    def update_control(current_vehicle: Vehicle) -> None:
        """
        Updates the control for a vehicle that is operating in an Freeway experiment.

        TODO: Update this documentation once the function is better written.

        :param current_vehicle:
        :return:
        """
