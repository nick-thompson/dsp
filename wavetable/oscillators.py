"""
This module is responsible for defining various oscillators.

Each oscillator renders a sawtooth waveform to an array, but with different
implementations (in particular, surrounding the detune parameter) for the sake
of examining the resulting differences in the output buffers.

Note: oscillators assume a standard sample rate of 44.1kHz.
"""

import numpy as np

from math import floor
from wavetable import TABLE_SIZE, table, gibbs_table

class StandardOscillator:
    """
    The standard oscillator is my best guess at how conventional software
    synthesizers treat detune when generating periodic waveforms.

    Very simply, the approach is to compute the frequency of the oscillator
    given its detune value before stepping through the wavetable.
    """

    def __init__(self, freq, detune, level):
        detune_ratio = pow(2, detune / 1200.0)
        fq = freq * detune_ratio
        cycles_per_sample = fq / 44100.0

        self.freq = fq
        self.incr = cycles_per_sample * TABLE_SIZE
        self.level = level

    def render(self, buf):
        index = 0.0

        for i in range(buf.size):
            read_index = int(floor(index))
            mask = TABLE_SIZE - 1

            read_index_wrapped_left = read_index & mask
            read_index_wrapped_right = (read_index + 1) & mask

            left = table[read_index_wrapped_left]
            right = table[read_index_wrapped_right]

            alpha = index - float(read_index)
            inv_alpha = 1.0 - alpha
            sample = (inv_alpha * left) + (alpha * right)

            buf[i] += sample * self.level
            index += self.incr


class ResamplingOscillator:
    """
    The resampling oscillator takes a different approach to applying detune
    to the oscillator's frequency by applying the behavior of
    pitching up a static buffer.

    In particular, this oscillator draws an intermediate buffer before rendering
    its true output. This is so that the frequency value can be used to render
    a waveform independent of the detune parameter, then we resample the
    intermediate buffer to accommodate the detune value.

    This approach introduces phase artifacts that, when played back next to a
    different, slightly out of tune, sawtooth wave, creates an interesting
    zipper-like characteristic in the sound.
    """

    def __init__(self, freq, detune, level):
        cycles_per_sample = freq / 44100.0

        self.freq = freq
        self.detune = detune
        self.incr = cycles_per_sample * TABLE_SIZE
        self.level = level
        self._standard = StandardOscillator(freq, 0.0, level)

    def render(self, buf):
        intermediate = np.zeros(buf.size, dtype='d')
        self._standard.render(intermediate)

        playback_rate = pow(2, self.detune / 1200.0)
        playback_index = 0.0

        for i in range(buf.size):
            read_index = int(floor(playback_index))
            read_index_left = read_index
            read_index_right = read_index + 1
            if read_index_left >= buf.size or read_index_right >= buf.size:
                break

            left = intermediate[read_index_left]
            right = intermediate[read_index_right]

            alpha = playback_index - float(read_index)
            inv_alpha = 1.0 - alpha
            sample = (inv_alpha * left) + (alpha * right)

            buf[i] += sample
            playback_index += playback_rate


