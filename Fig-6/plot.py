import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["timezone"] = "America/Chicago"

df = pd.read_parquet("../data/throughput/data.parquet")


def plot_tcp_throughput_cwnd(
    ax,
    measurement_group_time_short,
    dir,
    proto,
    cc_algo,
    legend=True,
    fontsize=12,
    max_throughput=125,
    sinr=False,
):
    # filter the dataframe for the current measurement_group_time_short, direction, protocol and cc_algo
    df_plot = df[
        (df["measurement_group_time_short"] == measurement_group_time_short)
        & (df["direction"] == dir)
        & (df["protocol"] == proto)
        & (df["tcp_cc_algo"] == cc_algo)
    ]

    # plot throughput
    ax.plot(
        df_plot["timestamp"], df_plot["mbits_per_second"], label=f"{proto} {cc_algo}"
    )

    # also plot tcp_cwnd for TCP on a twinx axis
    ax_cwnd = ax.twinx()
    ax_cwnd.plot(
        df_plot["timestamp"],
        df_plot["tcp_cwnd_megabytes"],
        label=f"{proto} {cc_algo} cwnd",
        color="coral",
        linestyle="-",
        linewidth=1,
    )

    # also plot SINR for TCP on a twinx axis
    if sinr:
        ax_sinr = ax.twinx()
        ax_sinr.plot(
            df_plot["timestamp"],
            df_plot["aim_average_sinr"],
            label="Average SINR (dB)",
            color="red",
            linestyle="-",
            linewidth=1,
        )
        ax_sinr.spines["right"].set_position(("outward", 40))
        ax_sinr.spines["right"].set_visible(True)
        ax_sinr.yaxis.set_label_position("right")
        ax_sinr.yaxis.set_ticks_position("right")
        ax_sinr.set_ylabel("Average SINR (dB)", fontsize=fontsize, color="red")
        # ax_sinr.tick_params(axis="y", colors="purple")
        ax_sinr.set_ylim((-10, 10))

    # now, we want to set a vertical line wherever the aim_satellite_id changes
    aim_satellite_id = df_plot["aim_satellite_id"].unique()
    for i in range(1, len(aim_satellite_id)):
        ax.axvline(
            x=df_plot[df_plot["aim_satellite_id"] == aim_satellite_id[i]].iloc[0][
                "timestamp"
            ],
            color="black",
            linestyle="--",
            linewidth=0.9,
        )

    # chart title with capitalized cc_algo
    if cc_algo == "reno":
        cc_algo_formal = "Reno"
    elif cc_algo == "cubic":
        cc_algo_formal = "CUBIC"
    elif cc_algo == "bbr":
        cc_algo_formal = "BBR"
    else:
        cc_algo_formal = ""

    ax.set_title(f"TCP {cc_algo_formal} {dir}", fontsize=fontsize)

    # change x-axis labels to just be HH:MM:SS
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter("%H:%M"))

    # change twin axis tick labels to have percent sign
    ax.set_ylim((0, max_throughput))
    ax_cwnd.set_ylim((0, 6))
    ax.set_ylabel("Throughput (Mbps)", color="C0", fontsize=fontsize)
    ax_cwnd.set_ylabel("TCP cwnd (MB)", color="coral", fontsize=fontsize)
    ax.set_xlabel("Time", fontsize=fontsize)
    for label in (
        ax.get_xticklabels() + ax.get_yticklabels() + ax_cwnd.get_yticklabels()
    ):
        label.set_fontsize(fontsize - 4)

    if legend:
        lines, labels = ax.get_legend_handles_labels()


def plot_throughput_cc_algo():

    # we'll select specific measurement_group_time_shorts to use for each of the subplots, mapping as follows:
    mapping = {
        ("reno", "downlink"): "3/13  7AM",
        ("reno", "uplink"): "3/13  7AM",
        ("cubic", "downlink"): "3/13  7AM",
        ("cubic", "uplink"): "3/13  7AM",
        ("bbr", "downlink"): "3/13  7AM",
        ("bbr", "uplink"): "3/12  9AM",
    }

    fig, ax = plt.subplots(3, 2, figsize=(20, 10))

    for dir in ["uplink", "downlink"]:
        for cc_algo in ["reno", "cubic", "bbr"]:
            for proto in ["tcp"]:
                ax_plot = ax[
                    0 if cc_algo == "reno" else 1 if cc_algo == "cubic" else 2,
                    0 if dir == "downlink" else 1,
                ]
                measurement_group_time_short = mapping[(cc_algo, dir)]
                df_plot = df[
                    (df["measurement_group_time_short"] == measurement_group_time_short)
                    & (df["direction"] == dir)
                    & (df["protocol"] == proto)
                    & (df["tcp_cc_algo"] == cc_algo)
                ]
                plot_tcp_throughput_cwnd(
                    ax_plot,
                    measurement_group_time_short,
                    dir,
                    proto,
                    cc_algo,
                    legend=False,
                    fontsize=16,
                    max_throughput=145,
                    sinr=True,
                )

    # and now, we manually add a single legend to the bottom of the entire figure
    lines = [
        mpl.lines.Line2D([0], [0], color="black", linestyle="--", linewidth=1.2),
        mpl.lines.Line2D([0], [0], color="blue", linestyle="-", linewidth=1.2),
        mpl.lines.Line2D([0], [0], color="coral", linestyle="-", linewidth=1.2),
        mpl.lines.Line2D([0], [0], color="red", linestyle="-", linewidth=1.2),
    ]
    fig.legend(
        lines,
        [
            "Inter-satellite handover event",
            "Throughput (Mbps)",
            "TCP cwnd (MB)",
            "Average SINR (dB)",
        ],
        loc=8,
        bbox_to_anchor=(0.5, -0.05),
        fontsize=15,
        ncol=4,
    )

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.4, wspace=0.3)
    fig.subplots_adjust(top=0.92)

    # save figure using modified measurement group time short
    measurement_group_time_short = measurement_group_time_short.replace("/", "_")
    fig.savefig(
        "tcp_cc_algo.png",
        bbox_inches="tight",  # This ensures all elements are included
        dpi=300,  # Increase resolution
        pad_inches=0.3,
    )  # Add padding around the figure


plot_throughput_cc_algo()
