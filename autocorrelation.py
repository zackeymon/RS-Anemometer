"""
Zack Xiang & Isaac Scott
Auto-correlation and S calculation
"""

import numpy as np
import os
import matplotlib.pyplot as plt


def stop_if_below_zero(sequence):
    for i, val in enumerate(sequence):
        if val <= 0:
            return sequence[:i]
    return sequence


def auto_correlation(data):
    n = len(data)
    x = np.array(data)
    x = x - x.mean()
    return np.correlate(x, x, mode='full')[-n:] / (x.var() * (np.arange(n, 0, -1)))


# The directory contains all the measurement data that require auto-correlation analysis
data_dir = 'grass'
labels = ('Adam', 'Brian', 'Camilla')

for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        data = np.loadtxt(os.path.join(subdir, file))
        Rs = stop_if_below_zero(auto_correlation(data))
        plt.plot(Rs, label=file)
        print(sum(Rs))

plt.legend(loc=0)
plt.xlabel(r'$\tau (s)$')
plt.ylabel(r'$R(\tau)$')
plt.show()
