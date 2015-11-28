import matplotlib.pyplot as plt
import numpy as np

from scipy import signal

f, (ax1, ax2) = plt.subplots(2, sharex=True)

for i in np.linspace(0.0, 1.0, 11):
    # A linear interpolation filter with a factor of `i`.
    w, h = signal.freqz([(1.0 - i), i])

    # Scale x-axis to Hz.
    x = w * 44100 / (2 * np.pi)

    # Plot amplitude response on the dB scale.
    ax1.plot(x,  20 * np.log10(abs(h)), color='c', alpha=1.0 - i)

    # Plot phase response in radians.
    ax2.plot(x, np.unwrap(np.angle(h)), color='c', alpha=1.0 - i)

ax1.set_title('Amplitude Response (dB)')
ax2.set_title('Phase Response (radians)')

ax2.set_yticks(np.linspace(-1.0, 0.0, 5) * np.pi)
ax2.set_yticklabels([r'$-\pi$', r'$-\frac{3\pi}{4}$', r'$-\frac{\pi}{2}$',
    r'$-\frac{\pi}{4}$', r'$0$'])

ax1.axis('tight')
ax2.axis('tight')

ax1.grid()
ax2.grid()

plt.show()
