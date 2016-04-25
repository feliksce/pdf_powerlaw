import powerlaw
from matplotlib import pyplot as plt
from pandas import read_csv
import numpy as np

file_src = "./on_off_times/1.txt"
input_data = read_csv(file_src, header=None, sep="\t")

for t in ["ON", "OFF"]:
	if t == "ON":
		data = input_data[0]
	if t == "OFF":
		data = input_data[1]

	experimental = powerlaw.Fit(data, xmin=min(data))
	experimental.plot_ccdf(label=t)

plt.legend()
plt.show()
