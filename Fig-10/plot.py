import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta

sys.path.append("../common/")
from ping import load_ping


filename = "../data/ping-oneweb-norway-250222.txt"

rtt_ts, rtt = load_ping(filename)


fig = plt.figure(figsize=(5, 4))

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["font.size"] = 16

ax = fig.add_subplot(111)
ax.ecdf(rtt, label="RTT")
ax.set_xlabel("RTT (ms)")
ax.set_ylabel("CDF")
ax.set_xlim(0, 300)
# ax.legend(loc="upper right")
plt.tight_layout()
plt.savefig("10a.png")
