# -*- coding: utf-8 -*-

"""
Output: Table coordination_summary.csv
Used in: Chapter 8
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

# import required libraries
import pandas as pd

# import the dataset
data = pd.read_csv("datasets_automatic/coordination_dataset.csv", sep=";")

# filter "other" coordination strategies out
data = data[data["Strategy"] != "O"]

# define a percentage function
def percent(i,j):
    if j > 0:
        return str(round ( i / (j / 100) , 1 ))+ " %"
    else:
        return "NA"
    
def percentages(l):
    s = sum(l)
    output = []
    for i in l:
        output.append(percent(i,s))
    return output

    

### 1 ### Create some summaries

# set some categories of interest
languages = ["", "Latin", "Oscan", "Umbrian", "Messapic"]
coordinands = ["", "Proper", "Verbs","Nouns"]
strategies = ["A", "S", "P"]

# retrieve information from the dataset
info = []
for l in languages:
    l_data = data[data["Language"].str.contains(l)]
    row = []
    for c in coordinands:
        c_data = l_data.copy()     
        if c != "":
            c_data = l_data[l_data[c] == 1].copy()
        absolute = []
        for s in strategies:
            s_data = c_data[c_data["Strategy"] == s]
            absolute.append(len(s_data))
        if l != "Latin" and l != "Messapic":
            absolute = [absolute[0], absolute[1] + absolute[2]]
        relative = percentages(absolute)
        row.append(absolute)
        row.append(relative)
    info.append(row)

# reorganise information into desired format
count = list(range(8))

columns = []
for i in count:
    column = []
    for x in info:
        column += x[i]
    columns.append(column)
    
# turn into a pandas dataframe
dataset = pd.DataFrame(data=columns)
dataset = dataset.transpose()

# export dataframe
dataset.to_csv("tables/coordination_summary.csv", sep=";", encoding="utf-8")




