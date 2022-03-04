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
from ApiHelpers import ExperimentType, WorldDirection
from Controller import Controller
from Experiment import Experiment
from FreewayController import FreewayController
from IntersectionController import IntersectionController
from Vehicle import Vehicle, VehicleType

# Library Imports
import carla
import pygame
from typing import List

from pygame.locals import K_w, K_a, K_s, K_d
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT


class EgoController(Controller):

    @staticmethod
    def update_control(current_vehicle: Vehicle, mode: str = "", avoid_collisions: bool = False) -> carla.VehicleControl:
        """
        Implementation of the update_control class for the Ego Vehicle type

        Applies control rules for the Ego Vehicle type. An Ego Vehicle can either be manually or
        automatically driven. A manual Ego Vehicle will be controlled by the user either using
        WASD or the arrow keys. An automatic Ego Vehicle will use either the Freeway or Intersection
        controller to control the Vehicle depending on the experiment type

        :param current_vehicle: the Vehicle object to which updated control needs to be applied
        :param mode: a string representing whether the Vehicle should target a certain "speed" or a
                     certain "distance" behind the vehicle it is following
        :param avoid_collisions: whether the Vehicle should actively avoid collisions with nearby vehicles
        :return: a carla.VehicleControl object representing the acceleration and steering that should
                 be applied to the current_vehicle
        """

        # If the Ego vehicle is not manually driven, apply automatic control
        if current_vehicle.type != VehicleType.MANUAL_EGO:
            if Experiment.experiment_type == ExperimentType.INTERSECTION:
                return FreewayController.update_control(current_vehicle, mode, avoid_collisions)
            return IntersectionController.update_control(current_vehicle, mode, avoid_collisions)

        # If the Ego vehicle is manually driven, apply manual control
        directions_held = EgoController.parse_keyboard_input()
        time_held = Experiment.clock.get_time()

        # Get the previous Control state and create a new control state
        previous_control = current_vehicle.get_control()
        new_control = carla.VehicleControl()

        # Apply some default values to the new control state
        new_control.throttle = 0.0
        new_control.brake = 0.0
        new_control.steer = 0.0

        # Update the control state
        if WorldDirection.FORWARD in directions_held:
            new_control.throttle = min(previous_control.throttle + 0.01, 1.00)

        if WorldDirection.BACKWARD in directions_held:
            new_control.brake = min(previous_control.brake + 0.2, 1)

        steer_increment = 5e-4 * time_held
        if WorldDirection.LEFT in directions_held:
            new_control.steer = -1 * steer_increment if previous_control.steer > 0 else previous_control.steer - steer_increment

        if WorldDirection.RIGHT in directions_held:
            new_control.steer = steer_increment if previous_control.steer < 0 else previous_control.steer + steer_increment

        # Return the new control state
        return new_control

    @staticmethod
    def parse_keyboard_input() -> List[WorldDirection]:
        """
        Parses the input from the Keyboard and returns the direction being input by the User.

        :return: a List of all directions that are being input
        """

        directions_held: List[WorldDirection] = []
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_UP] or keys_pressed[K_w]:
            directions_held.append(WorldDirection.FORWARD)

        if keys_pressed[K_LEFT] or keys_pressed[K_a]:
            directions_held.append(WorldDirection.LEFT)

        if keys_pressed[K_DOWN] or keys_pressed[K_s]:
            directions_held.append(WorldDirection.DOWN)

        if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
            directions_held.append(WorldDirection.RIGHT)

        return directions_held
