# -*- coding: utf-8 -*-

"""
Output: Table loanword_outliers.csv
Used in: Chapter 5
Author: Reuben J. Pitts
Date: 20/03/2023
"""


### 0 ### Imports

# import libraries
import pandas as pd

# import dataset
data = pd.read_csv("datasets_automatic/loanwords_dataset.csv", sep=";", index_col=0)

# set the desired number of outliers
n = 20


### 1 ### Outliers that are loans

# get a copy of the data
outlier_loans = data.copy()

# sort by wold information
outlier_loans = outlier_loans.sort_values(by="wold", ascending=True)
outlier_loans = outlier_loans.reset_index(drop=True)
outlier_loans.index += 1

# filter Latin loans
outlier_loans = outlier_loans[outlier_loans["latin_score"] > 0]

# create new dataset
outlier_loans = outlier_loans[["name","latin","latin_score","wold"]]
outlier_loans = outlier_loans[:n]


### 2 ### Outliers that are non-loans

# get a copy of the data
outlier_nonloans = data.copy()

# sort by wold information
outlier_nonloans = outlier_nonloans.sort_values(by="wold", ascending=False)
outlier_nonloans = outlier_nonloans.reset_index(drop=True)
outlier_nonloans.index += 1

# filter Latin non-loans
outlier_nonloans = outlier_nonloans[outlier_nonloans["latin_score"] < 0.25]

# create new dataset
outlier_nonloans = outlier_nonloans[["name","latin","latin_score","wold"]]
outlier_nonloans = outlier_nonloans[:n]


### 3 ### Create a nice synthesis of the two

# reverse the order of the nonloans
outlier_nonloans = outlier_nonloans.sort_values(by="wold", ascending=True)

# create a buffer row to separate the dataframes
buffer = pd.DataFrame(data=[["...","...","...","..."]],columns=outlier_loans.columns)

outliers = pd.concat([outlier_loans, buffer, outlier_nonloans])


### 4 ### Export as a .csv file
outliers.to_csv("tables/loanword_outliers.csv", sep=";", encoding="utf-8")




