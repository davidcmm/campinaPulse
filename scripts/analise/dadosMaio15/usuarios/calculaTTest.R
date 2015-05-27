#!/bin/Rscript
# Calculates the comparison tests (t-test and mann-whitney) for a set of two data sets

calculateTTests <- function(file1, file2, output1, output2, color, shouldPlot=FALSE){

    data1 <<- read.table(file1)
    data2 <<- read.table(file2)
    
    print(">> Equal")
    res<-wilcox.test(data1$V3, data2$V3, alternative="t", paired=F)
    print(paste(res$method, " ", res$p.value, " ", res$alternative))
    res <- t.test(data1$V3, data2$V3, alternative="t")
    print(paste(res$method, " ", res$p.value, " ", res$alternative))
    
    print(">> Less")
    res <- wilcox.test(data1$V3, data2$V3, alternative="l", paired=F)
    print(paste(res$method, " ", res$p.value, " ", res$alternative))
    res <- t.test(data1$V3, data2$V3, alternative="l")
    print(paste(res$method, " ", res$p.value, " ", res$alternative))
    
    print(">> Greater")
    res <- wilcox.test(data1$V3, data2$V3, alternative="g", paired=F)
    print(paste(res$method, " ", res$p.value, " ", res$alternative))
    res <- t.test(data1$V3, data2$V3, alternative="g")
    print(paste(res$method, " ", res$p.value, " ", res$alternative))
    
    #Creating boxplots of qscores per district
    if (shouldPlot){
        pdf(paste("boxplot", output1, ".pdf"), paper="special")
        boxplot(data1$V3, main=paste("Boxplot", output1), col=color)
        
        pdf(paste("boxplot", output2, ".pdf"), paper="special")
        boxplot(data2$V3, main=paste("Boxplot", output2), col=color)
        
        #Verifying if data is normal
        pdf(paste("norm", output1, "-", output2, ".pdf"), paper="special")
        par(mfrow=c(1,2))
        
        qqnorm(data1$V3)
        qqline(data1$V3)
        
        qqnorm(data2$V3)
        qqline(data2$V3)
        
        dev.off()
    }
}

args <- commandArgs(trailingOnly = TRUE)

if(length(args) > 1){
    calculateTTests(args[1], args[2], args[3], args[4], args[5], TRUE)
}
