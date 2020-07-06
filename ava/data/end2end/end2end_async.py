import numpy as np
import pandas as pd

from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple

rc('text', usetex=True)
plt.rc('font', family='serif', size=7)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)

# OpenCL
#h1 = (1.11, 1.13, 1.16, 1.38, 1.69, 1.55, 1.26, 1.19, 1.04, 1.04, 1.18, 1.14, 1.07, 1.05, 1.04)
#h2 = (1.104265127, 1.105114181, 1.038775741, 1.308188752, 1.085992564, 1.489058329, 1.255314684, 1.195669537, 1.00572341, 1.048695195, 1.174246363, 1.138840294, 1.068426624, 1.010775319, 1.010136583)
#label = ('backprop', 'bfs', 'b+tree', 'dwt2d', 'gaussian', 'heartwall', 'hybridsort', 'kmeans', 'lavaMD', 'lud', 'myocyte', 'nn', 'nw', 'pathfinder', 'srad')

# CUDA
h1 = (1.114893748, 1.031608621, 1.067299685, 1.094175096, 1.033881797, 1.022025541, 1.013558887, 1.035294118, 1.090028649, 1.045085082, 1.077713265)
h2 = (1.069319819, 0.9669534483, 1.033646688, 1.089176142, 1, 0.9746691742, 0.9735931478, 0.8666682353, 1.057067341, 1.009442651, 1.060387471)
label = ('backprop', 'bfs', 'gaussian', 'heartwall', 'hotspot', 'lud', 'needle', 'nn', 'pathfinder', 'srad\_v1', 'srad\_v2')

fig, ax = plt.subplots()

n_groups = len(h1)
index = np.arange(n_groups)
bar_width = 0.35
plt.ylim(0, 1.9)
#plt.axhline(y=1, color='grey', linewidth=0.5,linestyle='--')

minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minorLocator)

plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)


rects1 = ax.bar(index-0.5*bar_width, h1, bar_width,
                alpha=0.8, color='black')
rects2 = ax.bar(index+0.5*bar_width, h2, bar_width,
                alpha=0.3, color='black')

for rect in rects1:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height + 0.02,
            '%3.2f' % (height) + "%", ha='center', va='bottom', rotation=90)
for rect in rects2:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height + 0.02,
            '%3.2f' % (height) + "%", ha='center', va='bottom', rotation=90)

vals = ax.get_yticks()

ax.set_xlim(-0.5, 10.5)
ax.set_xticks(index)
ax.set_xticklabels(label, rotation=40)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()

fig.set_size_inches(3.25, 1.0)
plt.ylabel('Relative Runtime')
ax.legend((rects1, rects2), ('Sync', 'Async'), bbox_to_anchor=(0.5, 1.1), loc='upper center', ncol=2)
plt.savefig('end2end_async.pdf', dpi = 600, bbox_inches='tight', pad_inches=0)
# plt.show()
