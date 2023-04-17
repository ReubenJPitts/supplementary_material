# -*- coding: utf-8 -*-

"""
Output: Figure italian_genitive.png
Used in: Chapter 6
Author: Reuben J. Pitts
Date: 14/03/2023
"""


### 0 ### Imports

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.transforms import Bbox
import numpy as np

# set some parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (23,14)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 16

# import dataset
data = pd.read_csv("datasets_automatic/order_genitive.csv", sep=";", index_col=0)


### 1 ### Define the creation of subplots

# set an subplot
def add_to_ax(df, ax, title):
    
    # get a tabulation of the relevant data
    data = pd.crosstab(df.Century,df.Order)

    # get the relevant information
    labels = data.index
    try:
        verb_after = data[0]
    except:
        verb_after = [0]*len(data)
    try:
        verb_before = data[1]
    except:
        verb_before = [0]*len(data)
    
    # two datasets for visualising
    data[0] = verb_after
    data[1] = verb_before

    # set centuries
    include = [-4,-3,-2,-1,0]
    include = [i for i in include if i not in list(data.index)]
    for i in include:
        data.loc[i] = [0,0]

    # define data to plot
    data = data.sort_index()
    labels = data.index
    verb_after = list(data[0])
    verb_before = list(data[1])
    
    # set century labels
    labels = ["8-BCE" if i == -7 else i for i in labels]
    labels = ["7-BCE" if i == -6 else i for i in labels]
    labels = ["6-BCE" if i == -5 else i for i in labels]
    labels = ["5-BCE" if i == -4 else i for i in labels]
    labels = ["4-BCE" if i == -3 else i for i in labels]
    labels = ["3-BCE" if i == -2 else i for i in labels]
    labels = ["2-BCE" if i == -1 else i for i in labels]
    labels = ["1-BCE" if i == 0 else i for i in labels]
    labels = ["1-CE" if i == 1 else i for i in labels]
      
    # space out the columns
    x = np.arange(len(labels))
    width = 0.35
    
    # plot the chart
    rects1 = ax.bar(x - width/2, verb_after, width, label='genitive precedes head')
    rects2 = ax.bar(x + width/2, verb_before, width, label='genitive follows head')

    #ax.set_ylabel("number of occurrences")
    ax.set_title(title)
    ax.set_xticks(x, labels)
    ax.legend(loc = 'upper left')
    
    # set reasonable plot limits
    bottom, top = ax.get_ylim()
    t = top
    if t < 5:
        t = 5
    t = t * 1.5
    ax.set_ylim(top = t)

    # put text labels on the bars
    ax.bar_label(rects1, [rect.get_height() if rect.get_height() != 0 else "" for rect in rects1], padding=3)
    ax.bar_label(rects2, [rect.get_height() if rect.get_height() != 0 else "" for rect in rects2], padding=3)


### 2 ### Visualise dative plot for non-Latin languages

# set the grid
gs = gridspec.GridSpec(2, 6)
ax1 = plt.subplot(gs[0:1, 0:2])
ax2 = plt.subplot(gs[0:1, 2:4])
ax3 = plt.subplot(gs[0:1, 4:])
ax4 = plt.subplot(gs[1:, 0:2])
ax5 = plt.subplot(gs[1:, 2:4])
ax6 = plt.subplot(gs[1:, 4:])
fig = plt.gcf()
ax_lst = [ax1,ax2,ax3,ax4,ax5,ax6]

# get the Latin subset
latin = data[data["Language"] == "Latin"].copy()
latin = latin[latin["Language_(text)"] == "Latin"]

# create two plots
add_to_ax(latin,ax1,"Latin genitives")
latin = latin[latin["Meaning_category"] != "PROPER"]
add_to_ax(latin,ax4,"Latin non-proper genitives")

# get the Oscan subset
oscan = data[data["Language"] == "Oscan"].copy()
oscan = oscan[oscan["Language_(text)"] == "Oscan"]

# create two plots
add_to_ax(oscan,ax2,"Oscan genitives")
oscan = oscan[oscan["Meaning_category"] != "PROPER"]
add_to_ax(oscan,ax5,"Oscan non-proper genitives")

# get the Umbrian subset
umbrian = data[data["Language"] == "Umbrian"].copy()
umbrian = umbrian[umbrian["Language_(text)"] == "Umbrian"]

# create two plots
add_to_ax(umbrian,ax3,"Umbrian genitives")
umbrian = umbrian[umbrian["Meaning_category"] != "PROPER"]
add_to_ax(umbrian,ax6,"Umbrian non-proper genitives")

# remove white space between axes
plt.subplots_adjust(wspace=0.4, top=0.9)


### 3 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -0.5
right_margin = fig_width + 0.5
bottom_margin = -0.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# show the figure and save it
plt.savefig('figures/italian_genitive.pdf', bbox_inches=bbox, dpi=600)


