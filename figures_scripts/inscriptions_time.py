# -*- coding: utf-8 -*-

"""
Output: Figure inscriptions_time.png
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
from collections import Counter

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (13,21)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 15

# import datasets
data = pd.read_csv("datasets_manual/italian_epigraphy.csv", sep=";")


### 1 ### Process the data

# add some columns

data["date_average"] = [(i+j)/2 for i,j in zip(list(data["date_after"]),list(data["date_before"]))]
data["date_range"] = [abs(i-j) for i,j in zip(list(data["date_after"]),list(data["date_before"]))]

# eliminate some data
data = data[data["date_range"].notna()]
data = data[data["date_range"] < 201]

# add a field specifying century
data["century"] = [round((i+49)/100) for i in list(data["date_average"])]
data = data[data["century"] < 2]

# define the languages of interest
languages = ["Etruscan","Latin","Oscan","Other Sabellic languages","Venetic","Messapic"]
data["language"] = ["Other Sabellic languages" if i == "Umbrian" or i == "Old Sabellic" else i for i in data["language"]]

# create a figure with six subplots
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2)
ax_list = [ax1, ax2, ax3, ax4, ax5, ax6]

# enumerate over the six axes
for i, ax in enumerate(ax_list):
    
    # get century counts by language
    l = languages[i]
    subset = data[data["language"].str.contains(l)]
    count = Counter(list(subset["century"]))
    
    # set late Latin inscriptions to an arbitrarily high number
    if l == "Latin":
        count[0] = 5000
        count[1] = 5000
	
    # create a dataframe for century counts by language
    overview = pd.DataFrame(data=[-7,-6,-5,-4,-3,-2,-1,0,1],columns=["date"])
    overview["count"] = [count.get(i, 0) for i in list(overview["date"])]

    # define the parametres of the bar charts
    x = overview["date"]
    y = overview["count"]
    
    # create the bar chart
    ax.yaxis.grid(True)
    ax.set_title(l, y=0.9, fontsize=22)
    ax.set_ylim([0, 1800])
    ax.set_xlim([-7, 2])
    ax.bar(x,y)

    # set y_ticks on odd axes only
    if i%2 == 1:
        ax.yaxis.set_ticklabels([])

    # set BCE centuries as x_ticks
    ax.xaxis.set_major_locator(plt.FixedLocator(np.arange(-7, 2, 1)))
    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels[0] = ''
    labels[1] = '7th BCE'
    labels[2] = '6th BCE'
    labels[3] = '5th BCE'
    labels[4] = '4th BCE'
    labels[5] = '3rd BCE'
    labels[6] = '2nd BCE'
    labels[7] = '1st BCE'
    labels[8] = '1st CE'
    
    # set and rotate x_ticks
    ax.set_xticklabels(labels,rotation=45)


### 2 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# show the figure and save it
plt.savefig('figures/inscriptions_time.pdf', bbox_inches=bbox, dpi=600)
plt.show()

