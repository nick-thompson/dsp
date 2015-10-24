import matplotlib.pyplot as plt
import numpy as np

from math import floor
from wavetable.wavetable import table, gibbs_table
from wavetable.oscillators import StandardOscillator, ResamplingOscillator, RealTimeResamplingOscillator

def normalize(arr):
    """
    Normalize the values of the input array into the range [-1, 1].
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

# First, a comparison of the two wave tables. The first is our standard
# wavetable, the second uses sigma approximation to attenuate the Gibbs
# phenomenon.
x = np.linspace(0, 1, num=table.size, dtype='d')

plt.figure()
plt.subplot(121)
plt.plot(x, table)

plt.subplot(122)
plt.plot(x, gibbs_table)
plt.show()

# Next, we'll show the difference in the waveform produced by using resampling
# to apply detune when played next to a similar waveform vs. what I assume is
# the standard method of applying detune, as described in the oscillators file.
_x = np.linspace(0, 44100 * 4, 44100 * 4)

ss = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(ss)
StandardOscillator(43.65, 3.0, 0.5).render(ss)

rs = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(rs)
ResamplingOscillator(43.65, 3.0, 0.5).render(rs)

plt.plot(_x, normalize(trim(rs - ss, pow(2, 3 / 1200.0))))
plt.show()

# Now, to show that we can introduce the same artifacts in real time, we'll
# show that the output of the ResamplingOscillator and the
# RealTimeResamplingOscillator are actually the same.
rs = np.zeros(44100 * 4, dtype='d')
ResamplingOscillator(43.65, 3.0, 1.0).render(rs)

rt = np.zeros(44100 * 4, dtype='d')
RealTimeResamplingOscillator(43.65, 3.0, 1.0).render(rt)
trim(rt, pow(2, 3 / 1200.0))

assert np.allclose(rs, rt)
plt.plot(_x, rs - rt)
plt.show()
