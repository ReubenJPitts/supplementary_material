# -*- coding: utf-8 -*-

"""
Output: Dataset phonological_dataset.csv
Used in: Chapter 2
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

# import required libraries
import pandas as pd
from asjp import tokenise

# import the datasets
data_modern = pd.read_csv("datasets_manual/pairs_modern.csv", sep=";")
data_ancient = pd.read_csv("datasets_manual/pairs_ancient.csv", sep=";")


### 1 ### Levenshtein functions

# define which sounds count as vowels (for vowel-weighted distance)
vowels = "ieEaou"
    
# set distance metric
def distance(x,y,vw="no"):
    #note that vw can be set to "yes" for a vowel-weighted measure
	
    #set the default distance
    dist = 1

    #half-distance (if vowel-weighted)
    if vw == "yes":
        if x in vowels and y in vowels:
            if vowels[(vowels.index(x) + 1)%6] == y:
                dist = 0.5
            if vowels[(vowels.index(x) - 1)%6] == y:
                dist = 0.5
			
        if x in vowels or y in vowels:
            if x == "3" or y == "3":
                dist = 0.5

    #no distance
    if x == "" and y == "":
        dist = 0
    if x == y:
        dist = 0

    # return the calculated distance
    return dist

# use the above distance metric to calculate a levenshtein distance between two strings
def levenshtein(x, y, vw="no"):
    
    # split strings into constituent sounds
    x = [i for i in tokenise(x)]
    y = [i for i in tokenise(y)]

    # create a matrix
    length = list(range(len(y) + 1))
    matrix = []
    for i in length:
        l = [i]*(len(x)+1)
        matrix.append(l)
    matrix[0] = list(range(len(x) + 1))
    
    # iterate over the matrix
    # coordinates are i (for rows), j (for columns)

    for i in list(range(1,len(y) + 1)):
        for j in list(range(1,len(x) + 1)):

            # get the relevant sounds
            k = y[i-1]
            l = x[j-1]

            # get the value of the squares above, left and left above diagonally, in the matrix
            above = matrix[i-1][j]
            leftab = matrix[i-1][j-1]
            left = matrix[i][j-1]

            # get the phonological distances
            var1 = distance(k,"",vw=vw) + above
            var2 = distance(l,"",vw=vw) + left
            var3 = distance(k,l,vw=vw) + leftab

            # add the smallest value to the matrix
            matrix[i][j] = min([var1, var2, var3])

    # the last cell represents the levenshtein distance
    dist = matrix[-1][-1]
    return dist

# normalise levenshtein distance by the length of the longest string involved
def normalise(d,x,y):
    length = max(len(tokenise(x)),len(tokenise(y)))
    d = d / length
    return d


### 2 ### calculate modern distances

# sift out non-cognates
data_modern = data_modern[data_modern["cognate"] == 1]

# get the relevant language pairs
pairs = list(dict.fromkeys(list(data_modern["pairs"])))

# iterate over the language pairs
modern = []
for p in pairs:
    
    # sift out the relevant data
    subset = data_modern[data_modern["pairs"] == p]
    
    # get two token lists to compare
    x = list(subset["form_x"])
    y = list(subset["form_y"])
    
    # get their regular levenshtein distance and normalise it
    d = [levenshtein(x[i], y[i], vw="no") for i in range(len(x))]
    l = [normalise(d[i], x[i], y[i]) for i in range(len(x))]

    # take an average the normalised levenshtein distance
    lev_regular = round(sum(l)/len(l),4)

    # ditto for vowel-weighted levenshtein distance
    d = [levenshtein(x[i], y[i],vw="yes") for i in range(len(x))]
    l = [normalise(d[i], x[i], y[i]) for i in range(len(x))]

    # ditto average
    lev_vowel = round(sum(l)/len(l),4)

    # append to the dataset
    modern.append([p, lev_regular, lev_vowel])

modern = pd.DataFrame(modern, columns=["pair","regular","vowel-weighted"])


### 3 ### calculate ancient distances

# define three language pairs
pairs = [["oscan","umbrian"],["latin","oscan"],["latin","umbrian"]]

# iterate over the language pairs
ancient = []
for p in pairs:
    
    # get the relevant language data
    subset = data_ancient[p].copy()
    subset = subset[~subset[p[0]].isna()]
    subset = subset[~subset[p[1]].isna()]
    x = list(subset[p[0]])
    y = list(subset[p[1]])
    
    # get their regular levenshtein distance and normalise it
    d = [levenshtein(x[i], y[i], vw="no") for i in range(len(x))]
    l = [normalise(d[i], x[i], y[i]) for i in range(len(x))]

    # take an average the normalised levenshtein distance
    lev_regular = round(sum(l)/len(l),4)

    # ditto for vowel-weighted levenshtein distance
    d = [levenshtein(x[i], y[i],vw="yes") for i in range(len(x))]
    l = [normalise(d[i], x[i], y[i]) for i in range(len(x))]

    # ditto average
    lev_vowel = round(sum(l)/len(l),4)

    # append to the dataset
    ancient.append([p, lev_regular, lev_vowel])

ancient = pd.DataFrame(ancient, columns=["pair","regular","vowel-weighted"])


### 4 ### combine and clean up the two dataframes

# combine the dataframes
distances = pd.concat([modern,ancient])

# sort the dataframe
distances = distances.sort_values(by="vowel-weighted")
distances = distances.reset_index(drop=True)

# define cleaner pair names
pair_names = ["French Flemish ~ West Flemish",
"Afrikaans ~ Dutch",
"Brabantic ~ French Flemish",
"Umbrian ~ Oscan",
"Afrikaans ~ French Flemish",
"West Flemish ~ Limburgish",
"German ~ Dutch",
"Oscan ~ Latin",
"Dutch ~ Upper Saxon",
"English ~ Dutch",
"Dutch ~ Danish",
"Umbrian ~ Latin",
"Dutch ~ Icelandic",
"English ~ French"]

# substitute cleaner pair names
distances["pair"] = pair_names

# define which pairs are Italic
distances["italic"] = [1 if i in ["Umbrian ~ Latin","Oscan ~ Latin","Umbrian ~ Oscan"] else 0 for i in list(distances["pair"])]

# export dataset
distances.to_csv("datasets_automatic/phonological_dataset.csv", sep=";", encoding="utf-8")









