#!/bin/Rscript

#Agradavel
data = read.table("rgbQScoreAgrad.dat")

dados = data.frame(qscore=data$V2, red=data$V3, green=data$V4, blue=data$V5)
print(">>>> Regressao Agradavel: qscore = red + green + blue")
modelo = lm(qscore ~ red + green + blue, data=dados)
modelo
summary(modelo)


#Segurança
data = read.table("rgbQScoreSeg.dat")

dados = data.frame(qscore=data$V2, red=data$V3, green=data$V4, blue=data$V5)
print(">>>> Regressao Seguro: qscore = red + green + blue")
modelo = lm(qscore ~ red + green + blue, data=dados)
modelo
summary(modelo)
