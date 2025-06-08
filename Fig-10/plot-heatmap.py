import sys
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime

sys.path.append("../common/")
from ping import load_ping

latency = []
timestamps = []
ts, rtt = load_ping("../data/ping-oneweb-ut-eur-250222-040850.txt")

latency = np.array(rtt)
timestamps = np.array(ts)

datetimes = pd.to_datetime(timestamps)
df = pd.DataFrame({"Datetime": datetimes, "Value": latency})

df["Date"] = df["Datetime"].dt.date
df["Hour"] = df["Datetime"].dt.hour
df["Minute"] = df["Datetime"].dt.minute
df["Second"] = df["Datetime"].dt.second
dates = df["Date"].unique()
hours = df["Hour"].unique()

figsize = (10, 8)
fontsize = 26
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams.update({"font.size": fontsize})
plt.rcParams.update({"axes.labelsize": fontsize})
plt.rcParams.update({"xtick.labelsize": fontsize})
plt.rcParams.update({"ytick.labelsize": fontsize})

for date in dates:
    df_daily = df[df["Date"] == date]
    if date == datetime.date(2025, 2, 22):
        for hour in hours:
            if int(hour) == np.int32(5):
                df_hourly = df_daily[df_daily["Hour"] == hour]
                df_grouped = df_hourly.groupby(["Minute", "Second"]).min().reset_index()

                heatmap_data = df_grouped.pivot(
                    index="Minute", columns="Second", values="Value"
                )
                day = df["Date"].iloc[0]
                plt.figure(figsize=figsize)
                color = plt.get_cmap("viridis")
                color.set_bad("lightblue")
                sns.heatmap(
                    heatmap_data,
                    cmap=color,
                    cbar_kws={"label": "minRTT (ms)"},
                    vmin=80,
                    vmax=150,
                )
                plt.xlabel("Second")
                plt.ylabel("Minute of the hour")
                plt.tight_layout()
                plt.savefig("10b.png")
