import sys
from matplotlib import pyplot as plt

sys.path.append("../common/")
from ping import load_ping

fontsize = 18
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams.update({"font.size": fontsize})
plt.rcParams.update({"axes.labelsize": fontsize})
plt.rcParams.update({"xtick.labelsize": fontsize})
plt.rcParams.update({"ytick.labelsize": fontsize})

latency = {
    "Alaska": "../data/ping-10ms-60m-2024-11-30-05-00-00.txt",
    "Midwestern USA": "../data/ping-oneweb-gw-arawireless-250107-075911.txt",
    "UT-EUR": "../data/ping-oneweb-norway-250222.txt",
}

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
for region, file in latency.items():
    ts, rtt = load_ping(file)
    ax.ecdf(rtt, label=region, linewidth=2)

ax.set_xlabel("RTT (ms)")
ax.set_ylabel("CDF")
ax.set_xlim(0, 250)
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("latency-cdf.png")
