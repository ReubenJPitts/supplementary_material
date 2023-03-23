# -*- coding: utf-8 -*-

"""
Output: Regression analysis for coordination
Used in: Chapter 6
Author: Reuben J. Pitts
Date: 22/03/2023
"""


### 0 ### Imports

# import libraries
import pandas as pd
import matplotlib.pyplot as plt

# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor']='white'
plt.rcParams["figure.figsize"] = (20,10)
plt.rcParams.update({'font.size': 22})

# import datasets
data = pd.read_csv("regression_datasets/effect_plot_coordination.csv")


### 1 ### Create plot
fig, ax = plt.subplots()

x = data["Date_average"]
y = data["fit"]

yupper = data["upper"]
ylower = data["lower"]

ax.plot(x, y, c='#1f77b4', linewidth=3)
ax.fill_between(x, ylower, yupper, color='#1f77b4', alpha=0.2)

ax.set_ylabel("que        ...        et")
ax.set_ylim([0,1])
    
ax.get_yaxis().set_ticks([])
#ax.get_xaxis().set_ticks([])


### 2 ### Save the plot
plt.savefig('figures/coordination_regression.png', bbox_inches='tight', dpi=600)