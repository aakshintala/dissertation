import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple



gpu_num = (93,116,141,136,167,106,122,81,73,26)
nvidia_num = (39,39,53,47,56,60,55,38,36,12)
xlabel = range(2009, 2019)
output = 'gpu_stats.png'


fig, ax = plt.subplots()

n_groups = len(gpu_num)
index = np.arange(n_groups)
bar_width = 0.4
opacity = 0.65
plt.ylim(0, 180)

minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minorLocator)
plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)

rects1 = ax.bar(index, gpu_num, bar_width, alpha=opacity, color='black')
plt.plot(index, nvidia_num, 'bo-')
# for a, b in zip(index, nvidia_num):
#     plt.text(a, b, str(b))

ax.set_xticks(index)
ax.set_xticklabels(xlabel, fontsize=11)

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

plt.gcf().set_size_inches(6,3)
autolabel(rects1)
plt.ylabel('Relative Runtime')

plt.savefig(output, dpi = 600, bbox_inches='tight')
plt.show()
