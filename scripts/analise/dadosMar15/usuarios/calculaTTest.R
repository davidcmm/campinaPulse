#!/bin/Rscript
# Calculates the t.test for a set of two data sets

args <- commandArgs(trailingOnly = TRUE)

data1 = read.table(args[1])
data2 = read.table(args[2])

print(">> Equal")
t.test(data1$V3, data2$V3, alternative="t")

print(">> Less")
t.test(data1$V3, data2$V3, alternative="l")

print(">> Greater")
t.test(data1$V3, data2$V3, alternative="g")
