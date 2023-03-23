# -*- coding: utf-8 -*-

"""
Output: Table loanword_fields.csv
Used in: Chapter 5
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

# import libraries
import pandas as pd
import numpy as np

# import dataset
data = pd.read_csv("datasets_automatic/loanwords_dataset.csv", sep=";", index_col=0)


### 1 ### Subdivision by fields

fields = list(set(data["field"]))

output = [["All",len(data),np.mean(data["low_wold"]),np.mean(data["latin_score"])]]

for f in fields:
    subset = data[data["field"] == f].copy()
    wld = np.mean(subset["low_wold"])
    lat = np.mean(subset["latin_score"])
    count = len(subset)
    output.append([f,count,wld,lat])
    
data_cats = pd.DataFrame(data=output,columns=["Field","Count","WOLD","Latin"])


### 2 ### Export as csv file

# first clean the data up
data_cats["WOLD"] = round(data_cats["WOLD"],2)
data_cats["Latin"] = round(data_cats["Latin"],2)
data_cats = data_cats.sort_values(by="Latin", ascending=False)

# export
data_cats.to_csv("tables/loanword_fields.csv", sep=";")

