import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

rc('text', usetex=True)
plt.rc('font', family='serif', size=20)

# opencl
overhead = (1.119308241, 0.9994702326, 1.00917492,
            1.024476249, 1.002577776, 1.046582144,
            1.010735752, 1.00708802, 1.388105454, 1.184111)
print(sum(overhead) / len(overhead))
xlabel = ('cl\_nvidia', 'cl\_amd', 'cuda\_nvidia',
          'tf\_c', 'tf\_python', 'tf\_lite',
          'ncsdk', 'fpga', 'qat', 'hip')
output = 'end2end_dev.pdf'
ylim = 1.55

fig, ax = plt.subplots()

n_groups = len(overhead)
index = np.arange(n_groups)
bar_width = 0.5
opacity = 0.65
plt.ylim(0, ylim)
plt.axhline(y=1, color='grey', linewidth=0.5,linestyle='--')

minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minorLocator)
plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', bottom=False,top=False)


rects1 = ax.bar(index, overhead, bar_width, alpha=opacity, color='black')

ax.set_xticks(index)
ax.set_xticklabels(xlabel, rotation=45)

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
                "%3.3f" % height, ha=ha[xpos], va='bottom')

plt.gcf().set_size_inches(8, 5)
autolabel(rects1)
plt.ylabel('Relative Runtime')

plt.savefig(output, dpi = 600, bbox_inches='tight')
plt.show()
