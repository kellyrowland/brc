import matplotlib.pyplot as plt
import matplotlib.dates as dates

f = open('2014.txt')

views = []
vdates = []

for line in f.readlines():
	if u'/user-guide' in line:
		line = line.strip().split('\t')
		views.append(line[1])
		vdates.append(line[2])

f.close()

plot_dates = dates.datestr2num(vdates)

fig, ax = plt.subplots()
fig.autofmt_xdate()
ax.plot(plot_dates,views)

xfmt = dates.DateFormatter('%m-%d-%y')
ax.xaxis.set_major_formatter(xfmt)

plt.show()
