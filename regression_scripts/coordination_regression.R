# -*- coding: utf-8 -*-

"""
Output: Regression analysis for Latin coordination
Used in: Chapter 6
Author: Reuben J. Pitts
Date: 22/03/2023
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
#source("ClaesFunction_sum_stats.txt")


## 1 ## Import and modify the dataset

# import
DRP <- read.csv(file="datasets_automatic/coordination_dataset.csv", header=TRUE, stringsAsFactors=TRUE, sep=";")
str(DRP)

# only interested in Latin, and -que / et
DRP <- droplevels(filter(DRP, Language %in% c("Latin")))
DRP <- droplevels(filter(DRP, Strategy %in% c("P","S")))

# add some columns
DRP$Isogloss <- relevel(as.factor(ifelse(DRP$Strategy == "P", "que", ifelse(DRP$Strategy == "S", "et", NA))), ref="et")
DRP$Date_average <- (DRP$Date_before + DRP$Date_after) / 2


## 2 ## Run a model

# create model
model <-    glm(Isogloss ~ Date_average,
            data = DRP,
            family = "binomial")

# visualise
plot(effect("Date_average", model), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of partial effect of date", xlab="Date")

# export
plot_date <- effect("Date_average", model, return.grid = TRUE)
write.csv(plot_date, file = "regression_datasets/effect_plot_coordination.csv", row.names = FALSE, fileEncoding = "UTF-8")
