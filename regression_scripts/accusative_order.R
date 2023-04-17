# -*- coding: utf-8 -*-

"""
Output: Regression analysis for accusative object order
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


## 1 ## Import and modify the dataset

# import
DRP <- read.csv(file="datasets_automatic/order_accusative.csv", header=TRUE, stringsAsFactors=TRUE, sep=";")
str(DRP)

# add some columns
DRP$Head_reduced <- ave(as.character(DRP$Verbal_head), as.character(DRP$Verbal_head), FUN=function(i) replace(i, length(i) < 5, "REST"))
DRP$WordOrder <- relevel(as.factor(ifelse(DRP$Order == 1, "AfterVerb", ifelse(DRP$Order == 0, "BeforeVerb", NA))), ref="BeforeVerb")
DRP$MainClause <- relevel(as.factor(ifelse(DRP$Main_clause == 1, "Main", ifelse(DRP$Main_clause == 0, "Subordinate", NA))), ref="Main")

# show a tabulation of the distribution by language
table(DRP$WordOrder, DRP$Language)

# drop Old Sabellic and Venetic
DRP <- droplevels(filter(DRP, Language %ni% c("-", "Old Sabellic", "Venetic")))

# show a tabulation of the overall distribution
table(DRP$WordOrder)


## 2 ## Run some models

model <-    glm(WordOrder ~ Language + Date + Constituent + MainClause,
            data = DRP,
            family = "binomial")

plot(effect("Language", model), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of partial effect of language", xlab="Language")
plot(effect("Date", model), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of partial effect of date", xlab="Date")
plot(effect("Constituent", model), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of partial effect of length", xlab="Length")

plot_language <- effect("Language", model)
plot_date <- effect("Date", model, xlevels=1000)

mixed <-    glmer(WordOrder ~ Language + Date + Constituent + MainClause + (1|Head_reduced),
            data = DRP,
            family = "binomial",
            control = glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 100000)))

plot(effect("Language", mixed), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of partial effect of language", xlab="Language")
plot(effect("Date", mixed), multiline=TRUE, rescale.axis=FALSE, ylim=c(0,1), main="Effect plot of partial effect of date", xlab="Language")

mixed_plot_language <- effect("Language", mixed)
mixed_plot_date <- effect("Date", mixed, xlevels=1000)


### 3 ### Export csv files for plot
write.csv(plot_language, file = "regression_datasets/effect_plot_language.csv", row.names = FALSE, fileEncoding = "UTF-8")
write.csv(plot_date, file = "regression_datasets/effect_plot_date.csv", row.names = FALSE, fileEncoding = "UTF-8")
write.csv(mixed_plot_language, file = "regression_datasets/effect_plot_language_mixed.csv", row.names = FALSE, fileEncoding = "UTF-8")
write.csv(mixed_plot_date, file = "regression_datasets/effect_plot_date_mixed.csv", row.names = FALSE, fileEncoding = "UTF-8")


### 4 ## Run some models on a single language

LDRP <- droplevels(filter(DRP, Language %in% c("Latin")))
table(LDRP$WordOrder, LDRP$Date)

model <-    glm(WordOrder ~ Date + Constituent + MainClause,
            data = LDRP,
            family = "binomial")

mixed <-    glmer(WordOrder ~ Date + Constituent + MainClause + (1|Head_reduced),
            data = LDRP,
            family = "binomial",
            control = glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 100000)))


