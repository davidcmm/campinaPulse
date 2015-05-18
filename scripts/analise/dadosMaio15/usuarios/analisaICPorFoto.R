#!/bin/Rscript
# Calculates the confidence interval of qscores for each city point for each of the groups received

args <- commandArgs(trailingOnly = TRUE)

ic <- function(x) { 
	return (sd(x)/sqrt(length(x))*qt(.9995,11)) 
}

data1 <- read.table(args[1])
data2 <- read.table(args[2])

#Selecting only qscores
newdata1 <- data1 [ c(4:1003) ]
newdata2 <- data2 [ c(4:1003) ]

icData1 <- apply(newdata1, 1, ic)
icData2 <- apply(newdata2, 1, ic)

#Saving data
newframe1 <- data.frame(ques=data1$V1, photo=data1$V2, mean=data1$V3, dist=icData1, inf=data1$V3-icData1, sup=data1$V3+icData1)
newframe1 <- newframe1[with(newframe1, order(photo)), ]
write.table(newframe1, "teste1.txt", sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)

newframe2 <- data.frame(ques=data2$V1, photo=data2$V2, mean=data2$V3, dist=icData2, inf=data2$V3-icData1, sup=data2$V3+icData1)
newframe2 <- newframe2[with(newframe2, order(photo)), ]
write.table(newframe2, "teste2.txt", sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)
