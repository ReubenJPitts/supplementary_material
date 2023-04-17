# -*- coding: utf-8 -*-

"""
Output: Figure loanword_source.png
Used in: Chapter 5
Author: Reuben J. Pitts
Date: 20/03/2023
"""

### 0 ### Imports

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (21,13)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 27

# import dataset
data = pd.read_csv("datasets_automatic/loanwords_dataset.csv", sep=";", index_col=0)


### 1 ### Visualise loanword sources

# create the figure
fig = plt.figure()
ax = fig.add_axes([0, 0, 13/21, 1])

# select relevant data
sources = [i for i in list(data["latin_source"]) if i != "Latin"]
languages = ["Greek","Etruscan","Sabellic","Celtic","Semitic","Germanic"]
output = []
for l in languages:
    output.append([l,sources.count(l)])
data_lngs = pd.DataFrame(data=output,columns=["Source","Count"])

# create a piechart   
patches, texts, autotexts = ax.pie(data_lngs["Count"],labels=data_lngs["Source"],autopct='%1.1f%%',startangle = 90,counterclock=False,labeldistance=None)

# adjust some labels
autotexts[4]._y += 0.1
autotexts[5]._y += 0.25
autotexts[4]._x += 0.03
autotexts[5]._x += 0.05

#add a legend
ax.legend()
ax.legend(bbox_to_anchor=(1, 0.9))

# select a subset of the data
subset = data[data["distance_from_hearth"] == 0]
sources = [i for i in list(subset["latin_source"]) if i != "Latin"]
output = []
for l in languages:
    output.append([l,sources.count(l)])
data_lngs = pd.DataFrame(data=output,columns=["Source","Count"])

# create an inset piechart
leftshift = 0.15
ax_inset = fig.add_axes([(13/21)-leftshift, 0, 1-(13/21)+leftshift, 1-(13/21)+leftshift])

# add data
patches, texts, autotexts = ax_inset.pie(data_lngs["Count"],labels=data_lngs["Source"],autopct='%1.1f%%',startangle = 90,counterclock=False,labeldistance=None)
ax_inset.set_title("Distance from hearth = 'low'", fontsize=30)

# adjust some labels
autotexts[3]._y += 0.1
autotexts[4]._text = ""
autotexts[5]._text = ""


### 2 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# show the figure and save it
plt.savefig('figures/loanword_source.pdf', bbox_inches=bbox, dpi=600)

