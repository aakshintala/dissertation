import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple

mpl.rcParams.update({'font.size': 13})

VM1 = (0.3004, 0.2999)
VM2 = (0.1999, 0.2087)
VM3 = (0.2999, 0.2819)
VM4 = (0.1999, 0.2095)


label = ('(a) cl+cl+cl+cl', '(b) cl+cu+cu+cl')

fig, ax = plt.subplots()

n_groups = 2
index = np.arange(n_groups)
bar_width = 0.15
plt.ylim(0, 0.4)
plt.axhline(y=1, color='grey', linewidth=0.5,linestyle='--')

minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minorLocator)
plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)


rects1 = ax.bar(index-1.75*bar_width, VM1, bar_width,
                alpha=0.8, color='black')
rects2 = ax.bar(index-0.6*bar_width, VM2, bar_width,
                alpha=0.6, color='black')
rects3 = ax.bar(index+0.6*bar_width, VM3, bar_width,
                alpha=0.4, color='black')
rects4 = ax.bar(index+1.75*bar_width, VM4, bar_width,
                alpha=0.2, color='black')

ax.set_xticks(index)
ax.set_xticklabels(label)

vals = ax.get_yticks()
ax.set_yticklabels(['{:3.0f}%'.format(x*2*100) for x in vals])

for rect in rects1:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height,
            '%3.1f' % (height*100) + "%", ha='center', va='bottom')
for rect in rects2:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height,
            '%3.1f' % (height*100) + "%", ha='center', va='bottom')
for rect in rects3:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2., height,
            '%3.1f' % (height * 100) + "%", ha='center', va='bottom')
for rect in rects4:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2., height,
            '%3.1f' % (height * 100) + "%", ha='center', va='bottom')

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

plt.gcf().set_size_inches(7, 2.6)

plt.ylabel('Throughput Percentage')
ax.legend((rects1, rects2, rects3, rects4), ('VM1', 'VM2', 'VM3', 'VM4'),loc='upper center', ncol=4,
          bbox_to_anchor = (0.5, 1.05), fancybox = True, shadow = True)
plt.savefig('rate_limit_4vm.png', dpi = 600, bbox_inches='tight', transparent=True)
plt.show()