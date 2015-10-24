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

        for i in range(buf.size):
            index = i * self.incr
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

        for i in range(buf.size):
            playback_index = i * playback_rate
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


class RealTimeResamplingOscillator:
    """
    The real time resampling approach introduces the same phase artifacts as
    the ones introduced by the classic ResamplingOscillator, but does so in
    real time so that it might be used in real synthesizers.

    The approach differs only in that it does not use the intermediate buffer,
    but rather computes the necessary sample frames of what would be the
    intermediate buffer in order to complete the linear interpolation step
    shown in the render method of the ResamplingOscillator.
    """

    def __init__(self, freq, detune, level):
        cycles_per_sample = freq / 44100.0

        self.freq = freq
        self.detune = detune
        self.incr = cycles_per_sample * TABLE_SIZE
        self.level = level

    def render(self, buf):
        table_rate = self.incr
        mask = TABLE_SIZE - 1

        playback_rate = pow(2, self.detune / 1200.0)

        for i in range(buf.size):
            playback_pointer = i * playback_rate
            # Let x, y be indeces into what would be the intermediate buffer.
            x = int(floor(playback_pointer))
            y = x + 1

            # Let omega, theta be the interpolation factors for the
            # interpolation step on what would be read from the intermediate.
            theta = playback_pointer - float(x)
            omega = 1.0 - theta

            # So, assuming an existing intermediate buffer, E, we could compute
            # Si = buf[i] = (omega * E[x]) + (theta * E[y])
            # We now derive E[x] and E[y] to avoid the intermediate buffer.

            # Remember from the StandardOscillator,
            # E[x] = (beta * table[a]) + (alpha * table[b])
            a = int(floor(table_rate * x))
            b = a + 1
            alpha = (table_rate * x) - float(a)
            beta = 1.0 - alpha
            a_wrapped = a & mask
            b_wrapped = b & mask
            ex = (beta * table[a_wrapped]) + (alpha * table[b_wrapped])

            # Now we need E[y], which we can derive the same way.
            _a = int(floor(table_rate * y))
            _b = (_a + 1)
            _alpha = (table_rate * y) - float(_a)
            _beta = 1.0 - _alpha
            _a_wrapped = _a & mask
            _b_wrapped = _b & mask
            ey = (_beta * table[_a_wrapped]) + (_alpha * table[_b_wrapped])

            # From above, we now compute Si
            si = (omega * ex) + (theta * ey)
            buf[i] += si * self.level


