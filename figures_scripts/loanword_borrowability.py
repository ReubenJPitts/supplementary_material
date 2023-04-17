# -*- coding: utf-8 -*-

"""
Output: Figure loanword_borrowability.png
Used in: Chapter 5
Author: Reuben J. Pitts
Date: 14/03/2023
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
plt.rcParams["figure.figsize"] = (21,13)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 24

# import dataset
data = pd.read_csv("datasets_automatic/loanwords_dataset.csv", sep=";", index_col=0)


### 1 ### Visualise certainty correlation

# get the relevant data
certainty = [0, 0.25, 0.5, 0.75, 1]
SBC = []
for i in certainty:
    SBC.append(np.mean(data[data["latin_score"] == i]["wold"]))
SBC = [round(i,2) for i in SBC]

# add a line of best fit
a, b = np.polyfit(certainty, SBC, 1)
best_fit = [a * i for i in certainty]
best_fit = [b + i for i in best_fit]

# create the figure
plt.figure()
plt.scatter(certainty, SBC, s=100)
plt.plot(certainty, best_fit, linewidth=3)
plt.xticks(certainty)

# add or adjust labels
for i,j in zip(certainty,SBC):
    plt.text(i+0.01, j, str(j))
plt.xlabel('Latin loanword score', fontsize=27)
plt.ylabel('WOLD average loanword score', fontsize=27)

# set the limits of the plot
plt.xlim(-0.1,1.1)
plt.ylim(0.15,0.5)


### 2 ### Other miscellaneous statistics

print("WOLD for Latin non-loans", np.mean(data[data["binary_score"] == 0]["wold"]))
print("WOLD for Latin loans", np.mean(data[data["binary_score"] == 1]["wold"]))

print("WOLD for low DFH", np.mean(data[data["distance_from_hearth"] == 0]["wold"]))
print("WOLD for high DFH", np.mean(data[data["distance_from_hearth"] == 1]["wold"]))

print("Latin for low DFH", np.mean(data[data["distance_from_hearth"] == 0]["latin_score"]))
print("Latin for high DFH", np.mean(data[data["distance_from_hearth"] == 1]["latin_score"]))

print("WOLD for low frequency", np.mean(data[data["frequency_absolute"] < 2]["wold"]))
print("WOLD for high frequency", np.mean(data[data["frequency_absolute"] > 1]["wold"]))

print("Latin for low frequency", np.mean(data[data["frequency_absolute"] < 2]["latin_score"]))
print("Latin for high frequency", np.mean(data[data["frequency_absolute"] > 1]["latin_score"]))


### 3 ### Export

# specify margins
fig = plt.gcf()
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# show the figure and save it
plt.savefig('figures/loanword_borrowability.pdf', bbox_inches=bbox, dpi=600)


