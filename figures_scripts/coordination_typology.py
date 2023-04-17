# -*- coding: utf-8 -*-

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
from matplotlib.markers import MarkerStyle

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (21,13)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 21.5

# import datasets
data = pd.read_csv("datasets_manual/coordination_typology.csv", sep=";")


### 1 ### Visualise a map

# create a new geographical figure
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree())

# set the outlines of the map
ax.coastlines()
ax.add_feature(cfeature.OCEAN, zorder=0, edgecolor="white")
ax.add_feature(cfeature.LAND, zorder=0, edgecolor="white")
ax.set_extent((2, 51, 48, 25))

# create the scatter
subset = data[data["Strategy"] == "post"].copy()
ax.scatter(subset["Longitude"], subset["Latitude"], s=250, linewidth=2, edgecolor="black", zorder=1, label="'-que' strategy")

subset = data[data["Strategy"].isin(["both","medial"])].copy()
ax.scatter(subset["Longitude"], subset["Latitude"], s=250, linewidth=2, edgecolor="black", zorder=1, label="'et' strategy")

subset = data[data["Strategy"] == "both"].copy()
ax.scatter(subset["Longitude"], subset["Latitude"], s=150, marker=MarkerStyle('o', fillstyle='left'), c='#1f77b4', zorder=2)

# add a legend
ax.legend(prop={'size': 24})

# add language labels
txts = []
for l,lat,lon in zip(list(data["Language"]),list(data["Latitude"]),list(data["Longitude"])):
    txts.append(ax.text(lon+0.5,lat,l))

# adjust language labels
for txt in txts:
    if txt.get_text() in ["Old Persian", "Avestan"]:
        txt.remove()
    if txt.get_text() in ["Sumerian", "Punic", "Oscan", "Latin", "Coptic", "Ancient North Arabian", "Lydian"]:
        txt.set_position((txt.get_position()[0]-2, txt.get_position()[1]-1))
    if txt.get_text() in ["Lycian", "Luwian", "Hurrian", "Middle Persian"]:
        txt.set_position((txt.get_position()[0]-1.5, txt.get_position()[1]-1.2))
    if txt.get_text() in ["Elamite", "Phrygian", "Etruscan", "Gothic", "Messapic", "Venetic"]:
        txt.set_position((txt.get_position()[0]-1.5, txt.get_position()[1]+0.7))
    if txt.get_text() in ["Greek"]:
        txt.set_position((txt.get_position()[0]-1.8, txt.get_position()[1]+0.7))
    if txt.get_text() in ["Egyptian"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]+0.2))
    if txt.get_text() in ["Palaic"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]-0.2))
    if txt.get_text() in ["Mycenaean"]:
        txt.set_position((txt.get_position()[0]-3, txt.get_position()[1]-1.5))
    if txt.get_text() in ["Carian"]:
        txt.set_position((txt.get_position()[0]-1, txt.get_position()[1]+0.7))
    if txt.get_text() in ["Proto-North-West Caucasian"]:
        txt.set_position((txt.get_position()[0]-9, txt.get_position()[1]))
    if txt.get_text() in ["Proto-North-East Caucasian"]:
        txt.set_position((txt.get_position()[0]-7, txt.get_position()[1]+0.7))
    if txt.get_text() in ["Proto-Kartvelian"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]-0.7))
    if txt.get_text() in ["Hittite"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]-0.5))


### 2 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# show the figure and save it
plt.savefig('figures/coordination_typology.pdf', bbox_inches=bbox, dpi=600)
plt.show()
