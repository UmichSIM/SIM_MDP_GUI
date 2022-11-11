"""
Backend - IntersectionController Class
Created on Tue February 15, 2022

Summary: The IntersectionController class inherits from the base Controller class. It implements control
    from all the non-ego vehicles that are operating in an Intersection experiment type. These vehicles
    do need to manage traffic lights, and they must also manage distance to the vehicles in-front
    and to the side of them.
"""

# Local Imports
from .base_controller import VehicleController
from umich_sim.sim_backend.carla_modules import Vehicle

# Library Imports
import carla


def intersection_control(current_vehicle: Vehicle) -> None:
    """
    Updates the control for a vehicle that is operating in an Intersection experiment.

    TODO: Update this documentation once the function is better written.

    :param current_vehicle:
    :return: None
    """

    # If the path for the vehicle was never generated, raise an error
    if not current_vehicle.has_path():
        return

    # Initialize the VehicleControl object
    control: carla.VehicleControl = carla.VehicleControl()

    # Determine the steering angle needed
    steering_angle, end_of_path = VehicleController.steering_control(current_vehicle)

    if current_vehicle.current_section is not None:
        # Only check if the vehicle needs to stop if it hasn't already been assigned a target location
        if current_vehicle.target_location is None:
            # Determine if the vehicle needs to stop at a light, set the target location if needed
            stop_at_light, target_location = current_vehicle.current_section.stop_at_light(
                current_vehicle,
                current_vehicle.breaking_distance
            )
            if stop_at_light:
                current_vehicle.target_location = target_location

    # Determine if the vehicle is currently turning and set the target speed appropriately
    if abs(steering_angle) > 0.05:
        current_vehicle.target_speed = current_vehicle.turning_speed
    else:
        current_vehicle.target_speed = current_vehicle.straight_speed

    # Determine the throttle needed
    throttle = VehicleController.throttle_control(current_vehicle)

    # Don't allow inactive vehicles to move
    if current_vehicle.active:
        # Stop the car if we've reached the end of the path
        if end_of_path:
            current_vehicle.active = False
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
