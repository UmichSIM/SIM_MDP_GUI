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

# Local Imports
from ApiHelpers import WorldDirection, ExperimentType, VehicleType, to_numpy_vector, rotate_vector

# Library Imports
import carla
import math
import numpy as np
from typing import List, Tuple

GREEN = carla.Color(0, 255, 0)
ORANGE = carla.Color(252, 177, 3)
RED = carla.Color(255, 0, 0)


class Vehicle:

    def __init__(self, carla_vehicle: carla.Vehicle, name: str, type_id: VehicleType, safety_distance: float = 10.0):
        super().__init__()

        # Stores the Carla Vehicle object associated with this particular vehicle
        self.carla_vehicle: carla.Vehicle = carla_vehicle

        # The type of this Vehicle
        self.type_id: VehicleType = type_id

        # The user specified name for each vehicle
        self.name: str = name

        # The "safe" distance that the vehicle attempts to maintain between itself and the vehicle in front
        self.safety_distance = safety_distance

        # List of the carla.Vector3Ds that represent the locations of every other Vehicle in the
        # experiment
        self.other_vehicle_locations: List[np.array] = []

        # List that stores the raw waypoints that the vehicle will travel through
        self.waypoints: List[carla.Transform] = []

        # List that stores the high-resolution trajectory that vehicle uses for path following
        # This trajectory is generated by smoothing and generating intermediate points connecting
        # the waypoints together
        self.trajectory: List[carla.Transform] = []

    def has_path(self):
        """
        Getter for whether the Vehicle has an initialized path to follow.

        :return: True if the vehicles path was initialized, and false otherwise
        """
        return not len(self.waypoints) == 0

    def move_vehicle_location(self, new_position: carla.Transform) -> None:
        """
        Updates the position of the Vehicle to a new position.

        :param new_position: a carla.Transform representing the new location of the vehicle
        :return: None
        """
        self.carla_vehicle.set_transform(new_position)

    def get_vehicle_size(self) -> Tuple[float, float]:
        """
        Gets the size of the vehicle's bounding box as a width, length tuple.

        If this function doesn't work as intended, blame Austin
        :return: the width and length of the vehicle as a tuple
        """
        return self.carla_vehicle.bounding_box.extent[0], self.carla_vehicle.bounding_box.extent[1]

    def get_current_speed(self) -> float:
        """
        Gets the current forward speed of the Vehicle.

        :return: the current forward speed of the Vehicle as a float
        """
        velocity = self.carla_vehicle.get_velocity()
        return (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5

    def get_current_position(self) -> Tuple[float, float]:
        """
        Gets the current position of the vehicle.

        :return: the current position of the Vehicle as an (x,y) tuple
        """
        transform = self.carla_vehicle.get_transform()
        return transform.location.x, transform.location.y

    def get_current_rotation(self) -> float:
        """
        Gets the current rotation of the vehicle (yaw).

        :return: the current rotation of the vehicle as a float
        """
        transform = self.carla_vehicle.get_transform()
        return transform.rotation.yaw

    def update_other_vehicle_locations(self, other_vehicles: List) -> None:
        """
        Updates the internal list with the transforms of all other Vehicles in the simulation

        :param other_vehicles: a List of all other Vehicles in the Simulation
        :return: None
        """

        current_location = self.get_location_vector()
        self.other_vehicle_locations = [x.get_location_vector()
                                        for x in other_vehicles if x.carla_vehicle.id != self.carla_vehicle.id]
        self.other_vehicle_locations.sort(key=lambda x: np.linalg.norm(current_location - x))

    def _check_vehicle_in_direction(self, direction: WorldDirection, experiment_type: ExperimentType) -> Tuple[bool, float]:
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

        # Required distance between two vehicles to be "safe"
        if direction in [WorldDirection.FORWARD, WorldDirection.BACKWARD]:
            required_distance = self.safety_distance + self.carla_vehicle.bounding_box.extent.x / 2
        else:
            required_distance = self.safety_distance + self.carla_vehicle.bounding_box.extent.y / 2

        current_location: np.array = self.get_location_vector()

        # Determine what vector we need to evaluate based on the given direction
        current_vector: np.array = to_numpy_vector(self.carla_vehicle.get_transform().get_forward_vector())
        if direction == WorldDirection.BACKWARD:
            current_vector = rotate_vector(current_vector, 180)
        elif direction == WorldDirection.LEFT:
            current_vector = rotate_vector(current_vector, 270)
        elif direction == WorldDirection.RIGHT:
            current_vector = rotate_vector(current_vector, 90)

        current_unit_vector: np.array = current_vector / np.linalg.norm(current_vector)

        for other_location in self.other_vehicle_locations:
            # Calculate the displacement vector between the current car and the other car
            displacement_vector: np.array = other_location - current_location
            unit_displacement_vector: np.array = displacement_vector / np.linalg.norm(displacement_vector)

            # Now determine the angle between the displacement vector and the forward vector of the current car
            angle = math.acos(np.dot(current_unit_vector, unit_displacement_vector))

            # If the angle is small enough, then the vehicle is in front of the current vehicle
            if angle < math.atan(self.carla_vehicle.bounding_box.extent.y / self.carla_vehicle.bounding_box.extent.x):
                distance = np.linalg.norm(displacement_vector)
                if distance < required_distance:
                    return True, distance

        return False, 0.0

    def check_vehicle_in_front(self, experiment_type: ExperimentType) -> (bool, float):
        """
        Determines if there is a vehicle in front of this vehicle.

        :param experiment_type: an ExperimentType enum specifying the current experiment type
        :return: a tuple containing whether there is a vehicle in front and the distance if there
                 is a vehicle in front.
        """

        return self._check_vehicle_in_direction(WorldDirection.FORWARD, experiment_type)

    def check_vehicle_in_back(self, experiment_type: ExperimentType) -> Tuple[bool, float]:
        """
        Determines if there is a vehicle behind this vehicle.

        :param experiment_type: an ExperimentType enum specifying the current experiment type
        :return: a tuple containing whether there is a vehicle in back and the distance if there
                 is a vehicle in back.
        """

        return self._check_vehicle_in_direction(WorldDirection.BACKWARD, experiment_type)

    def check_vehicle_to_left(self, experiment_type: ExperimentType) -> Tuple[bool, float]:
        """
        Determines if there is a vehicle to the left of this vehicle.

        :param experiment_type: an ExperimentType enum specifying the current experiment type
        :return: a tuple containing whether there is a vehicle to the left and the distance if there
                 is a vehicle to the left.
        """

        return self._check_vehicle_in_direction(WorldDirection.LEFT, experiment_type)

    def check_vehicle_to_right(self, experiment_type: ExperimentType) -> Tuple[bool, float]:
        """
        Determines if there is a vehicle to the right of this vehicle.

        :param experiment_type: an ExperimentType enum specifying the current experiment type
        :return: a tuple containing whether there is a vehicle to the right and the distance if there
                 is a vehicle to the right.
        """

        return self._check_vehicle_in_direction(WorldDirection.RIGHT, experiment_type)

    # Maybe relocate this function, decide later
    def draw_waypoints(self, world: carla.World) -> None:
        """
        Draws the waypoints and trajectory that the vehicle is following.

        :param world: a carla.World object representing the current simulator world.
        :return: None
        """

        for i in range(len(self.waypoints) - 1):
            world.debug.draw_point(self.waypoints[i].location, size=0.15, color=ORANGE, life_time=0.0)

        world.debug.draw_point(self.waypoints[-1].location, size=0.15, color=RED, life_time=0.0)

        for i in range(1, len(self.trajectory)):
            begin = self.trajectory[i-1].location
            end = self.trajectory[i].location
            world.debug.draw_line(begin, end, thickness=0.05, color=ORANGE, life_time=0.0)

    def get_location_vector(self, dims=3) -> np.array:
        """
        Getter for the current location of the Vehicle as a numpy.array with length three

        :param dims: number of dimensions that the output vector will have
        :return: the current location of the vector as a numpy.array
        """
        location = self.carla_vehicle.get_location()
        if dims == 3:
            return np.array([location.x, location.y, location.z])
        return np.array([location.x, location.y])
