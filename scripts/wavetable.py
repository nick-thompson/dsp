#!/usr/bin/env python

"""
Script for generating a series of band-limited wavetables and writing the result
out to a binary file.

In particular, we generate 128 tables corresponding to the MIDI note range, with
the appropriate number of harmonics for each MIDI note value. Each table is of
size 4096 samples for high quality rendering and to accommodate the large number
of partials in the lower end of the frequency range.

This process is carried out once for each of four wave types: sine, triangle,
sawtooth, and square.
"""

import numpy as np
import matplotlib.pyplot as plt

from math import floor

TABLE_SIZE = 4096
NUM_RANGES = 128
NUM_TYPES = 4

SAMPLE_RATE = 44100.0
NYQUIST = SAMPLE_RATE / 2.0
MAX_PARTIALS = TABLE_SIZE / 2

data = np.zeros(NUM_TYPES * NUM_RANGES * TABLE_SIZE, dtype='d')

def normalize(arr):
    """
    Normalize the values of the input array into the range [-1, 1].
    """
    arr /= np.max(np.abs(arr), axis=0)
    return arr

def note_to_freq(note):
    """
    Return the frequency value for a given MIDI note value.
    """
    return 440.0 * pow(2.0, (note - 69) / 12.0)

def gen_sine(order = 0):
    """
    Writes the sine wavetable into `data`.
    """
    for i in range(NUM_RANGES):
        t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
        table = np.sin(2 * np.pi * t)

        offset = order * NUM_RANGES * TABLE_SIZE + i * TABLE_SIZE
        data[offset:offset + TABLE_SIZE] = table

def gen_triangle(order = 1):
    """
    Writes the triangle wavetable series into `data`.
    """
    for i in range(NUM_RANGES):
        freq = note_to_freq(i)
        num_partials = min(int(floor(NYQUIST / freq)), MAX_PARTIALS)

        t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
        table = np.zeros(TABLE_SIZE, dtype='d')
        alt = -1.0

        for j in range(num_partials):
            k = j + 1
            if k % 2 == 0:
                continue

            alt *= -1

            # Dampen the kth partial using the Lanczos sigma factor to
            # attenuate the Gibbs phenomenon.
            sigma = np.sinc(k * np.pi / (2 * num_partials))
            table -= np.sin(2 * np.pi * k * t) / (alt * k * k * np.pi) * sigma

        normalize(table)
        offset = order * NUM_RANGES * TABLE_SIZE + i * TABLE_SIZE
        data[offset:offset + TABLE_SIZE] = table
    pass

def gen_sawtooth(order = 2):
    """
    Writes the sawtooth wavetable series into `data`.

    Computed using all integer harmonics of the fundamental frequency.
    """
    for i in range(NUM_RANGES):
        freq = note_to_freq(i)
        num_partials = min(int(floor(NYQUIST / freq)), MAX_PARTIALS)

        t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
        table = np.zeros(TABLE_SIZE, dtype='d')

        for j in range(num_partials):
            k = j + 1

            # Dampen the kth partial using the Lanczos sigma factor to
            # attenuate the Gibbs phenomenon.
            sigma = np.sinc(k * np.pi / (2 * num_partials))
            table -= np.sin(2 * np.pi * k * t) / (k * np.pi) * sigma

        normalize(table)
        offset = order * NUM_RANGES * TABLE_SIZE + i * TABLE_SIZE
        data[offset:offset + TABLE_SIZE] = table

def gen_square(order = 3):
    """
    Writes the square wavetable series into `data`.

    Computed using only odd integer harmonics of the fundamental frequency.
    """
    for i in range(NUM_RANGES):
        freq = note_to_freq(i)
        num_partials = min(int(floor(NYQUIST / freq)), MAX_PARTIALS)

        t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
        table = np.zeros(TABLE_SIZE, dtype='d')

        for j in range(num_partials):
            k = j + 1
            if k % 2 == 0:
                continue

            # Dampen the kth partial using the Lanczos sigma factor to
            # attenuate the Gibbs phenomenon.
            sigma = np.sinc(k * np.pi / (2 * num_partials))
            table -= np.sin(2 * np.pi * k * t) / (k * np.pi) * sigma

        normalize(table)
        offset = order * NUM_RANGES * TABLE_SIZE + i * TABLE_SIZE
        data[offset:offset + TABLE_SIZE] = table

if __name__ == '__main__':
    gen_sine()
    gen_triangle()
    gen_sawtooth()
    gen_square()

    # TODO: In the last few wavetables of each series, it looks like the single
    # sine cycle is in the wrong phase?

    # TODO: Each wavetable uses different dampening factors because the number
    # of partials is decreasing. For effective pitch slides, might need to keep
    # the denominator constant for each wavetable in the series.

    # For interactive drawing, iterating through the wavetables...
    # x = np.linspace(0, 1, num=TABLE_SIZE, dtype='f')
    # plt.ion()
    # Iterate...
    #   plt.clf()
    #   plt.plot(x, y)
    #   plt.draw()
    #   time.sleep(0.05)

    # Scale the output into little-endian 32-bit signed integers.
    factor = 2**31 - 1
    output = (data * factor).astype('<i4')
    output.tofile('wavetable.data')
