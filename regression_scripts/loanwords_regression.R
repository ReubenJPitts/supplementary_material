# -*- coding: utf-8 -*-

"""
Output: Regression analysis for Latin loanwords
Used in: Chapter 5
Author: Reuben J. Pitts
Date: 23/03/2023
"""


### 0 ### Imports

library(stringr)
library(dplyr)
library(effects)
library(lme4)
library(lmerTest)
library(lmtest)
library(MuMIn)
library(reshape2)

options(scipen = 10)
rm(list = ls())
set.seed(19790427)

"%ni%" <- Negate("%in%")


## 1 ## Import and modify the dataset

# import
DRP <- read.csv(file="datasets_automatic/loanwords_dataset.csv", header=TRUE, stringsAsFactors=TRUE, sep=";")
str(DRP)


## 2 ## Run a model

# create model
model <-    glm(binary_score ~ distance_from_hearth + frequency + wold,
            data = DRP,
            family = "binomial")

# visualise
plot(effect("wold", model), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of partial effect of date", xlab="WOLD")
plot(effect("frequency", model), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of frequency", xlab="Frequency")
plot(effect("distance_from_hearth", model), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of DFH", xlab="DFH")

# export
plot_date <- effect("wold", model, xlevels=1000)
write.csv(plot_date, file = "regression_datasets/effect_plot_loanwords.csv", row.names = FALSE, fileEncoding = "UTF-8")
