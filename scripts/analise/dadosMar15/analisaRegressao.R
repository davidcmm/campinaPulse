#!/bin/Rscript

#Agradavel
data = read.table("rgbQScoreAgrad.dat", header=TRUE)
dados = data.frame(qscore=data$qscore, red=data$red, green=data$green, blue=data$blue, diag=data$diag, hor=data$hor, vert=data$vert)

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
data = read.table("rgbQScoreSeg.dat", header=TRUE)
dados = data.frame(qscore=data$qscore, red=data$red, green=data$green, blue=data$blue, diag=data$diag, hor=data$hor, vert=data$vert)

print(">>>> Regressao Seguro: qscore = red + green + blue + diag + hor + vert")
modelo = lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
modelo
summary(modelo)

print(">>>> Regressao Seguro: qscore = red + green + diag + hor")
modelo = lm(qscore ~ red + green + diag + hor, data=dados)
modelo
summary(modelo)
