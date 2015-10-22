import matplotlib.pyplot as plt
import numpy as np

from math import floor
from wavetable.wavetable import table, gibbs_table
from wavetable.oscillators import StandardOscillator, ResamplingOscillator, RealTimeResamplingOscillator

x = np.linspace(0, 1, num=table.size, dtype='d')

# Our standard wavetable
plt.plot(x, table)
plt.show()

# The Gibbs-savvy table
plt.plot(x, gibbs_table)
plt.show()

# Visualize the difference from the resampling detune vs. the standard detune.
detuned_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(detuned_output)
StandardOscillator(43.65, 3.0, 0.5).render(detuned_output)

detuned_resampling_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(detuned_resampling_output)
ResamplingOscillator(43.65, 3.0, 0.5).render(detuned_resampling_output)

diff = detuned_resampling_output - detuned_output

# Clean out the diff
playback_rate = pow(2, 3 / 1200.0)
last_good_sample = floor(diff.size / playback_rate)
diff[last_good_sample:] = 0.0

# Normalize
diff /= np.max(np.abs(diff), axis=0)

plt.plot(np.linspace(0, diff.size, diff.size), diff)
plt.show()

rt_resampling_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(rt_resampling_output)
RealTimeResamplingOscillator(43.65, 3.0, 0.5).render(rt_resampling_output)
plt.plot(np.linspace(0, rt_resampling_output.size, rt_resampling_output.size),
        rt_resampling_output)
plt.show()
