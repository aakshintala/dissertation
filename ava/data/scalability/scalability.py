import numpy as np
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple

#mpl.rcParams.update({'font.size': 19})
rc('text', usetex=True)
plt.rc('font', family='serif', size=7)

nativeValue = np.array((1, 1.978349028, 3.95037858, 8.19273578, 16.35143818))

gValue = np.array((1.12294617, 2.169777988, 4.271492691, 8.648873674, 17.80381146))
bMaxErr = (0, 0, 0.064, 0.157, 0.346)
bMinErr = (0, 0, 0.064, 0.166, 0.486)

bValue = np.array((1.12294617, 2.185159496, 4.306235687, 8.733074513, 18.07918704))
gMaxErr = (0, 0, 0.011, 0.166, 0.354)
gMinErr = (0, 0, 0.011, 0.394, 0.569)

label = ('1', '2', '4', '8', '16')

fig, ax = plt.subplots()

n_groups = 5
index = np.arange(n_groups)
bar_width = 0.27
plt.ylim(0, 27)
#plt.axhline(y=1, color='grey', linewidth=0.5,linestyle='--')

minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minorLocator)
plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)
error_config = dict(elinewidth=1, capsize=3, ecolor='k')

rectsG = ax.bar(index, gValue, bar_width,
                # yerr=(gMaxErr, gMinErr),error_kw=error_config,
                alpha=0.6, color='black')

rectsB = ax.bar(index+bar_width, bValue, bar_width,
                # yerr=(bMaxErr, bMinErr),error_kw=error_config,
                alpha=0.3, color='black')

rectsNative = ax.bar(index-bar_width, nativeValue, bar_width,
                # yerr=(bMaxErr, bMinErr),error_kw=error_config,
                alpha=0.9, color='black')


ax.set_xticks(index)
ax.set_xticklabels(label)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

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
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], height + 0.05,
                "%.2f" % height, ha=ha[xpos], va='bottom', size=7, rotation=90)

plt.gcf().set_size_inches(3, 1.0)
autolabel(rectsG)
autolabel(rectsB)
autolabel(rectsNative)
plt.ylabel('Relative Runtime')
ax.legend((rectsNative, rectsG, rectsB), ('Native', 'VM', 'App'),loc='upper left',
          shadow=False, ncol=1)
plt.savefig('scalability.pdf', dpi = 600, bbox_inches='tight', pad_inches=0)
# plt.show()
