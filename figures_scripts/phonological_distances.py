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

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (10,20)

# import datasets
data = pd.read_csv("datasets_automatic/phonological_dataset.csv", sep=";", index_col=0)


### 1 ### Process the data

# sort the data
data = data.sort_values(by="vowel-weighted", ascending=False)


### 2 ### Create a figure

# create a figure
fig, ax = plt.subplots()
ax.xaxis.grid(True)

# create the bar charts
ax.barh(data["pair"],data["regular"],label="ANLD",color="#ff7c0c")
ax.barh(data["pair"],data["vowel-weighted"],label="Vowel-weighted ANLD",color="#2074b4")

# put Italic languages in a different colour
data["regular"] = [r if i == 0 else 0 for r,i in zip(list(data["regular"]),list(data["italic"]))]
data["vowel-weighted"] = [r if i == 0 else 0 for r,i in zip(list(data["vowel-weighted"]),list(data["italic"]))]
ax.barh(data["pair"],data["regular"],color="#ffcea3")
ax.barh(data["pair"],data["vowel-weighted"],color="#add3f0")

# create a legend
ax.legend()

# save and show figure
plt.savefig('figures/phonological_distances.png', bbox_inches='tight', dpi=600)
plt.show()
