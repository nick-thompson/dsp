import numpy as np

from wavetable.oscillators import StandardOscillator
from scipy.io import wavfile

standard_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 1.0).render(standard_output)
wavfile.write('sounds/standard.wav', 44100, standard_output)

detuned_output = np.zeros(44100 * 4, dtype='d')
StandardOscillator(43.65, 0.0, 0.5).render(detuned_output)
StandardOscillator(43.65, 3.0, 0.5).render(detuned_output)
wavfile.write('sounds/detuned_standard.wav', 44100, detuned_output)
