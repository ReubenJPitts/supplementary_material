
"""
Output: Figure coordination_typology.png
Used in: Chapter 8
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (21,13)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 16

# set size of markers
marker_size = 80
marker_edge = 1

# import datasets
wals = pd.read_csv("WALS/values.csv", sep=",")
lang = pd.read_csv("WALS/languages.csv", sep=",")

# modify and combine
wals = wals[wals["Parameter_ID"] == "83A"]
wals = wals.merge(lang, how="left", left_on="Language_ID", right_on="ID", suffixes=("","_languages"))


### 1 ### Visualise a map

# create a new geographical figure
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree())

# set the outlines of the map
ax.coastlines()
ax.add_feature(cfeature.OCEAN, zorder=0, edgecolor="white")
ax.add_feature(cfeature.LAND, zorder=0, edgecolor="white")
#ax.set_extent((-120, 180, 80, -80))

# create the scatter
subset = wals[wals["Value"] == 1].copy()
ax.scatter(subset["Longitude"], subset["Latitude"], s=marker_size, linewidth=marker_edge, edgecolor="black", zorder=1, label="Object precedes Verb")

subset = wals[wals["Value"] == 2].copy()
ax.scatter(subset["Longitude"], subset["Latitude"], s=marker_size, linewidth=marker_edge, edgecolor="black", zorder=1, label="Object follows Verb")

# add a legend
ax.legend(prop={'size': 22}, loc="lower left")


### 3 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# show the figure
plt.savefig('figures/object_order_typology.pdf', bbox_inches=bbox, dpi=600)
plt.show()