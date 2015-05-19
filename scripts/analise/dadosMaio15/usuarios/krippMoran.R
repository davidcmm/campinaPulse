#!/bin/Rscript
# Calculates the Krippendorf Alpha for general data and the Moran I score
library(irr)
library(ape)

args <- commandArgs(trailingOnly = TRUE)

#Kripp
krippAlpha <- function () {
	agra <- args[2]
	seg <- args[3]

	dadosAgra <- read.table(agra, header=TRUE, row.names=1)
	dadosSeg <- read.table(seg, header=TRUE, row.names=1)
	matrizAgra <- data.matrix(dadosAgra)
	matrizSeg <- data.matrix(dadosSeg)

	res <- kripp.alpha(matrizAgra, method="nominal")
	res1 <- kripp.alpha(matrizSeg, method="nominal")
	print (">>> Agra")
	print (res)
	print (">>> Seg")
	print (res1)
}


#Moran I
moranI <- function () {
	agra <- args[2]
	seg <- args[3]

	data <- read.table(agra, sep="+", header=F)
	data.dists <- as.matrix(dist(cbind(data$V5, data$V4)))

	data.dists.inv <- 1/(1+data.dists)
	diag(data.dists.inv) <- 0
	
	print(">> Agradavel observed expected p.value")
	result <- Moran.I(data$V3, data.dists.inv)
	print(paste(result$observed, " ", result$expected, " ", result$p.value))

	data <- read.table(seg, sep="+", header=F)
	data.dists <- as.matrix(dist(cbind(data$V5, data$V4)))

	data.dists.inv <- 1/(1+data.dists)
	diag(data.dists.inv) <- 0
	
	print(">> Seguro observed expected p.value")
	result <- Moran.I(data$V3, data.dists.inv)
	print(paste(result$observed, " ", result$expected, " ", result$p.value))
}

execute <- args[1]

if (execute == 'both'){
	krippAlpha()
	moranI()	
} else if (execute == 'moran') {
	moranI()
} else if (execute == 'kripp') {
	krippAlpha()
}
