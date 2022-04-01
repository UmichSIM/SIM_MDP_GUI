"""
Backend - Vehicle Class
Created on Tue February 15, 2022

Summary: The Vehicle class represents a single vehicle in the CARLA simulation environment. It stores
    all relevant information for a single instance. Provides a high level interface for controlling a
    vehicle's motion through a Controller class.

References:
    Helpers

Referenced By:
    Controller
    EgoController
    Experiment

"""

# Local Imports
from Helpers import WorldDirection, VehicleType, to_numpy_vector, rotate_vector, ORANGE, RED

# Library Imports
import carla
import math
import numpy as np
from simple_pid import PID
from typing import List, Tuple


class Vehicle:

    def __init__(self, carla_vehicle: carla.Vehicle, name: str, type_id: VehicleType,
                 target_distance: float = 15.0, target_speed: float = 35.0,
                 breaking_distance: float = 20.0):
        super().__init__()

        # Stores the Carla Vehicle object associated with this particular vehicle
        self.carla_vehicle: carla.Vehicle = carla_vehicle

        # The type of this Vehicle
        self.type_id: VehicleType = type_id

        # The user specified name for each vehicle
        self.name: str = name

        # The target distance that the vehicle will maintain between itself and the car in front of it
        self.target_distance: float = target_distance

        # PID controller to manage maintaining the target distance
        self.distance_pid_controller = PID(0.5, 0.02, 0.3, setpoint=0)
        self.distance_pid_controller.output_limits = (-1, 1)

        # The target speed that the vehicle will maintain (current in KM/H)
        self.target_speed = target_speed

        # PID controller to manage maintaining the target speed
        self.speed_pid_controller = PID(-0.5, -0.02, -0.3, setpoint=0)
        self.speed_pid_controller.output_limits = (-1, 1)

        # The target location that the vehicle will attempt to stop at
        self.target_location: carla.Location = None

        # PID controller to manage arriving at the target location
        self.location_pid_controller = PID(-0.5, -0.00, -0.3, setpoint=0)
        self.location_pid_controller.output_limits = (-1, 1)

        # The distance before the target location that the vehicle will start breaking
        self.breaking_distance: float = breaking_distance

        # List of the np.arrays that represent the locations of every other Vehicle in the
        # experiment along with the length of the vehicle's bounding box
        self.other_vehicle_locations: List[Tuple[np.array, float]] = []

        # List that stores the raw waypoints that the vehicle will travel through
        self.waypoints: List[carla.Transform] = []

        # List that stores the high-resolution trajectory that vehicle uses for path following
        # This trajectory is generated by smoothing and generating intermediate points connecting
        # the waypoints together
        self.trajectory: List[carla.Transform] = []

        # The current section that the Vehicle is on, can either be an Intersection or Freeway Section
        self.current_section = None

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

    def apply_control(self, new_control: carla.VehicleControl) -> None:
        """
        Updates the control state being applied to the Vehicle.

        Provides a wrapper around the carla.Vehicle.apply_control function.

        :param new_control: the carla.VehicleControl to apply to the Vehicle
        :return: None
        """
        self.carla_vehicle.apply_control(new_control)

    def get_vehicle_size(self) -> carla.Vector3D:
        """
        Gets the size of the vehicle's bounding box as a width, length tuple.

        If this function doesn't work as intended, blame Austin
        :return: the width and length of the vehicle as a tuple
        """
        return self.carla_vehicle.bounding_box.extent

    def get_current_speed(self, units="kmh") -> float:
        """
        Gets the current forward speed of the Vehicle.

        :param units: Specifies the units that the speed should be returned in. Either "kmh" or "mph"
        :return: the current forward speed of the Vehicle as a float
        """
        velocity = self.carla_vehicle.get_velocity()
        speed = (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5

        if units == "kmh":
            return speed * 3.6
        elif units == "mph":
            return speed * 2.23694

        raise Exception("Invalid units passed into get_current_speed function. Expected either \"kmh\" or \"mph\"")

    def get_current_location(self) -> carla.Location:
        """
        Gets the current Location of the vehicle.

        :return: the current position of the Vehicle a carla.Location
        """
        return self.carla_vehicle.get_location()

    def get_current_rotation(self) -> float:
        """
        Gets the current rotation of the vehicle (yaw).

        :return: the current rotation of the vehicle as a float
        """
        transform = self.carla_vehicle.get_transform()
        return transform.rotation.yaw

    def update_other_vehicle_locations(self, other_vehicles: List) -> None:
        """
        Updates the internal list with the transforms of all other Vehicles in the simulation.

        Also stores the vehicle length of all other vehicles in the Simulation. This enables distance
        calculates to take into account bumper to bumper distance

        :param other_vehicles: a List of all other Vehicles in the Simulation
        :return: None
        """

        current_location = self.get_location_vector()
        self.other_vehicle_locations = [(x.get_location_vector(), x.get_vehicle_size().y)
                                        for x in other_vehicles if x.carla_vehicle.id != self.carla_vehicle.id]
        self.other_vehicle_locations.sort(key=lambda x: np.linalg.norm(current_location - x[0]))

    def _check_vehicle_in_direction(self, direction: WorldDirection) -> Tuple[bool, float]:
        """
        Determines if there is a vehicle next to the current vehicle in any given direction.

        Uses the vehicles current rotation to check if there are any vehicles nearby in any
        cardinal direction. Forward uses a direction vector of [0, 1]. Backward uses a direction
        vector of [0, -1]. Left uses a direction vector of [-1, 0]. Right uses a direction vector of
        [0, 1].

        :param direction: a WorldDirection enum specifying which direction to check for vehicles
        :return: a tuple containing whether there is a vehicle in the given direction and the
                 distance if said vehicle exists
        """

        # Required distance between two vehicles to be "safe"
        if direction in [WorldDirection.FORWARD, WorldDirection.BACKWARD]:
            required_distance = 1.2 * self.target_distance + self.carla_vehicle.bounding_box.extent.x / 2
        else:
            required_distance = 1.2 * self.target_distance + self.carla_vehicle.bounding_box.extent.y / 2

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

        for other_location, vehicle_length in self.other_vehicle_locations:
            # Calculate the displacement vector between the current car and the other car
            displacement_vector: np.array = other_location - current_location
            unit_displacement_vector: np.array = displacement_vector / np.linalg.norm(displacement_vector)

            # Now determine the angle between the displacement vector and the forward vector of the current car
            angle = math.acos(np.dot(current_unit_vector, unit_displacement_vector))

            # If the angle is small enough, then the vehicle is in front of the current vehicle
            if angle < math.atan(self.carla_vehicle.bounding_box.extent.y / self.carla_vehicle.bounding_box.extent.x):
                distance = np.linalg.norm(displacement_vector)
                if distance < required_distance:
                    # Subtract the Vehicle length to account for the bumper to bumper distance
                    return True, distance - vehicle_length

        return False, 0.0

    def check_vehicle_in_front(self) -> Tuple[bool, float]:
        """
        Determines if there is a vehicle in front of this vehicle.

        :return: a tuple containing whether there is a vehicle in front and the distance if there
                 is a vehicle in front.
        """

        return self._check_vehicle_in_direction(WorldDirection.FORWARD)

    def check_vehicle_in_back(self) -> Tuple[bool, float]:
        """
        Determines if there is a vehicle behind this vehicle.

        :return: a tuple containing whether there is a vehicle in back and the distance if there
                 is a vehicle in back.
        """

        return self._check_vehicle_in_direction(WorldDirection.BACKWARD)

    def check_vehicle_to_left(self) -> Tuple[bool, float]:
        """
        Determines if there is a vehicle to the left of this vehicle.

        :return: a tuple containing whether there is a vehicle to the left and the distance if there
                 is a vehicle to the left.
        """

        return self._check_vehicle_in_direction(WorldDirection.LEFT)

    def check_vehicle_to_right(self) -> Tuple[bool, float]:
        """
        Determines if there is a vehicle to the right of this vehicle.

        :return: a tuple containing whether there is a vehicle to the right and the distance if there
                 is a vehicle to the right.
        """

        return self._check_vehicle_in_direction(WorldDirection.RIGHT)

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

        :param dims: number of dimensions that the output vector will have (either 2 or 3)
        :return: the current location of the vector as a numpy.array
        """
        location = self.carla_vehicle.get_location()
        if dims == 3:
            return np.array([location.x, location.y, location.z])
        if dims == 2:
            return np.array([location.x, location.y])
        raise Exception("Invalid number of dimensions passed to get_location_vector")
