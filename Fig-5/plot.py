import sys

import pandas as pd
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


filename = "../data/ping-oneweb-gw-arawireless-250107-075911.txt"
ts, rtt = load_ping(filename)

start = ts[0]
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
plt.savefig("iowa_rtt_cdf.eps")
plt.savefig("iowa_rtt_cdf.png")
