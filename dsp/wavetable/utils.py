"""
Module for utility functions on Numpy arrays.
"""

import numpy as np

from math import floor
from scipy.io import wavfile

def normalize(arr):
    """
    Normalize the values of the input array into the range [-1, 1] in place.
    """
    arr /= np.max(np.abs(arr), axis=0)
    return arr

def trim(arr, amt):
    """
    Zero out the tail end of the given array in place.

    The first N frames of the array are left in tact, where N is (1 / amt)
    percent of the length of arr.
    """
    n = floor(arr.size / amt)
    arr[n:] = 0.0
    return arr

def note_to_freq(note):
    """
    Return the frequency value for a given MIDI note value.
    """
    return 440.0 * pow(2.0, (note - 69) / 12.0)

def write_wav(name, sr, arr):
    """
    Write a numpy array to disk as a little-endian 32-bit signed WAV file.

    Parameters
    name : Output file name
    sr : Output sample rate
    arr : The numpy array to write
    """
    factor = 2**31 - 1
    output = (arr * factor).astype('<i4')
    wavfile.write(name, sr, output)

def write_pcm(name, arr):
    """
    Write a numpy array to disk as a PCM file. Virtually the same as `write_wav`
    above, but the resulting file doesn't have the WAV header.

    Parameters
    name : Output file name
    arr : The numpy array to write
    """
    factor = 2**31 - 1
    output = (arr * factor).astype('<i4')
    output.tofile(name)
