# -*- coding: utf-8 -*-

"""
Output: Figure sabellic_locative.png
Used in: Chapter 7
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

### 0 ### Preliminaries

# import some required libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (20,30)
plt.rcParams.update({'font.size': 16})

# import the dataset
locative = pd.read_csv(r"datasets_automatic/locative_dataset.csv", sep=";")

# set rightshift
rightshift = 0.2


### 1 ### Create a map

# set a projection which verticalises Italy
fig, axs = plt.subplots(1, 2, subplot_kw={"projection": ccrs.PlateCarree()})

# set ax names
titles = ["Inscriptions before 400 BCE","Inscriptions after 400 BCE"]

# iterate over axes
for i, ax in enumerate(axs):

    # get the dataframe with the relevant information
    data = locative[locative["Old"] == [1,0][i]].copy()

    # set the outlines of the map
    ax.coastlines()
    ax.add_feature(cfeature.OCEAN, zorder=0, edgecolor="white")
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor="white")
    ax.set_extent((11, 18.55, 46.5, 37.5), crs=ccrs.PlateCarree())

    subset = data[data["Isogloss"] == 0].copy()
    ax.scatter(subset["Longitude"], subset["Latitude"], s=250, linewidth=2, edgecolor="black", zorder=1, transform=ccrs.PlateCarree(), label="old locative")

    subset = data[data["Isogloss"] == 1].copy()
    ax.scatter(subset["Longitude"], subset["Latitude"], s=250, linewidth=2, edgecolor="black", zorder=1, transform=ccrs.PlateCarree(), label="renewed locative")
   
    subset = data[data["Isogloss"] == 0].copy()
    ax.scatter(subset["Longitude"], subset["Latitude"], s=150, marker=MarkerStyle('o', fillstyle='left'), c='#1f77b4', zorder=2)
   
    # set titles
    ax.set_title(titles[i])
    
    # set a legend
    ax.legend(loc="upper right")

# reduce the size between the subplots
plt.subplots_adjust(wspace=0.01)


### 2 ### Export and save
plt.savefig('figures/sabellic_locative.png', bbox_inches='tight', dpi=600)
plt.show()





