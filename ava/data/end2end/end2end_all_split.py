import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import pandas as pd
from StringIO import StringIO

rc('text', usetex=True)
plt.rc('font', family='serif', size=20)

def autolabel(rects, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                "%3.2f" % height, ha=ha[xpos], va='bottom', rotation=60)

# read data
raw = ''
with open('end2end_all.csv', 'r') as file:
        raw = file.read().replace('\n', '')
data = pd.read_csv(StringIO(raw), quotechar='"', header=None, skipinitialspace=True).values
print(data)
print("\n")

fig, ax = plt.subplots()
width = 1
group_gap = 1

groups = len(data)/3
pos = 0
x_ind = []
x_labels = []
for group_id in range(5):
    num_bench = sum(x is not np.nan for x in list(data[group_id*3]))
    x = [t + group_gap + pos for t in range(num_bench)]
    pos = pos + num_bench + group_gap
    x_ind = np.concatenate((x_ind, x))
    y = [float(t) for t in list(data[group_id*3+2, :num_bench])]
    x_labels = np.concatenate((x_labels, list(data[group_id*3+1, :num_bench])))
    rect = ax.bar(x, y, width, color='black', alpha=0.5, edgecolor= "black", label=data[group_id*3, 0].replace('_', '\_'))
    autolabel(rect)
    plt.text(pos - num_bench/2 - group_gap - 0.5, -1.2, data[group_id*3, 0].replace('_', '\_'))

ax.set_xticks([t+0.5 for t in x_ind])
ax.set_xticklabels([t.replace('_', '\_') for t in x_labels])
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

fig.tight_layout()

plt.gcf().set_size_inches(20, 5)
plt.xlim(0, pos)
plt.ylim(0, 2.5)
plt.ylabel('Relative Runtime')

plt.savefig('end2end_all_part1.pdf', dpi = 600, bbox_inches='tight')
plt.show()

# second plot
fig, ax = plt.subplots()
pos = 0
x_ind = []
x_labels = []
for group_id in range(5, groups):
    num_bench = sum(x is not np.nan for x in list(data[group_id*3]))
    x = [t + group_gap + pos for t in range(num_bench)]
    pos = pos + num_bench + group_gap
    x_ind = np.concatenate((x_ind, x))
    y = [float(t) for t in list(data[group_id*3+2, :num_bench])]
    x_labels = np.concatenate((x_labels, list(data[group_id*3+1, :num_bench])))
    rect = ax.bar(x, y, width, color='black', alpha=0.5, edgecolor= "black", label=data[group_id*3, 0].replace('_', '\_'))
    autolabel(rect)
    plt.text(pos - num_bench/2 - group_gap - 0.5, -1.0, data[group_id*3, 0].replace('_', '\_'))

ax.set_xticks([t+0.5 for t in x_ind])
ax.set_xticklabels([t.replace('_', '\_') for t in x_labels])
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

fig.tight_layout()

plt.gcf().set_size_inches(20, 5)
plt.xlim(0, pos)
plt.ylim(0, 2.0)
plt.ylabel('Relative Runtime')

plt.savefig('end2end_all_part2.pdf', dpi = 600, bbox_inches='tight')
plt.show()
