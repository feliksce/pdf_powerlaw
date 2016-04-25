# finds dirs with on/off times and makes pdf cdf and ccdf plots

from plot_alongside import Draw
import os

input_path = "."
file_cwd = set()

for dir_name, subdir_list, file_list in os.walk(input_path):
	for filename in file_list:
		if filename.endswith(".txt"):
			file_cwd.add(dir_name)
		else:
			continue

for file_path in file_cwd:
	for each in os.listdir(file_path):
		if each.endswith("thresh-1.txt"):
			output = file_path + "/out"
			if not os.path.exists(output):
				os.mkdir(output)
			src = file_path + "/" + each
			f = Draw(src)
			print("Plotting: {}".format(src))
			print("\tpl...")
			f.plot(output_dir=output)
			print("\ttpl...")
			f.plot(output_dir=output, distribution="tpl")
