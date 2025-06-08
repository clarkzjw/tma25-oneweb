# flake8: noqa: E501

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["timezone"] = "America/Chicago"

# use default color cycle
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=plt.cm.tab10.colors)

# Load data. Some data will be interrupted, incomplete, etc; see the parsing errors for details.
# This is mostly test runs which were cancelled early, or even empty runs where the server was temporarily unavailable.

protocols = ["tcp_bbr", "tcp_cubic", "tcp_reno", "udp"]
directions = ["uplink", "downlink"]
data_dir = Path("../data/throughput")

df = pd.DataFrame()


def split_json_by_braces(text):
    lines = text.splitlines()
    jsons = []
    current = []

    for line in lines:
        if line == "{":
            current = [line]
        elif line == "}":
            current.append(line)
            jsons.append("\n".join(current))
            current = []
        else:
            current.append(line)

    return jsons


def load_iperf3_data(filepath: str, direction: str, concat_with=None) -> pd.DataFrame:
    """Load iperf3 uplink data from json and return a DataFrame."""

    jstrings = split_json_by_braces(open(filepath).read())
    jdatas = [json.loads(j) for j in jstrings]
    dfs = []

    for i, jdata in enumerate(jdatas):
        try:
            start_time = jdata["start"]["timestamp"]["timesecs"]
            results = {
                "start_time": [],
                "timestamp": [],
                "protocol": [],
                "direction": [],
                "tcp_cc_algo": [],
                "mbits_per_second": [],
                "bytes_sent": [],
                "tcp_cwnd_megabytes": [],
                "retransmissions": [],
                "udp_lost_packets": [],
                "udp_lost_percent": [],
            }

            for interval, server_interval in zip(
                jdata["intervals"], jdata["server_output_json"]["intervals"]
            ):
                timestamp = start_time + interval["sum"]["start"]

                if direction == "downlink":
                    sender_interval = server_interval
                    receiver_interval = interval
                elif direction == "uplink":
                    sender_interval = interval
                    receiver_interval = server_interval

                mbits_per_second = receiver_interval["sum"]["bits_per_second"] / 1e6

                if jdata["start"]["test_start"]["protocol"] == "UDP":
                    udp_lost_packets = receiver_interval["sum"]["lost_packets"]
                    udp_lost_percent = receiver_interval["sum"]["lost_percent"]
                    retransmissions = None
                    tcp_cwnd_megabytes = None
                    bytes_sent = sender_interval["sum"]["bytes"]
                    protocol = "udp"
                    tcp_cc_algo = None
                elif jdata["start"]["test_start"]["protocol"] == "TCP":
                    udp_lost_packets = None
                    udp_lost_percent = None
                    retransmissions = sender_interval["sum"]["retransmits"]
                    tcp_cwnd_megabytes = sender_interval["streams"][0]["snd_cwnd"] / 1e6
                    bytes_sent = sender_interval["sum"]["bytes"]
                    protocol = "tcp"
                    tcp_cc_algo = jdata["end"]["sender_tcp_congestion"]

                results["protocol"].append(protocol)
                results["direction"].append(direction)
                results["tcp_cc_algo"].append(tcp_cc_algo)
                results["start_time"].append(start_time)
                results["timestamp"].append(timestamp)
                results["bytes_sent"].append(bytes_sent)
                results["mbits_per_second"].append(mbits_per_second)
                results["retransmissions"].append(retransmissions)
                results["tcp_cwnd_megabytes"].append(tcp_cwnd_megabytes)
                results["udp_lost_packets"].append(udp_lost_packets)
                results["udp_lost_percent"].append(udp_lost_percent)

            df = pd.DataFrame(results)
            df["start_time"] = (
                pd.to_datetime(df["start_time"], unit="s", utc=True)
                .dt.tz_convert("america/chicago")
                .dt.strftime("%Y-%m-%d %I:%M:%S %p")
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
            dfs.append(df)
        except Exception as e:
            print(f"{type(e).__name__} processing JSON Data #{i} from {filepath}: {e}")
            # print(f"  JSON was: {jdata}")
            continue

    df = pd.concat(dfs, ignore_index=True)
    if concat_with is not None:
        df = pd.concat([df, concat_with], ignore_index=True)
    return df


for protocol in protocols:
    for direction in directions:
        try:
            df = load_iperf3_data(
                str(data_dir / f"{protocol}_{direction}.log"), direction, concat_with=df
            )
        except Exception as e:
            print(f"Error loading {protocol}_{direction}: {e}")
            continue

# combine protocol and congestion control algorithm into one column for name
df["full_proto_name"] = df["protocol"].apply(lambda x: x.upper()) + df[
    "tcp_cc_algo"
].apply(lambda x: " " + x.upper() if x else "")
df["full_proto_name"] = df["full_proto_name"].replace("TCP RENO", "TCP Reno")

df_sum_bytime = df.groupby(
    ["start_time", "full_proto_name", "direction"], dropna=False
).agg({"mbits_per_second": ["mean"]})
df_sum_bytime.reset_index(inplace=True)
df_sum_bytime.columns = df_sum_bytime.columns.get_level_values(0)

# remove egregious outliers which are a result of abnormal, non-congestion control behavior
df_sum_bytime = df_sum_bytime[
    (df_sum_bytime["mbits_per_second"] >= 50) | (df_sum_bytime["direction"] == "uplink")
]

# Next, we'll combine all the measurements for each protocol and direction
df_sum = df_sum_bytime.groupby(["full_proto_name", "direction"], dropna=False).agg(
    {"mbits_per_second": ["mean", "std"]}
)
df_sum = df_sum.reindex(["UDP", "TCP BBR", "TCP Reno", "TCP CUBIC"], level=0)
df_sum.reset_index(inplace=True)

mean_df = df_sum.pivot(
    index="full_proto_name", columns="direction", values=("mbits_per_second", "mean")
)
std_df = df_sum.pivot(
    index="full_proto_name", columns="direction", values=("mbits_per_second", "std")
)

# sort according to protocol: UDP, TCP BBR, TCP Reno, TCP CUBIC
mean_df = mean_df.reindex(["UDP", "TCP BBR", "TCP Reno", "TCP CUBIC"])
std_df = std_df.reindex(["UDP", "TCP BBR", "TCP Reno", "TCP CUBIC"])

fig, ax = plt.subplots(figsize=(5, 3.5))

x = np.arange(len(mean_df))  # label locations
width = 0.3  # width of the bars

# Plot data
bar1 = ax.bar(
    x - width / 2,
    mean_df["downlink"],
    width,
    yerr=std_df["downlink"],
    label="Downlink",
    capsize=5,
    color="C0",
)
bar2 = ax.bar(
    x + width / 2,
    mean_df["uplink"],
    width,
    yerr=std_df["uplink"],
    label="Uplink",
    capsize=5,
    color="C1",
)

ax.set_ylabel("Throughput (Mbps)")
ax.set_xticks(x)
ax.set_xticklabels(mean_df.index, rotation=0)
ax.set_yticks(np.arange(0, 101, 20))
ax.yaxis.grid(True, linestyle="--", alpha=0.7, zorder=0)
ax.set_axisbelow(True)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2, frameon=True)

plt.tight_layout()
plt.savefig("fig7.png", dpi=300, bbox_inches="tight")
