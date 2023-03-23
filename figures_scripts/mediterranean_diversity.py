# -*- coding: utf-8 -*-

"""
Output: Figure mediterranean_diversity.png
Used in: Chapter 2
Author: Reuben J. Pitts
Date: 14/03/2023
"""


### 0 ### Imports

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'

# import datasets
data = pd.read_csv("datasets_manual/mediterranean_diversity.csv", sep=";")


### 1 ### Enrich the dataset

# clean the data
data = data[data["Relevant"] == 1]

# add a column specifying marker size for attestation
data["Size"] = [(1/i)*600 for i in list(data["Type"])]

# add a column specifying colour for attestation
colour_types = ["#19b10b","#d5d813","#f1ae1e","#f66055"]
data["Colour"] = [colour_types[i-1] for i in list(data["Type"])]


### 2 ### Create a map

# create a new geographical figure
fig, ax = plt.subplots(figsize=(25,20), subplot_kw={"projection": ccrs.PlateCarree()})

# set the outlines of the map
ax.coastlines()
ax.add_feature(cfeature.OCEAN, zorder=0, edgecolor="white")
ax.add_feature(cfeature.LAND, zorder=0, edgecolor="white")
ax.set_extent((-10, 50, 50, 25))

# create the scatter plot
for i,a in enumerate(["excellent","good","intermediate","poor"]):
    subset = data[data["Type"] == i+1].copy()
    ax.scatter(subset["Longitude"], subset["Latitude"], color=subset["Colour"], s=subset["Size"], alpha=1, linewidth=2, edgecolor="black", zorder=1, label=a)

# add language labels
txts = []
for l,lat,lon,t in zip(list(data["Name"]), list(data["Latitude"]), list(data["Longitude"]), list(data["Type"])):
    txts.append(ax.text(lon+0.4+((5-t)/10),lat,l,fontsize="15"))

# adjust language labels
for txt in txts:
    # language markers to be deleted
    if txt.get_text() in ["Old Persian"]:
        txt.remove()
    # language markers to be shifted down only
    if txt.get_text() in ["Iberian", "Hebrew", "Lemnian", "Greek", "Sicel", "Latin", "Punic", "Milyan", "Sidetic", "Galatian"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]-0.5))
    # language markers to be shifted left and up
    if txt.get_text() in ["Lepontic", "Elamite", "Luwian", "Elymian", "Etruscan"]:
        txt.set_position((txt.get_position()[0]-3, txt.get_position()[1]+0.5))
    # language markers to be centred below
    if txt.get_text() in ["Messapic", "Numidian", "Sicanian", "Phrygian"]:
        txt.set_position((txt.get_position()[0]-2, txt.get_position()[1]-1))
    # language markers to be shifted left below
    if txt.get_text() in ["Lycian"]:
        txt.set_position((txt.get_position()[0]-3, txt.get_position()[1]-1))

# add a legend
ax.legend(prop={'size': 22})

# show the figure and save it
plt.savefig('figures/mediterranean_diversity.png', bbox_inches='tight', dpi=600)
plt.show()
