# -*- coding: utf-8 -*-

"""
Output: Various syntax datasets
Used in: Chapter 6
Author: Reuben J. Pitts
Date: 14/03/2023
"""


### 0 ### Imports

# import required libraries
import pandas as pd

# import pandas
from CEIPoM_import import CEIPoM
from syntax_query import TreeSearch


### 1 ### Clean up data and add fields

# create a TreeSearch object
CEIPoM_syntax = TreeSearch(CEIPoM)

# filter by inscriptions with a date and at least one full sentence
CEIPoM = CEIPoM[CEIPoM["Finite_verb"] == True]
CEIPoM = CEIPoM[CEIPoM["Date_before"] != ""]

# create an average date field
CEIPoM["Date"] = [(i+j)/2 for i,j in zip(list(CEIPoM["Date_before"]),list(CEIPoM["Date_after"]))]

# create categories by century
CEIPoM["Century"] = [round((i+49)/100) for i in list(CEIPoM["Date"])]


### 2 ### Define a word-order function

def word_order(i, j):
    try:
        i = [int(CEIPoM_syntax.information("Token_position", t)) for t in i]
        j = [int(CEIPoM_syntax.information("Token_position", t)) for t in j]
    except:
        return None
    if len(i) > 0 and len(j) > 0 and max(i) < min(j):
        return 1
    elif len(i) > 0 and len(j) > 0 and max(j) < min(i):
        return 0
    else:
        return None
    # True = i precedes j


### 3 ### Create two object datasets (accusative and dative) and the adverbials

# filter objects from CEIPoM
objects = CEIPoM[CEIPoM["Relation"].str.contains("OBJ")].copy()
objects = objects[objects["Part_of_speech"] != "verb"]
print(len(objects))

# get siblings, heads, lengths, etc for each Token_ID
siblings = []
heads = []
constituent = []
verbal_head = []
main_clause = []

# get the required information
for i in objects.index:
    s = CEIPoM_syntax.smart_siblings(i)
    h = CEIPoM_syntax.smart_parents(i)
    
    # get length of each constituent
    c = sum([len(CEIPoM_syntax.direct_tree_children(i)) for i in s]) + len(s)
    
    # get info about the verbal head
    if len(h) > 0:
        verbal_head.append(CEIPoM_syntax.information("Classical_Latin_equivalent",h[0]))
        main_clause.append(CEIPoM_syntax.information("Relation",h[0]))
    else:
        verbal_head.append("")
        main_clause.append("")
        
    # add them to the lists
    siblings.append(s)
    heads.append(h)
    constituent.append(c)
    
    # this might take a while, so keep track of where we are
    print(list(objects.index).index(i),len(objects))

# add them to the dataframe
objects = objects.copy()
objects["Heads"] = heads
objects["Siblings"] = siblings
objects["Constituent"] = constituent
objects["Verbal_head"] = verbal_head

# specify whether main clause or not
objects["Main_clause"] = [1 if i in ["PRED","PRED_CO"] else 0 for i in main_clause]

# specify the word order isogloss
objects["Order"] = [word_order(i,j) for i,j in zip(list(objects["Heads"]),list(objects["Siblings"]))]

# filter out Nones
objects = objects[objects["Order"].isin([0,1])]
objects = objects.copy()
objects["Order"] = [int(i) for i in list(objects["Order"])]

# filter sibling doubles
objects["Check"] = [str(sorted(i)) for i in objects["Siblings"]]
objects = objects.drop_duplicates(subset=["Check"])

# add Konneker variable
Konneker_young = [1513, 1481, 1113, 1300, 1255, 1305, 1297, 1214, 1303, 1304, 1483, 1484, 1485, 1487, 1442]
Konneker_old = [1298, 962, 963, 1070, 1068, 1067, 1066, 1064, 1059, 1062, 921, 910, 1027, 977, 975, 978, 976, 1036, 1203, 1477, 1428, 1161]
konneker = zip([1 if t in Konneker_young else 0 for t in list(objects["Text_ID"])],[-1 if t in Konneker_old else 0 for t in list(objects["Text_ID"])])
objects["Konneker"] = [y + o for y,o in konneker]

# export the dataframes
objects[objects["Case"] == "ACC"].to_csv("datasets_automatic/order_accusative.csv", sep=";", encoding="utf-8")
objects[objects["Case"] == "DAT"].to_csv("datasets_automatic/order_dative.csv", sep=";", encoding="utf-8")


### 3 ### Create adverb dataframe

# filter adverbials from CEIPoM
adverbs = CEIPoM[CEIPoM["Relation"].str.contains("ADV")].copy()
adverbs = adverbs[adverbs["Part_of_speech"].isin(["noun","adjective","pronoun","adverb"])]
print(len(adverbs))

# get siblings, heads, lengths, etc for each Token_ID
siblings = []
heads = []
constituent = []
verbal_head = []
main_clause = []
verb_or_not = []

# get the required information
for i in adverbs.index:
    s = CEIPoM_syntax.smart_siblings(i)
    h = CEIPoM_syntax.smart_parents(i)
    
    # get length of each constituent
    c = sum([len(CEIPoM_syntax.direct_tree_children(i)) for i in s]) + len(s)
    
    # get info about the verbal head
    if len(h) > 0:
        verbal_head.append(CEIPoM_syntax.information("Classical_Latin_equivalent",h[0]))
        main_clause.append(CEIPoM_syntax.information("Relation",h[0]))
        verb_or_not.append(CEIPoM_syntax.information("Part_of_speech",h[0]))
    else:
        verbal_head.append("")
        main_clause.append("")
        verb_or_not.append("")
        
    # add them to the lists
    siblings.append(s)
    heads.append(h)
    constituent.append(c)
    
    # this might take a while, so keep track of where we are
    print(list(adverbs.index).index(i),len(adverbs))

# add them to the dataframe
adverbs = adverbs.copy()
adverbs["Heads"] = heads
adverbs["Siblings"] = siblings
adverbs["Constituent"] = constituent
adverbs["Verbal_head"] = verbal_head
adverbs["Verb_or_not"] = verb_or_not

# specify whether main clause or not
adverbs["Main_clause"] = [1 if i in ["PRED","PRED_CO"] else 0 for i in main_clause]

# eliminate adverbs whose head is not a verb
adverbs = adverbs[adverbs["Verb_or_not"] == "verb"]

# specify the word order isogloss
adverbs["Order"] = [word_order(i,j) for i,j in zip(list(adverbs["Heads"]),list(adverbs["Siblings"]))]

# filter out Nones
adverbs = adverbs[adverbs["Order"].isin([0,1])]
adverbs = adverbs.copy()
adverbs["Order"] = [int(i) for i in list(adverbs["Order"])]

# filter sibling doubles
adverbs["Check"] = [str(sorted(i)) for i in adverbs["Siblings"]]
adverbs = adverbs.drop_duplicates(subset=["Check"])

# export the dataframes
adverbs.to_csv("datasets_automatic/order_adverbial.csv", sep=";", encoding="utf-8")


### 4 ### Create the nominal attribute dataframes

# get CEIPoM self-merged to specify heads
attributes = CEIPoM.copy()
attributes = attributes.merge(attributes, how="inner", left_on="Head", right_index=True, suffixes=["","_head"])

# now filter actual attributes
attributes = attributes[attributes["Relation"].str.contains("ATR")]
print(len(attributes))

# get rid of relationships we don't want
attributes = attributes[~attributes["Relation_head"].str.contains("COORD")]
attributes = attributes[~attributes["Relation_head"].str.contains("Aux")]

# add a word order column
attributes["Order"] = [word_order([i],[j]) for i,j in zip(list(attributes["Head"]),list(attributes.index))]

# filter out Nones
attributes = attributes[attributes["Order"].isin([0,1])]
attributes = attributes.copy()
attributes["Order"] = [int(i) for i in list(attributes["Order"])]

# export the dataframes
attributes[attributes["Case"] == "GEN"].to_csv("datasets_automatic/order_genitive.csv", sep=";", encoding="utf-8")
attributes[attributes["Part_of_speech"].isin(["adjective","numeral"])].to_csv("datasets_automatic/order_adjective.csv", sep=";", encoding="utf-8")


    
    
    
    
    
    
    
    
    