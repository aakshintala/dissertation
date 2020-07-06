from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=15)

class Data:
    data: pd.DataFrame

    def __init__(self):
        self.data = pd.read_csv(Path(__file__).parent / "bf_unfairness.csv", header=None)
        data_values = self.data.values
        print(data_values)

        self.x_label = [row[0].strip('ND_') for row in data_values[1:]]
        self.x_label = [label.replace('_', '\_') for label in self.x_label]
        self.bitfusion = [float(row[1].strip('%')) for row in data_values[1:]]
        self.ava = [float(row[2].strip('%')) for row in data_values[1:]]


data = Data()

ax: plt.Axes
ax2: plt.Axes
fig: plt.Figure
fig, ax = plt.subplots(ncols=1)

n = len(data.x_label)

ax.plot(range(1, n+1), data.bitfusion, marker='o', label='FlexDirect', color='black')
# ax.plot(range(1, n+1), data.ava, marker='^', label='AvA', color='black')

for i,j in zip(range(1, n+1) ,data.bitfusion):
    if i == 1 or i == n or i == n-2:
        ax.annotate("{0:.0f}".format(j), xy=(i-0.25,j+5))
# for i,j in zip(range(1, n+1) ,data.ava):
#     if i == n or i == n-2:
#         ax.annotate("{0:.0f}".format(j), xy=(i-0.25,j+1))

ax.legend(loc='upper center', ncol=2)
ax.set_xlim(0.5, n+0.5)
ax.set_ylim(0, 105)
ax.set_xticks(range(1, n+1))
ax.set_xticklabels(data.x_label)
ax.set_xlabel('Needle Throughput (ms/kernel)')
ax.set_ylabel('Unfairness')
yticks = mtick.PercentFormatter()
ax.yaxis.set_major_formatter(yticks)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.gcf().set_size_inches(6, 1.8)
plt.savefig('bf_unfairness.pdf', dpi = 600, bbox_inches='tight')
plt.show()
