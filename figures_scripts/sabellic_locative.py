# -*- coding: utf-8 -*-

"""
Output: Figure sabellic_locative.png
Used in: Chapter 7
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Preliminaries

# import some required libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (21,12)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 22

# import CEIPoM
from CEIPoM_import import CEIPoM

# import the dataset
locative = pd.read_csv(r"datasets_manual/sabellic_locative.csv", sep=";")


### 1 ### Modify the dataset

# filter dataset
locative = locative[~locative["Isogloss"].str.contains("\?")]
locative = locative[~locative["Isogloss"].str.contains("[2]")]
locative = locative[locative["Morphology"].str.contains("O-stem")]

# enrich with CEIPoM geochronological data
locative = locative.merge(CEIPoM, how="left", left_on="CEIPoM Token", right_on="Token_ID", suffixes=("","_CEIPoM"))

# manually adjust a single case of wrong coordinates
locative.at[11,"Longitude"] = 14.3748737
locative.at[11,"Latitude"] = 40.6251617

# split locative into two chunks
locative["Date_average"] = [(i+j)/2 for i,j in zip(list(locative["Date_after"]),list(locative["Date_before"]))]
locative["Old"] = [1 if i < -399 else 0 for i in list(locative["Date_average"])]

# create a binary isogloss field
locative["Binary"] = [0 if i == "[1]" else 1 for i in locative["Isogloss"]]

# count occurrences per coordinate
locative = locative.groupby(["Latitude", "Longitude","Old"])["Binary"].value_counts().rename("Count").reset_index()

# rescale sizes
locative["Size"] = [250*i for i in locative["Count"]]

# sort data such that largest markers are lowest
locative = locative.sort_values(by="Count",ascending=False)


### 2 ### Create a map

# create a figure
fig, axs = plt.subplots(1, 2, subplot_kw={"projection": ccrs.PlateCarree()})

# set ax names
titles = ["Inscriptions before 400 BCE","Inscriptions after 400 BCE"]

# iterate over axes
for i, ax in enumerate(axs):

    # set the correct position for the ax
    ax.set_position([[0,0,0.47,1],[0.53,0,0.47,1]][i])
    
    # get the dataframe with the relevant information
    data = locative[locative["Old"] == [1,0][i]].copy()

    # set the outlines of the map
    ax.coastlines()
    ax.add_feature(cfeature.OCEAN, zorder=0, edgecolor="white")
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor="white")
    ax.set_extent((11, 18.55, 46.5, 37.5), crs=ccrs.PlateCarree())

    # scatter the data
    subset_old = data[data["Binary"] == 0].copy()
    ax.scatter(subset_old["Longitude"], subset_old["Latitude"], s=subset_old["Size"], linewidth=1, edgecolor="black")

    subset_new = data[data["Binary"] == 1].copy()
    ax.scatter(subset_new["Longitude"], subset_new["Latitude"], s=subset_new["Size"], linewidth=1, edgecolor="black")
    
    # add scatter markers for legend
    ax.scatter(0,0, s=250, linewidth=2, c="#1f77b4", edgecolor="black", label="old locative")
    ax.scatter(0,0, s=250, linewidth=2, c="#ff7f0e", edgecolor="black", label="renewed locative")
    ax.scatter(0,0, s=250*5, linewidth=2, c="white", alpha=0, label=" ")
    ax.scatter(0,0, s=250*1, linewidth=2, c="#1f77b4", edgecolor="black", label="1 occurrence")
    ax.scatter(0,0, s=250*5, linewidth=2, c="#1f77b4", edgecolor="black", label="5 occurrences")
    ax.scatter(0,0, s=250*5, linewidth=2, c="white", alpha=0, label=" ")

    # set titles
    ax.set_title(titles[i])
    ax.legend()
    

### 3 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 2.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# save and show figure
plt.savefig("figures/sabellic_locative.png", bbox_inches=bbox, dpi=600)
plt.show()

# reimport and resave as pdf
img = mpimg.imread("figures/sabellic_locative.png")
fig = plt.figure()
plt.imshow(img)
plt.axis("off")

with PdfPages("figures/sabellic_locative.pdf") as pdf:
    pdf.savefig(fig, bbox_inches="tight", pad_inches=0, dpi=600)
    plt.close(fig)




