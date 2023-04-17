# -*- coding: utf-8 -*-

"""
Output: Regression analysis for accusative object order
Used in: Chapter 6
Author: Reuben J. Pitts
Date: 22/03/2023
"""


### 0 ### Imports

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (21,13)

# specify fonts
plt.rcParams['font.family'] = 'Brill'
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.size'] = 20

# import datasets
plot_language = pd.read_csv("regression_datasets/effect_plot_language.csv")
plot_date = pd.read_csv("regression_datasets/effect_plot_date.csv")
mixed_plot_language = pd.read_csv("regression_datasets/effect_plot_language_mixed.csv")
mixed_plot_date = pd.read_csv("regression_datasets/effect_plot_date_mixed.csv")

[plot_language,mixed_plot_language]
[plot_date,mixed_plot_date]


### 1 ### Create dataset
fig, axs = plt.subplots(2, 2)

data = [plot_language, mixed_plot_language]
titles = ["Fixed-effects model","Mixed-effects model"]

for i, ax in enumerate(axs[0]):

    x = data[i]["Language"]
    y = data[i]["fit"]
    yupper = data[i]["upper"] - data[i]["fit"]
    ylower = data[i]["fit"] - data[i]["lower"]
    
    ax.set_title(titles[i],fontsize=29)
    ax.plot(x, y, c='#1f77b4', linewidth=3)
    ax.errorbar(x, y, yerr=[ylower, yupper], capsize=10)

    ax.set_ylabel("object-verb        ...        verb-object")
    ax.set_ylim([0,1])
    
    ax.get_yaxis().set_ticks([])

data = [plot_date, mixed_plot_date]

for i, ax in enumerate(axs[1]):
        
    x = data[i]["Date"]
    y = data[i]["fit"]
    ylower = data[i]["upper"]
    yupper = data[i]["lower"]
        
    ax.plot(x, y, c='#1f77b4', linewidth=3)
    ax.fill_between(x, ylower, yupper, color='#1f77b4', alpha=0.2)
    
    ax.set_ylabel("object-verb        ...        verb-object")
    ax.set_xlabel("date (BCE)")
    
    ax.set_ylim([0,1])
    ax.set_xlim([-620,-50])
        
    ax.get_yaxis().set_ticks([])

# remove white space between axes
plt.subplots_adjust(wspace=0.1)


### 3 ### Export

# specify margins
fig_width, fig_height = fig.get_size_inches()
left_margin = -1.5
right_margin = fig_width + 1.5
bottom_margin = -1.5
top_margin = fig_height + 1.5
bbox = Bbox.from_extents(left_margin, bottom_margin, right_margin, top_margin)

# save and show figure
plt.savefig('figures/syntax_regression.pdf', bbox_inches=bbox, dpi=600)