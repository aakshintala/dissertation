import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple
import pandas as pd

rc('text', usetex=True)
plt.rc('font', family='serif', size=7)

# Data
r = range(4)
raw_data = {'loading':   [3.702, 3.886, 3.894, 3.701],
            'transfer':  [16.109, 457.827, 63.938, 68.662],
            'marshal':   [11.679, 63.082, 68.893, 19.283],
            'unmarshal': [2.151, 68.84, 81.672, 16.037],
            'execution': [463.653, 925.305, 10216.182, 66.287],
            'unaccounted': [72.706, 211.06, 95.421, 37.514]}

names = ('CL:\ndwt2d', 'CUDA:\ngaussian', 'TF:\nimage', 'QAT:\nzip')
df = pd.DataFrame(raw_data)

# From raw value to percentage
totals = [i+j+k+l+m+n for i,j,k,l,m,n in zip(df['loading'], df['transfer'], df['marshal'],
    df['unmarshal'], df['execution'], df['unaccounted'])]
loading_bar = [i / j * 100 for i,j in zip(df['loading'], totals)]
transfer_bar = [i / j * 100 for i,j in zip(df['transfer'], totals)]
marshal_bar = [i / j * 100 for i,j in zip(df['marshal'], totals)]
unmarshal_bar = [i / j * 100 for i,j in zip(df['unmarshal'], totals)]
execution_bar = [i / j * 100 for i,j in zip(df['execution'], totals)]
unaccounted_bar = [i / j * 100 for i,j in zip(df['unaccounted'], totals)]

fig = plt.figure()
ax = plt.subplot(111)
bar_width = 0.75
colors = ["#fffba3", '#fb9a99', '#33a02c', '#b2df8a', '#1f78b4', '#a6cee3']
ax.bar(r, loading_bar, bar_width, color=colors[0], label='loading', bottom=[i+j+k+l+m for i,j,k,l,m in zip(transfer_bar, marshal_bar, unmarshal_bar, execution_bar, unaccounted_bar)])
ax.bar(r, transfer_bar, bar_width, color=colors[1], label='transfer', bottom=[i+j+k+l for i,j,k,l in zip(marshal_bar, unmarshal_bar, execution_bar, unaccounted_bar)])
ax.bar(r, marshal_bar, bar_width, color=colors[2], label='marshal', bottom=[i+j+k for i,j,k in zip(unmarshal_bar, execution_bar, unaccounted_bar)])
ax.bar(r, unmarshal_bar, bar_width, color=colors[3], label='unmarshal', bottom=[i+j for i,j in zip(execution_bar, unaccounted_bar)])
ax.bar(r, execution_bar, bar_width, color=colors[4], label='execution', bottom=unaccounted_bar)
ax.bar(r, unaccounted_bar, bar_width, color=colors[5], label='unaccounted')

def autolabel(ax, rects, pred=None):
    for rect in rects:
        height = rect.get_height()
        if pred and pred(height):
            ax.text(rect.get_x() + rect.get_width()/1.5, height,
                    '%3.2f' % (height) + "%", ha='center', va='bottom', rotation=60, fontsize=13)

plt.xticks(r, names, rotation=60, ha="right")
plt.ylim((0,100))
chartBox = ax.get_position()
ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
plt.legend(loc='upper center', bbox_to_anchor=(1.45, 0.9), shadow=False, ncol=1)
plt.ylabel('Percentage of Runtime')

minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minorLocator)
plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)

plt.gcf().set_size_inches(2.5, (6/9) * 2.5)
plt.savefig('breakdown.pdf', dpi = 600, bbox_inches='tight')
# plt.show()
