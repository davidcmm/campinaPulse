#!/bin/Rscript
# Calculates the confidence interval of qscores for each city point for each of the groups received

library(ggplot2)
library(rmarkdown)
library(knitr)

#Calculates the variance that should be added or removed from the mean
ic <- function(x) { 
	#return (sd(x)/sqrt(length(x))*qt(.975,99))#95% confidence interval for a sample of 1000 items
	#print (100 * qnorm(1-(0.05/2)) * sd(x) / (5 * mean(x)))^2
	return (sd(x)/sqrt(length(x))*qnorm(1-(0.05/2)))#95% confidence interval, significance level of 0.05 (alpha) - sample 100
}

icForFeatures <- function(x) { 
	return (sd(x)/sqrt(length(x))*qt(.975,99))#95% confidence interval for a sample of 1000 items
	#print (100 * qnorm(1-(0.05/2)) * sd(x) / (5 * mean(x)))^2
	#return (sd(x)/sqrt(length(x))*qnorm(1-(0.05/2)))#95% confidence interval, significance level of 0.05 (alpha) - sample 100
}

# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)

  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)

  numPlots = length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                    ncol = cols, nrow = ceiling(numPlots/cols))
  }

 if (numPlots==1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

analyseICForFeatures <- function(data){
      icData <- icForFeatures(data$movCars[[1]])
      meanVal <- mean(data$movCars[[1]])
      norm <- meanVal / data$movCarsN[[1]]
      medianVal <- median(data$movCars[[1]])
      norm2 <- medianVal / data$movCarsN[[1]]
      print(paste("movCars", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE) 
      icData <- icForFeatures(data$parkCars[[1]])
      meanVal <- mean(data$parkCars[[1]])
      norm <- meanVal / data$parkCarsN[[1]]
      medianVal <- median(data$parkCars[[1]])
      norm2 <- medianVal / data$parkCarsN[[1]]
      print(paste("parkCars", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$movCicly[[1]])
      meanVal <- mean(data$movCicly[[1]])
      norm <- meanVal / data$movCiclyN[[1]]
      medianVal <- median(data$movCicly[[1]])
      norm2 <- medianVal / data$movCiclyN[[1]]
      print(paste("movCicly", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$buildId[[1]])
      meanVal <- mean(data$buildId[[1]])
      norm <- meanVal / data$buildIdN[[1]]
      medianVal <- median(data$buildId[[1]])
      norm2 <- medianVal / data$buildIdN[[1]]
      print(paste("buildId", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$buildNRec[[1]])
      meanVal <- mean(data$buildNRec[[1]])
      norm <- meanVal / data$buildNRecN[[1]]
      medianVal <- median(data$buildNRec[[1]])
      norm2 <- medianVal / data$buildNRecN[[1]]
      print(paste("buildNRec", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$tree[[1]])
      meanVal <- mean(data$tree[[1]])
      norm <- meanVal / data$treeN[[1]]
      medianVal <- median(data$tree[[1]])
      norm2 <- medianVal / data$treeN[[1]]
      print(paste("tree", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$smallPla[[1]])
      meanVal <- mean(data$smallPla[[1]])
      norm <- meanVal / data$smallPlaN[[1]]
      medianVal <- median(data$smallPla[[1]])
      norm2 <- medianVal / data$smallPlaN[[1]]
      print(paste("smallPla", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$diffBuild[[1]])
      meanVal <- mean(data$diffBuild[[1]])
      norm <- meanVal / data$diffBuildN[[1]]
      medianVal <- median(data$diffBuild[[1]])
      norm2 <- medianVal / data$diffBuildN[[1]]
      print(paste("diffBuild", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$streeFur[[1]])
      meanVal <- mean(data$streeFur[[1]])
      norm <- meanVal / data$streeFurN[[1]]
      medianVal <- median(data$streeFur[[1]])
      norm2 <- medianVal / data$streeFurN[[1]]
      print(paste("streeFur", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$basCol[[1]])
      meanVal <- mean(data$basCol[[1]])
      norm <- meanVal / data$basColN[[1]]
      medianVal <- median(data$basCol[[1]])
      norm2 <- medianVal / data$basColN[[1]]
      print(paste("basCol", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$ligh[[1]])
      meanVal <- mean(data$ligh[[1]])
      norm <- meanVal / data$lighN[[1]]
      medianVal <- median(data$ligh[[1]])
      norm2 <- medianVal / data$lighN[[1]]
      print(paste("ligh", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=
FALSE)
      icData <- icForFeatures(data$accenCol[[1]])
      meanVal <- mean(data$accenCol[[1]])
      norm <- meanVal / data$accenColN[[1]]
      medianVal <- median(data$accenCol[[1]])
      norm2 <- medianVal / data$accenColN[[1]]
      print(paste("accenCol", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$peop[[1]])
      meanVal <- mean(data$peop[[1]])
      norm <- meanVal / data$peopN[[1]]
      medianVal <- median(data$peop[[1]])
      norm2 <- medianVal / data$peopN[[1]]
      print(paste("peop", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$graff[[1]])
      meanVal <- mean(data$graff[[1]])
      norm <- meanVal / data$graffN[[1]]
      medianVal <- median(data$graff[[1]])
      norm2 <- medianVal / data$graffN[[1]]
      print(paste("graff", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$buildDiffAges[[1]])
      meanVal <- mean(data$buildDiffAges[[1]])
      norm <- meanVal / data$buildDiffAgesN[[1]]
      medianVal <- median(data$buildDiffAges[[1]])
      norm2 <- medianVal / data$buildDiffAgesN[[1]]
      print(paste("buildDiffAges", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$streetWid[[1]])
      meanVal <- mean(data$streetWid[[1]])
      norm <- meanVal / data$streetWidN[[1]]
      medianVal <- median(data$streetWid[[1]])
      norm2 <- medianVal / data$streetWidN[[1]]
      print(paste("streetWid", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$sidewalkWid[[1]])
      meanVal <- mean(data$sidewalkWid[[1]])
      norm <- meanVal / data$sidewalkWidN[[1]]
      medianVal <- median(data$sidewalkWid[[1]])
      norm2 <- medianVal / data$sidewalkWidN[[1]]
      print(paste("sidewalkWid", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$buildHeight[[1]])
      meanVal <- mean(data$buildHeight[[1]])
      norm <- meanVal / data$buildHeightN[[1]]
      medianVal <- median(data$buildHeight[[1]])
      norm2 <- medianVal / data$buildHeightN[[1]]
      print(paste("buildHeight", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$longSight[[1]])
      meanVal <- mean(data$longSight[[1]])
      norm <- meanVal / data$longSightN[[1]]
      medianVal <- median(data$longSight[[1]])
      norm2 <- medianVal / data$longSightN[[1]]
      print(paste("longSight", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$debris[[1]])
      meanVal <- mean(data$debris[[1]])
      norm <- meanVal / data$debrisN[[1]]
      medianVal <- median(data$debris[[1]])
      norm2 <- medianVal / data$debrisN[[1]]
      print(paste("debris", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$pavement[[1]])
      meanVal <- mean(data$pavement[[1]])
      norm <- meanVal / data$pavementN[[1]]
      medianVal <- median(data$pavement[[1]])
      norm2 <- medianVal / data$pavementN[[1]]
      print(paste("pavement", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$landscape[[1]])
      meanVal <- mean(data$landscape[[1]])
      norm <- meanVal / data$landscapeN[[1]]
      medianVal <- median(data$landscape[[1]])
      norm2 <- medianVal / data$landscapeN[[1]]
      print(paste("landscape", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
      icData <- icForFeatures(data$propStreetWall[[1]])
      meanVal <- mean(data$propStreetWall[[1]])
      norm <- meanVal / data$propStreetWallN[[1]]
      medianVal <- median(data$propStreetWall[[1]])
      norm2 <- medianVal / data$propStreetWallN[[1]]
      print(paste("propStreetWall", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
      icData <- icForFeatures(data$propWind[[1]])
      meanVal <- mean(data$propWind[[1]])
      norm <- meanVal / data$propWindN[[1]]
      medianVal <- median(data$propWind[[1]])
      norm2 <- medianVal / data$propWindN[[1]]
      print(paste("propWind", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
      icData <- icForFeatures(data$propSkyAhead[[1]])
      meanVal <- mean(data$propSkyAhead[[1]])
      norm <- meanVal / data$propSkyAheadN[[1]]
      medianVal <- median(data$propSkyAhead[[1]])
      norm2 <- medianVal / data$propSkyAheadN[[1]]
      print(paste("propSkyAhead", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
      icData <- icForFeatures(data$propSkyAcross[[1]])
      meanVal <- mean(data$propSkyAcross[[1]])
      norm <- meanVal / data$propSkyAcrossN[[1]]
      medianVal <- median(data$propSkyAcross[[1]])
      norm2 <- medianVal / data$propSkyAcrossN[[1]]
      print(paste("propSkyAcross", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
      icData <- icForFeatures(data$propActiveUse[[1]])
      meanVal <- mean(data$propActiveUse[[1]])
      norm <- meanVal / data$propActiveUseN[[1]]
      medianVal <- median(data$propActiveUse[[1]])
      norm2 <- medianVal / data$propActiveUseN[[1]]
      print(paste("propActiveUse", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
}

#Selecting only qscores
analyseIC <- function(file1, file2, type1, type2, shouldPlot=FALSE){
  data1 <- read.table(file1)
  data2 <- read.table(file2)
  
  newdata1 <- data1 [ c(4:103) ]
  newdata2 <- data2 [ c(4:103) ]
  
  icData1 <- apply(newdata1, 1, ic)
  icData2 <- apply(newdata2, 1, ic)
  
  temp1 <- lapply(as.character(data1$V2), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][1])
  temp2 <- lapply(as.character(data2$V2), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][1])
  
  neigs1 <- unlist(lapply(temp1, '[[', 1))
  neigs2 <- unlist(lapply(temp2, '[[', 1))
  
  #Saving data
  newframe1 <- data.frame(ques=data1$V1, photo=data1$V2, mean=data1$V3, dist=icData1, inf=data1$V3-icData1, sup=data1$V3+icData1, neig=neigs1)
  newframe1 <- newframe1[with(newframe1, order(photo)), ]
  newframe1$type <- type1
  write.table(newframe1, "teste1.txt", sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)
  
  newframe2 <- data.frame(ques=data2$V1, photo=data2$V2, mean=data2$V3, dist=icData2, inf=data2$V3-icData1, sup=data2$V3+icData1, neig=neigs2)
  newframe2 <- newframe2[with(newframe2, order(photo)), ]
  newframe2$type <- type2
  write.table(newframe2, "teste2.txt", sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)
  
  total <- rbind(newframe1, newframe2)
  size <- nrow(total)
  total$photo <- 1:size
  total$photo [ c((size/2+1):size) ] <- (1:(size/2))
  
  centro <<- total[total$neig == "centro",]
  liberdade <<- total[total$neig == "liberdade",]
  catole <<- total[total$neig == "catole",]
 
  #if(shouldPlot){        
  #    
  #  pdf(file=paste("IC-Centro-", type1, "-", type2, ".pdf"), paper="special")
  #  ggplot(centro, aes(x=photo, y=mean, colour=type)) + geom_point(shape=1, size=2) + geom_errorbar(aes(ymin=inf, ymax=sup)) + facet_grid(. ~ques, shrink=TRUE) + xlab("Local") + ylab("QScore") + ggtitle("Centro")
  #  
  #  pdf(file=paste("IC-Liberdade-", type1, "-", type2, ".pdf"), paper="special")
  #  ggplot(liberdade, aes(x=photo, y=mean, colour=type)) + geom_point(shape=1, size=2) + geom_errorbar(aes(ymin=inf, ymax=sup)) + facet_grid(. ~ques, shrink=TRUE) + xlab("Local") + ylab("QScore") + ggtitle("Liberdade")
  #  
  #  pdf(file=paste("IC-Catole-", type1, "-", type2, ".pdf"), paper="special")
  #  ggplot(catole, aes(x=photo, y=mean, colour=type)) + geom_point(shape=1, size=2) + geom_errorbar(aes(ymin=inf, ymax=sup)) + facet_grid(. ~ques, shrink=TRUE) + xlab("Local") + ylab("QScore") + ggtitle("Catolé")
    
  #  dev.off()
  # }
 
}
#multiplot(g1, g2, g3, cols=1)

# solt$type <- "solteiro"
# casa$type <- "casado"
# novo <- rbind(solt, casa)
# novo$photo <- 1:156 + novo$photo [c(79:156) ] <- 1:78

args <- commandArgs(trailingOnly = TRUE)

if (length(args) > 1){
  file1 <- args[1]
  file2 <- args[2]
  type1 <- args[3]
  type2 <- args[4]
  
  analyseIC(file1, file2, type1, type2, TRUE)
}


