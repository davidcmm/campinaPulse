#!/bin/Rscript
# Analyses the regression of QScore in terms of color and amount of lines according to previous data of all-subset
library(leaps)

calculateRegression <- function(file1, file2, shouldPlot=FALSE){
    #Agradavel
    data = read.table(file1, header=TRUE)
    
    #Evaluating possible regressions with all-subset
    dados = data.frame(qscore=data$qscore, red=data$red, green=data$green, blue=data$blue, diag=data$diag, hor=data$hor, vert=data$vert)
    regsubsetsAgrad.out <<- regsubsets(qscore ~ red + green + blue + diag + vert + hor, data = dados, nbest = 1, nvmax = NULL, force.in = NULL, force.out = NULL, method = "exhaustive")
    if(shouldPlot){
      pdf(file = paste(file1, ".pdf"))
      plot(regsubsetsAgrad.out, scale = "adjr2", main = "Adjusted R^2")
      dev.off()
    }
                   
    print(">>>> Regressao Agradavel: qscore = red + green + blue + diag + hor + vert")
    #modelo = lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
    modeloAgrad <<- lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
    print(modeloAgrad)
    print(summary(modeloAgrad))
    
    #print(">>>> Regressao Agradavel: qscore = red + green + blue + diag")
    #modelo = lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
    #modelo = lm(qscore ~ red + green + blue + diag, data=dados)
    #print(modelo)
    #print(summary(modelo))
    
    #Seguranca
    data = read.table(file2, header=TRUE)

    #Evaluating possible regressions with all-subset
    dados = data.frame(qscore=data$qscore, red=data$red, green=data$green, blue=data$blue, diag=data$diag, hor=data$hor, vert=data$vert)
    regsubsetsSeg.out <<- regsubsets(qscore ~ red + green + blue + diag + vert + hor, data = dados, nbest = 1, nvmax = NULL, force.in = NULL, force.out = NULL, method = "exhaustive")
    if(shouldPlot){
        pdf(file = paste(file2, ".pdf"))
        plot(regsubsetsSeg.out, scale = "adjr2", main = "Adjusted R^2")
        dev.off()
    }
    
    print(">>>> Regressao Seguro: qscore = red + green + blue + diag + hor + vert")
    modeloSeg <<- lm(qscore ~ red + green + blue + diag + hor + vert, data=dados)
    print(modeloSeg)
    print(summary(modeloSeg))
    
    #print(">>>> Regressao Seguro: qscore = red + green + diag + hor")
    #modelo = lm(qscore ~ red + green + diag + hor, data=dados)
    #print(modelo)
    #print(summary(modelo))
}


args <- commandArgs(trailingOnly = TRUE)

if (length(args) > 1){
    #Agradavel
    file1 = args[1]
    
    #Seguranca
    file2 = args[2]
    
    calculateRegression(file1, file2, TRUE)
}