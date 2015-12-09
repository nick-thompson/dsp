"""
Module for utility functions on Numpy arrays.
"""

import numpy as np

from math import floor

def normalize(arr):
    """
    Normalize the values of the input array into the range [-1, 1] in place.
    """
    arr /= np.max(np.abs(arr), axis=0)
    return arr

def trim(arr, amt):
    """
    Zero out the tail end of the given array.

    The first N frames of the array are left in tact, where N is (1 / amt)
    percent of the length of arr.
    """
    n = floor(arr.size / amt)
    arr[n:] = 0.0
    return arr
