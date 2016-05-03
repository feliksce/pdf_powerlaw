# import qdpy
#
# file = "./on_off_times/1.txt"
#
# f = qdpy.QDPlot(file)
# for i in range(2):
# 	f.collect(i)
# 	f.fit("all")
# # f.collect("ON")
# # f.fit("all")

import qdpy
import os

for each in os.listdir("./on_off_times"):
	if each.endswith(".txt"):
		file_dir = "./on_off_times/{}".format(each)
		print("plotting data: {}".format(file_dir))
		f = qdpy.QDPlot(file_dir)
		f.collect("on")
		f.fit("all")
f.calculate_data()
print("Done.")
