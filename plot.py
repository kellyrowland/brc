import matplotlib.pyplot as plt
import matplotlib.dates as dates

f = open('2014-2015.txt')

views = []
vdates = []
total_list = []

for line in f.readlines():
	line = line.strip().split('\t')
	total_list.append((line[0],line[1],line[2]))

f.close()

pages = set(i[0] for i in total_list)

for page in pages:
	views = []
	vdates = []
	for i in total_list:
		if page == i[0]:
			views.append(i[1])
			vdates.append(i[2])
	plot_dates = dates.datestr2num(vdates)

	fig, ax = plt.subplots()
	fig.autofmt_xdate()
	ax.plot(plot_dates,views)

	xfmt = dates.DateFormatter('%m-%d-%y')
	ax.xaxis.set_major_formatter(xfmt)

	pagename = page.translate(None, '/') # remove leading forward slash
	fig.savefig(str(pagename))
	plt.close(fig)
