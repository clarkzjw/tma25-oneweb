import sys

import matplotlib.pyplot as plt

sys.path.append("../common/")
from ping import load_ping


fontsize = 16
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams.update({"font.size": fontsize})
plt.rcParams.update({"axes.labelsize": fontsize})
plt.rcParams.update({"xtick.labelsize": fontsize})
plt.rcParams.update({"ytick.labelsize": fontsize})


filename = "../data/ping-10ms-60m-2024-11-30-05-00-00.txt"
ts, rtt = load_ping(filename)

figsize = (5, 4)
fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111)
ax.ecdf(rtt, label="RTT")
ax.set_xlabel("RTT (ms)")
ax.set_ylabel("CDF")
ax.set_xlim(0, 300)
plt.tight_layout()
plt.savefig("alaska_rtt_cdf.eps")
plt.savefig("alaska_rtt_cdf.png")
