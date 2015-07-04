#!/bin/Rscript
# Calculates the comparison tests (t-test and mann-whitney) for a set of two data sets
library(ggplot2)

agradavel <- "agrad%C3%A1vel?"
seguro <- "seguro?"

calculateTTests2 <- function(file1, file2, output1, output2, shouldPlot=FALSE){
  data1 <<- read.table(file1)
  data2 <<- read.table(file2)
  
  agra1 <- data1[data1$V1 == agradavel,]
  agra2 <- data2[data2$V1 == agradavel,]
  
  seg1 <- data1[data1$V1 == seguro,]
  seg2 <- data2[data2$V1 == seguro,]
  
  print(">> Equal Agra")
  res<-wilcox.test(agra1$V3, agra2$V3, alternative="t", paired=F)
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  res <- t.test(agra1$V3, agra2$V3, alternative="t")
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  
  print(">> Less Agra")
  res <- wilcox.test(agra1$V3, agra2$V3, alternative="l", paired=F)
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  res <- t.test(agra1$V3, agra2$V3, alternative="l")
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  
  print(">> Greater Agra")
  res <- wilcox.test(agra1$V3, agra2$V3, alternative="g", paired=F)
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  res <- t.test(agra1$V3, agra2$V3, alternative="g")
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  
  print(">> Equal Seg")
  res<-wilcox.test(seg1$V3, seg2$V3, alternative="t", paired=F)
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  res <- t.test(seg1$V3, seg2$V3, alternative="t")
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  
  print(">> Less Seg")
  res <- wilcox.test(seg1$V3, seg2$V3, alternative="l", paired=F)
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  res <- t.test(seg1$V3, seg2$V3, alternative="l")
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  
  print(">> Greater Seg")
  res <- wilcox.test(seg1$V3, seg2$V3, alternative="g", paired=F)
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  res <- t.test(seg1$V3, seg2$V3, alternative="g")
  print(paste(res$method, " ", res$p.value, " ", res$alternative))
  
  #Creating boxplots of qscores per group
  if (shouldPlot){
    pdf(paste("boxplotAgra", output1, ".pdf"), paper="special")
    #boxplot(data1$V3, main=paste("Boxplot", output1), col=color)
    ggplot(data1, aes(y=agra1$V3, x=c(output1)))+geom_boxplot() 
    + geom_point(position = position_jitter(width = 0.2)) 
    +theme_bw()+ xlab("") + ylab("QScore")
    +ylim(2, 8)+theme(axis.text=element_text(size=14), axis.title=element_text(size=14))
    
    pdf(paste("boxplotAgra", output2, ".pdf"), paper="special")
    #boxplot(data2$V3, main=paste("Boxplot", output2), col=color)
    ggplot(data2, aes(y=agra2$V3, x=c(output2)))+geom_boxplot()
    + geom_point(position = position_jitter(width = 0.2)) 
    +theme_bw()+ xlab("") + ylab("QScore")
    +ylim(2, 8)+theme(axis.text=element_text(size=14), axis.title=element_text(size=14))
    
    pdf(paste("boxplotSeg", output1, ".pdf"), paper="special")
    #boxplot(data1$V3, main=paste("Boxplot", output1), col=color)
    ggplot(data1, aes(y=agra1$V3, x=c(output1)))+geom_boxplot() 
    + geom_point(position = position_jitter(width = 0.2)) 
    +theme_bw()+ xlab("") + ylab("QScore")
    +ylim(2, 8)+theme(axis.text=element_text(size=14), axis.title=element_text(size=14))
    
    pdf(paste("boxplotSeg", output2, ".pdf"), paper="special")
    #boxplot(data2$V3, main=paste("Boxplot", output2), col=color)
    ggplot(data2, aes(y=agra2$V3, x=c(output2)))+geom_boxplot()
    + geom_point(position = position_jitter(width = 0.2)) 
    +theme_bw()+ xlab("") + ylab("QScore")
    +ylim(2, 8)+theme(axis.text=element_text(size=14), axis.title=element_text(size=14))
    
    #Verifying if data is normal
    pdf(paste("norm", output1, "-", output2, ".pdf"), paper="special")
    par(mfrow=c(2,2))
    
    qqnorm(agra1$V3)
    qqline(agra1$V3)
    
    qqnorm(agra2$V3)
    qqline(agra2$V3)
    
    qqnorm(seg1$V3)
    qqline(seg1$V3)
    
    qqnorm(seg2$V3)
    qqline(seg2$V3)
    
    dev.off()
  }
}  

calculateTTests <- function(file1, file2, output1, output2, shouldPlot=FALSE){

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
        #boxplot(data1$V3, main=paste("Boxplot", output1), col=color)
        ggplot(data1, aes(y=data1$V3, x=c(output1)))+geom_boxplot()
        dev.off()
        
        pdf(paste("boxplot", output2, ".pdf"), paper="special")
        #boxplot(data2$V3, main=paste("Boxplot", output2), col=color)
        ggplot(data2, aes(y=data2$V3, x=c(output2)))+geom_boxplot()
        dev.off()
        
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
    calculateTTests(args[1], args[2], args[3], args[4], TRUE)
}
