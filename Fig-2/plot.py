import json
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

fontsize = 14
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams.update({"font.size": fontsize})
plt.rcParams.update({"axes.labelsize": fontsize})

lonW = 0
lonE = -180
latS = 0
latN = 90
centralLat = (latN + latS) / 2
centralLon = (lonW + lonE) / 2

resolution = "110m"
projPlateCarree = ccrs.PlateCarree()

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection=projPlateCarree)
ax.coastlines(resolution=resolution, color="gray")
ax.set_extent([-178, 180, -90, 90], crs=projPlateCarree)

snp_filename = "./oneweb-snp.csv"
with open(snp_filename, "r") as f:
    for line in f.readlines():
        lon = float(line.split(",")[0])
        lat = float(line.split(",")[1])
        ax.scatter(lon, lat, s=80, color="red", marker="x")

pop_filename = "./oneweb-pop.json"
with open(pop_filename, "r") as f:
    data = f.read()
    for node in json.loads(data):
        if node["type"] == "pop":
            lat = node["lat"]
            lon = node["lon"]
            ax.scatter(lon, lat, s=80, color="blue", marker="+")

ax.scatter(-180, 0, s=80, color="red", marker="x", label="OneWeb SNP")
ax.scatter(-180, 0, s=80, color="blue", marker="+", label="OneWeb PoP")
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig("oneweb-snp-pop.png")
