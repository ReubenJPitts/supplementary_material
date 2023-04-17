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
plt.rcParams['font.size'] = 19

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
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree())

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
    txts.append(ax.text(lon+0.4+((5-t)/10),lat,l))

# adjust language labels
for txt in txts:
    
    # language markers to be deleted
    if txt.get_text() in ["Old Persian"]:
        txt.remove()
        
    # language markers to move:
    if txt.get_text() in ["Elamite", "Celtiberian", "Egyptian", "Greek", "Macedonian"]:
        txt.set_position((txt.get_position()[0]-3, txt.get_position()[1]+0.8))
    if txt.get_text() in ["Hebrew"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]-0.5))
    if txt.get_text() in ["Rhaetic"]:
        txt.set_position((txt.get_position()[0]-2, txt.get_position()[1]+0.8))
    if txt.get_text() in ["Galatian"]:
        txt.set_position((txt.get_position()[0]-0.5, txt.get_position()[1]-0.8))
    if txt.get_text() in ["Sidetic"]:
        txt.set_position((txt.get_position()[0]-0.3, txt.get_position()[1]+0.3))
    if txt.get_text() in ["Milyan"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]-0.7))
    if txt.get_text() in ["Pisidian"]:
        txt.set_position((txt.get_position()[0]-1.7, txt.get_position()[1]+0.6))   
    if txt.get_text() in ["Luwian"]:
        txt.set_position((txt.get_position()[0]-2.5, txt.get_position()[1]+0.8))
    if txt.get_text() in ["Phrygian"]:
        txt.set_position((txt.get_position()[0]-2, txt.get_position()[1]+0.8))
    if txt.get_text() in ["Messapic"]:
        txt.set_position((txt.get_position()[0]-2, txt.get_position()[1]+0.7))
    if txt.get_text() in ["Lemnian"]:
        txt.set_position((txt.get_position()[0]-2.4, txt.get_position()[1]-0.8))
    if txt.get_text() in ["Numidian"]:
        txt.set_position((txt.get_position()[0]-4.5, txt.get_position()[1]-0.4))
    if txt.get_text() in ["Lydian"]:
        txt.set_position((txt.get_position()[0]-2, txt.get_position()[1]-1))
    if txt.get_text() in ["Carian"]:
        txt.set_position((txt.get_position()[0]-1.3, txt.get_position()[1]+0.7))
    if txt.get_text() in ["Elymian"]:
        txt.set_position((txt.get_position()[0]-3.7, txt.get_position()[1]))
    if txt.get_text() in ["Sicel"]:
        txt.set_position((txt.get_position()[0]-1.5, txt.get_position()[1]+0.8))
    if txt.get_text() in ["Lycian"]:
        txt.set_position((txt.get_position()[0]-2.7, txt.get_position()[1]-1.2))
    if txt.get_text() in ["Tartessian"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]+0.3))
    if txt.get_text() in ["Sicanian"]:
        txt.set_position((txt.get_position()[0]-3, txt.get_position()[1]-0.7))
    if txt.get_text() in ["Thracian"]:
        txt.set_position((txt.get_position()[0]-1, txt.get_position()[1]+0.8))
    if txt.get_text() in ["Punic"]:
        txt.set_position((txt.get_position()[0], txt.get_position()[1]-0.6))
    if txt.get_text() in ["Iberian"]:
        txt.set_position((txt.get_position()[0]-2, txt.get_position()[1]+0.6))
    if txt.get_text() in ["Lepontic"]:
        txt.set_position((txt.get_position()[0]-4, txt.get_position()[1]))
    if txt.get_text() in ["Venetic"]:
        txt.set_position((txt.get_position()[0]-0.7, txt.get_position()[1]+0.7))
    if txt.get_text() in ["Etruscan"]:
        txt.set_position((txt.get_position()[0]-4.3, txt.get_position()[1]-0.3))
    if txt.get_text() in ["Latin"]:
        txt.set_position((txt.get_position()[0]-3.2, txt.get_position()[1]-0.3))
    if txt.get_text() in ["Oscan"]:
        txt.set_position((txt.get_position()[0]-3, txt.get_position()[1]+0.3))
    if txt.get_text() in ["Umbrian"]:
        txt.set_position((txt.get_position()[0]-0.2, txt.get_position()[1]-0.15))
    if txt.get_text() in ["Old Sabellic"]:
        txt.set_position((txt.get_position()[0]-2.7, txt.get_position()[1]+0.55))
 
# add a legend
ax.legend(prop={'size': 22})


### 3 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# show the figure and save it
plt.savefig('figures/mediterranean_diversity.pdf', bbox_inches=bbox, dpi=600)
plt.show()
