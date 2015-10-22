import matplotlib.pyplot as plt
import numpy as np

from math import floor
from wavetable.wavetable import table, gibbs_table
from wavetable.oscillators import StandardOscillator, ResamplingOscillator, RealTimeResamplingOscillator

def make_diff(a, b, trim, normalize=True):
    """
    Calculate and normalize the difference between two audio buffers.

    The `trim` argument specifies what amount of the tail end of the diff
    to zero out before normalizing.
    """
    _diff = a - b
    if trim > 0:
        n = floor(_diff.size / trim)
        _diff[n:] = 0.0

    if normalize:
        _diff /= np.max(np.abs(_diff), axis=0)
    return _diff

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

# Next, we'll take a look at the difference in the waveform produced by using
# resampling to apply the detune parameter.
_x = np.linspace(0, 44100 * 4, 44100 * 4)

detuned_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(detuned_output)
StandardOscillator(43.65, 3.0, 0.5).render(detuned_output)

detuned_resampling_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(detuned_resampling_output)
ResamplingOscillator(43.65, 3.0, 0.5).render(detuned_resampling_output)

_a = make_diff(detuned_resampling_output, detuned_output, pow(2, 3 / 1200.0))

plt.plot(_x, _a)
plt.show()

# Now, we'll look at the same difference but this time using the real time
# resampling oscillator. In theory the result should be the same.
rt_resampling_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(rt_resampling_output)
RealTimeResamplingOscillator(43.65, 3.0, 0.5).render(rt_resampling_output)

_b = make_diff(rt_resampling_output, detuned_output, 0)

plt.plot(_x, _b)
plt.show()

# Now to show whether the differences are in fact the same, we plot the
# difference between the two diff arrays.
_c = make_diff(_a, _b, pow(2, 3 / 1200.0), normalize=False)

# Interesting numbers here... I'm guessing floating point rounding error? But
# the upwards trend on the graph suggests something could be going wrong in
# the real time algorithm.
print np.sum(_c)
print np.sum(_c) / _c.size

plt.plot(_x, _c)
plt.show()
