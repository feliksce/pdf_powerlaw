# plots pdf 'by-hand'

import powerlaw
from matplotlib import pyplot as plt
from pandas import read_csv
import numpy as np
import math


file_src = "./on_off_times/1.txt"
input_data = read_csv(file_src, header=None, sep="\t")
data = [data * 1000 for data in input_data[1]]

experimental = powerlaw.Fit(data, xmin=min(data))
# experimental.plot_pdf()
# experimental.power_law.plot_pdf()
# experimental.truncated_power_law.plot_pdf()
pdf = experimental.pdf()

x = list(pdf[0])
bin_centers = [(x[n] + x[n+1]) / 2000 for n in range(len(x)-1)]
y = list(pdf[1])

for each in range(len(y)):
	print(bin_centers[each], y[each], sep="\t")

# del x[0], y[0]

# for i,j in zip(x, y):
#     plt.annotate('{:.1G})'.format(j), xy=(i,j), xytext=(50,0), textcoords='offset points')
#     plt.annotate('({:.1G},'.format(i), xy=(i,j))

plt.plot(bin_centers, y, "ro")
plt.loglog()
plt.show()
