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
import numpy as np

# import dataset
data = pd.read_csv("datasets_automatic/loanwords_dataset.csv", sep=";", index_col=0)


### 1 ### Field subdivision by language

# list of languages
languages = ["Greek","Etruscan","Sabellic","Celtic","Semitic","Germanic"]

# get a list of fields
fields = [""] + list(set(data["field"]))

# create an empty list of lists
output = []

# iterate over fields
for f in fields:
    
    # set an empty row
    row = []
    
    # get the relevant subset for the current field
    subset = data[data["field"].str.contains(f)]
    
    # include a category for the entire dataset
    if f == "":
        f = "All"
        
    # add regular stats to the table
    row.append(f)
    row.append(len(subset))
    row.append(np.mean(subset["low_wold"]))
    row.append(np.mean(subset["latin_score"]))
    
    # iterate over language
    for l in languages:
        row.append(len(subset[subset["latin_source"].str.contains(l)]))
    
    # eliminate Greek
    row.append(np.mean(subset[~subset["latin_source"].str.contains("Greek")]["latin_score"]))
    
    # add to the list of lists
    output.append(row)
        
data_cats = pd.DataFrame(data=output,columns=["Field","Count","WOLD","Latin"] + languages + ["without_Greek"])


### 2 ### Clean and export the dataset

# clean the data up
data_cats["WOLD"] = round(data_cats["WOLD"],2)
data_cats["Latin"] = round(data_cats["Latin"],2)
data_cats["without_Greek"] = round(data_cats["without_Greek"],2)
data_cats = data_cats.sort_values(by="Latin", ascending=False)
 
# confidence score by language
for l in languages:
    subset = data[data["latin_source"].str.contains(l)]
    print(l,np.mean(subset["latin_score"]))

# Export dataset
data_cats.to_csv('tables/loanword_non_greek.csv', sep=";")

