"""
Backend - Controller Class
Created on Tue February 15, 2022

Summary: The Controller class is a static base class that implements control over the vehicles in the
    Simulation. This class provides the basic interface and functions that all Controller classes can use.
    Ego, Intersection, and Freeway controllers are derived from this base class

References:
    Helpers
    Vehicle

Referenced By:
    EgoController
    FreewayController
    IntersectionController
    TestExperiment

"""

# Local Imports
from Helpers import to_numpy_vector, smooth_path, VehicleType
from Vehicle import Vehicle

# Library Imports
import carla
import heapq
import numpy as np
import random
from typing import List, Tuple

# Global variable to define how far apart waypoints on the road network should be
WAYPOINT_SEPARATION = 15

# Global constant that dictates how strongly speed affects the Pure Pursuit lookahead distance
SPEED_CONSTANT = 0.075

# Global constant that dictates how much additional stopping distance the vehicle gains per kilometer per hour
STOP_DISTANCE_FACTOR = 0.25


class Controller:

    # Static carla.World object representing the simulator world
    world: carla.World = None

    @staticmethod
    def update_control(current_vehicle: Vehicle) -> None:
        """
        Abstract function that dictates how a derived Controller class should update the Vehicles control.

        All derived controller classes must implement this method. The update_control method takes in a
        vehicle and determines what control parameters should be passed to it to update its acceleration
        and steering in the Carla simulation. This function will call apply_control on the current
        vehicle to steer the vehicle in the correct direction.

        :param current_vehicle: the Vehicle object to which updated control needs to be applied
        :return: None
        """
        pass

    @staticmethod
    def generate_path(current_vehicle: Vehicle, starting_point: carla.Waypoint, ending_point: carla.Waypoint) -> \
            Tuple[List[carla.Waypoint], List[carla.Waypoint]]:
        """
        Calculates the shortest trajectory between the starting endpoint and ending waypoint of the Vehicle's route.

        Uses A* pathfinding algorithm to determine the shortest path between the starting waypoint and
        the ending waypoint. All paths will follow Carla's autogenerated waypoints that define the
        valid road network. The path is guaranteed to take the shortest number of jumps between waypoints,
        however there is no guarantee that the path will be the shortest in terms of absolute distance.

        :param current_vehicle: the Vehicle object that the path needs to be generated for
        :param starting_point: the carla.Waypoint object that the vehicle will be starting at
        :param ending_point: the carla.Waypoint object that the vehicle will be ending at
        :return: None
        """

        # Location of the destination waypoint
        destination: np.array = to_numpy_vector(ending_point.transform.location)

        # List of tuples containing each explored waypoint, the current distance to that waypoint,
        # and the index of their previous waypoint along the path
        explored_list: List[Tuple[carla.Waypoint, int]] = []

        # List of Tuples used as a Priority Queue. The first int is the straight line distance
        # between the waypoint and the destination. The second Tuple contains the waypoint
        # and the index of the previous waypoint in the path
        potential_list: List[Tuple[int, Tuple[carla.Waypoint, int]]] = []

        # Add the initial point to the potential_list
        heapq.heappush(potential_list, (0, (starting_point, -1)))

        # Main A* loop
        while True:

            # Grab the current waypoint and previous index
            _, (current_waypoint, current_previous_index) = heapq.heappop(potential_list)

            # Add them to the explored list
            explored_list.append((current_waypoint, current_previous_index))

            # If the search is over, backtrack to build the path
            if Controller._end_of_search(current_waypoint, ending_point):
                waypoints = Controller._backtrack_path(explored_list)
                trajectory = smooth_path(waypoints, num_passes=2) if len(waypoints) > 0 else waypoints
                return waypoints, trajectory

            # Check all the potential next waypoints and add them to the potential list
            # if they haven't already been explored
            potential_new_waypoints = Controller._get_next_waypoints(current_waypoint)
            already_explored_waypoint_ids = [x[0].id for x in explored_list]
            for potential_new_waypoint in potential_new_waypoints:
                if potential_new_waypoint.id not in already_explored_waypoint_ids:
                    distance_to_destination = np.linalg.norm(to_numpy_vector(potential_new_waypoint.transform.location)
                                                             - destination)
                    heapq.heappush(potential_list,
                                   (distance_to_destination + random.random(),
                                    (potential_new_waypoint, len(explored_list) - 1)))

            # Handle the case of no path between the starting and ending waypoint
            if len(potential_list) == 0:
                raise Exception(f"Unable to find path between waypoints {starting_point.id} and {ending_point.id}")

    @staticmethod
    def steering_control(current_vehicle: Vehicle) -> Tuple[float, bool]:
        """
        Implements path following using the Pure Pursuit Path Tracking algorithm.

        Link to a paper on the subject can be found here:
        https://www.ri.cmu.edu/publications/implementation-of-the-pure-pursuit-path-tracking-algorithm/
        Determines what steering angle the vehicle needs to remain on the path outlined by its waypoints.
        Chooses a lookahead distance based on the vehicle's current speed and identifies the waypoint
        that is closest to that lookahead distance. Then, calculates the curve that connects the Vehicle's
        current location to that destination waypoint. The inverse tangent of the curve can then be
        taken to determine the steering angle needed.

        :param current_vehicle: a Vehicle object representing the vehicle to be controlled
        :return: a Tuple where the first element is a float representing the steering angle in radians
                 (bounded between -1 and 1) and the second element is if the Vehicle has reached
                 the end of the path
        """

        # Get the current location and forward facing vector of the vehicle
        current_location: np.array = current_vehicle.get_location_vector(dims=2)
        forward_facing_vector: np.array = to_numpy_vector(
            current_vehicle.carla_vehicle.get_transform().get_forward_vector(), dims=2)
        unit_forward_facing_vector: np.array = forward_facing_vector / np.linalg.norm(forward_facing_vector)

        # Find the closest waypoint to the vehicles current location
        trajectory: List[carla.Transform] = current_vehicle.trajectory
        trajectory_point_distances: List[np.array] = [
            np.linalg.norm(to_numpy_vector(x.location, dims=2) - current_location)
            for x in trajectory]
        nearest_trajectory_point_index = np.argmin(trajectory_point_distances)

        # Determine what our lookahead distance should be
        current_forward_speed = np.linalg.norm(to_numpy_vector(current_vehicle.carla_vehicle.get_velocity()))
        lookahead_distance = 1.0 + current_forward_speed * SPEED_CONSTANT

        # Find the next waypoint that is at least lookahead distance away, or at the end of the path
        current_distance = 0
        index = nearest_trajectory_point_index + 1
        while current_distance < lookahead_distance and index < len(trajectory):
            current_distance += np.linalg.norm(
                to_numpy_vector(trajectory[index].location) - to_numpy_vector(trajectory[index - 1].location))
            index += 1

        # Stop the car if we've reached the end of the path
        if index >= len(trajectory):
            return 0.0, True

        # Identify our new goal waypoint
        goal_trajectory_point = trajectory[index]
        distance_from_current_location_to_goal = trajectory_point_distances[index]

        # Calculate the angle between the vehicles forward facing vector and the distance vector between the
        # car and goal waypoint
        distance_vector = to_numpy_vector(goal_trajectory_point.location, dims=2) - current_location
        unit_distance_vector = distance_vector / np.linalg.norm(distance_vector)
        theta = np.arctan2(unit_distance_vector[1], unit_distance_vector[0]) - \
            np.arctan2(unit_forward_facing_vector[1], unit_forward_facing_vector[0])

        # Lastly, get the length of the vehicle and calculate the steering angle
        # The 1.5 is an arbitrary scaling factor to account for the fact that Pure Pursuit doesn't do
        # 90 degree turns very well
        vehicle_length = current_vehicle.carla_vehicle.bounding_box.extent.y * 2
        steering_angle = 1.5 * np.arctan2(2 * vehicle_length * np.sin(theta), distance_from_current_location_to_goal)

        return steering_angle, False

    @staticmethod
    def throttle_control(current_vehicle: Vehicle) -> float:
        """
        Applies throttle control to the vehicle based on its current setting.

        The different modes that a vehicle can operate in are a "target_location", "target_speed", or
        "target_distance".

        In target_location mode, the vehicle will accelerate maintain its target speed
        until it is within a certain distance of its target location. Then, it will brake to smoothly
        stop at that location. This mode is activated if the current_vehicle has a valid target location
        and the vehicle is within its pre-defined breaking distance.

        In target_distance mode, the vehicle will accelerate or decelerate as necessary to maintain a
        target distance from the vehicle in-front of it. This mode is activated if there is a vehicle in front
        of the current vehicle within 1.2 times the current vehicle's safety distance. This mode can never be
        activated for a lead vehicle.

        In target_speed mode, the vehicle will accelerate up to its target speed and then apply the acceleration
        necessary to maintain that speed. This mode will be activated if neither of the other modes apply.

        :param current_vehicle: the Vehicle object to calculate the throttle for
        :return: a float representing the throttle to be applied to the vehicle (between -1 and 1)
        """

        # Determine the largest throttle that a vehicle should be allowed to apply. A Vehicle should
        # never be allowed to travel faster than their target speed
        max_throttle = Controller._throttle_target_speed(current_vehicle)
        follow_throttle = None
        stop_throttle = None

        # Determine if the vehicle is close enough to the vehicle in front of it that it needs to
        # adjust its throttle
        if current_vehicle.type_id != VehicleType.LEAD:
            car_in_front, current_distance = current_vehicle.check_vehicle_in_front()
            if car_in_front:
                follow_throttle = Controller._throttle_target_distance(current_vehicle, current_distance)

        # Determine if the vehicle is close enough to an intersection that it needs to
        # adjust its throttle
        if current_vehicle.target_location is not None:
            current_distance = np.sum(to_numpy_vector(current_vehicle.target_location) -
                                      current_vehicle.get_location_vector())
            if current_distance <= current_vehicle.breaking_distance:
                stop_throttle = Controller._throttle_target_location(current_vehicle)

        # Lastly, determine the most appropriate throttle to apply to the vehicle
        if follow_throttle is not None and stop_throttle is not None:
            return min([max_throttle, follow_throttle, stop_throttle])
        if follow_throttle is not None:
            return min([max_throttle, follow_throttle])
        if stop_throttle is not None:
            return min([max_throttle, stop_throttle])
        return max_throttle

    @staticmethod
    def _avoid_collisions(current_vehicle: Vehicle) -> Tuple[bool, carla.VehicleControl]:
        """
        Determines if the Vehicle needs to change its control to avoid a collision.

        Checks if the Vehicle is nearing a collision with another nearby Vehicle (to the left or right),
        and provides a new carla.VehicleControl object that will allow the Vehicle to avoid the
        collision. Designed to be called either within or after update_control.

        :param current_vehicle: the Vehicle object that will be checked for near collisions
        :return: a tuple of (bool, carla.VehicleControl). The first element will be True if the Vehicle
                 needs to avoid a collision. If True, the second element will contain a
                 new carla.VehicleControl that should be applied to the Vehicle.
        """
        pass

    @staticmethod
    def _end_of_search(current_waypoint: carla.Waypoint, ending_waypoint: carla.Waypoint) -> bool:
        """
        Determines if the A* search has successfully arrived at its destination point.

        To finish the search, the current waypoint must be less than half of WAYPOINT_SEPARATION
        away from the ending waypoint

        :param current_waypoint: a carla.Waypoint representing the current waypoint in the search
        :param ending_waypoint: a carla.Waypoint representing the ending waypoint in the search
        :return: a bool representing if the search is finished
        """

        current_location = current_waypoint.transform.location
        ending_location = ending_waypoint.transform.location
        separation = current_location.distance(ending_location)
        if separation < WAYPOINT_SEPARATION / 2:
            return True
        return False

    @staticmethod
    def _backtrack_path(explored_list: List[Tuple[carla.Waypoint, int]]) -> List[carla.Transform]:
        """
        Backtracks the explored path to build the shortest path from the initial point to the final destination.

        :param explored_list: a List of Tuples where the first element is a carla.Waypoint object
                              and the second element is the list index of the ancestor waypoint
        :return: a list of carla.Transforms representing the completed path
        """

        # Initialize the path and the ending locations
        path: List[carla.Waypoint] = []
        current_waypoint, current_index = explored_list[-1]

        # Continue backtracking until the first waypoint is reached
        while current_index != -1:
            path.append(current_waypoint)
            current_waypoint, current_index = explored_list[current_index]

        return path[::-1]

    @staticmethod
    def _get_next_waypoints(current_waypoint: carla.Waypoint) -> List[carla.Waypoint]:
        """
        Gets a list of all the possible next waypoints from the current waypoint

        :param current_waypoint: a carla.Waypoint representing the current waypoint
        :return: a List of carla.Waypoints
        """

        # Get all the possible next waypoints
        new_potential_waypoints: List[carla.Waypoint] = current_waypoint.next(WAYPOINT_SEPARATION)

        # Also add additional waypoints if the current waypoint is an intersection
        if current_waypoint.is_junction:
            junction_points = current_waypoint.get_junction().get_waypoints(carla.LaneType.Driving)
            for pair in junction_points:
                if pair[0].id == current_waypoint.id:
                    new_potential_waypoints.append(pair[1])
                elif pair[1].id == current_waypoint.id:
                    new_potential_waypoints.append(pair[0])

        return new_potential_waypoints

    @staticmethod
    def _throttle_target_location(current_vehicle: Vehicle) -> float:
        """
        Determines what throttle the Vehicle needs to stop at its target location.

        Uses the current speed of the vehicle and the distance to the target location to determine
        how much breaking needs to be applied to stop the vehicle. If the car is moving too slowly
        and breaking is not necessary, light throttle will be applied.

        :param current_vehicle: the Vehicle to calculate the throttle for
        :return: the throttle value to apply to the vehicle (between -1 and 1)
        """

        # Calculate the distance to the target location
        distance_to_location = np.sum(to_numpy_vector(current_vehicle.target_location, dims=2) -
                                      current_vehicle.get_location_vector(dims=2))

        # Calculate the vehicle's stopping distance
        stopping_distance = current_vehicle.get_current_speed() * STOP_DISTANCE_FACTOR

        # Pass the difference between the distance to the location
        # and the current stopping distance to the PID controller
        throttle = current_vehicle.location_pid_controller(distance_to_location - stopping_distance)
        return max(min(throttle, 1), -1)

    @staticmethod
    def _throttle_target_distance(current_vehicle: Vehicle, current_distance: float) -> float:
        """
        Determines what throttle the Vehicle needs to remain a target_distance away from the Vehicle in front.

        The Vehicle will accelerate until it is within the target distance of the Vehicle in front of it.
        Then, the Vehicle will alternate accelerating and breaking to maintain a constant distance from
        the vehicle in front.

        :param current_vehicle: the Vehicle to calculate the throttle for
        :param current_distance: the current distance between the Vehicle and the Vehicle in front
        :return: the throttle value to apply to the vehicle (between -1 and 1)
        """
        # Subtract by the Vehicle size to account for the bumper to bumper distance
        throttle = current_vehicle.distance_pid_controller(current_vehicle.target_distance - current_distance -
                                                           current_vehicle.get_vehicle_size().y)
        return max(min(throttle, 1), -1)

    @staticmethod
    def _throttle_target_speed(current_vehicle: Vehicle) -> float:
        """
        Determines what throttle the Vehicle needs to maintain a constant speed.

        The Vehicle will accelerate or decelerate as needed to maintain the constant target_speed

        :param current_vehicle: the Vehicle to calculate the throttle for
        :return: the throttle value to apply to the Vehicle (between -1 and 1)
        """

        throttle = current_vehicle.speed_pid_controller(current_vehicle.target_speed -
                                                        current_vehicle.get_current_speed())
        return max(min(throttle, 1), -1)

    @staticmethod
    def get_vehicles_current_waypoint(vehicle: Vehicle) -> carla.Waypoint:
        """
        Gets an OpenDrive waypoint located at the Vehicle's current location.

        :param vehicle: the Vehicle whose current waypoint is desired
        :return: a carla.Waypoint located at the vehicle's current location
        """
        return Controller.world.get_map().get_waypoint(vehicle.carla_vehicle.get_location())