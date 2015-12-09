import matplotlib.pyplot as plt
import numpy as np

from math import floor
from wavetable.oscillators import StandardOscillator, ResamplingOscillator, RealTimeResamplingOscillator
from wavetable.utils import normalize, trim
from wavetable.wavetable import WaveType

# Next, we'll show the difference in the waveform produced by using resampling
# to apply detune when played next to a similar waveform vs. what I assume is
# the standard method of applying detune, as described in the oscillators file.
_x = np.linspace(0, 44100 * 4, 44100 * 4)

ss = np.zeros(44100 * 4, dtype='d')
StandardOscillator(WaveType.SAWTOOTH, 43.65, 0.0, 0.5).render(ss)
StandardOscillator(WaveType.SAWTOOTH, 43.65, 3.0, 0.5).render(ss)

rs = np.zeros(44100 * 4, dtype='d')
StandardOscillator(WaveType.SAWTOOTH, 43.65, 0.0, 0.5).render(rs)
ResamplingOscillator(WaveType.SAWTOOTH, 43.65, 3.0, 0.5).render(rs)

plt.plot(_x, normalize(trim(rs - ss, pow(2, 3 / 1200.0))))
plt.show()

# Now, to show that we can introduce the same artifacts in real time, we'll
# show that the output of the ResamplingOscillator and the
# RealTimeResamplingOscillator are actually the same.
rs = np.zeros(44100 * 4, dtype='d')
ResamplingOscillator(WaveType.SAWTOOTH, 43.65, 3.0, 1.0).render(rs)

rt = np.zeros(44100 * 4, dtype='d')
RealTimeResamplingOscillator(WaveType.SAWTOOTH, 43.65, 3.0, 1.0).render(rt)
trim(rt, pow(2, 3 / 1200.0))

assert np.allclose(rs, rt)
plt.plot(_x, rs - rt)
plt.show()
