#!/usr/bin/env python3
"""
Mappings to change data to appropriate type
"""
def LinearMap(val:int, _max:int)->float:
    """
    map the input linearly to [-1,1]
    Inputs:
        val: value to be mapped
        _max: max possible value
    return: val/_max as float
    """
    assert(abs(val)<=_max)
    return val/_max
