# plots pdf, cdf and ccdf alongside in one line
import powerlaw
from matplotlib import pyplot as plt
from pandas import read_csv
from numpy import mean, std, median
import math
import sys
import os


class QDPlot:
	# TODO add verbose
	# TODO add argparse
	# TODO save figures
	# TODO save parameters in a file
	# TODO calculate parameters averages and store them in data

	def __init__(self, input_data):
		# TODO add try
		self.input_data = read_csv(input_data, header=None, sep="\t")
		self.directory = os.path.dirname(input_data)
		self.filename = input_data.split("/")[-1]
		self.experimental = None
		self.events = None
		self.ax1 = None
		self.ax2 = None
		self.ax3 = None
		self.distribution = None
		self.data_output = None

	# a must be 0 for ON and 1 for OFF
	def collect(self, events):
		self.events = events.lower() if not str(events).isdigit() else "on" if events == 0 else "off"
		i = 0 if events in ("on", "ON", "On", 0) else 1 if events in ("off", "Off", "OFF", 1) else print("Dupa")
		data = [x * 1000 for x in self.input_data[i]]
		# create object with data
		# TODO throws exception 'ValueError: No columns to parse from file' while grabbing non valid file
		experimental = powerlaw.Fit(data, xmin=min(data))
		# TODO add color
		self.experimental = experimental
		return experimental

	# double underscore means class private
	# functions to plot
	def __pdf(self):
		points = self.experimental.pdf()
		x = list(points[0])
		bin_centers = [(x[n] + x[n + 1]) / 2 for n in range(len(x) - 1)]
		x = bin_centers
		y = list(points[1])
		y = [each if each != 0 else None for each in y]
		return x, y

	def __cdf(self):
		points = self.experimental.ccdf()
		x = [x for x in points[0]]
		y = [1 - y for y in points[1]]
		return x, y

	def __ccdf(self):
		points = self.experimental.ccdf()
		x = [x for x in points[0]]
		y = [y for y in points[1]]
		return x, y

	def plot(self):
		# TODO implement created functions which plot independently
		fig = plt.figure(figsize=(15, 5))
		# plot pdf
		self.ax1 = fig.add_subplot(131)
		x, y = self.__pdf()
		self.ax1.plot(x, y, "b.", label="pdf")
		# plot cdf
		self.ax2 = fig.add_subplot(132)
		x, y = self.__cdf()
		self.ax2.plot(x, y, "b.", label="cdf")
		# plot ccdf
		self.ax3 = fig.add_subplot(133)
		x, y = self.__ccdf()
		self.ax3.plot(x, y, "b.", label="ccdf")

	# TODO maybe rename fit_all and then add different functions for pdf, cdf and ccdf?
	def fit(self, distribution, save=True, show=False):
		self.distribution = distribution
		self.plot()
		ls = "--"

		def pl():
			color = "green"
			a = pl_a()
			self.experimental.power_law.plot_pdf(ax=self.ax1, label="pl\na={0:.4G}".format(a), ls=ls, color=color)
			self.experimental.power_law.plot_cdf(ax=self.ax2, label="pl", ls=ls, color=color)
			self.experimental.power_law.plot_ccdf(ax=self.ax3, label="pl", ls=ls, color=color)

		def pl_a():
			a = self.experimental.power_law.alpha
			return a

		def tpl():
			color = "red"
			a = tpl_a()
			l = tpl_l()
			self.experimental.truncated_power_law.plot_pdf(ax=self.ax1,
			    label="tpl\na={0:.4G}\nL={1:.4G}".format(a, l),
			    ls=ls, color=color)
			self.experimental.truncated_power_law.plot_cdf(ax=self.ax2, label="tpl", ls=ls, color=color)
			self.experimental.truncated_power_law.plot_ccdf(ax=self.ax3, label="tpl", ls=ls, color=color)

		def tpl_a():
			a = self.experimental.truncated_power_law.alpha
			return a

		def tpl_l():
			l = self.experimental.truncated_power_law.Lambda
			return l

		# TODO add __save_data to each group
		if distribution == "none":
			distribution = None
			pass
		elif distribution == "pl":
			pl()
			a = pl_a()
			self.__save_data(self.filename, self.distribution, a)
		elif distribution == "tpl":
			tpl()
			a = tpl_a()
			l = tpl_l()
			self.__save_data(self.filename, self.distribution, a, l)
		elif distribution == "all":
			distribution = "pl + tpl"
			pl()
			a = pl_a()
			self.__save_data(self.filename, "pl", a)
			tpl()
			a = tpl_a()
			l = tpl_l()
			self.__save_data(self.filename, "tpl", a, l)
		else:
			print("No distribution chosen. [pl/tpl/all/none]", file=sys.stderr)
			exit()

		title_flag = 0
		titles = ["pdf", "cdf", "ccdf"]
		ylabels = ["p(x)", "p(X<x)", "p(X≥x)"]

		for each in [self.ax1, self.ax2, self.ax3]:
			handles, labels = each.get_legend_handles_labels()
			each.legend(handles, labels, loc="best")
			each.set_title(titles[title_flag])
			each.set_xlabel("x [s]")
			each.set_ylabel(ylabels[title_flag])

			labels = [str(int(math.log10(item / 1000))) for item in each.get_xticks().tolist()]
			labels = ["10$^\mathrm{" + entry + "}$" for entry in labels]
			each.set_xticklabels(labels)

			title_flag += 1

		plt.suptitle("name: {}, events: {}, fit: {}".format(self.filename, self.events, distribution))
		plt.tight_layout()
		plt.subplots_adjust(top=.85)
		if save:
			self.__save_plot()
		if show:
			plt.show()

	# TODO ask if want ot overwrite?
	def __save_plot(self):
		filename = self.filename[:-4] if self.filename[-4] == "." else self.filename
		plot_name = "{}_{}_{}".format(filename, self.events, self.distribution)
		save_dir = "{}/fit_out".format(self.directory)
		full_path = "{}/fit_out/{}.png".format(self.directory, plot_name)
		if not os.path.exists(save_dir):
			os.mkdir(save_dir)
		plt.savefig(full_path)

	# functions for statistics and saving output data
	def __save_data(self, filename, distribution, a=None, l=None):
		save_dir = "{}/data_out".format(self.directory)
		output = "{}_data.txt".format(distribution.lower())
		full_path = "{}/{}".format(save_dir, output)
		self.data_output = save_dir
		if not os.path.exists(save_dir):
			os.mkdir(save_dir)

		with open(full_path, "a+") as f:
			if l:
				f.write("{}\t{}\t{}\n".format(filename, a, l))
			else:
				f.write("{}\t{}\n".format(filename, a))
		f.close()

	def calculate_data(self):
		pl_file = "{}/pl_data.txt".format(self.data_output)
		tpl_file = "{}/tpl_data.txt".format(self.data_output)
		if os.path.exists(pl_file):
			column = read_csv(pl_file, header=None, sep="\t")
			print("pl")
			print("mean\t{}\nstdev\t{}\nmedian\t{}\n".format(
				mean(column[1]), std(column[1]), median(column[1])
			))
			with open(pl_file, "a") as f:
				f.write("mean\t{}\nstdev\t{}\nmedian\t{}\n".format(
					mean(column[1]), std(column[1]), median(column[1])
				))
			f.close()
		if os.path.exists(tpl_file):
			column = read_csv(tpl_file, header=None, sep="\t")
			print("tpl")
			print("mean\t{}\t{}\nstdev\t{}\t{}\nmedian\t{}\t{}\n".format(
				mean(column[1]), mean(column[2]),
				std(column[1]), std(column[2]),
				median(column[1]), median(column[2]),
			))
			with open(tpl_file, "a") as f:
				f.write("mean\t{}\t{}\nstdev\t{}\t{}\nmedian\t{}\t{}\n".format(
					mean(column[1]), mean(column[2]),
					std(column[1]), std(column[2]),
					median(column[1]), median(column[2]),
				))
			f.close()


def main(*args):
	for each in args:
		if each.endswith(".txt"):
			file_dir = each
			print("plotting data: {}".format(file_dir))
			f = QDPlot(file_dir)
			f.collect("on")
			f.fit("all")


if __name__ == "__main__":
	main(sys.argv[1:])
