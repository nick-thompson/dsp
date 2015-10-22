import numpy as np

from math import floor
from wavetable.oscillators import StandardOscillator, ResamplingOscillator, RealTimeResamplingOscillator
from scipy.io import wavfile

standard_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 1.0).render(standard_output)
wavfile.write('sounds/standard.wav', 44100, standard_output)

detuned_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(detuned_output)
StandardOscillator(43.65, 3.0, 0.5).render(detuned_output)
wavfile.write('sounds/detuned_standard.wav', 44100, detuned_output)

detuned_resampling_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(detuned_resampling_output)
ResamplingOscillator(43.65, 3.0, 0.5).render(detuned_resampling_output)
wavfile.write('sounds/detuned_resampling.wav', 44100, detuned_resampling_output)

diff = detuned_resampling_output - detuned_output

# Clean out the diff
playback_rate = pow(2, 3 / 1200.0)
last_good_sample = floor(diff.size / playback_rate)
diff[last_good_sample:] = 0.0

# Normalize
diff /= np.max(np.abs(diff), axis=0)
wavfile.write('sounds/standard_resampling_diff.wav', 44100, diff)

# Real time resampling
rt_resampling_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(rt_resampling_output)
RealTimeResamplingOscillator(43.65, 3.0, 0.5).render(rt_resampling_output)
wavfile.write('sounds/realtime_resampling.wav', 44100, rt_resampling_output)
