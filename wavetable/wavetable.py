"""
Module for generating band-limited sine, triangle, sawtooth, and square
wavetables.

Construction is done with additive synthesis, including partials just up to
Nyquist so as to avoid aliasing, with no accommodation for the Gibbs Phenomenon.

Note that the table size and the sample rate in this implementation are fixed,
where in practice they should likely be configurable. In particular, it's often
a good idea to reduce the size of the wavetable for the higher frequency tables,
because in a larger table the iterator (when rendering from the table) ends up
really big. Each read, then, could essentially be considered a random access.
Depending on the host's paging and caching architecture, this can be a large
performance hit.
"""

import matplotlib.pyplot as plt
import numpy as np
import time

from math import floor
from utils import normalize, note_to_freq

TABLE_SIZE = 4096

SAMPLE_RATE = 44100.0
NYQUIST = SAMPLE_RATE / 2.0
MAX_PARTIALS = TABLE_SIZE / 2

class WaveType:
    """
    A hacky enum encapsulating the various wave types.
    """
    SINE = 0
    TRIANGLE = 1
    SAWTOOTH = 2
    SQUARE = 3

def _sine():
    """
    Returns a sine wavetable.
    """
    t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
    table = np.sin(2 * np.pi * t)
    return normalize(table)

def _triangle(fq):
    """
    Returns a band-limited triangle wavetable.

    Parameters
    fq : Frequency used to determine the number of bands drawn in the table.
    """
    num_partials = min(int(floor(NYQUIST / fq)), MAX_PARTIALS)

    t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
    table = np.zeros(TABLE_SIZE, dtype='d')
    alt = -1.0

    for j in range(num_partials):
        k = j + 1
        if k % 2 == 0:
            continue

        alt *= -1
        table -= np.sin(2 * np.pi * k * t) / (alt * k * k * np.pi)

    return normalize(table)

def _sawtooth(fq):
    """
    Returns a band-limited sawtooth wavetable.

    Parameters
    fq : Frequency used to determine the number of bands drawn in the table.
    """
    num_partials = min(int(floor(NYQUIST / fq)), MAX_PARTIALS)

    t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
    table = np.zeros(TABLE_SIZE, dtype='d')

    for j in range(num_partials):
        k = j + 1
        table -= np.sin(2 * np.pi * k * t) / (k * np.pi)

    return normalize(table)

def _square(fq):
    """
    Returns a band-limited square wavetable.

    Parameters
    fq : Frequency used to determine the number of bands drawn in the table.
    """
    num_partials = min(int(floor(NYQUIST / fq)), MAX_PARTIALS)

    t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
    table = np.zeros(TABLE_SIZE, dtype='d')

    for j in range(num_partials):
        k = j + 1
        if k % 2 == 0:
            continue

        table -= np.sin(2 * np.pi * k * t) / (k * np.pi)

    return normalize(table)

def build(wavetype, fq):
    """
    Public API for constructing a band-limited wavetable.

    Parameters
    wavetype : WaveType specifying the type of table to be constructed.
    fq : Frequency used to determine the number of bands drawn in the table.
    """
    if wavetype == WaveType.SINE:
        return _sine()
    elif wavetype == WaveType.TRIANGLE:
        return _triangle(fq)
    elif wavetype == WaveType.SAWTOOTH:
        return _sawtooth(fq)
    elif wavetype == WaveType.SQUARE:
        return _square(fq)
    else:
        raise Exception('Unrecognized WaveType.')

if __name__ == '__main__':
    # Show an interactive plot of the band-limited tables.
    x = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')

    plt.ion()
    for i in range(4):
        # Span the MIDI range in steps of 16 notes.
        for j in range(0, 129, 16):
            fq = note_to_freq(j)
            table = build(i, fq)
            plt.clf()
            plt.plot(x, table)
            plt.draw()
            time.sleep(0.15)

    plt.ioff()
