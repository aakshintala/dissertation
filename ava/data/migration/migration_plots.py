from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rc

rc('text', usetex=True)
plt.rc('font', family='serif', size=6)

class Data:
    full: pd.DataFrame

    def __init__(self):
        data = pd.read_csv(Path(__file__).parent / "data.csv", header=None)

        benchmark_properties = data[0:4].T.dropna()
        benchmark_properties.columns=("benchmark", "kernel_time_ms", "end2end_time_s", "calls")
        benchmark_properties[["kernel_time_ms", "end2end_time_s"]] = \
            benchmark_properties[["kernel_time_ms", "end2end_time_s"]].astype(float)
        benchmark_properties[["calls"]] = benchmark_properties[["calls"]].astype(int)
        benchmark_properties[["benchmark"]] = benchmark_properties[["benchmark"]].astype(str)
        benchmark_properties["end2end_time_ms"] = benchmark_properties.end2end_time_s * 1000
        del benchmark_properties["end2end_time_s"]

        self.benchmark_properties = benchmark_properties

        my_cols = range(201)
        data = pd.read_csv(Path(__file__).parent / "raw_data_10g_ethernet.csv", header=None,
                                names = my_cols, engine = 'python')
        migrations = pd.DataFrame(columns=("benchmark", "rep","migration_point", "time_ms"))
        data_values = data.values
        for offset in range(0, 29, 2):
            tmp = data[offset:offset+2].T[1:].dropna()
            tmp.columns = ("migration_point", "time_ms")
            tmp["benchmark"] = str(data_values[offset, 0])
            tmp["rep"] = range(len(tmp))
            migrations = migrations.append(tmp, sort=True)
        migrations["time_ms"] = migrations["time_ms"].astype(float)
        migrations["migration_point"] = migrations["migration_point"].astype(int)
        self.migrations = migrations

        self.full = self.migrations.merge(self.benchmark_properties, on="benchmark")
        self.data=data

    @property
    def benchmarks(self):
        return self.benchmark_properties.benchmark.values

    def migration_time_by_benchmark(self, benchmarks):
        return [self.migrations[self.migrations.benchmark == benchmark].time_ms.values
                for benchmark in benchmarks]

    def migration_fraction_by_benchmark(self, benchmarks):
        d = self.full.copy()
        d["fraction"] = d.time_ms / d.end2end_time_ms
        return [d[d.benchmark == benchmark].fraction.values
                for benchmark in benchmarks]


data = Data()

ax1: plt.Axes
ax2: plt.Axes
fig: plt.Figure
fig, (ax1, ax2) = plt.subplots(ncols=2, gridspec_kw = {'width_ratios':[14, 1]})

def fraction_plot(ax, benchmarks, ylabel):
    if ylabel:
        ax.set_ylabel("Migration time as a fraction of benchmark run time")
    ax.violinplot([v * 100 for v in data.migration_fraction_by_benchmark(benchmarks)],
                  showmedians=True, widths=1)
    ax.set_xticks(range(1, len(benchmarks) + 1))
    ax.set_xticklabels(benchmarks, rotation='45')
    yticks = mtick.PercentFormatter()
    ax.yaxis.set_major_formatter(yticks)

fraction_plot(ax1, benchmarks=['backprop', 'bfs', 'b+tree', 'gaussian', 'heartwall',
                               'hybridsort', 'kmeans', 'lavaMD', 'lud', 'myocyte', 'nn', 'nw',
                               'pathfinder', 'srad'], ylabel=True)
fraction_plot(ax2, benchmarks=["dwt2d"], ylabel=False)

fig.set_size_inches(3.5, 1.75)
plt.savefig("factor_plot.pdf", bbox_inches='tight')
# plt.show()


ax1: plt.Axes
ax2: plt.Axes
fig: plt.Figure
fig, (ax1, ax2) = plt.subplots(ncols=2, gridspec_kw = {'width_ratios':[13, 2]})

def time_plot(ax, benchmarks, ylabel):
    if ylabel:
        ax.set_ylabel("Migration time (ms)")
    ax.tick_params('y', pad=0.1)
    # plt.setp(ax.yaxis.get_majorticklabels(), rotation=45)
    d = data.migration_time_by_benchmark(benchmarks)
    ax.violinplot(d, showmedians=True, widths=1, showextrema=False)
    for i, dd in enumerate(d):
        ax.vlines(i+1, min(dd), max(dd), color='b', linestyle='-', lw=0.5)
    ax.set_xticks(range(1, len(benchmarks) + 1))
    ax.set_xticklabels(benchmarks, rotation='45', ha="right")

time_plot(ax1, benchmarks=['backprop', 'bfs', 'b+tree', 'gaussian', 'heartwall',
                               'hybridsort', 'lavaMD', 'lud', 'nn', 'nw',
                               'pathfinder', 'srad', "dwt2d", ], ylabel=True)
time_plot(ax2, benchmarks=['myocyte', 'kmeans'], ylabel=False)

fig.set_size_inches(3, 1)
plt.savefig("time_plot.pdf", bbox_inches='tight', pad_inches=0)

for b in data.benchmarks:
    print("{}: {}".format(b, len(data.migration_time_by_benchmark([b])[0])))
