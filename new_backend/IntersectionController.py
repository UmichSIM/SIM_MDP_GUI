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
from ApiHelpers import VehicleType, ThrottleControlType
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

        if not current_vehicle.has_path():
            return

        # Initialize the VehicleControl object
        control = VehicleControl()

        # Determine the steering angle needed
        steering_angle, end_of_path = Controller.steering_control(current_vehicle)

        # Determine the throttle needed
        if current_vehicle.type_id == VehicleType.LEAD:
            throttle = Controller.throttle_control(current_vehicle, ThrottleControlType.TARGET_SPEED)
        else:
            throttle = Controller.throttle_control(current_vehicle, ThrottleControlType.TARGET_LOCATION)

        # Stop the car if we've reached the end of the path
        if end_of_path:
            control.steer = 0
            control.throttle = 0
            control.brake = 1.0
            current_vehicle.carla_vehicle.apply_control(control)
            return

        # Otherwise, apply the steering and constant acceleration
        control.steer = steering_angle
        control.throttle = throttle if throttle > 0 else 0
        control.brake = abs(throttle) if throttle < 0 else 0
        current_vehicle.apply_control(control)

