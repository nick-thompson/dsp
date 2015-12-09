#!/usr/bin/env python

"""
Script for generating a series of band-limited wavetables and writing the result
out to a PCM file (commonly referred to as mipmapping, drawing the comparison to
the similar process in computer graphics).

Here we build 128 tables corresponding to the MIDI note range, such that each
MIDI note renders from a band-limited wavetable with exactly the right number
of harmonics, for each of the four wave types availabile in
wavetable/wavetable.py.

N.B. (1): Most of the implementations I've seen for this use far fewer tables,
usually something like 3 tables per octave. In that case, you have to be a
little more careful about mapping note frequencies to the appropriate range, but
the computational cost there is well worth the memory saved. Additionally, this
script produces 128 identical tables for the sine wave (because band-limiting a
sine wave has no effect) for simplicity, which you would never really want to
do in a high performance plugin.

N.B. (2): The Unix tool `xxd` is really useful for converting the resulting PCM
file to a C-style array literal, making it very easy to build into your plugin
binary.
"""

import numpy as np

from wavetable import wavetable
from wavetable.utils import normalize

NUM_RANGES = 128
NUM_TYPES = 4

def note_to_freq(note):
    """
    Return the frequency value for a given MIDI note value.
    """
    return 440.0 * pow(2.0, (note - 69) / 12.0)

if __name__ == '__main__':
    tables = []
    for i in range(NUM_TYPES):
        for j in range(NUM_RANGES):
            fq = note_to_freq(j)
            table = wavetable.build(i, fq)
            tables.append(table)

    mipmap = np.concatenate(tables)

    # Scale the output into little-endian 32-bit signed integers.
    factor = 2**31 - 1
    output = (mipmap * factor).astype('<i4')
    output.tofile('mipmap.pcm')

