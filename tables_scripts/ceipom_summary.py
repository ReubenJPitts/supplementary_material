# -*- coding: utf-8 -*-

"""
Output: Table ceipom_summary.csv
Used in: Chapter 4
Author: Reuben J. Pitts
Date: 14/03/2023
"""


### 0 ### Imports

# import libraries
import pandas as pd

# import CEIPoM
from CEIPoM_import import CEIPoM
from CEIPoM_import import texts


### 1 ### Create some summary statistics

# define a table to fill with the values
table = []

# define the relevant languages and iterate over them
languages = ['', 'Latin', 'Oscan', 'Messapic', 'Venetic', 'Umbrian', 'Old Sabellic']
for l in languages:
    
    # get datasets by language
    row = [l]
    if l == "":
        row = ["CEIPoM"]
    t_subset = texts[texts["Language"].str.contains(l)]
    c_subset = CEIPoM[CEIPoM["Language"].str.contains(l)]
    c_subset = c_subset[c_subset["Token"] != "-"]
    
    # number of texts
    t_total = len(t_subset)
    row.append(t_total)
    
    # number of tokens
    c_total = len(c_subset)
    row.append(c_total)
    
    # percentage of analysable tokens
    analyse = len(t_subset[t_subset["Analysable_token"] == True])
    analyse = analyse / (t_total / 100)
    row.append(round(analyse,2))
    
    # percentage full sentences
    analyse = len(t_subset[t_subset["Analysable_token"] == True])
    sent = len(t_subset[t_subset["Finite_verb"] == True])
    sent = sent / (analyse / 100)
    row.append(round(sent,2))
    
    # average length of texts
    length = t_subset["Text_length"]
    row.append(round(length.mean(),2))
    row.append(int(length.median()))
    row.append(int(length.max()))
    
    # percentage of proper names
    proper = len(c_subset[c_subset["Meaning_category"] == "PROPER"])
    proper = proper / (c_total / 100)
    row.append(round(proper,2))
    
    # number of non-proper lemmata
    lemma = c_subset[c_subset["Meaning_category"] != "PROPER"]
    lemma = lemma[lemma["Lemma"] != "-"]
    lemma = list(lemma["Lemma"])
    
    # unique lemmas
    uniques = len(list(set(lemma)))
    row.append(uniques)
    row.append(round(uniques / (len(lemma) / 100),2))
    
    # add the row to the table
    table.append(row)
    
# create a dataframe and flip it
table = pd.DataFrame(table)
table = table.transpose()

# export the dataframe
table.to_csv("tables/ceipom_summary.csv", sep=";")



