import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple

from pygments.util import xrange


mpl.rcParams.update({'font.size': 14})

def add_line(ax, xpos, ypos):
    line = plt.Line2D([xpos, xpos], [0, ypos],
                      transform=ax.transAxes, color='black', linewidth=1)
    line.set_clip_on(False)
    ax.add_line(line)


#groupA
gaussianA1 = (3.01, 3.42)
gaussianA2 = (3.04, 3.41)

#groupB
gaussianB = (2.35, 2.74)
bfsB = (1.77, 1.85)

#groupC
clC = (3.14, 4.41)
cudaC = (4.31, 4.18)

label = ('native', 'vm', 'native', 'vm', 'native', 'vm')
group_label = ('(a)', '(b)', '(c)')

fig, ax = plt.subplots()

index = [0,1,2,3,4,5]
indexA = np.arange(2)
indexB = np.arange(2)+2
indexC = np.arange(2)+4
bar_width = 0.25
plt.ylim(0, 5.6)
plt.axhline(y=1, color='grey', linewidth=0.5,linestyle='--')

minorLocator = AutoMinorLocator(1)
ax.xaxis.set_minor_locator(minorLocator)
plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)

dist = 0.7
rgaussianA1 = ax.bar(indexA-dist*bar_width, gaussianA1, bar_width, alpha=0.8, color='black')
rgaussianA2 = ax.bar(indexA+dist*bar_width, gaussianA2, bar_width, alpha=0.8, color='black')

rgaussianB = ax.bar(indexB-dist*bar_width, gaussianB, bar_width, alpha=0.8, color='black')
rbfsB = ax.bar(indexB+dist*bar_width, bfsB, bar_width, alpha=0.4, color='black')

rclC = ax.bar(indexC-dist*bar_width, clC, bar_width, alpha=0.8, color='black')
rcudaC = ax.bar(indexC+dist*bar_width, cudaC, bar_width, alpha=0.6, color='black', hatch='//')

ax.set_xticks(index)
ax.set_xticklabels(label)
#label_group_bar(ax, data)

scale = 1. / 3
for pos in [1, 2]:
    add_line(ax, pos * scale, -.1)
for pos in xrange(0, 3):
    lxpos = pos * scale + scale / 2
    ax.text(lxpos, -.1, group_label[pos], ha='center', transform=ax.transAxes)

fig.tight_layout()
plt.subplots_adjust(bottom=0.1)

def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom', rotation=20)

plt.gcf().set_size_inches(8,3)
autolabel(rgaussianA1)
autolabel(rgaussianA2)
autolabel(rgaussianB)
autolabel(rbfsB)
autolabel(rclC)
autolabel(rcudaC)


plt.ylabel('Relative Runtime')
ax.legend((rbfsB, rclC, rcudaC), ('bfs', 'gaussian (opencl)', 'gaussian (cuda)'),loc='upper center', ncol=4,
          bbox_to_anchor=(0.5, 1.1), fancybox=True, shadow=True)
plt.savefig('concurrency_new.png', dpi = 600, bbox_inches='tight')
plt.show()