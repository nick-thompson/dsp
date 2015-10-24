"""
Module for generating band-limited sawtooth wavetables.

For the sake of this project, we're looking only at the results in the low
end of the frequency spectrum. Our oscillators will be used to produce bass
notes near F1, or 43.65Hz. Thus only one band-limited wavetable should suffice
for the note ranges we're interested in.

To be safe, we'll assume our oscillators won't produce frequencies higher than
50Hz. At 50Hz, 441 harmonics can be drawn before aliasing occurs. Thus we build
one wavetable of size 1024 sample frames with 441 harmonics here via additive
synthesis. We'll build another, almost identical, wavetable which applies a
slight dampening to the partials to attenuate the Gibbs phenomenon.
"""

import numpy as np

from utils import normalize

TABLE_SIZE = 1024

_t = np.linspace(0, 1, num=TABLE_SIZE, dtype='d')
_num_harmonics = 441

_table = np.zeros(TABLE_SIZE, dtype='d')
_gibbs_table = np.zeros(TABLE_SIZE, dtype='d')

# Fill the wavetables via additive synthesis
for k in range(1, _num_harmonics + 1):
    _table -= np.sin(2 * np.pi * k * _t) / (k * np.pi)

    # Dampen the kth partial in the _gibbs_table using the Lanczos sigma factor.
    sigma = np.sinc(k * np.pi / (2 * _num_harmonics))
    _gibbs_table -= np.sin(2 * np.pi * k * _t) / (k * np.pi) * sigma

normalize(_table)
normalize(_gibbs_table)

def shape(x):
    k = 2 * 0.8 / (1.0 - 0.8)
    return (1.0 + k) * x / (1.0 + k * abs(x))

def get(i, gibbs=False):
    if gibbs:
        return shape(_gibbs_table[i])
    return shape(_table[i])
