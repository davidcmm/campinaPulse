#!/bin/Rscript
# Analyses the regression of QScore in terms of color and amount of lines according to previous data of all-subset
library(leaps)

args <- commandArgs(trailingOnly = TRUE)

#Agradavel
data = read.table(args[1], header=TRUE)

#Evaluating possible regressions with all-subset
dados = data.frame(qscore=data$qscore, red=data$red, green=data$green, blue=data$blue, diag=data$diag, hor=data$hor, vert=data$vert)
regsubsets.out <- regsubsets(qscore ~ red + green + blue + diag + vert + hor, data = dados, nbest = 1, nvmax = NULL, force.in = NULL, force.out = NULL, method = "exhaustive")
jpeg(file = paste(args[1], ".jpg"))
plot(regsubsets.out, scale = "adjr2", main = "Adjusted R^2")
               
print(">>>> Regressao Agradavel: qscore = red + green + blue + diag + hor + vert")
#modelo = lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
modelo = lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
modelo
summary(modelo)

print(">>>> Regressao Agradavel: qscore = red + green + blue + diag")
#modelo = lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
modelo = lm(qscore ~ red + green + blue + diag, data=dados)
modelo
summary(modelo)


#Segurança
data = read.table(args[2], header=TRUE)

#Evaluating possible regressions with all-subset
dados = data.frame(qscore=data$qscore, red=data$red, green=data$green, blue=data$blue, diag=data$diag, hor=data$hor, vert=data$vert)
regsubsets.out <- regsubsets(qscore ~ red + green + blue + diag + vert + hor, data = dados, nbest = 1, nvmax = NULL, force.in = NULL, force.out = NULL, method = "exhaustive")
jpeg(file = paste(args[2], ".jpg"))
plot(regsubsets.out, scale = "adjr2", main = "Adjusted R^2")

print(">>>> Regressao Seguro: qscore = red + green + blue + diag + hor + vert")
modelo = lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
modelo
summary(modelo)

print(">>>> Regressao Seguro: qscore = red + green + diag + hor")
modelo = lm(qscore ~ red + green + diag + hor, data=dados)
modelo
summary(modelo)
