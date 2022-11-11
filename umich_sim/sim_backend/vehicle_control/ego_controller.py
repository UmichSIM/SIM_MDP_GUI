"""
Backend - EgoController Class
Created on Tue February 15, 2022

Summary: The EgoController class inherits from the base Controller class. It implements control
    specifically for the Ego vehicle. Ego vehicles must be able to be driven both autonomously
    and manually.
"""

# Local Imports
from .base_controller import VehicleController
from .freeway_controller import freeway_control
from umich_sim.sim_backend.carla_modules import Vehicle
from umich_sim.sim_backend.helpers import VehicleType, ExperimentType
from umich_sim.wizard import Wizard

# Library Imports
import carla
from typing import Callable


class EgoController:

    @staticmethod
    def update_control(current_vehicle: Vehicle,
                       experiment_type: ExperimentType) -> None:
        """
        Implementation of the update_control class for the Ego Vehicle type

        Applies control rules for the Ego Vehicle type. An Ego Vehicle can either be manually or
        automatically driven. A manual Ego Vehicle will be controlled by the user either using
        WASD or the arrow keys. An automatic Ego Vehicle will use either the Freeway or Intersection
        controller to control the Vehicle depending on the experiment type

        :param current_vehicle: the Vehicle object to which updated control needs to be applied
        :param experiment_type: the current experiment type as a string, either "freeway" or "intersection"
        :return: None
        """

        # If the Ego vehicle is not manually driven, apply automatic control
        if current_vehicle.type_id == VehicleType.EGO:
            if experiment_type == ExperimentType.FREEWAY:
                freeway_control(current_vehicle)
            else:
                raise Exception(
                    "Invalid experiment type passed to update_control")
            return

        if current_vehicle.type_id == VehicleType.EGO_FULL_MANUAL:
            Wizard.get_instance().tick()
