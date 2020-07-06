import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import pandas as pd
import sys
if sys.version_info[0] > 2:
    from io import StringIO
    print("Error: we need Python 3 for this script\n")
else:
    from StringIO import StringIO

rc('text', usetex=True)
plt.rc('font', family='serif', size=6)

def autolabel(rects, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                "%3.2f" % height, ha=ha[xpos], va='bottom', rotation=80)

# read data
raw = ''
with open('end2end_all.csv', 'r') as file:
        raw = file.read() #.replace('\n', '')
data = pd.read_csv(StringIO(raw), quotechar='"', header=None, skipinitialspace=True).values
print(data)
print("\n")

fig, ax = plt.subplots()
width = 1
group_gap = 1

groups = len(data)//3
pos = 0
x_ind = []
x_labels = []
for group_id in range(groups):
    num_bench = sum(x is not np.nan for x in list(data[group_id*3]))
    x = [t + group_gap + pos for t in range(num_bench)]
    pos = pos + num_bench + group_gap
    x_ind = np.concatenate((x_ind, x))
    y = [float(t) for t in list(data[group_id*3+2, :num_bench])]
    x_labels = np.concatenate((x_labels, list(data[group_id*3+1, :num_bench])))
    label = data[group_id * 3 + 1, 0]
    rect = ax.bar(x, y, width, color=([(0.3,)*3, (0.8,)*3] * num_bench)[:num_bench])
    for xx, yy in zip(x, y):
        if yy > 2.3:
            ax.text(xx, 2.3, r"\bf {:1.2f}".format(yy), ha='center', va='top', rotation=90, color="white")
        else:
            ax.text(xx, yy + 0.05, r"{:1.2f}".format(yy), ha='center', va='bottom', rotation=90, color="black")
    offset = 1.0 if group_id in (3, 6, 9) else (0.4 if group_id is 7 else 0.5)
    ax.text(pos - num_bench/2 - offset,
            -2.1,
            data[group_id*3, 0].replace('_', '\_'),
            ha='center',
            rotation= 0,
            fontsize=8)
    print(group_id, data[group_id*3])
            # rotation=30 if group_id in (2, 3, 7) else 0)
    # ax.text(pos - num_bench/2 - 0.5, -0.9 if 2 <= group_id < 5 else -1, data[group_id*3, 0].replace('_', '\_'), ha='center', rotation=30 if 2 <= group_id < 5 else 0)

ax.tick_params(axis='x', which='both',length=0)
ax.set_xticks([t+0.5 for t in x_ind])
ax.set_xticklabels([t.replace('_', '\_') for t in x_labels])
plt.setp( ax.xaxis.get_majorticklabels(), rotation=90, ha="right")

fig.tight_layout()

plt.gcf().set_size_inches(6.5, 1)
plt.xlim(0, pos)
plt.ylim(0, 2.5)
plt.ylabel('Relative Runtime')

plt.savefig('end2end_all.pdf', dpi = 600, bbox_inches='tight', pad_inches=0)
# plt.show()
