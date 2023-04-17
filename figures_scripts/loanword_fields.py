# -*- coding: utf-8 -*-

"""
Output: Figure loanword_fields.png
Used in: Chapter 5
Author: Reuben J. Pitts
Date: 20/03/2023
"""

### 0 ### Imports

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 22

# work out figure size
label_offset = 0.6
plt.rcParams["figure.figsize"] = (13*label_offset,21)

# import dataset
data = pd.read_csv("tables/loanword_fields.csv", sep=";", index_col=0)


### 1 ### Create a bar chart

# flip the data
data = data.sort_values(by="Latin", ascending=True)

# create a chart
fig, ax = plt.subplots()

# get the data
x = [i + " (" + str(j) + ")" for i,j in zip(list(data["Field"]),list(data["Count"]))]
y = data["Latin"]
z = data["WOLD"]
i = np.arange(len(data))
w = 0.35

# visualise the data
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.05))
ax.xaxis.grid(True,which="both")
ax.barh(i+w,y,w,label="Latin")
ax.barh(i,z,w,label="WOLD")

# set some labels
ax.set_xlabel('Average loanword score')
ax.set_yticks(i+w / 2)
ax.set_yticklabels(x)

# add a legend
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
plt.savefig('figures/loanword_fields.pdf', bbox_inches=bbox, dpi=600)
plt.show()
