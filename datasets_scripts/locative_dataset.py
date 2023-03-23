# -*- coding: utf-8 -*-

"""
Output: Dataset sabellic_locative.csv
Used in: Chapter 7
Author: Reuben J. Pitts
Date: 14/03/2023
"""


### 0 ### Preliminaries

# import some required libraries
import pandas as pd

# import the CEIPoM data
from CEIPoM_import import CEIPoM
from treesearch import TreeSearch
syntax = TreeSearch(CEIPoM)


### 1 ### Create a locative dataset

# sift sabellic languages
sabellic = CEIPoM[CEIPoM["Language_family"].str.contains("::Sabellic")]

# sift locative nouns from the database
locative = sabellic.copy()
locative = locative[locative["Part_of_speech"] == "noun"]
locative = locative[locative["Case"] == "LOC"]
locative = locative[locative["Number"] == "singular"]

# add isogloss for final n
locative["Isogloss"] = [1 if i[-1] in ["n","m"] else 0 for i in list(locative["Token_clean"])]

# manually adjust a single case of wrong coordinates
locative.at[153618,"Longitude"] = 14.3748737
locative.at[153618,"Latitude"] = 40.6251617

# get rid of 154673
locative = locative[locative["Text_ID"] != 909]

# split locative into two chronological slices
locative["Date_average"] = [(i+j)/2 for i,j in zip(list(locative["Date_after"]),list(locative["Date_before"]))]
locative["Old"] = [1 if i < -399 else 0 for i in list(locative["Date_average"])]

# get dataset for individual places
locative = locative.sort_values(by="Latitude")
locative = locative.sort_values(by="Longitude")
locative = locative.drop_duplicates(subset=["Latitude","Longitude","Isogloss","Old"])


### 2 ### Export dataset
locative.to_csv("datasets_automatic/locative_dataset.csv", sep=";", encoding="utf-8")




