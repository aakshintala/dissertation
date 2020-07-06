import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from collections import namedtuple

rc('text', usetex=True)
plt.rc('font', family='serif', size=13)

# OpenCL
h1 = (1.11, 1.13, 1.16, 1.38, 1.69, 1.55, 1.26, 1.19, 1.04, 1.04, 1.18, 1.14, 1.07, 1.05, 1.04)
h2 = (1.30, 1.16, 1.39, 1.89, 1.70, 1.96, 1.71, 1.33, 1.11, 1.11, 1.18, 1.14, 1.13, 1.15, 1.06)
label = ('backprop', 'bfs', 'b+tree', 'dwt2d', 'gaussian', 'heartwall', 'hybridsort', 'kmeans', 'lavaMD', 'lud', 'myocyte', 'nn', 'nw', 'pathfinder', 'srad')

# CUDA
#h1 = (1.09288444, 1.043691913, 1.065634213, 1.452050412, 1.038258761, 1.035948778, 1.021155739, 1.097756601, 1.012641895, 1.019385748, 1.074302644)
#h2 = (1.310818373, 1.084398268, 1.144944977, 2.408033204, 1.057784777, 1.119783559, 1.090527126, 1.114197857, 1.086825341, 1.024546078, 1.169992854)
#label = ('backprop', 'bfs', 'gaussian', 'heartwall', 'hotspot', 'lud', 'needle', 'nn', 'pathfinder', 'srad\_v1', 'srad\_v2')

fig, ax = plt.subplots()

n_groups = len(h1)
index = np.arange(n_groups)
bar_width = 0.3
plt.ylim(0, 2.5)
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
            '%3.2f' % (height) + "%", ha='center', va='bottom')
for rect in rects2:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height,
            '%3.2f' % (height) + "%", ha='center', va='bottom')

vals = ax.get_yticks()

ax.set_xticks(index)
ax.set_xticklabels(label, rotation=45)

fig.tight_layout()

plt.gcf().set_size_inches(12,6)
plt.ylabel('Relative Runtime')
ax.legend((rects1, rects2), ('Shared memory', 'VM socket'),loc='upper center')
plt.savefig('end2end_transport.pdf', dpi = 600, bbox_inches='tight')
plt.show()
