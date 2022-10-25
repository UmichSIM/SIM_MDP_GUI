"""
Backend - FreewayController Class
Created on Tue February 15, 2022

Summary: The FreewayController class inherits from the base Controller class. It implements control
    from all the non-ego vehicles that are operating in a Freeway experiment type. These vehicles
    do not need to manage traffic lights, however they must manage distance to the vehicles in-front
    and to the side of them.
"""

# Local Imports
from .base_controller import VehicleController
from umich_sim.sim_backend.helpers import VehicleType
from umich_sim.sim_backend.carla_modules import Vehicle

# Library Imports
import carla


class FreewayController:

    @staticmethod
    def update_control(current_vehicle: Vehicle) -> None:
        """
        Updates the control for a vehicle that is operating in an Freeway experiment.

        TODO: Update this documentation once the function is better written.
        TODO: Consolidate duplicate code with IntersectionController

        :param current_vehicle:
        :return:
        """

        # If the path for the vehicle was never generated, raise an error
        if not current_vehicle.has_path():
            return

        # Initialize the VehicleControl object
        control: carla.VehicleControl = carla.VehicleControl()

        # Determine the steering angle needed
        steering_angle, end_of_path = VehicleController.steering_control(current_vehicle)

        # Determine the throttle needed
        if current_vehicle.type_id == VehicleType.LEAD:
            throttle = VehicleController.throttle_control(current_vehicle)
        else:
            throttle = VehicleController.throttle_control(current_vehicle)

        # Don't allow inactive vehicles to move
        if current_vehicle.active:
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
