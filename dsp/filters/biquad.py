"""
Module defining various biquad filters.

This implementation follows the discussion presented by Robert Bristow-Johnson
in his "Cookbook formulae for audio EQ biquad filter coefficients" article
on MusicDSP.org: http://www.musicdsp.org/files/Audio-EQ-Cookbook.txt
"""

import matplotlib.pyplot as plt
import numpy as np

from scipy import signal
from wavetable.oscillators import StandardOscillator, RealTimeResamplingOscillator
from wavetable.wavetable import WaveType

class BiquadFilter(object):
    """
    Biquad filter base class.

    Handles most of the filter internals, but leaves computing the coefficients
    to the subclass constructors.
    """

    def __init__(self, b0, b1, b2, a0, a1, a2):
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2

        # Zero pad the initial input and output buffers. The filter will be in
        # its transient state for 2 samples before reaching steady state.
        self._x = np.zeros(2)
        self._y = np.zeros(2)

    def process_block(self, input_buffer, output_buffer):
        _len = input_buffer.size
        _x = np.concatenate((self._x, input_buffer))
        _y = np.concatenate((self._y, output_buffer))

        for i in range(2, _len):
            sample = (self.b0 / self.a0) * _x[i]     \
                   + (self.b1 / self.a0) * _x[i - 1] \
                   + (self.b2 / self.a0) * _x[i - 2] \
                   - (self.a1 / self.a0) * _y[i - 1] \
                   - (self.a2 / self.a0) * _y[i - 2]

            _y[i] = sample

        np.copyto(output_buffer, _y[2:])
        self._x = input_buffer[-2:]
        self._y = output_buffer[-2:]

    def plot(self, ax1, ax2, color='c', alpha=1.0):
        w, h = signal.freqz([self.b0, self.b1, self.b2],
                [self.a0, self.a1, self.a2])

        # Scale x-axis to Hz.
        x = w * 44100 / (2 * np.pi)

        # Plot amplitude response on the dB scale.
        ax1.plot(x,  20 * np.log10(abs(h)), color=color, alpha=alpha)

        # Plot phase response in radians.
        ax2.plot(x, np.unwrap(np.angle(h)), color=color, alpha=alpha)

        ax1.set_title('Amplitude Response (dB)')
        ax2.set_title('Phase Response (radians)')

        ax2.set_yticks(np.linspace(-2.0, 0.0, 9) * np.pi)
        ax2.set_yticklabels([
            r'$-2\pi$',
            r'',
            r'$-\frac{3\pi}{2}$',
            r'',
            r'$-\pi$',
            r'',
            r'$-\frac{\pi}{2}$',
            r'',
            r'$0$'])

        ax1.axis('tight')
        ax2.axis('tight')

        ax1.grid()
        ax2.grid()


class AllpassFilter(BiquadFilter):
    """
    Allpass filter implementation.
    H(s) = (s^2 - s/Q + 1) / (s^2 + s/Q + 1)

    Parameters:
    fs : Sampling frequency.
    f0 : Center frequency; sets the phase crossing (where the phase response
         crosses -pi) at f0.
    Q : Quality; input should be a positive number, with numbers smaller than
        1.0 greatly reducing the slope of the phase response, and numbers
        greater than one creating a sharp cliff at f0.
    """

    def __init__(self, fs, f0, Q):
        w0 = 2 * np.pi * f0 / fs
        alpha = np.sin(w0) / (2 * Q)

        b0 = 1. - alpha
        b1 = -2. * np.cos(w0)
        b2 = 1. + alpha
        a0 = 1. + alpha
        a1 = -2. * np.cos(w0)
        a2 = 1. - alpha

        super(AllpassFilter, self).__init__(b0, b1, b2, a0, a1, a2)


if __name__ == '__main__':
    # Show the frequency response as we move the cutoff frequency.
    _, (ax1, ax2) = plt.subplots(2, sharex=True)

    for i in range(220, 22000, 4000):
        apf = AllpassFilter(44100, i, 1.0)
        apf.plot(ax1, ax2, 'c', float(i) / 22000)

    plt.show()

    # Show the frequency response as we move the Q factor.
    _, (ax1, ax2) = plt.subplots(2, sharex=True)

    for i in np.linspace(0.2, 2.0, 5):
        apf = AllpassFilter(44100, 8220, i)
        apf.plot(ax1, ax2, 'c', float(i) / 2.0)

    plt.show()

    # Now we'll take a look at how this allpass filter affects the waveform
    # of an input signal so we can compare it with how the drop-sample
    # interpolation filter of the ResamplingOscillator.
    fs = 44100
    duration = 1
    size = fs * duration

    x = np.linspace(0, size, size)

    ss = np.zeros(size, dtype='d')
    StandardOscillator(WaveType.SAWTOOTH, 43.65, 3.0, 1.0).render(ss)

    rs = np.zeros(size, dtype='d')
    RealTimeResamplingOscillator(WaveType.SAWTOOTH, 43.65, 3.0, 1.0).render(rs)

    ap = np.zeros(size, dtype='d')
    apf = AllpassFilter(44100, 18000, 0.1)
    apf.process_block(ss, ap)

    plt.figure()
    plt.subplot(211)
    plt.plot(x, rs - ss)

    plt.subplot(212)
    plt.plot(x, ap - ss)

    plt.show()
