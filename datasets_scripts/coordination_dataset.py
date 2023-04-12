# -*- coding: utf-8 -*-

"""
Output: Dataset italy_coordination.csv
Used in: Chapter 8
Author: Reuben J. Pitts
Date: 14/03/2023
"""

### 0 ### Imports

# import some required libraries
import pandas as pd

# import the CEIPoM data
from CEIPoM_import import CEIPoM
from syntax_query import TreeSearch
syntax = TreeSearch(CEIPoM)


### 1 ### Get the raw data for coordination in CEIPoM

# Get coordinating tokens and iterate over them
coords = list(CEIPoM[CEIPoM["Relation"] == "COORD"].index)
coord_data = []

for c in coords:
    row = [c]
    
    # Get the token and lemma
    row.append(syntax.lemma(c))
    row.append(syntax.token(c))

    # Get its relevant children
    children = syntax.direct_aux_co_children(c)
    if len(children) > 0:
        
        # Count the coordinands
        row.append(len(children))
    
        # Get the most common relation of its children
        row.append(max(set([syntax.relation(i) for i in children]), key = [syntax.relation(i) for i in children].count))

        # Get the most common part of speech of its children
        row.append(max(set([syntax.information("Part_of_speech",i) for i in children]), key = [syntax.information("Part_of_speech",i) for i in children].count))
    
        # Get the most common semantic category of its children
        row.append(max(set([syntax.information("Meaning_category",i) for i in children]), key = [syntax.information("Meaning_category",i) for i in children].count))
    
    else:
        row += ["NA","NA","NA","NA"]
    
    # Check if there are AuxY's among the topological children and how many
    row.append(len([i for i in syntax.direct_tree_children(c) if syntax.relation(i) == "AuxY"]))
    
    # Get other info
    row.append(syntax.information("Language_(text)",c))
    row.append(syntax.information("Date_before",c))
    row.append(syntax.information("Date_after",c))
    row.append(syntax.information("Sentence",c))
    
    # add this iteration to the data 
    coord_data.append(row)
    
# aggregate the information into a dataframe
data = pd.DataFrame(coord_data,columns=["Token_ID","Lemma","Token","Children","Relation","POS","Category","AuxY","Language","Date_before","Date_after","Sentence"])


### 2 ### Enrich the CEIPoM dataframe

# specify if the coordinands are names
data["Proper"] = [1 if i == "PROPER" else 0 for i in list(data["Category"])]

# specify if the coordinands are verbal
data["Verbs"] = [1 if i == "verb" else 0 for i in list(data["POS"])]

# specify if the coordinands are non-proper nominals
data["Nouns"] = [1 if i == "noun" and j != "PROPER" else 0 for i,j in zip(list(data["POS"]),list(data["Category"]))]

# specify if the coordination is polysyndetic
data["Polysyndeton"] = [1 if type(i) != str and i > 2 else 0 for i in list(data["Children"])]

# specify number of conjunctions
data["Bisyndeton"] = [1 if type(i) != str and i-1 == j else 0 for i,j in zip(list(data["Children"]),list(data["AuxY"]))]

# specify minus one strategy
data["Minus_one"] = [1 if type(i) != str and i-2 == j else 0 for i,j in zip(list(data["Children"]),list(data["AuxY"]))]

# label lexical nature of coordination strategies
primary = ["12472a","10362a","15180a","14490a"]
secondary = ["10385a","13568a","14730a","14512a"]

types = []
for l in list(data["Lemma"]):
    if l == "" or l == "-":
        types.append("A")
    elif l in primary:
        types.append("P")
    elif l in secondary:
        types.append("S")
    else:
        types.append("O")
data["Strategy"] = types


### 3 ### export the dataframe
data.to_csv("datasets_automatic/coordination_dataset.csv", sep=";", encoding="utf-8")

