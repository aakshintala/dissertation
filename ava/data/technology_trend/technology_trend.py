import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import rc

rc('text', usetex=True)
plt.rc('font', family='serif', size=6)

column_names=('Accelerators', 'Accelerator APIs', 'Hypervisor support')

data = np.genfromtxt('data.csv', delimiter=',', names=[''].append(column_names), skip_header=True)
data = np.array([list(row) for row in data])

x_label = [int(x) for x in data[:, 0]]
fig = plt.figure(figsize=(2.75, 1.3))
ax = plt.subplot(111)
colors = ('#1b9e77', '#d95f02', '#e41a1c', '#7570b3', '#984ea3', 'black')
markers = ('+', None, '^', 'x', None, None)
styles = ('solid', 'solid', 'solid', 'solid', 'dashed', 'dashdot')
for i in range(len(column_names)):
    if i != 3:
        plt.plot(x_label, data[:,i+1], color=colors[i], marker=markers[i], markersize=3, linestyle=styles[i], lw=1)

#plt.ylabel('Cumulative Number')
plt.xticks(x_label)
plt.xlim((2010, 2019))
plt.ylim((0, 60))

ax = plt.gca()
yticks = ax.yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#box = ax.get_position()
#ax.set_position([box.x0, box.y0 + box.height * 0.1,
#                 box.width, box.height * 0.9])
# Put a legend below current axis
plt.legend(column_names, loc='upper left', fancybox=True, shadow=False, ncol=1)

fig.tight_layout()
plt.gcf().set_size_inches(3, 1.2)
plt.savefig('technology_trend.pdf', dpi = 600, bbox_inches='tight', pad_inches=0)
plt.show()
