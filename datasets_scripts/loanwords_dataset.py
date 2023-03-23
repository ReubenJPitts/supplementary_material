# -*- coding: utf-8 -*-

"""
Output: Dataset loanwords_dataset.csv
Used in: Chapter 5
Author: Reuben J. Pitts
Date: 20/03/2023
"""


### 0 ### Imports

# import some libraries
import pandas as pd

# import the dataset
data = pd.read_csv("datasets_manual/loanwords_italic.csv", sep=";")
data = data[data["selection"] == "selection"].copy()
data = data.dropna(subset=["latin_score"])

# import PROIEL
texts = ["caes-gal.xml","cic-att.xml","cic-off.xml","latin-nt.xml"]
proiel = [open("PROIEL/{}".format(i), 'r', encoding='utf-8').read() for i in texts]

# import WOLD
wold = pd.read_csv("WOLD/forms.csv", sep=",")
lang = pd.read_csv("WOLD/languages.csv", sep=",")
lang = lang.set_index("ID")

# define "average"
def average(l):
    return (sum(list(l)) / len(list(l)))
    

### 1 ### Enrich with frequency data

# get the lemma information from PROIEL
proiel  = "".join(proiel)
proiel = proiel.split("\n")
proiel = [i for i in proiel if i.find('lemma="')>-1]
proiel = [i[i.find('lemma="')+7:] for i in proiel]
proiel = [i[:i.find('"')] for i in proiel]
proiel = ["".join([i for i in j if i.lower() in "abcdefghijklmnopqrstuvwxyz"]) for j in proiel]

# for each item in the Latin translation, get its frequency in the PROIEL list
data["frequency_absolute"] = [proiel.count(i) for i in list(data["latin"])]
data["frequency"] = [1 if i > 2 else 0 for i in list(data["frequency_absolute"])]


### 2 ### Enrich with WOLD data

# convert the IDs (necessary because excel otherwise turns everything into dates)
data["id"] = [i.replace("#","-") for i in list(data["id"])]

# search for lemmata with equivalents in the Italic dataset only
wold = wold[wold["Parameter_ID"].isin(list(data["id"]))]

# get scores for each WOLD language
language_data = []
languages = list(set(wold["Language_ID"]))
for l in languages:
    subset = wold[wold["Language_ID"] == l].copy()
    score = average(subset["BorrowedScore"])
    name = lang.loc[[l]]["Name"].item()
    language_data.append([l,name,score])
language = pd.DataFrame(data=language_data,columns=["id","name","score"])

# clean up the dataset
language = language.sort_values(by="score")
language = language.reset_index(drop=True)

# get an average loanword score for latin
latin_average = average(data["latin_score"])

# check how many languages to take from the bottom to get a score approaching this
scores = list(language["score"])
cumulative_scores = [average(scores[:i]) for i in list(range(1,len(scores)+1))]
distance_from_latin = [abs(i-latin_average) for i in cumulative_scores]
low_borrowers = list(language["id"])[:distance_from_latin.index(min(distance_from_latin))+1]

# get an average borrowing score from WOLD
scores = []
for i in data["id"]:
    subset = wold[wold["Parameter_ID"] == i].copy()
    scores.append(average(subset["BorrowedScore"]))
data["wold"] = scores

# get an average low borrowing score from WOLD
low_wold = wold[wold["Language_ID"].isin(low_borrowers)]
scores = []
for i in data["id"]:
    subset = low_wold[low_wold["Parameter_ID"] == i].copy()
    scores.append(average(subset["BorrowedScore"]))
data["low_wold"] = scores


### 3 ### Add a binary score as well
data["binary_score"] = [1 if i > 0.7 else 0 for i in data["latin_score"]]


### 4 ### Export dataset
data.to_csv("datasets_automatic/loanwords_dataset.csv", sep=";", encoding="utf-8")


