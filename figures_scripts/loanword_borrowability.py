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

# set some parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams["figure.figsize"] = (20,12)
plt.rcParams['savefig.facecolor']='white'
plt.rcParams.update({'font.size': 25})

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
plt.plot(certainty, best_fit)
plt.xticks(certainty)

# add or adjust labels
for i,j in zip(certainty,SBC):
    plt.text(i+0.01, j, str(j))
plt.xlabel('Latin loanword score')
plt.ylabel('WOLD low average loanword score')

# set the limits of the plot
plt.xlim(-0.1,1.1)
plt.ylim(0.15,0.5)


### 2 ### Export and save
plt.savefig('figures/loanword_borrowability.png', bbox_inches='tight', dpi=600)


