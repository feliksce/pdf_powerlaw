# converts data to [ms] and draws pdf function in comparison with ccdf function

import powerlaw
from matplotlib import pyplot as plt
from pandas import read_csv
import numpy as np

file_src = "./on_off_times/1.txt"
input_data = read_csv(file_src, header=None, sep="\t")

for type in ["ON", "OFF"]:
	if type == "ON":
		on = [x * 1000 for x in input_data[0]]
		data = on
	if type == "OFF":
		off = [x * 1000 for x in input_data[1]]
		data = off

	experimental = powerlaw.Fit(data, xmin=min(data))
	experimental.plot_ccdf(label=type)
	experimental.plot_pdf(label=type, ls="--")

plt.xlabel("t [ms]")
plt.ylabel("p(t), p(T≥t)")
plt.legend()
plt.show()
