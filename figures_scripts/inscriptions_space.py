# -*- coding: utf-8 -*-

"""
Output: Figure inscriptions_space.png
Used in: Chapter 2
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (21,13)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 18

# import datasets
data = pd.read_csv("datasets_manual/italian_epigraphy.csv", sep=";")


### 1 ### Process the data

# add some columns
data["date_average"] = [(i+j)/2 for i,j in zip(list(data["date_after"]),list(data["date_before"]))]
data["date_range"] = [abs(i-j) for i,j in zip(list(data["date_after"]),list(data["date_before"]))]

# eliminate some data
data = data[data["date_range"].notna()]
data = data[data["date_range"] < 201]
data["longitude"] = pd.to_numeric(data["longitude"], errors='coerce')
data = data[data["longitude"].notna()]
data["latitude"] = pd.to_numeric(data["latitude"], errors='coerce')
data = data[data["latitude"].notna()]

# add a field specifying century
data["century"] = [round((i+49)/100) for i in list(data["date_average"])]
data = data[data["century"] < 2]

# add a bit of scatter to the coordinates
data["longitude"] = data["longitude"] + 0.08 * np.random.randn(len(data))
data["latitude"] = data["latitude"] + 0.08 * np.random.randn(len(data))

# create a collection of three dataframes by chronological slices
backup = data.copy()
collection = [backup[backup["date_average"] < -399].copy(),backup[(backup["date_average"] < -199) & (backup["date_average"] > -400)].copy(),backup[backup["date_average"] > -200].copy()]
titles = ["Before 400 BCE","400 to 200 BCE","After 200 BCE"]

# specify pointer size
pointersize = 30


### 2 ### Create some maps

# specify a projection that places Italy as vertically as possible
fig, axs = plt.subplots(1, 3, subplot_kw={"projection": ccrs.InterruptedGoodeHomolosine()})

# iterate over the subplots
for i, ax in enumerate(axs):
    
    # specify the position of the subplots
    ax.set_position([[0,0,0.3,1],[0.35,0,0.3,1],[0.7,0,0.3,1]][i])
    
    # get the dataframe with the relevant information
    data = collection[i]

    # define the outlines of the map
    ax.coastlines()
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor="white")
    ax.add_feature(cfeature.OCEAN, zorder=10, edgecolor="white")
    ax.set_extent((11, 17.7, 47, 37.5), crs=ccrs.PlateCarree())

    # specify languages explicitly to define a useful zorder
    subset = data[data["language"].str.contains("Latin")].copy()
    ax.scatter(subset["latitude"], subset["longitude"], color="red", s=pointersize, zorder=2, transform=ccrs.PlateCarree(), label="Latin")
    
    subset = data[data["language"].str.contains("Etruscan")].copy()
    ax.scatter(subset["latitude"], subset["longitude"], color="green", s=pointersize, zorder=1, transform=ccrs.PlateCarree(), label="Etruscan")

    subset = data[data["language"].str.contains("Oscan")].copy()
    ax.scatter(subset["latitude"], subset["longitude"], color="blue", s=pointersize, zorder=3, transform=ccrs.PlateCarree(), label="Oscan")

    subset = data[data["language"].str.contains("Umbrian")].copy()
    ax.scatter(subset["latitude"], subset["longitude"], color="pink", s=pointersize, zorder=4, transform=ccrs.PlateCarree(), label="Umbrian")

    subset = data[data["language"].str.contains("Messapic")].copy()
    ax.scatter(subset["latitude"], subset["longitude"], color="orange", s=pointersize, zorder=5, transform=ccrs.PlateCarree(), label="Messapic")

    subset = data[data["language"].str.contains("Old Sabellic")].copy()
    ax.scatter(subset["latitude"], subset["longitude"], color="brown", s=pointersize, zorder=6, transform=ccrs.PlateCarree(), label="Old Sabellic")

    subset = data[data["language"].str.contains("Venetic")].copy()
    ax.scatter(subset["latitude"], subset["longitude"], color="purple", s=pointersize, zorder=7, transform=ccrs.PlateCarree(), label="Venetic")

    # set titles
    ax.set_title(titles[i],fontsize=22)
    
    # set legends for the third subplot online
    if i == 2:
        lgnd = ax.legend()
        for handle in lgnd.legendHandles:
            handle.set_sizes([100])
        lgnd.set_zorder(11)


### 3 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# save and show figure
plt.savefig('figures/inscriptions_space.png', bbox_inches=bbox, dpi=600)
plt.show()

# reimport and resave as pdf
# (goes via png > pdf to ensure that the pdf isn't too heavy)
img = mpimg.imread("figures/inscriptions_space.png")
fig = plt.figure()
plt.imshow(img)
plt.axis("off")

with PdfPages("figures/inscriptions_space.pdf") as pdf:
    pdf.savefig(fig, bbox_inches="tight", pad_inches=0, dpi=600)
    plt.close(fig)



