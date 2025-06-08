import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd

from skyfield.api import load, wgs84
from datetime import datetime, timedelta

sys.path.append("../common/")
from ping import load_ping


def load_tle_data(tle_file):
    satellites = load.tle_file(tle_file)
    print("Loaded", len(satellites), "satellites")
    return {sat.name: sat for sat in satellites}


def plot(
    start,
    sinr_ts,
    sinr_values,
    rtt_ts,
    rtt_values,
):
    fig = plt.figure(layout="constrained", figsize=(9, 3))

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    axRTT = fig.add_subplot(111)
    axRTT.plot(
        rtt_ts,
        rtt_values,
        # label="RTT",
        color="tab:blue",
        linestyle="None",
        marker=".",
        markersize=1,
    )
    axRTT.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    axRTT.set_xlabel("Time")
    axRTT.set_ylabel("RTT (ms)", color="tab:blue")
    axRTT.set_xlim(rtt_ts[0], rtt_ts[-1])
    axRTT.set_ylim(0, 600)

    axSINR = axRTT.twinx()
    axSINR.plot(
        sinr_ts,
        sinr_values,
        label="SINR",
        color="tab:red",
        linestyle="None",
        marker=".",
        markersize=1,
    )
    axSINR.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    axSINR.set_xlabel("Time")
    axSINR.set_ylabel("Average SINR (dB)", color="tab:red")
    axSINR.set_ylim(0, 20)

    handover_ts = {
        "2025-03-14T20:50:29+00:00": "ONEWEB-0680",
        "2025-03-14T20:52:55+00:00": "ONEWEB-0714",
        "2025-03-14T20:55:02+00:00": "ONEWEB-0615",
        "2025-03-14T20:57:24+00:00": "ONEWEB-0528",
        "2025-03-14T20:59:35+00:00": "",
    }
    for ts in handover_ts:
        axSINR.axvline(
            x=datetime.fromisoformat(ts),
            color="black",
            linestyle="--",
            ymax=0.1,
        )
        axSINR.text(
            datetime.fromisoformat(ts),
            0.8,
            handover_ts[ts],
            rotation=0,
            fontsize=10,
        )

    axRTT.plot(
        [],
        [],
        color="tab:red",
        linestyle="solid",
        label="Average SINR (dB)",
        marker="None",
    )
    axRTT.plot(
        [],
        [],
        color="black",
        linestyle="dashed",
        label="Inter-satellite handover event",
        marker="None",
    )

    axRTT.legend(loc="upper right")

    for label in (
        axRTT.get_xticklabels() + axRTT.get_yticklabels() + axSINR.get_yticklabels()
    ):
        label.set_fontsize(10)

    plt.tight_layout()
    plt.savefig("fig9.png")
    plt.close()


dish_model = "intellian"

json_directory = "./satellites"
tle_file = "../data/ut-eur/oneweb_tle_2025-03-14T20_22_17Z.txt"
ping_file = (
    "../data/ut-eur/ping-svalbard--85.199.204.3-10ms-60m-2025-03-14-20-20-51.txt"
)
observer_alt = 0

rtt_ts, rtt_values = load_ping(ping_file)

dt = "2025-03-14-"

sinr_data = "../data/ut-eur/aim.parquet"
df = pd.read_parquet(sinr_data)
df.loc[df["sinr_aim_manager_log"] == -100, "sinr_aim_manager_log"] = None
df.head()

series = pd.Series(df["sinr_aim_manager_log"].values, index=df["timestamp"])
series = series.resample("0.1s").mean()
series.ffill(inplace=True)
df2 = pd.DataFrame(
    {
        "timestamp": series.index,
        "sinr_aim_manager_log": series.values,
    }
)

start = datetime.fromisoformat("2025-03-14T20:50:07+00:00")
df2["timestamp"] = pd.to_datetime(df2["timestamp"], unit="ms")
df2 = df2[
    (df2["timestamp"] > pd.to_datetime(start).to_datetime64())
    & (df2["timestamp"] < pd.to_datetime(start + timedelta(minutes=10)).to_datetime64())
]

df_rtt = pd.DataFrame(
    {
        "timestamp": rtt_ts,
        "rtt": rtt_values,
    }
)
df_rtt["timestamp"] = pd.to_datetime(df_rtt["timestamp"], unit="ms")
df_rtt = df_rtt[
    (df_rtt["timestamp"] > start)
    & (df_rtt["timestamp"] < start + timedelta(minutes=10))
]

plot(
    start,
    df2["timestamp"].tolist(),
    df2["sinr_aim_manager_log"].tolist(),
    df_rtt["timestamp"].tolist(),
    df_rtt["rtt"].tolist(),
)
