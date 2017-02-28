import numpy as np
import csv
import os
import matplotlib.pyplot as plt


def auto_correlation(data):
    n = len(data)
    x = np.array(data)
    x = x - x.mean()
    # Correlate using some convolution
    return np.correlate(x, x, mode='full')[-n:] / (x.var() * (np.arange(n, 0, -1)))


data_dir = 'pond'
taus = np.arange(0, 600, 0.1)

for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        data = np.loadtxt(os.path.join(subdir, file))
        Rs = auto_correlation(data)
        plt.plot(Rs[:100])
        print(sum(Rs[:100]))

# randoms = np.random.uniform(0., 1., size=10000)
# plt.plot(auto_correlation(randoms))
# print(sum(auto_correlation(randoms)[:-1000]))

# sins = np.sin(taus)
# sin_rs = auto_correlation(sins)
# plt.plot(taus, sin_rs)
# print(sum(sin_rs))


plt.show()
