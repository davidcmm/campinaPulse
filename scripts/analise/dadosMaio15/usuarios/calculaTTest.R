#!/bin/Rscript
# Calculates the comparison tests (t-test and mann-whitney) for a set of two data sets

args <- commandArgs(trailingOnly = TRUE)

data1 = read.table(args[1])
data2 = read.table(args[2])
file1 = args[3]
file2 = args[4]
color = args[5]

print(">> Equal")
wilcox.test(data1$V3, data2$V3, alternative="t", paired=F)
t.test(data1$V3, data2$V3, alternative="t")

print(">> Less")
wilcox.test(data1$V3, data2$V3, alternative="l", paired=F)
t.test(data1$V3, data2$V3, alternative="l")

print(">> Greater")
wilcox.test(data1$V3, data2$V3, alternative="g", paired=F)
t.test(data1$V3, data2$V3, alternative="g")

#Creating boxplots of qscores per district
pdf(paste("boxplot", file1, ".pdf"), paper="special")
boxplot(data1$V3, main=paste("Boxplot", file1), col=color)

pdf(paste("boxplot", file2, ".pdf"), paper="special")
boxplot(data2$V3, main=paste("Boxplot", file2), col=color)

#Verifying if data is normal
pdf(paste("norm", file1, "-", file2, ".pdf"), paper="special")
par(mfrow=c(1,2))

qqnorm(data1$V3)
qqline(data1$V3)

qqnorm(data2$V3)
qqline(data2$V3)
