# plots pdf, cdf and ccdf alongside in one line
import powerlaw
from matplotlib import pyplot as plt
from pandas import read_csv
from numpy import mean, std
import math
import sys


class QDPlot:
	# TODO add verbose
	# TODO add argparse
	# TODO save figures
	# TODO save parameters in a file
	# TODO calculate parameters averages and store them in data

	def __init__(self, input_data):
		# TODO add try
		self.input_data = read_csv(input_data, header=None, sep="\t")
		self.filename = input_data.split("/")[-1]
		self.experimental = None
		self.events = None

	# a must be 0 for ON and 1 for OFF
	# TODO change 0 and 1 for more legible text
	def collect(self, events):
		self.events = events.lower() if not str(events).isdigit() else "on" if events == 0 else "off"
		i = 0 if events in ("on", "ON", "On", 0) else 1 if events in ("off", "Off", "OFF", 1) else print("Dupa")
		data = [x * 1000 for x in self.input_data[i]]
		# create object with data
		experimental = powerlaw.Fit(data, xmin=min(data))
		# TODO add color
		self.experimental = experimental
		return experimental

	# double underscore means class private
	def __plot(self):
		# TODO implement created functions which plot independently
		fig = plt.figure(figsize=(15, 5))
		self.ax1 = fig.add_subplot(131)
		self.ax2 = fig.add_subplot(132)
		self.ax3 = fig.add_subplot(133)
		self.experimental.plot_pdf(ax=self.ax1, label="pdf")
		self.experimental.plot_cdf(ax=self.ax2, label="cdf")
		self.experimental.plot_ccdf(ax=self.ax3, label="ccdf")

	# TODO maybe rename fit_all and then add different functions for pdf, cdf and ccdf?
	def fit(self, distribution):
		self.__plot()
		ls = "--"

		def pl():
			a = self.experimental.power_law.alpha
			self.experimental.power_law.plot_pdf(ax=self.ax1, label="pl\na={0:.4G}".format(a), ls=ls)
			self.experimental.power_law.plot_cdf(ax=self.ax2, label="pl", ls=ls)
			self.experimental.power_law.plot_ccdf(ax=self.ax3, label="pl", ls=ls)

		def tpl():
			a = self.experimental.truncated_power_law.alpha
			l = self.experimental.truncated_power_law.Lambda
			self.experimental.truncated_power_law.plot_pdf(ax=self.ax1,
			    label="tpl\na={0:.4G}\nL={1:.4G}".format(a, l),
			    ls=ls)
			self.experimental.truncated_power_law.plot_cdf(ax=self.ax2, label="tpl", ls=ls)
			self.experimental.truncated_power_law.plot_ccdf(ax=self.ax3, label="tpl", ls=ls)

		if distribution == "none":
			distribution = None
			pass
		elif distribution == "pl":
			pl()
		elif distribution == "tpl":
			tpl()
		elif distribution == "all":
			distribution = "pl + tpl"
			pl()
			tpl()
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

		# TODO ask if show?
		plt.suptitle("name: {}, events: {}, fit: {}".format(self.filename, self.events, distribution))
		plt.tight_layout()
		plt.subplots_adjust(top=.85)
		plt.show()


file = "./on_off_times/1.txt"

f = QDPlot(file)
for i in range(2):
	f.collect(i)
	for t in ["pl", "tpl"]:
		f.fit("all")
# f.collect(0)
# f.fit("all")

#
# class Draw:
#
# 	def __init__(self, file_src):
# 		self.file_src = file_src
# 		self.output_dir = ""
# 		self.pl = []
# 		self.tpl_a = []
# 		self.tpl_l = []
#
# 	def plot(self, output_dir=".", show=False, distribution="pl"):
# 		if distribution not in ["pl", "tpl"]:
# 			raise NameError
# 		input_data = read_csv(self.file_src, header=None, sep="\t")
#
# 		fig = plt.figure(figsize=(15, 5))
# 		ax1 = fig.add_subplot(131)
# 		ax2 = fig.add_subplot(132)
#
# 		ax3 = fig.add_subplot(133)
#
# 		for type in ["ON", "OFF"]:
# 			if type == "ON":
# 				on = [x * 1000 for x in input_data[0]]
# 				data = on
# 				color = "red"
# 			if type == "OFF":
# 				off = [x * 1000 for x in input_data[1]]
# 				data = off
# 				color = "blue"
#
# 			# experimental data
# 			experimental = powerlaw.Fit(data, xmin=min(data))
# 			# probability functions plots
# 			experimental.plot_pdf(label=type.lower(), ls="-", ax=ax1, color=color)
# 			experimental.plot_cdf(label=type.lower(), ls="-", ax=ax2, color=color)
# 			experimental.plot_ccdf(label=type.lower(), ls="-", ax=ax3, color=color)
# 			# fits
# 			if distribution == "pl":
# 				experimental.power_law.plot_pdf(label="pl fit".format(distribution), ls="--", ax=ax1, color=color)
# 				experimental.power_law.plot_cdf(label="pl fit", ls="--", ax=ax2, color=color)
# 				experimental.power_law.plot_ccdf(label="pl fit", ls="--", ax=ax3, color=color)
# 			if distribution == "tpl":
# 				experimental.truncated_power_law.plot_pdf(label="tpl fit", ls="--", ax=ax1, color=color)
# 				experimental.truncated_power_law.plot_cdf(label="tpl fit", ls="--", ax=ax2, color=color)
# 				experimental.truncated_power_law.plot_ccdf(label="tpl fit", ls="--", ax=ax3, color=color)
#
# 			# parameters
# 			if distribution == "pl":
# 				alpha = experimental.power_law.alpha
# 				self.pl.append(alpha)
#
# 			if distribution == "tpl":
# 				alpha = experimental.truncated_power_law.alpha
# 				lam = experimental.truncated_power_law.Lambda
# 				self.tpl_a.append(alpha)
# 				self.tpl_l.append(lam)
#
# 		title_flag = 0
# 		titles = ["pdf", "cdf", "ccdf"]
# 		ylabels = ["p(x)", "p(X<x)", "p(X≥x)"]
#
# 		for each in [ax1, ax2, ax3]:
# 			handles, labels = each.get_legend_handles_labels()
# 			each.legend(handles, labels, loc="best")
# 			each.set_title(titles[title_flag])
# 			each.set_xlabel("x [s]")
# 			each.set_ylabel(ylabels[title_flag])
#
# 			labels = [str(int(math.log10(item / 1000))) for item in each.get_xticks().tolist()]
# 			labels = ["10$^\mathrm{" + entry + "}$" for entry in labels]
# 			each.set_xticklabels(labels)
#
# 			title_flag += 1
#
# 		filename = self.file_src.split("/")[-1]
# 		if distribution == "pl":
# 			fig.suptitle("{}: {}, alpha = {:.4G}".format(distribution, filename, alpha))
# 		if distribution == "tpl":
# 			fig.suptitle("{}: {}, alpha = {:.4G}, lambda = {:.4G}".format(distribution, filename, alpha, lam))
# 		plt.tight_layout()
# 		plt.subplots_adjust(top=.85)
# 		plt.savefig("{}/{}_{}".format(output_dir, filename[:-4], distribution))
# 		if show:
# 			plt.show()
# 		plt.clf()
#
# 		if distribution == "pl":
# 			with open("{}/out_data_pl.txt".format(output_dir), "a") as f:
# 				f.write("{}\t{}\t{}\n".format(filename[:-4], distribution, alpha))
# 				f.close()
# 		if distribution == "tpl":
# 			with open("{}/out_data_tpl.txt".format(output_dir), "a") as f:
# 				f.write("{}\t{}\t{}\t{}\n".format(filename[:-4], distribution, alpha, lam))
# 				f.close()
#
# 	def calculate_average(self):
# 		pl_a_avg = mean(self.pl)
# 		tpl_a_avg = mean(self.tpl_a)
# 		tpl_l_avg = mean(self.tpl_l)
#
# 		pl_a_std = std(self.pl)
# 		tpl_a_std = std(self.tpl_a)
# 		tpl_l_std = std(self.tpl_l)
#
# 		with open("{}/out_data_pl.txt".format(self.output_dir), "a") as f:
# 			f.write("average\tpl\t{}\t{}\n".format(pl_a_avg, pl_a_std))
# 		with open("{}/out_data_tpl.txt".format(self.output_dir), "a") as f:
# 			f.write("average\ttpl\t{}\t{}\t{}\t{}\n".format(tpl_a_avg, tpl_a_std, tpl_l_avg, tpl_l_std))
