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

# set some parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams["figure.figsize"] = (15,20)
plt.rcParams['savefig.facecolor']='white'
plt.rcParams.update({'font.size': 20})

# import dataset
data = pd.read_csv("tables/loanword_fields.csv", sep=";", index_col=0)


### 1 ### Create a bar chart

# flip the data
data = data.sort_values(by="Latin", ascending=True)

# create a chart
fig, ax = plt.subplots(figsize=(10,20))

# get the data
x = [i + " (" + str(j) + ")" for i,j in zip(list(data["Field"]),list(data["Count"]))]
y = data["Latin"]
z = data["WOLD"]
i = np.arange(len(data))
w = 0.35

# visualise the data
ax.xaxis.grid(True)
ax.barh(i+w,y,w,label="Latin")
ax.barh(i,z,w,label="WOLD")

# set some labels
ax.set_xlabel('Average loanword score')
ax.set_yticks(i+w / 2)
ax.set_yticklabels(x)

# add a legend
ax.legend()


### 2 ### Export and save

plt.savefig('figures/loanword_fields.png', bbox_inches='tight', dpi=600)
