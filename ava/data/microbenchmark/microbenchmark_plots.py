from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from matplotlib import rc
import sys

rc('text', usetex=True)
plt.rc('font', family='serif', size=7)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)

class Data:
    vm_data: pd.DataFrame
    native_data: pd.DataFrame

    column_names = ("benchmark", "rep", "time_ms", "work", "size")

    def __init__(self):
        self.vm_data = pd.read_csv(Path(__file__).parent / "microbenchmark_vm_nodataops.csv", header=None)
        self.vm_data = self.vm_data.append(pd.read_csv(Path(__file__).parent / "microbenchmark_vm_nodataops_2.csv", header=None))
        self.vm_data.columns = self.column_names

        self.native_data = pd.read_csv(Path(__file__).parent / "microbenchmark_native_nodataops.csv", header=None)
        self.native_data.columns = self.column_names

        self.benchmarks = set(self.vm_data.benchmark.values)

        self.vm_means = self._extract_aggregate(self.vm_data)
        self.native_means = self._extract_aggregate(self.native_data)

        self.means = self.vm_means.merge(self.native_means, on=["benchmark", "work", "size"],
                                         suffixes=("_vm","_native"))
        self.means["ratio"] = self.means.time_ms_vm["mean"] / self.means.time_ms_native["mean"]
        self.means["ratio_std"] = self.means.time_ms_vm["std"] / self.means.time_ms_native["mean"]
        self.means["overhead_ms"] = (self.means.time_ms_vm["mean"] - self.means.time_ms_native["mean"])
        self.means["overhead_ms_std"] = (self.means.time_ms_vm["std"] + self.means.time_ms_native["std"])
        self.means["calls_per_s"] = 1.0 / (self.means.time_ms_native["mean"] / 1000)
        self.means["mib_per_s"] = (self.means["size"] / 1024) / (self.means["time_ms_native"]["mean"] / 1000)

    def _extract_aggregate(self, d):
        ret = d[d.rep >= 15]. \
            groupby(["benchmark", "work", "size"]).aggregate([np.mean, np.std]).reset_index()
        del ret["rep"]
        ret.time_ms += 0.00001
        return ret

    def __getattr__(self, item):
        return self.means[self.means.benchmark == item]


data = Data()

fig: plt.Figure

if False:
    fig, ax = plt.subplots()
    heatmap_data = data.in_transfer[["work", "size", "overhead_ms", "overhead_ms_std"]].pivot("work", "size")
    # heatmap_data.columns = heatmap_data.columns.get_level_values(-1)
    # heatmap_data = np.log(heatmap_data)
    im = ax.imshow(heatmap_data["overhead_ms"])

    ax.set_title("Call+return overhead (ms)")

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(set(heatmap_data.columns.get_level_values(-1)))))
    ax.set_yticks(np.arange(len(heatmap_data.index)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(heatmap_data.columns.get_level_values(-1))
    ax.set_yticklabels(heatmap_data.index)
    plt.ylabel("Work (ms)")
    plt.xlabel("Data (KiB)")

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(heatmap_data.index)):
        for j in range(len(set(heatmap_data.columns.get_level_values(-1)))):
            text = ax.text(
                j, i, "{:5.2f}\n({:4.3f})".format(heatmap_data["overhead_ms"].values[i, j],
                                                     heatmap_data["overhead_ms_std"].values[i, j]),
                ha="center", va="center", color="w")

    fig.tight_layout()
    plt.show()

if False:
    fig, ax = plt.subplots(nrows=4) # (ncols=len(data.benchmarks))

    def scatter(ax, data):
        x, y, c = data[data.work > 0][["mib_per_s", "overhead_ms", "size"]].T.values
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        # print(p, p(x))
        # ax.plot(x, p(x))
        # ax.scatter(*data[["calls_per_s", "ratio"]].T.values, alpha=0.5)
        ax.scatter(x, y, c=c, alpha=0.5)
        # ax.set_xscale('log')
        # ax.set_yscale('log')
        return p

    in_transfer_poly = scatter(ax[0], data.in_transfer)
    in_shadow_poly = scatter(ax[1], data.in_shadow)
    out_existing_poly = scatter(ax[2], data.out_existing)
    noop_poly = scatter(ax[3], data.noop)

    # plt.savefig("factor_plot.pdf", bbox_inches='tight')
    plt.show()

if True:
    def line(ax: plt.Axes, data, x_col, work = None, size = None, y_log=False):
        selector = (data.work == work if work is not None else 1) & (data["size"] == size if size is not None else 1)
        x, c_s, m_s, r = data[selector][[x_col, "calls_per_s", "mib_per_s", "ratio"]].T.values
        # ax.plot(x, c_s)
        # ax.plot(x, m_s)
        ax.plot(x / 1024, r, label="{}".format(work), linewidth=1)
        # ax.set_xscale('log')
        if y_log:
            ax.set_yscale('log')
    #
    # fig, ax = plt.subplots(nrows=len(set(data.means.work)))
    # for i, work in enumerate(sorted(set(data.means.work))):
    #     line(ax[i], data.in_transfer, "size", work=work)
    # plt.show()

    fig, ax = plt.subplots(nrows=1)
    for i, work in enumerate([1, 10, 100, 1000]):
        line(ax, data.in_transfer, "size", work=work, y_log=True)
    ax.set_xscale('log')
    ax.set_xticks(np.array([1, 32, 1024, 65536]) / 1024.0)
    ax.set_xticklabels(["1KiB", "32KiB", "1MiB", "64MiB"])
    ax.set_yticks(np.array([1, 1.28, 2, 3, 5, 10]))
    ax.set_yticklabels(["1$\\times$", "1.28$\\times$", "2$\\times$", "3$\\times$", "5$\\times$", "10$\\times$"])
    ax.legend(title="Work (ms)")
    plt.xlabel("Data Transferred")
    plt.ylabel("Relative Runtime")

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    fig.set_size_inches(3.25, 1.3)
    plt.savefig("overhead_plot.pdf", bbox_inches='tight', pad_inches=0)

# fig, ax = plt.subplots(nrows=len(set(data.means["size"])))
# for i, size in enumerate(sorted(set(data.means["size"]))):
#     line(ax[i], data.in_transfer, "work", size=size, y_log=True)
# plt.show()

sys.exit()

## Call-intensive

def line(ax: plt.Axes, data, work = None, size = None, y_log=False):
    selector = (data.work == work if work is not None else 1) & (data["size"] == size if size is not None else 1)
    x, c_s, m_s, r = data[selector][["size", "calls_per_s", "mib_per_s", "ratio"]].T.values
    # ax.plot(x, c_s)
    # ax.plot(x, m_s)
    ax.plot(x / 1024, r, label="{}".format(work), linewidth=1)
    # ax.set_xscale('log')
    if y_log:
        ax.set_yscale('log')
#
# fig, ax = plt.subplots(nrows=len(set(data.means.work)))
# for i, work in enumerate(sorted(set(data.means.work))):
#     line(ax[i], data.in_transfer, "size", work=work)
# plt.show()

fig, ax = plt.subplots(nrows=1)
work = 0
selector = (data.in_transfer.work == work) & (data.in_transfer["size"] >= 1)
x = data.in_transfer[selector][["size"]].values
vm = data.in_transfer[selector].time_ms_vm[["mean"]].values
native = data.in_transfer[selector].time_ms_native[["mean"]].values
multiplier = 65536 / x
ax.plot(x / 1024, vm * multiplier)
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xticks(np.array([1, 32, 1024, 65536]) / 1024.0)
ax.set_xticklabels(["1KiB", "32KiB", "1MiB", "64MiB"])
# ax.set_yticks(np.array([1, 2, 3, 5, 10]))
# ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda y, _: "{:3.0f}$\\times$".format(y)))
# ax.legend(title="Work (ms)")
plt.xlabel("Data transferred")
plt.ylabel("Relative runtime")

fig.set_size_inches(3.25, 1.5)
# plt.savefig("overhead_plot.pdf", bbox_inches='tight')
plt.show()

fig, ax = plt.subplots(nrows=1)
selector = (data.in_transfer["size"] == 0) & (data.in_transfer.work >= 1)
x = data.in_transfer[selector][["work"]].values
vm = data.in_transfer[selector].time_ms_vm[["mean"]].values
native = data.in_transfer[selector].time_ms_native[["mean"]].values
multiplier = 1000 / x
ax.plot(x, vm * multiplier)
# ax.set_yscale('log')
ax.set_xscale('log')
# ax.set_xticks(np.array([1, 32, 1024, 65536]) / 1024.0)
# ax.set_xticklabels(["1KiB", "32KiB", "1MiB", "64MiB"])
# ax.set_yticks(np.array([1, 2, 3, 5, 10]))
# ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda y, _: "{:3.0f}$\\times$".format(y)))
# ax.legend(title="Work (ms)")
plt.xlabel("Data transferred")
plt.ylabel("Relative runtime")

fig.set_size_inches(3.25, 1.5)
# plt.savefig("overhead_plot.pdf", bbox_inches='tight')
plt.show()
