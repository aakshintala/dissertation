import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple


#group2
gaussian = (3.34, 2.68, 4.32)

label = ('(a) baseline', '(b)', '(c)', '(d)')

fig, ax = plt.subplots()

index = np.arange(4)
index1 = np.arange(1)
index2 = np.arange(3)+1
bar_width = 0.25
plt.ylim(0, 5)
plt.axhline(y=1, color='grey', linewidth=0.5,linestyle='--')

minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minorLocator)
plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)


rGCuda = ax.bar(index1-1.15*bar_width, 2.76, bar_width,
                alpha=0.8, color='black') #, hatch='//')
rGOpencl = ax.bar(index1, 1.65, bar_width,
               alpha=0.4, color='black') #hatch='\\')
rBfsOpencl = ax.bar(index1+1.15*bar_width, 1, bar_width,
                    alpha=0.6, color='black', hatch='//')

rgaussian = ax.bar(index2-0.6*bar_width, gaussian, bar_width,
                   alpha=0.4, color='black')
rgaussian_g = ax.bar(index1+1+0.6*bar_width, 3.34, bar_width,
                     alpha=0.4, color='black')
rgaussian_bfs = ax.bar(index1+2+0.6*bar_width, 1.81, bar_width,
                       alpha=0.6, color='black', hatch='//')
rgaussian_cuda = ax.bar(index1+3+0.6*bar_width, 4.09, bar_width,
                        alpha=0.8, color='black')


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

plt.gcf().set_size_inches(6,4.5)
autolabel(rGCuda)
autolabel(rGOpencl)
autolabel(rBfsOpencl)
autolabel(rgaussian)
autolabel(rgaussian_g)
autolabel(rgaussian_bfs)
autolabel(rgaussian_cuda)

plt.ylabel('Relative Runtime')
ax.legend((rGCuda, rGOpencl, rBfsOpencl), ('gaussian (cuda)', 'gaussian (opencl)', 'bfs (cl)'),loc='upper center', ncol=3)
plt.savefig('concurrency.png', dpi = 600, bbox_inches='tight')
plt.show()