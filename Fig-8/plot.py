import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["timezone"] = "America/Chicago"

df = pd.read_parquet("../data/throughput/data.parquet")


def plot_udp_throughput_packetloss_handovers(
    ax,
    measurement_group_time_short,
    direction,
    protocol,
    legend=True,
    fontsize=12,
    max_throughput=125,
    plot_range=None,
    time_format="%H:%M",
    title=None,
):
    df_plot = df[
        (df["measurement_group_time_short"] == measurement_group_time_short)
        & (df["direction"] == direction)
        & (df["protocol"] == protocol)
    ]

    if plot_range is not None:
        df_plot = df_plot[df_plot["timestamp"].between(plot_range[0], plot_range[1])]

    ax.plot(
        df_plot["timestamp"], df_plot["mbits_per_second"], label=protocol, linewidth=2
    )

    ax_sinr = ax.twinx()
    ax_sinr.plot(
        df_plot["timestamp"],
        df_plot["aim_average_sinr"],
        label=f"{protocol} % packet loss",
        color="red",
        linewidth=2,
    )

    ax_sinr.set_ylabel("Average SINR (dB)", color="red", fontsize=fontsize)
    ax_sinr.set_ylim((-20, 20))

    # plot satellite handover events
    aim_satellite_id = df_plot["aim_satellite_id"].unique()

    # plot first satellite
    height = -10

    ax.text(
        x=df_plot.iloc[0]["timestamp"],
        y=height,
        s=f"ONEWEB-{int(aim_satellite_id[0]):04}",
        fontsize=fontsize - 6,
        ha="left",
        va="bottom",
    )

    # plot subsequent handovers
    for i in range(1, len(aim_satellite_id)):
        handover_time = df_plot[
            df_plot["aim_satellite_id"] == aim_satellite_id[i]
        ].iloc[0]["timestamp"]
        ax.vlines(
            x=handover_time,
            ymin=-15,
            ymax=0,
            color="black",
            linestyle="--",
            linewidth=0.9,
        )
        # alternate height between -10 and -5
        # height = -15 if height == -10 else -10
        ax.text(
            x=handover_time,
            y=height,
            s=f"-{int(aim_satellite_id[i]):04}",
            fontsize=fontsize - 6,
            ha="left",
            va="bottom",
        )

    # configure axes
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter(time_format))
    ax.set_xlim([df_plot["timestamp"].min(), df_plot["timestamp"].max()])
    ax.set_ylim((-15, max_throughput))
    ax.set_ylabel("Throughput (Mbps)", fontsize=fontsize, color="C0")
    ax.set_xlabel("Time", fontsize=fontsize)

    # set font sizes
    for label in (
        ax.get_xticklabels() + ax.get_yticklabels() + ax_sinr.get_yticklabels()
    ):
        label.set_fontsize(fontsize - 2)

    # add baseline
    ax.axhline(y=0, color="C0", linestyle="--", linewidth=0.7)

    # add legend if requested
    if legend:
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax_sinr.get_legend_handles_labels()
        handover_line = [
            mpl.lines.Line2D([0], [0], color="black", linestyle="--", linewidth=0.9)
        ]
        ax.legend(
            lines + lines2 + handover_line,
            [
                "Throughput (Mbps)",
                "Average SINR (dB)",
                "Inter-satellite handover event",
            ],
            loc=1,
            fontsize=fontsize - 2,
        )


# Create plot
fig, ax = plt.subplots(1, 1, figsize=(9, 3))

plot_range = pd.date_range(
    "2025-03-12 9:23:45", "2025-03-12 9:25:25", tz="America/Chicago", periods=2
)

plot_udp_throughput_packetloss_handovers(
    ax,
    "3/12  9AM",
    "uplink",
    "udp",
    fontsize=12,
    plot_range=plot_range,
    time_format="%H:%M:%S",
)

fig.savefig("8b.png", bbox_inches="tight", dpi=300)


def plot_tcp_throughput_handovers(
    ax,
    measurement_group_time_short,
    direction,
    protocol,
    legend=True,
    fontsize=12,
    max_throughput=125,
    plot_range=None,
    time_format="%H:%M",
    title=None,
):
    # filter data
    df_plot = df[
        (df["measurement_group_time_short"] == measurement_group_time_short)
        & (df["direction"] == direction)
        & (df["protocol"] == protocol)
    ]

    if plot_range is not None:
        df_plot = df_plot[df_plot["timestamp"].between(plot_range[0], plot_range[1])]

    # print(df_plot)

    # plot throughput
    ax.plot(
        df_plot["timestamp"], df_plot["mbits_per_second"], label=protocol, linewidth=2
    )

    # plot tcp_cwnd on twin axis
    ax_cwnd = ax.twinx()
    ax_cwnd.plot(
        df_plot["timestamp"],
        df_plot["tcp_cwnd_megabytes"],
        label=f"{protocol} cwnd",
        color="coral",
        linewidth=2,
    )

    # configure cwnd axis
    ax_cwnd.set_ylabel("TCP cwnd (MB)", color="coral", fontsize=fontsize)
    ax_cwnd.set_ylim((-0.24, 2))

    # plot satellite handover events
    aim_satellite_id = df_plot["aim_satellite_id"].unique()

    # plot first satellite ID
    ax.text(
        x=df_plot.iloc[0]["timestamp"],
        y=-10,
        s=f"ONEWEB-{int(aim_satellite_id[0]):04}",
        fontsize=fontsize - 6,
        ha="left",
        va="bottom",
    )

    # plot subsequent handovers
    for i in range(1, len(aim_satellite_id)):
        handover_time = df_plot[
            df_plot["aim_satellite_id"] == aim_satellite_id[i]
        ].iloc[0]["timestamp"]
        ax.vlines(
            x=handover_time,
            ymin=-15,
            ymax=0,
            color="black",
            linestyle="--",
            linewidth=0.9,
        )
        ax.text(
            x=handover_time,
            y=-10,
            s=f"-{int(aim_satellite_id[i]):04}",
            fontsize=fontsize - 6,
            ha="left",
            va="bottom",
        )

    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter(time_format))
    ax.set_xlim([df_plot["timestamp"].min(), df_plot["timestamp"].max()])
    ax.set_ylim((-15, max_throughput))
    ax.set_ylabel("Throughput (Mbps)", fontsize=fontsize, color="C0")
    ax.set_xlabel("Time", fontsize=fontsize)

    for label in (
        ax.get_xticklabels() + ax.get_yticklabels() + ax_cwnd.get_yticklabels()
    ):
        label.set_fontsize(fontsize - 2)

    ax.axhline(y=0, color="C0", linestyle="--", linewidth=0.7)

    # Add legend if requested
    if legend:
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax_cwnd.get_legend_handles_labels()
        handover_line = [
            mpl.lines.Line2D([0], [0], color="black", linestyle="--", linewidth=0.9)
        ]
        ax.legend(
            lines + lines2 + handover_line,
            ["Throughput (Mbps)", "TCP cwnd (MB)", "Inter-satellite handover event"],
            loc=1,
            fontsize=fontsize,
        )


fig, ax = plt.subplots(1, 1, figsize=(9, 3))

plot_range = pd.date_range(
    "2025-03-13 8:19:00", "2025-03-13 8:20:30", tz="America/Chicago", periods=2
)

plot_tcp_throughput_handovers(
    ax,
    "3/13  7AM",
    "uplink",
    "tcp",
    fontsize=12,
    plot_range=plot_range,
    time_format="%H:%M:%S",
    # max_throughput=80,
)

fig.savefig("8a.png", bbox_inches="tight", dpi=300)
