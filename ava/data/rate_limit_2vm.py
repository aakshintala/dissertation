import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple


mpl.rcParams.update({'font.size': 11})

h1 = (0.4934, 0.6, 0.5155, 0.6107)

h2 = (0.5066, 0.4, 0.4845, 0.3893)

label = ('(a) cl+cl', '(b) cl+cl', '(c) cl+cu', '(d) cl+cu')

fig, ax = plt.subplots()

n_groups = 4
index = np.arange(n_groups)
bar_width = 0.3
plt.ylim(0, 0.8)
plt.axhline(y=1, color='grey', linewidth=0.5,linestyle='--')

minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minorLocator)

plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)


rects1 = ax.bar(index-0.65*bar_width, h1, bar_width,
                alpha=0.6, color='black')
rects2 = ax.bar(index+0.65*bar_width, h2, bar_width,
                alpha=0.3, color='black')

for rect in rects1:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height,
            '%3.1f' % (height*100) + "%", ha='center', va='bottom')
for rect in rects2:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height,
            '%3.1f' % (height*100) + "%", ha='center', va='bottom')

vals = ax.get_yticks()
ax.set_yticklabels(['{:3.0f}%'.format(x*100) for x in vals])

ax.set_xticks(index)
ax.set_xticklabels(label)

fig.tight_layout()

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
                '{}'.format(height), ha=ha[xpos], va='bottom')

plt.gcf().set_size_inches(6,3.5)
# autolabel(rects1)
# autolabel(rects2)
plt.ylabel('Throughput Percentage')
ax.legend((rects1, rects2), ('VM1', 'VM2'),loc='upper center')
plt.savefig('rate_limit_2vm.png', dpi = 600, bbox_inches='tight')
plt.show()
