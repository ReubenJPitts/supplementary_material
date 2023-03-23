# -*- coding: utf-8 -*-

"""
Output: Figures typology_dendrogram.png, typology_heatmap.png, typology_mds.png, typology_mds_subsets.png
Used in: Chapter 11
Author: Reuben J. Pitts
Date: 14/03/2023
"""


### 0 ### imports

# import some libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from adjustText import adjust_text
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

# set some matplotlib parameters
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (30,15)
plt.rcParams.update({'font.size': 17})

# import the datasets
data = pd.read_csv("datasets_manual/typology.csv", sep=";")
data = data.sort_values(by="ID")
wals = pd.read_csv("WALS/values.csv", sep=",")


### 1 ### some important underlying definitions

# define how percentages work
def percentage(i,j):
    if i == 0:
        return np.nan
    return j / (i / 100)
    
# set up a distance metric
def item_distance(i,j):
    if i == 0 or j == 0:
        return 0, 0
    elif i == j:
        return 1, 0
    else:
        return 1, 1

# apply the distance metric to a list, accounting correctly for missing values
def list_distance(l1,l2):
    total = 0
    distance = 0
    for i, j in zip(l1,l2):
        x, y = item_distance(i,j)
        total += x
        distance += y
    return percentage(total, distance) / 100

# calculate the distance of two languages in *data*
def language_distance(x,y):
    x = list(data[x])
    y = list(data[y])
    return list_distance(x,y)

# get the information for a specific language in the WALS dataset
def language_wals(l):
    subset = wals[wals["Language_ID"] == l].copy()
    subset = subset[subset["Parameter_ID"].str.contains("A")]
    parametres = [int(i[:-1]) for i in subset["Parameter_ID"]]
    values = list(subset["Value"])
    output = [0]*len(data)
    ids = list(data["ID"])
    for p,v in zip(parametres,values):
        if p in ids:
            output[ids.index(p)] = v
    return output

# turn a list of languages into a list of all possible pairs
def pairify(l):
    pairs = [(x, y) for x in l for y in l]
    pairs = [tuple(sorted(i)) for i in pairs]
    pairs = list(dict.fromkeys(pairs))
    pairs = [(i,j) for i,j in pairs if i != j]
    return pairs


### 2 ### the key definitions which do the heavy lifting

# turn the dataset into a similarity matrix
def similarity(df, p=3, m=0.25):
    
    # l defines the number of columns which should be ignored on the left (containing e.g. feature descriptions)
    # m defines the number of values a language must minimally attest to be included
    
    # sift out irrelevant columns, based on value of l and m:
    for l in list(df.columns)[p:]:
       if len([i for i in list(df[l]) if i != 0]) / len(df) < 0.25:
           df = df.drop(columns=[l])

    # get a list of the relevant selection of languages
    languages = list(df.columns)[p:]

    # create a similarity matrix of these languages
    output = []
    for i in languages:
        row = []
        for j in languages:
            row.append(language_distance(i,j))
        output.append(row)
        
    # turn into a pandas dataframe and return
    return pd.DataFrame(output, index=languages, columns=languages)

# reduce the dimensionality of the similarity matrix
def mds(matrix):
    
    # define an mds model
    model = MDS(dissimilarity="precomputed")
    mds_data = model.fit_transform(matrix)

    # get two dimensions to visualise and return them
    x = mds_data[:, 0]
    y = mds_data[:, 1]
    return x, y

# create a hierarchical clustering dendrogram
def hcd(matrix):

    # set the model
    distances_hca = matrix.to_numpy()
    cluster = AgglomerativeClustering(distance_threshold=0, n_clusters=None, affinity='precomputed', linkage='single')
    model = cluster.fit(distances_hca)

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    # return useful output
    linkage_matrix = np.column_stack([model.children_, model.distances_, counts]).astype(float)
    return linkage_matrix


### 3 ### process the typological dataset and fetch some exploratory statistics

# define the WALS codes for the modern languages we're interested in
modern = {"bsq":"Basque", "fre":"French", "iri":"Irish", "spa":"Spanish", "grk":"Greek", "aeg":"Arabic", "heb":"Hebrew", "ita":"Italian", "alb":"Albanian", "scr":"Serbian-Croatian"}

# add them to the dataset
for l in list(modern.keys()):
    data[modern[l]] = language_wals(l)


### 4 ### get some statistics

# get the average distance for all languages
all_languages = list(data.columns)[4:]
print(np.mean([language_distance(i,j) for i,j in pairify(all_languages)]))

# get the average distance for all ancient languages
all_ancient = ['Latin','Oscan','Venetic','Umbrian','Old_Sabellic','Etruscan','Messapic','Phrygian','Greek_Ancient','Gaulish','Punic']
print(np.mean([language_distance(i,j) for i,j in pairify(all_ancient)]))

# get the average distance for all ancient IE languages
all_ancient = ['Latin','Oscan','Venetic','Umbrian','Old_Sabellic','Messapic','Phrygian','Greek_Ancient','Gaulish']
print(np.mean([language_distance(i,j) for i,j in pairify(all_ancient)]))

# get the average distance within Italy
ancient_italy = ['Latin','Oscan','Venetic','Umbrian','Old_Sabellic','Etruscan','Messapic']
print(np.mean([language_distance(i,j) for i,j in pairify(ancient_italy)]))

# get the average distance within Italy without Etruscan
ancient_italy = ['Latin','Oscan','Venetic','Umbrian','Old_Sabellic','Messapic']
print(np.mean([language_distance(i,j) for i,j in pairify(ancient_italy)]))
print(np.mean([language_distance(i,"Etruscan") for i in ancient_italy]))


### 5 ### show a heatmap

# turn the (dissimilarity) matrix into a similarity matrix and round the numbers
matrix = similarity(data)
languages = list(matrix.index)
matrix = matrix.to_numpy()
matrix = 1 - matrix
matrix = matrix.round(2)

# create the heatmap figure
fig, ax = plt.subplots()
im = ax.imshow(matrix, cmap="Blues")

# set the names of the languages along the axes
ax.set_xticks(np.arange(len(languages)), labels=languages)
ax.set_yticks(np.arange(len(languages)), labels=languages)

# rotate the x-axis language labels by 45 degrees
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# put the similarity values on the plot
for i in range(len(languages)):
    for j in range(len(languages)):
        if i != j:
            text = ax.text(j, i, matrix[i, j], ha="center", va="center", color="black")

# add a title and turn the square plot into a rectangle
ax.set_title("similarity matrix (darker = more similar)")
ax.set_aspect(0.7)

# display and save the plot
plt.savefig('figures/typology_heatmap.png', bbox_inches='tight', dpi=600)
plt.show()


### 6 ### visualise a dendrogram

# set some parametres
plt.rcParams['lines.linewidth'] = 3.0

# first define the model
matrix = similarity(data)
languages = list(matrix.index)
dendrodata = hcd(matrix)

# create a new plot
fig, ax = plt.subplots(figsize=(15,25))

# create the dendrogram
dendrogram(dendrodata, color_threshold=0, orientation="right")

# add the language labels
ax.set_yticks((np.arange(len(languages))*10)+5)
ax.set_yticklabels([languages[int(i.get_text())] for i in ax.get_yticklabels()],fontsize=20)
ax.set_xticklabels(["","",""])

# display and save the plot
plt.savefig('figures/typology_dendrogram.png', bbox_inches='tight', dpi=600)
plt.show()


### 7 ### visualise MDS with three plots (genealogy, chronology)

# first define the model
matrix = similarity(data)
languages = list(matrix.index)
x, y = mds(matrix)

# size markers by attestation
language_att = [len(data[data[i] != 0]) for i in languages]
size = [(i*2)-30 for i in language_att]
size = [30 if i < 30 else i for i in size]

# create a plot with three vertical subplots
fig, [ax1, ax2, ax3] = plt.subplots(3, figsize=(15,30))

# for the first plot, define genealogical relations
colours = []
for l in languages:
    if l in ['Latin', 'Oscan', 'Umbrian', 'Old_Sabellic', 'French', 'Spanish', 'Italian']:
        colours.append("blue")
    if l in ['Venetic', 'Messapic', 'Greek_Ancient', 'Greek', 'Phrygian', 'Albanian', 'Serbian-Croatian']:
        colours.append("royalblue")
    if l in ['Gaulish', 'Irish']:
        colours.append("darkblue")
    if l in ['Etruscan']:
        colours.append("red")
    if l in ['Punic', 'Arabic', 'Hebrew']:
        colours.append("green")
    if l in ['Basque']:
        colours.append("orange")

# add first scatter plot
texts = []
for i in range(len(languages)):
    ax1.scatter(x[i], y[i], s=size[i], color=colours[i])
    
# add language labels and adjust
    if languages[i] == "Old_Sabellic":
        texts.append(ax1.text(x[i], y[i], "Old Sabellic"))
    elif languages[i] == "Greek_Ancient":
        texts.append(ax1.text(x[i], y[i], "Ancient Greek"))
    else:
        texts.append(ax1.text(x[i], y[i], languages[i]))

# add a title and legend
ax1.set_title("Colour-coded by genealogy", fontsize=22)
ax1.legend([patches.Patch(facecolor='blue'),patches.Patch(facecolor='darkblue'),patches.Patch(facecolor='royalblue'),patches.Patch(facecolor='red'),patches.Patch(facecolor='green'),patches.Patch(facecolor='orange')],
           ["Italic","Celtic","Other Indo-European","Tyrrhenian","Semitic","Basque"],
           bbox_to_anchor=(1.32, 0.75))
adjust_text(texts,ax=ax1)

# get rid of tick-labels
ax1.set_xticks([])
ax1.set_yticks([])

# for the second plot, define geography
colours = []
for l in languages:
    if l in ['Latin', 'Oscan', 'Umbrian', 'Old_Sabellic', 'Venetic', 'Messapic', 'Etruscan', 'Italian']:
        colours.append("blue")
    if l in ['Greek_Ancient','Greek', 'Albanian', 'Serbian-Croatian']:
        colours.append("red")
    if l in ['Gaulish', 'Basque', 'French', 'Irish', 'Spanish']:
        colours.append("orange")
    if l in ['Punic','Phrygian','Arabic','Hebrew']:
        colours.append("green")

# add second scatter plot
texts = []
for i in range(len(x)):
    ax2.scatter(x[i], y[i], s=size[i], color=colours[i])
    
    # add language labels and adjust
    if languages[i] == "Old_Sabellic":
        texts.append(ax2.text(x[i], y[i], "Old Sabellic"))
    elif languages[i] == "Greek_Ancient":
        texts.append(ax2.text(x[i], y[i], "Ancient Greek"))
    else:
        texts.append(ax2.text(x[i], y[i], languages[i]))

# add a title and legend
ax2.set_title("Colour-coded by geography", fontsize=22)
ax2.legend([patches.Patch(facecolor='blue'),patches.Patch(facecolor='red'),patches.Patch(facecolor='orange'),patches.Patch(facecolor='green')],
           ["Italy","Balkans","Western Europe","Eastern Mediterranean"],
           bbox_to_anchor=(1.34, 0.55))
adjust_text(texts,ax=ax2)

# get rid of tick-labels
ax2.set_xticks([])
ax2.set_yticks([])

# for the third plot, define chronology
colours = []
for l in languages:
    if l in ['Latin', 'Oscan', 'Umbrian', 'Old_Sabellic', 'Venetic', 'Messapic', 'Etruscan', 'Greek_Ancient', 'Gaulish', 'Phrygian', 'Punic']:
        colours.append("blue")
    if l in ['Basque', 'Greek', 'French', 'Irish', 'Spanish', 'Arabic', 'Hebrew', 'Italian', 'Albanian', 'Serbian-Croatian']:
        colours.append("orange")

# add third scatter plot
texts = []
for i in range(len(x)):
    ax3.scatter(x[i], y[i], s=size[i], color=colours[i])
    
    # add language labels and adjust
    if languages[i] == "Old_Sabellic":
        texts.append(ax3.text(x[i], y[i], "Old Sabellic"))
    elif languages[i] == "Greek_Ancient":
        texts.append(ax3.text(x[i], y[i], "Ancient Greek"))
    else:
        texts.append(ax3.text(x[i], y[i], languages[i]))

# add a title and legend
ax3.set_title("Colour-coded by chronology", fontsize=22)
ax3.legend([patches.Patch(facecolor='blue'),patches.Patch(facecolor='orange')],
           ["ancient languages","modern languages"],
           bbox_to_anchor=(1.30, 0.50))
adjust_text(texts,ax=ax3)

# get rid of tick-labels
ax3.set_xticks([])
ax3.set_yticks([])

# remove empty space between subplots
plt.subplots_adjust(wspace=0.1, hspace=0.1)

# display and save the plot
plt.savefig('figures/typology_mds.png', bbox_inches='tight', dpi=600)
plt.show()


### 8 ### multiple MDS by subset

# specify subsets and accompanying titles
criteria = ["Phonology","Morphology","Syntax"]
titles = ["Phonology","Morphology","Syntax"]

# reduce level of types
types = list(data["Category"])
types = ["Morphology" if i == "Categories" else i for i in types]
types = ["Morphology" if i == "Words" else i for i in types]
types = ["Syntax" if i == "Order" else i for i in types]
data["Category"] = types

# create a figure
fig, axes = plt.subplots(3, figsize=(15,30))

# iterate over subplots
for i, ax in enumerate(axes):
    
    # define the current subset
    criterion = criteria[i]
    title = titles[i]
    
    # add a title to the axis
    ax.set_title(title, fontsize=22)
    
    # select relevant subset of the typological dataset
    subset = data.copy()
    subset = subset[subset["Category"].str.contains(criterion)]
    
    # run the model
    matrix = similarity(subset)
    languages = list(matrix.index)
    x, y = mds(matrix)

    # define Ancient Italy as a specific colour
    colours = []
    for l in languages:
        if l in ['Latin', 'Oscan', 'Umbrian', 'Old_Sabellic', 'Venetic', 'Messapic', 'Etruscan']:
            colours.append("blue")
        else:
            colours.append("grey")
      
    # scatter the data
    texts = []
    for i in range(len(x)):
        ax.scatter(x[i], y[i], s=75, color=colours[i])
        
        # add language labels and adjust
        if languages[i] == "Old_Sabellic":
            texts.append(ax.text(x[i], y[i], "Old Sabellic"))
        elif languages[i] == "Greek_Ancient":
            texts.append(ax.text(x[i], y[i], "Ancient Greek"))
        else:
            texts.append(ax.text(x[i], y[i], languages[i]))
    
    # add legend
    ax.legend([patches.Patch(facecolor='blue'),patches.Patch(facecolor='grey')],
               ["Ancient Italian peninsula","Other languages"],
               bbox_to_anchor=(1.34, 0.55))

    # adjust text
    adjust_text(texts,ax=ax)
    
    # get rid of tick-labels
    ax.set_xticks([])
    ax.set_yticks([])

# remove empty space between subplots
plt.subplots_adjust(wspace=0.1, hspace=0.1)

# display and save the plot
plt.savefig('figures/typology_mds_subsets.png', bbox_inches='tight', dpi=600)
plt.show()








