from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=6)

class Data:
    data: pd.DataFrame
    raw_data: pd.DataFrame

    def __init__(self):
        self.raw_data = pd.read_csv(Path(__file__).parent / "sosp19-ava-data-schedule.csv", header=None)
        self.data = pd.DataFrame()
        for first_row, last_row, controller_type in [(24, 87, "fixed"), (160, 223, "adaptive")]:
            for i in range(first_row, last_row, 3):
                prog_a, prog_b = self.raw_data.iloc[i, 0:2]
                pair_data = self.raw_data.iloc[i:i+2, 5:].T.dropna().astype(int)
                pair_data.columns = ["a_call_time_us", "b_call_time_us"]
                pair_data["controller_type"] = controller_type
                pair_data["a_prog"] = prog_a
                pair_data["b_prog"] = prog_b
                pair_data["period_number"] = range(len(pair_data))
                self.data = self.data.append(pair_data)
        a_call_time_us = self.data["a_call_time_us"].values
        b_call_time_us = self.data["b_call_time_us"].values
        self.data["bias_500ms"] = (a_call_time_us - b_call_time_us) / (a_call_time_us + b_call_time_us)
        self.data["bias_1000ms"] = np.concatenate((
            ((a_call_time_us[1:] + a_call_time_us[:-1]) - (b_call_time_us[1:] + b_call_time_us[:-1])) /
            ((a_call_time_us[1:] + a_call_time_us[:-1]) + (b_call_time_us[1:] + b_call_time_us[:-1])),
            [0]
        ))
        self.data = self.data.reset_index()

    def by_pairs(self, pairs):
        return np.concatenate(tuple(
            self.data[self.data.a_prog == a & self.data.b_prog == b]
            for a, b in pairs
        ))

    def biases_by_kind(self, type, col):
        return self.data[self.data.controller_type == type][col].values.flatten()


data = Data()

ax: plt.Axes
ax2: plt.Axes
fig: plt.Figure
fig, ax = plt.subplots(ncols=1)

#yticks = ax.yaxis.get_major_ticks()
#yticks[0].label1.set_visible(False)

ax.set_ylabel("Unfairness")
kinds = [(type, col) for type in ["fixed", "adaptive"] for col in ["bias_500ms", "bias_1000ms"]]
plot_data = [abs(data.biases_by_kind(type, col)) * 100 for type, col in kinds]
# ax.violinplot(plot_data, showmedians=True, widths=0.8)
ax.violinplot(plot_data, showmedians=True, widths=0.8, showextrema=False)
for i, dd in enumerate(plot_data):
    ax.vlines(i + 1, min(dd), max(dd), color='b', linestyle='-', lw=0.5)
ax.set_xticks(range(1, len(kinds) + 1))
ax.set_xticklabels(["Fixed\n(P=0.5s)", "Fixed\n(P=1s)", "Adaptive\n(P=0.5s)", "Adaptive\n(P=1s)"])
yticks = mtick.PercentFormatter()
ax.yaxis.set_major_formatter(yticks)
ax.set_ylim(0, 40)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Loop over data dimensions and create text annotations.
for i, d in enumerate(plot_data):
    median = np.median(d)
    text = ax.text(i+1+0.25, median, "{:.1f}\%".format(median),
                   ha="left", va="center", color="black")

fig.set_size_inches(3, 1)
plt.savefig("bias_plot.pdf", bbox_inches='tight', pad_inches=0)
# plt.show()

