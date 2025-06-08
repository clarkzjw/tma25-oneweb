# flake8: noqa: E501

import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

sys.path.append("../common/")
from ping import load_ping


fontsize = 16
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams.update({"font.size": fontsize})
plt.rcParams.update({"axes.labelsize": fontsize})
plt.rcParams.update({"xtick.labelsize": fontsize})
plt.rcParams.update({"ytick.labelsize": fontsize})


def plot_cdf(ts, rtt):
    start = datetime.datetime(2025, 1, 12, 0, 0).replace(tzinfo=datetime.timezone.utc)
    end = start + datetime.timedelta(hours=24)

    series = pd.Series(rtt, index=ts)
    series = series[start:end]

    figsize = (5, 4)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.ecdf(series.values, label="RTT")
    ax.set_xlabel("RTT (ms)")
    ax.set_ylabel("CDF")
    ax.set_xlim(0, 300)
    plt.tight_layout()
    plt.savefig("5a.png")


def plot_heatmap(ts, rtt):
    date = "2025-01-12"
    figsize = (10, 8)
    fontsize = 26

    plt.rcParams.update({"font.size": fontsize})
    plt.rcParams.update({"axes.labelsize": fontsize})
    plt.rcParams.update({"xtick.labelsize": fontsize})
    plt.rcParams.update({"ytick.labelsize": fontsize})

    df = pd.DataFrame({"Datetime": pd.to_datetime(ts), "Value": rtt})
    df["Date"] = df["Datetime"].dt.date
    df["Hour"] = df["Datetime"].dt.hour
    df["Minute"] = df["Datetime"].dt.minute

    df = df[df["Date"] == pd.Timestamp(date).date()]
    df_grouped = df.groupby(["Hour", "Minute"]).min().reset_index()

    heatmap = df_grouped.pivot(index="Hour", columns="Minute", values="Value")

    plt.figure(figsize=figsize)
    sns.heatmap(heatmap, cmap="viridis", cbar_kws={"label": "minRTT (ms)"})
    plt.xlabel("Minute")
    plt.ylabel("Hour of Day")
    plt.tight_layout()
    plt.savefig("5b.png")


if __name__ == "__main__":
    filename = "../data/ping-oneweb-gw-arawireless-250107-075911.txt"
    ts, rtt = load_ping(filename)
    plot_cdf(ts, rtt)
    plot_heatmap(ts, rtt)
