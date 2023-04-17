# -*- coding: utf-8 -*-

"""
Output: Figure phonological_distances.png
Used in: Chapter 2
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 27

# work out figure size
label_offset = 0.6
plt.rcParams["figure.figsize"] = (13*label_offset,21)

# import datasets
data = pd.read_csv("datasets_automatic/phonological_dataset.csv", sep=";", index_col=0)


### 1 ### Process the data

# sort the data
data = data.sort_values(by="vowel-weighted", ascending=False)


### 2 ### Create a figure

# create a figure
fig, ax = plt.subplots()

# specify a grid
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
ax.xaxis.grid(True, which="both")

# create the bar charts
ax.barh(data["pair"],data["regular"],label="ANLD",color="#ff7c0c")
ax.barh(data["pair"],data["vowel-weighted"],label="Vowel-weighted",color="#2074b4")

# put Italic languages in a different colour
data["regular"] = [r if i == 0 else 0 for r,i in zip(list(data["regular"]),list(data["italic"]))]
data["vowel-weighted"] = [r if i == 0 else 0 for r,i in zip(list(data["vowel-weighted"]),list(data["italic"]))]
ax.barh(data["pair"],data["regular"],color="#ffcea3")
ax.barh(data["pair"],data["vowel-weighted"],color="#add3f0")

# create a legend
ax.set_xlabel("Phonological distance")
ax.legend()


### 3 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5 - (13*(1-label_offset))
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# show the figure and save it
plt.savefig('figures/phonological_distances.pdf', bbox_inches=bbox, dpi=600)
plt.show()
