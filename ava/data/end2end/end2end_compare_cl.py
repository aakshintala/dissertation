import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple

rc('text', usetex=True)
plt.rc('font', family='serif', size=16)

# OpenCL
h1 = (1.159874608, 1.085585586, 1.162793572, 1.362833531, 1.177246827, 1.24071991, 1.236181818, 1.077955791, 1.024690883, 1.004429644, 2.459387807, 1.056853436, 1.067269823, 1.165820515, 1.057284462)
h2 = (1.066877743, 1.043544144, 1.147843386, 1.129205047, 1.09167842, 1.14904387, 1.104278075, 1.0541351, 1.003917379, 0.9988066826, 2.477737502, 1.030100294, 1.020698049, 1.106554586, 1.056580075)
h3 = (1.059561129, 1.022522523, 1.128240702, 1.090265551, 1.02867701, 1.146044994, 1.088235294, 1.05099608, 0.9953703704, 1.00052481, 2.043501774, 1.020066863, 1.018110211, 1.076289845, 1.021216467)
label = ('backprop', 'bfs', 'b+tree', 'dwt2d', 'gaussian', 'heartwall', 'hybridsort', 'kmeans', 'lavaMD', 'lud', 'myocyte', 'nn', 'nw', 'pathfinder', 'srad')

fig, (ax, ax2) = plt.subplots(2, 1, sharex=True)
plt.subplots_adjust(hspace=0.001)
ax.set_ylim(1.8, 2.7)
ax2.set_ylim(0.6, 1.5)

# hide the spines between ax and ax2
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

n_groups = len(h1)
index = np.arange(n_groups)
bar_width = 0.2
#plt.axhline(y=1, color='grey', linewidth=0.5,linestyle='--')

minorLocator = AutoMinorLocator(2)
ax2.xaxis.set_minor_locator(minorLocator)

ax.tick_params(which='minor', length=4)
ax.tick_params(which='major', bottom=False,top=False)
plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)

rects1 = ax.bar(index-1.25*bar_width, h1, bar_width,
                alpha=0.6, color='black')
rects2 = ax.bar(index, h2, bar_width,
                alpha=0.3, color='black')
rects3 = ax.bar(index+1.25*bar_width, h3, bar_width,
                alpha=0.8, color='black')

rects2_1 = ax2.bar(index-1.25*bar_width, h1, bar_width,
                alpha=0.6, color='black')
rects2_2 = ax2.bar(index, h2, bar_width,
                alpha=0.3, color='black')
rects2_3 = ax2.bar(index+1.25*bar_width, h3, bar_width,
                alpha=0.8, color='black')

def autolabel(ax, rects, pred=None):
    for rect in rects:
        height = rect.get_height()
        if pred and pred(height):
            ax.text(rect.get_x() + rect.get_width()/1.5, height,
                    '%3.2f' % (height) + "%", ha='center', va='bottom', rotation=60, fontsize=13)

d = .01  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

autolabel(ax, rects1, lambda h : h > 2)
autolabel(ax, rects2, lambda h : h > 2)
autolabel(ax, rects3, lambda h : h > 2)

autolabel(ax2, rects2_1, lambda h : h < 2)
autolabel(ax2, rects2_2, lambda h : h < 2)
autolabel(ax2, rects2_3, lambda h : h < 2)

ax2.set_xticks(index)
ax2.set_xticklabels(label, rotation=45)

fig.tight_layout()

plt.gcf().set_size_inches(12, 4)
#ax.set_ylabel('Relative Runtime')
fig.text(0.06, 0.6, 'Relative Runtime', ha='center', va='center', rotation='vertical')
ax.legend((rects1, rects2, rects3), ('VM socket', 'Shared memory', 'Shared memory with asynchrony'),loc='upper left')
plt.savefig('end2end_compare_cl.pdf', dpi = 600, bbox_inches='tight')
plt.show()
