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

import Controller

class IntersectionController(Controller):

    def __init__(self):
        pass