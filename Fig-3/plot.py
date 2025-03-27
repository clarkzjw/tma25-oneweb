# flake8: noqa: E501

import sys
from datetime import timedelta

from matplotlib import pyplot as plt
from matplotlib import dates as mdates

sys.path.append("../common/")
from ping import load_ping
from aim import process_aim_file

ts, rtt = load_ping("../data/ping-oneweb-gw-250306-120000.txt")
aim = process_aim_file("../data/AIM_355866000274220_2025_03_06_19_54_54.csv")

start = ts[0] + timedelta(seconds=447)
end = start + timedelta(seconds=549)

figsize = (20, 6)

fig = plt.figure(figsize=figsize)

fontsize = 16
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams.update({"font.size": fontsize})
plt.rcParams.update({"axes.labelsize": fontsize})
plt.rcParams.update({"xtick.labelsize": fontsize})
plt.rcParams.update({"ytick.labelsize": fontsize})

color1 = "tab:blue"
color2 = "tab:red"

ax1 = fig.add_subplot(111)
ax1.set_ylabel("sin", color=color1)
ax1.plot(ts, rtt, label="RTT", color=color1)

ax1.set_ylim(0, 700)
ax1.set_xlabel("Time")
ax1.set_ylabel("RTT (ms)")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
ax1.xaxis.set_major_locator(mdates.SecondLocator(interval=40))

ax2 = ax1.twinx()
ax2.set_ylabel("sin", color=color2)
ax2.plot(aim.seq_ts, aim.avg_sinr, label="Average SINR (dB)", color=color2)
ax2.set_ylabel("Average SINR (dB)")
ax2.set_ylim(-15, 15)

for i in range(len(aim.handover_ts)):
    if aim.handover_ts[i] < start:
        continue
    if aim.handover_ts[i] > end:
        break
    ax1.axvline(x=aim.handover_ts[i], color="black", linestyle="--", ymax=0.1)
    ax1.text(
        aim.handover_ts[i],
        15,
        f"ONEWEB-0{aim.sat_ids[i]}",
        rotation=0,
        fontsize=fontsize,
    )
ax2.plot([], [], color="black", linestyle="--", label="Inter-satellite handover event")

ax1.set_xlim(start, end)
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("oneweb.eps")
plt.savefig("oneweb.png")
