#!/bin/Rscript
suppressMessages(library(ggplot2, quietly=TRUE))
suppressMessages(library(plyr, quietly=TRUE))
suppressMessages(library(scales, quietly=TRUE))
suppressMessages(library(reshape, quietly=TRUE))

#Gerando percentuais gerais
args <- commandArgs(trailingOnly = TRUE)
data <- read.table(args[1], skip=1)

data$V4 <- data$V2/661
data$V5 <- data$V2/data$V3

sorted <- data[order(-data$V4),]
write.table(sorted, file="percentualGeralPorTotalDeComparacoes.dat")
sorted <- data[order(-data$V5),]
write.table(sorted, file="percentualGeralPorComparacoes.dat")
