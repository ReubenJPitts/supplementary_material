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

# set some parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams["figure.figsize"] = (15,20)
plt.rcParams['savefig.facecolor']='white'
plt.rcParams.update({'font.size': 20})

# import dataset
data = pd.read_csv("datasets_automatic/loanwords_dataset.csv", sep=";", index_col=0)


### 1 ### Visualise loanword sources

# create the figure
fig, ax = plt.subplots(1, 1, figsize=(15,10))

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
ax.legend(bbox_to_anchor=(1.4, 0.8), loc='center right')

# select a subset of the data
subset = data[data["distance_from_hearth"] == 0]
sources = [i for i in list(subset["latin_source"]) if i != "Latin"]
output = []
for l in languages:
    output.append([l,sources.count(l)])
data_lngs = pd.DataFrame(data=output,columns=["Source","Count"])

# create an inset piechart
ax_inset = fig.add_axes([0.67, 0.1, 0.4, 0.4])
patches, texts, autotexts = ax_inset.pie(data_lngs["Count"],labels=data_lngs["Source"],autopct='%1.1f%%',startangle = 90,counterclock=False,labeldistance=None)
ax_inset.set_title("DFH = low")

# adjust some labels
autotexts[3]._y += 0.06
autotexts[4]._y += 0.25
autotexts[4]._x += 0.03
autotexts[5]._text = ""


### 2 ### Export and save
plt.savefig('figures/loanword_source.png', bbox_inches='tight', dpi=600)

