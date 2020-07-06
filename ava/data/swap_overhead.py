import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({'font.size': 13})

best = (12.07, 22.164, 44.93, 89.92, 155.44, 266.48)
worst = (542.95, 532.63, 527.29, 524.65, 523.24, 522.54)

label = ('16 MB', '32 MB', '64 MB', '128 MB', '256 MB', '512 MB')
fig, ax = plt.subplots()

index = np.arange(6)
ax.set_xticks(index)
ax.set_xticklabels(label)

plt.ylim(0, 620)
ax.plot(best, marker='o', color='black', label='Best')
ax.plot(worst, marker='^', color='black', label='Worst')
for i,j in zip(index,best):
    ax.text(i, j+20, str(j))
for i,j in zip(index,worst):
    ax.text(i, j+10, str(j))
ax.legend(loc='center left')

plt.ylabel('Runtime (milliseconds/op)')

plt.gcf().set_size_inches(6,2.4)
plt.savefig('swap_overhead.png', dpi = 600, bbox_inches='tight')
plt.show()

