"""
Backend - FreewayController Class
Created on Tue February 15, 2022

Summary: The FreewayController class inherits from the base Controller class. It implements control
    from all the non-ego vehicles that are operating in a Freeway experiment type. These vehicles
    do not need to manage traffic lights, however they must manage distance to the vehicles in-front
    and to the side of them.

References:

Referenced By:

"""

import Controller

class FreewayController(Controller):

    def __init__(self):
        pass