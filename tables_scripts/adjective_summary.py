# -*- coding: utf-8 -*-

"""
Output: Table adjective_summary.csv
Used in: Chapter 6
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

# import pandas
import pandas as pd

# import dataset
data = pd.read_csv("datasets_enriched/order_adjective_enriched.csv", sep=";", index_col=0)

# define a percentage function
def percentage(i,j):
    if j == 0:
        return "NA"
    return str(round(i / (j / 100), 2)) + " %"


### 1 ### Create a tabular overview

# filter the data
data = data[data["Semantics"] != "DELETE"]

# set some parametres
categories = [""] + list(set(data["Semantics"]))
languages = [""] + list(set(data["Language"]))

# iterate over the parametres
summary = []
for c in categories:
    row = []
    for l in languages:
        
        subset = data.copy()
        subset = subset[subset["Language"].str.contains(l)]
        subset = subset[subset["Semantics"].str.contains(c)]
        
        order = list(subset["Order"])
        
        row.append(percentage(order.count(0),len(order)) + " (" + str(len(order)) + ")")
    summary.append(row)

summary = pd.DataFrame(data=summary, columns=["All"] + list(set(data["Language"])), index=["all"] + list(set(data["Semantics"])))


### 2 ### Reorder the dataset
# define conversion to numeric
def convert_numeric(l):
    newlist = []
    for i in l:
        i = i[:-1]
        i = i[i.find("(")+1:]
        newlist.append(int(i))
    return newlist

# get numeric frequency counts to order by
category_orders = convert_numeric(list(summary["All"]))
language_orders = convert_numeric(summary.loc[["all"]].values.flatten().tolist())

# reorder columns
summary = summary[list(reversed([x for _, x in sorted(zip(language_orders, list(summary.columns)))]))]

# reorder rows
summary = summary.reindex(list(reversed([x for _, x in sorted(zip(category_orders, list(summary.index)))])))


### 3 ###
summary.to_csv("tables/adjective_summary.csv", sep=";")






