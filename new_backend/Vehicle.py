"""
Backend - Vehicle Class
Created on Tue February 15, 2022

Summary: The Vehicle class represents a single vehicle in the CARLA simulation environment. It stores
    all relevant information for a single instance. Provides a high level interface for controlling a
    vehicle's motion through a Controller class.

References:
    Carla Python API

Referenced By:

"""

import carla
from typing import List
from ApiHelpers import WorldDirection, ExperimentType


class Vehicle(carla.Vehicle):

    def __init__(self, id_number: int, name: str, safety_distance: float):
        super().__init__()

        # The unique internal ID for each vehicle
        self.id: int = id_number

        # The user specified name for each vehicle
        self.name: str = name

        # The "safe" distance that the vehicle attempts to maintain between itself and the vehicle in front
        self.safety_distance = safety_distance

        # List of the carla.Transforms for every other vehicle in the Simulation.
        # Tracking both the position and forward facing vector is necessary to calculate
        # distance between vehicles and relative positioning between vehicles
        self.other_vehicle_transforms: List[carla.Transform] = []

        # List that stores the waypoints that the vehicle will travel through
        self.waypoints: List[carla.Transform] = []

    def move_vehicle_location(self, new_position: carla.Transform) -> None:
        """
        Updates the position of the Vehicle to a new position.

        :param new_position: a carla.Transform representing the new location of the vehicle
        :return: None
        """
        self.set_transform(new_position)

    def get_vehicle_size(self) -> (float, float):
        """
        Gets the size of the vehicle's bounding box as a width, length tuple.

        If this function doesn't work as intended, blame Austin
        :return: the width and length of the vehicle as a tuple
        """
        return self.bounding_box.extent[0], self.bounding_box.extent[1]

    def get_current_speed(self) -> float:
        """
        Gets the current forward speed of the Vehicle.

        :return: the current forward speed of the Vehicle as a float
        """
        velocity = self.get_velocity()
        return (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5

    def get_current_position(self) -> (float, float):
        """
        Gets the current position of the vehicle.

        :return: the current position of the Vehicle as an (x,y) tuple
        """
        transform = self.get_transform()
        return transform.location.x, transform.location.y

    def get_current_rotation(self) -> float:
        """
        Gets the current rotation of the vehicle (yaw).

        :return: the current rotation of the vehicle as a float
        """
        transform = self.get_transform()
        return transform.rotation.yaw

    # def update_other_vehicle_transforms(self, other_vehicles: List[Vehicle]) -> None:
    #     """
    #     Updates the internal list with the transforms of all other Vehicles in the simulation
    #
    #     :param other_vehicles: a List of all other Vehicles in the Simulation
    #     :return: None
    #     """
    #
    #     # See carla_env.py -> update_vehicle_distance
    #     pass

    def _check_vehicle_in_direction(self, direction: WorldDirection, experiment_type: ExperimentType) -> (bool, float):
        """
        Determines if there is a vehicle next to the current vehicle in any given direction.

        Uses the vehicles current rotation to check if there are any vehicles nearby in any
        cardinal direction. Forward uses a direction vector of [0, 1]. Backward uses a direction
        vector of [0, -1]. Left uses a direction vector of [-1, 0]. Right uses a direction vector of
        [0, 1].

        :param direction: a WorldDirection enum specifying which direction to check for vehicles
        :param experiment_type: an ExperimentType enum specifying which experiment type is currently running
        :return: a tuple containing whether there is a vehicle in the given direction and the
                 distance if said vehicle exists
        """


    def check_vehicle_in_front(self, experiment_type: ExperimentType) -> (bool, float):
        """
        Determines if there is a vehicle in front of this vehicle.

        :param experiment_type: an ExperimentType enum specifying the current experiment type
        :return: a tuple containing whether there is a vehicle in front and the distance if there
                 is a vehicle in front.
        """

        return self._check_vehicle_in_direction(WorldDirection.FORWARD, experiment_type)

    def check_vehicle_in_back(self, experiment_type: ExperimentType) -> (bool, float):
        """
        Determines if there is a vehicle behind this vehicle.

        :param experiment_type: an ExperimentType enum specifying the current experiment type
        :return: a tuple containing whether there is a vehicle in back and the distance if there
                 is a vehicle in back.
        """

        return self._check_vehicle_in_direction(WorldDirection.BACKWARD, experiment_type)

    def check_vehicle_to_left(self, experiment_type: ExperimentType) -> (bool, float):
        """
        Determines if there is a vehicle to the left of this vehicle.

        :param experiment_type: an ExperimentType enum specifying the current experiment type
        :return: a tuple containing whether there is a vehicle to the left and the distance if there
                 is a vehicle to the left.
        """

        return self._check_vehicle_in_direction(WorldDirection.LEFT, experiment_type)

    def check_vehicle_to_right(self, experiment_type: ExperimentType) -> (bool, float):
        """
        Determines if there is a vehicle to the right of this vehicle.

        :param experiment_type: an ExperimentType enum specifying the current experiment type
        :return: a tuple containing whether there is a vehicle to the right and the distance if there
                 is a vehicle to the right.
        """

        return self._check_vehicle_in_direction(WorldDirection.RIGHT, experiment_type)

    # Maybe relocate this function, decide later
    def draw_waypoints(self) -> None:
        """
        Draws the waypoints and trajectory that the vehicle is following.

        :return: None
        """

        for i in range(len(self.points) - 1):
            location = carla.Location(x=self.points[i][0], y=self.points[i][1], z=5.0)
            self.world.debug.draw_point(location, size=0.1, color="orange", life_time=0.0, persistent_lines=True)

        location = carla.Location(x=self.points[-1][0], y=self.points[-1][1], z=5.0)
        self.world.debug.draw_point(location, size=0.1, color="red", life_time=0.0, persistent_lines=True)

        for i in range(1, len(self.points)):
            begin = carla.Location(x=self.points[i-1][0], y=self.points[i-1][1], z=5.0)
            end = carla.Location(x=self.points[i][0], y=self.points[i][1], z=5.0)
            self.world.debug.draw_line(begin, end, thickness=0.8, color="orange", life_time=0.0, persistent_lines=True)

