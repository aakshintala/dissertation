from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=15)

def autolabel(rects, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                "%3.1f" % height, ha=ha[xpos], va='bottom')

class Data:
    def __init__(self):
        self.groups = ["16 KiB", "128 KiB", "512 KiB"]
        self.uncontended = [17311.679, 17862.319, 18165.203]
        self.contended = [8704.848, 11780.853, 15775.025]


data = Data()

ax= plt.Axes
ax2= plt.Axes
fig= plt.Figure
fig, ax = plt.subplots(ncols=1)

# n = len(data.x_label)
barwidth = 0.35
uncontended = [x - barwidth/1.8 for x in np.arange(3)]
contended = [x + barwidth/1.8 for x in np.arange(3)]

rect1 = ax.bar(uncontended, [x/1024 for x in data.uncontended], width=barwidth, label='Uncontended', color=[(0.3,)*3])
autolabel(rect1)
rect2 = ax.bar(contended, [x/1024 for x in data.contended], width=barwidth, label='Contended', color=[(0.8,)*3])
autolabel(rect2)

# ax.set_xlim(0.5, n+0.5)
ax.set_ylim(0, 24)
ax.set_xticks(np.arange(3))
ax.set_xticklabels(data.groups)
ax.set_xlabel('Block Size')
ax.set_ylabel('Throughput (Gib/s)')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.gcf().set_size_inches(6, 1.6)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), shadow=False, ncol=2)
plt.savefig('qat_unfairness.pdf', dpi = 600, bbox_inches='tight')
plt.show()
