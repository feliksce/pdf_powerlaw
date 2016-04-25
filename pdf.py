import powerlaw
from matplotlib import pyplot as plt
from pandas import read_csv
import numpy as np

file_src = "./on_off_times/1.txt"
input_data = read_csv(file_src, header=None, sep="\t")

for type in ["ON", "OFF"]:
	if type == "ON":
		data = input_data[0]
	if type == "OFF":
		data = input_data[1]

	# data binning
	d = {}
	for number in data:
		if number not in d.keys():
			d[number] = 1
		else:
			d[number] += 1

	x = []
	y = []

	for key, val in sorted(d.items()):
		print("{:.03f}\t{}".format(key, val))
		x.append(key)
		y.append(val)

	experimental = powerlaw.Fit(data, xmin=min(data), discrete=True)
	experimental.plot_ccdf()


	# plt.plot(x, y, "bo")
	plt.loglog()
	plt.title(type)
	plt.suptitle(file_src)
	plt.show()


	# experimental = powerlaw.Fit(data, xmin=min(data))

	# # check for output data from pdf
	# pdf = experimental.pdf()
	# cdf = experimental.cdf()
	# ccdf = experimental.ccdf()
	# print(type)
	# print("data", data)
	# print("pdf", pdf)
	# print("cdf", cdf)
	# print("ccdf", ccdf)


	# fig1 = experimental.plot_ccdf(label="ccdf {}".format(type.lower()))
	# fig2 = experimental.plot_pdf(label="pdf {}".format(type.lower()))

# plt.legend()
# # plt.xlim([min(data), max(data)])
# # plt.ylim([min(data), max(data)])
# plt.show()
