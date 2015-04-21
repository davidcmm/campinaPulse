#!/bin/Rscript
# Calculates the Krippendorf Alpha for general data and the Moran I score
library(irr)
library(ape)

args <- commandArgs(trailingOnly = TRUE)

#Kripp
krippAlpha <- function () {
	dadosAgra <- read.table("consenseMatrixAgra.dat", header=TRUE, row.names=1)
	dadosSeg <- read.table("consenseMatrixSeg.dat", header=TRUE, row.names=1)
	matrizAgra <- data.matrix(dadosAgra)
	matrizSeg <- data.matrix(dadosSeg)

	kripp.alpha(matrizAgra, method="nominal")
	kripp.alpha(matrizSeg, method="nominal")
}


#Moran I
moranI <- function () {
	agra <- args[2]
	seg <- args[3]

	data<-read.table(agra, sep="+", header=F)
	ozone.dists <- as.matrix(dist(cbind(ozone$V5, ozone$V4)))

	ozone.dists.inv <- 1/(1+ozone.dists)
	diag(ozone.dists.inv) <- 0
	
	print(">> Agradavel")
	Moran.I(ozone$V3, ozone.dists.inv)

	data<-read.table(seg, sep="+", header=F)
	ozone.dists <- as.matrix(dist(cbind(ozone$V5, ozone$V4)))

	ozone.dists.inv <- 1/(1+ozone.dists)
	diag(ozone.dists.inv) <- 0
	
	print(">> Seguro")
	Moran.I(ozone$V3, ozone.dists.inv)
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
