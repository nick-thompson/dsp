import matplotlib.pyplot as plt
import numpy as np

from wavetable.wavetable import table, gibbs_table

x = np.linspace(0, 1, num=table.size, dtype='d')

plt.plot(x, table)
plt.show()

plt.plot(x, gibbs_table)
plt.show()
