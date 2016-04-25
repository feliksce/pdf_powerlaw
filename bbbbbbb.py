# plots pdf, cdf and ccdf alongside in one line, separately for on and off times

import powerlaw
from matplotlib import pyplot as plt
from pandas import read_csv
import numpy as np
import math


file_src = "./on_off_times/1.txt"
input_data = read_csv(file_src, header=None, sep="\t")

fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

title_flag = 0
titles = ["pdf", "cdf", "ccdf"]
ylabels = ["p(x)", "p(X<x)", "p(X≥x)"]

for type in ["ON"]:
	if type == "ON":
		on = [x * 1000 for x in input_data[0]]
		data = on
	if type == "OFF":
		off = [x * 1000 for x in input_data[1]]
		data = off

	# experimental data
	experimental = powerlaw.Fit(data, xmin=min(data))
	# probability functions plots
	experimental.plot_pdf(label="{} times".format(type.lower()), ls="-", ax=ax1)
	experimental.plot_cdf(label="{} times".format(type.lower()), ls="-", ax=ax2)
	experimental.plot_ccdf(label="{} times".format(type.lower()), ls="-", ax=ax3)
	# fits
	experimental.power_law.plot_pdf(label="power-law fit", ls="--", ax=ax1)
	experimental.power_law.plot_cdf(label="power-law fit", ls="--", ax=ax2)
	experimental.power_law.plot_ccdf(label="power-law fit", ls="--", ax=ax3)
	# parameters
	a = experimental.power_law.alpha
	# l = experimental.truncated_power_law.Lambda
	s = experimental.power_law.sigma

for each in [ax1, ax2, ax3]:
	handles, labels = each.get_legend_handles_labels()
	each.legend(handles, labels, loc="best")
	each.set_title(titles[title_flag])
	each.set_xlabel("x [s]")
	each.set_ylabel(ylabels[title_flag])

	labels = [str(int(math.log10(item / 1000))) for item in each.get_xticks().tolist()]
	labels = ["10$^\mathrm{" + entry + "}$" for entry in labels]
	each.set_xticklabels(labels)

	title_flag += 1

filename = file_src.split("/")[-1]
fig.suptitle("{}, a={:.4G}".format(filename, a))
plt.tight_layout()
plt.subplots_adjust(top=.85)
plt.show()
plt.clf()
title_flag = 0
