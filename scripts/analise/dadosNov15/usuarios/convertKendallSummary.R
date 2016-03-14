#!/bin/Rscript
#Analyses and calculates confidence intervals for features analysis
library(dplyr)

icOnValues <- function(mean, sd, n) { 
	return (sd/sqrt(n)*qnorm(1-(0.05/2)))#95% confidence interval, significance level of 0.05 (alpha) - sample 100
  #value = 1 - (1-0.05)**(1/26) #Sidak
  #return (sd/sqrt(n)*qnorm(1-(value/2)))
	#value = 1 - (1-0.05/26) #Bonferroni
	#return (sd/sqrt(n)*qnorm(1-(value/2)))
}

icOnValuesSidak <- function(mean, sd, n) { 
	#return (sd/sqrt(n)*qnorm(1-(0.05/2)))#95% confidence interval, significance level of 0.05 (alpha) - sample 100
  value = 1 - (1-0.05)**(1/26) #Sidak
  return (sd/sqrt(n)*qnorm(1-(value/2)))
	#value = 1 - (1-0.05/26) #Bonferroni
	#return (sd/sqrt(n)*qnorm(1-(value/2)))
}

icForFeatures <- function(x) { 
	return (sd(x)/sqrt(length(x))*qt(.975,99))#95% confidence interval for a sample of 1000 items
	#print (100 * qnorm(1-(0.05/2)) * sd(x) / (5 * mean(x)))^2
	#return (sd(x)/sqrt(length(x))*qnorm(1-(0.05/2)))#95% confidence interval, significance level of 0.05 (alpha) - sample 100
}

analyseICForFeatures <- function(data){
	#Features simulated values analysis
      icData <- icForFeatures(data$movCars[[1]])
      meanVal <- mean(data$movCars[[1]])
      norm <- meanVal / data$movCarsN[[1]]
      medianVal <- median(data$movCars[[1]])
      norm2 <- medianVal / data$movCarsN[[1]]
#      print(paste("movCars", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE) 
      featureAnalysis <- data.frame(feature="movCars", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2)
      icData <- icForFeatures(data$parkCars[[1]])
      meanVal <- mean(data$parkCars[[1]])
      norm <- meanVal / data$parkCarsN[[1]]
      medianVal <- median(data$parkCars[[1]])
      norm2 <- medianVal / data$parkCarsN[[1]]
      featureAnalysis <- rbind(featureAnalysis, data.frame(feature="parkCars", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$movCicly[[1]])
      meanVal <- mean(data$movCicly[[1]])
      norm <- meanVal / data$movCiclyN[[1]]
      medianVal <- median(data$movCicly[[1]])
      norm2 <- medianVal / data$movCiclyN[[1]]
      #print(paste("movCicly", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="movCicly", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$buildId[[1]])
      meanVal <- mean(data$buildId[[1]])
      norm <- meanVal / data$buildIdN[[1]]
      medianVal <- median(data$buildId[[1]])
      norm2 <- medianVal / data$buildIdN[[1]]
      #print(paste("buildId", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="buildId", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$buildNRec[[1]])
      meanVal <- mean(data$buildNRec[[1]])
      norm <- meanVal / data$buildNRecN[[1]]
      medianVal <- median(data$buildNRec[[1]])
      norm2 <- medianVal / data$buildNRecN[[1]]
      #print(paste("buildNRec", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="buildNRec", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$tree[[1]])
      meanVal <- mean(data$tree[[1]])
      norm <- meanVal / data$treeN[[1]]
      medianVal <- median(data$tree[[1]])
      norm2 <- medianVal / data$treeN[[1]]
      #print(paste("tree", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="tree", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$smallPla[[1]])
      meanVal <- mean(data$smallPla[[1]])
      norm <- meanVal / data$smallPlaN[[1]]
      medianVal <- median(data$smallPla[[1]])
      norm2 <- medianVal / data$smallPlaN[[1]]
      #print(paste("smallPla", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="smallPla", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$diffBuild[[1]])
      meanVal <- mean(data$diffBuild[[1]])
      norm <- meanVal / data$diffBuildN[[1]]
      medianVal <- median(data$diffBuild[[1]])
      norm2 <- medianVal / data$diffBuildN[[1]]
     # print(paste("diffBuild", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="diffBuild", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$streeFur[[1]])
      meanVal <- mean(data$streeFur[[1]])
      norm <- meanVal / data$streeFurN[[1]]
      medianVal <- median(data$streeFur[[1]])
      norm2 <- medianVal / data$streeFurN[[1]]
     # print(paste("streeFur", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="streeFur", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$basCol[[1]])
      meanVal <- mean(data$basCol[[1]])
      norm <- meanVal / data$basColN[[1]]
      medianVal <- median(data$basCol[[1]])
      norm2 <- medianVal / data$basColN[[1]]
     # print(paste("basCol", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="basCol", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$ligh[[1]])
      meanVal <- mean(data$ligh[[1]])
      norm <- meanVal / data$lighN[[1]]
      medianVal <- median(data$ligh[[1]])
      norm2 <- medianVal / data$lighN[[1]]
      #print(paste("ligh", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="ligh", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$accenCol[[1]])
      meanVal <- mean(data$accenCol[[1]])
      norm <- meanVal / data$accenColN[[1]]
      medianVal <- median(data$accenCol[[1]])
      norm2 <- medianVal / data$accenColN[[1]]
      #print(paste("accenCol", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="accenCol", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$peop[[1]])
      meanVal <- mean(data$peop[[1]])
      norm <- meanVal / data$peopN[[1]]
      medianVal <- median(data$peop[[1]])
      norm2 <- medianVal / data$peopN[[1]]
     # print(paste("peop", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="peop", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$graff[[1]])
      meanVal <- mean(data$graff[[1]])
      norm <- meanVal / data$graffN[[1]]
      medianVal <- median(data$graff[[1]])
      norm2 <- medianVal / data$graffN[[1]]
    #  print(paste("graff", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="graff", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$buildDiffAges[[1]])
      meanVal <- mean(data$buildDiffAges[[1]])
      norm <- meanVal / data$buildDiffAgesN[[1]]
      medianVal <- median(data$buildDiffAges[[1]])
      norm2 <- medianVal / data$buildDiffAgesN[[1]]
#      print(paste("buildDiffAges", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="buildDiffAges", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$streetWid[[1]])
      meanVal <- mean(data$streetWid[[1]])
      norm <- meanVal / data$streetWidN[[1]]
      medianVal <- median(data$streetWid[[1]])
      norm2 <- medianVal / data$streetWidN[[1]]
      #print(paste("streetWid", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="streetWid", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$sidewalkWid[[1]])
      meanVal <- mean(data$sidewalkWid[[1]])
      norm <- meanVal / data$sidewalkWidN[[1]]
      medianVal <- median(data$sidewalkWid[[1]])
      norm2 <- medianVal / data$sidewalkWidN[[1]]
      #print(paste("sidewalkWid", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="sidewalkWid", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$buildHeight[[1]])
      meanVal <- mean(data$buildHeight[[1]])
      norm <- meanVal / data$buildHeightN[[1]]
      medianVal <- median(data$buildHeight[[1]])
      norm2 <- medianVal / data$buildHeightN[[1]]
#      print(paste("buildHeight", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="buildHeight", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$longSight[[1]])
      meanVal <- mean(data$longSight[[1]])
      norm <- meanVal / data$longSightN[[1]]
      medianVal <- median(data$longSight[[1]])
      norm2 <- medianVal / data$longSightN[[1]]
      #print(paste("longSight", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="longSight", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$debris[[1]])
      meanVal <- mean(data$debris[[1]])
      norm <- meanVal / data$debrisN[[1]]
      medianVal <- median(data$debris[[1]])
      norm2 <- medianVal / data$debrisN[[1]]
      #print(paste("debris", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="debris", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$pavement[[1]])
      meanVal <- mean(data$pavement[[1]])
      norm <- meanVal / data$pavementN[[1]]
      medianVal <- median(data$pavement[[1]])
      norm2 <- medianVal / data$pavementN[[1]]
#      print(paste("pavement", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="pavement", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$landscape[[1]])
      meanVal <- mean(data$landscape[[1]])
      norm <- meanVal / data$landscapeN[[1]]
      medianVal <- median(data$landscape[[1]])
      norm2 <- medianVal / data$landscapeN[[1]]
#      print(paste("landscape", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="landscape", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$propStreetWall[[1]])
      meanVal <- mean(data$propStreetWall[[1]])
      norm <- meanVal / data$propStreetWallN[[1]]
      medianVal <- median(data$propStreetWall[[1]])
      norm2 <- medianVal / data$propStreetWallN[[1]]
#      print(paste("propStreetWall", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="propStreetWall", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$propWind[[1]])
      meanVal <- mean(data$propWind[[1]])
      norm <- meanVal / data$propWindN[[1]]
      medianVal <- median(data$propWind[[1]])
      norm2 <- medianVal / data$propWindN[[1]]
      #print(paste("propWind", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="propWind", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$propSkyAhead[[1]])
      meanVal <- mean(data$propSkyAhead[[1]])
      norm <- meanVal / data$propSkyAheadN[[1]]
      medianVal <- median(data$propSkyAhead[[1]])
      norm2 <- medianVal / data$propSkyAheadN[[1]]
      #print(paste("propSkyAhead", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="propSkyAhead", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$propSkyAcross[[1]])
      meanVal <- mean(data$propSkyAcross[[1]])
      norm <- meanVal / data$propSkyAcrossN[[1]]
      medianVal <- median(data$propSkyAcross[[1]])
      norm2 <- medianVal / data$propSkyAcrossN[[1]]
     # print(paste("propSkyAcross", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)      
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="propSkyAcross", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))
      icData <- icForFeatures(data$propActiveUse[[1]])
      meanVal <- mean(data$propActiveUse[[1]])
      norm <- meanVal / data$propActiveUseN[[1]]
      medianVal <- median(data$propActiveUse[[1]])
      norm2 <- medianVal / data$propActiveUseN[[1]]
      #print(paste("propActiveUse", meanVal, meanVal - icData, meanVal + icData, norm, norm2), quote=FALSE)    
	featureAnalysis <- rbind(featureAnalysis, data.frame(feature="propActiveUse", realS=meanVal, lowerS=meanVal-icData, higherS=meanVal+icData, normS=norm, normS2=norm2))

	print(arrange(featureAnalysis, desc(abs(normS))))

	#Urban Qualities simulated values analysis
      qualitySum <- mean(data$movCars[[1]]) + mean(data$movCicly[[1]]) + mean(data$parkCars[[1]]) + mean(data$peop[[1]]) + mean(data$diffBuild[[1]]) + mean(data$buildNRec[[1]]) + mean(data$buildDiffAges[[1]]) + mean(data$ligh[[1]]) + mean(data$graff[[1]]) + mean(data$basCol[[1]]) + mean(data$accenCol[[1]]) + mean(data$streeFur[[1]]) + mean(data$tree[[1]]) + mean(data$smallPla[[1]])
      qualities <- data.frame(feature="complexity", value=qualitySum, norm=qualitySum / (data$movCarsN[[1]] + data$movCiclyN[[1]] + data$parkCarsN[[1]] + data$peopN[[1]] + data$diffBuildN[[1]] + data$buildNRecN[[1]] + data$buildDiffAgesN[[1]] + data$lighN[[1]] + data$graffN[[1]] + data$basColN[[1]] + data$accenColN[[1]] + data$streeFurN[[1]] + data$treeN[[1]] + data$smallPlaN[[1]]) )

      qualitySum <- mean(data$movCars[[1]]) + mean(data$movCicly[[1]]) + mean(data$peop[[1]]) + mean(data$ligh[[1]]) + mean(data$streeFur[[1]]) + mean(data$tree[[1]]) + mean(data$smallPla[[1]]) + mean(data$longSight[[1]]) + mean(data$streetWid[[1]]) #+ mean(data$buildHeight[[1]])
	qualities <- rbind(qualities, data.frame(feature="humanScale", value=qualitySum, norm=qualitySum / (data$movCarsN[[1]] + data$movCiclyN[[1]] + data$peopN[[1]] + data$lighN[[1]] + data$streeFurN[[1]] + data$treeN[[1]] + data$smallPlaN[[1]] + data$longSightN[[1]] + data$streetWidN[[1]])))

      qualitySum <- mean(data$peop[[1]]) + mean(data$buildId[[1]]) + mean(data$buildNRec[[1]]) + mean(data$basCol[[1]])
	qualities <- rbind(qualities, data.frame(feature="imageability", value=qualitySum, norm=qualitySum / (data$peopN[[1]] + data$buildIdN[[1]] + data$buildNRecN[[1]] + data$basColN[[1]])))

      qualitySum <- mean(data$ligh[[1]]) + mean(data$tree[[1]]) + mean(data$longSight[[1]]) + mean(data$streetWid[[1]])#+ mean(data$buildHeight[[1]])
	qualities <- rbind(qualities, data.frame(feature="enclosure", value=qualitySum, norm=qualitySum / (data$lighN[[1]] + data$treeN[[1]] + data$longSightN[[1]] + data$streetWidN[[1]])))

      qualitySum <- mean(data$peop[[1]]) + mean(data$buildDiffAges[[1]]) + mean(data$ligh[[1]]) + mean(data$basCol[[1]]) + mean(data$accenCol[[1]])+ mean(data$streeFur[[1]])#+ mean(data$buildHeight[[1]])
	qualities <- rbind(qualities, data.frame(feature="coherence", value=qualitySum, norm=qualitySum / (data$peopN[[1]] + data$buildDiffAgesN[[1]] + data$lighN[[1]] + data$basColN[[1]] + data$accenColN[[1]]+ data$streeFurN[[1]])))

      qualitySum <- mean(data$movCars[[1]]) + mean(data$longSight[[1]]) + mean(data$streetWid[[1]])
	qualities <- rbind(qualities, data.frame(feature="linkage", value=qualitySum, norm=qualitySum / (data$movCarsN[[1]] + data$longSightN[[1]] + data$streetWidN[[1]])))

      qualitySum <- mean(data$buildId[[1]]) + mean(data$longSight[[1]])
	qualities <- rbind(qualities, data.frame(feature="legibility", value=qualitySum, norm=qualitySum / (data$buildIdN[[1]] + data$longSightN[[1]])))

      qualitySum <- mean(data$sidewalkWid[[1]])#+ mean(data$buildHeight[[1]])
	qualities <- rbind(qualities, data.frame(feature="transparency", value=qualitySum, norm=qualitySum / (data$sidewalkWidN[[1]])))

      qualitySum <- mean(data$graff[[1]]) + mean(data$streeFur[[1]]) + mean(data$debris[[1]]) + mean(data$pavement[[1]]) + mean(data$landscape[[1]])#+ mean(data$buildHeight[[1]])
	qualities <- rbind(qualities, data.frame(feature="tidiness", value=qualitySum, norm=qualitySum / (data$graffN[[1]] + data$streeFurN[[1]] + data$debrisN[[1]] + data$pavementN[[1]] + data$landscapeN[[1]])))

     print(arrange(qualities, desc(abs(value))))

    #Printing qualities and their respective features
    print(filter(qualities, feature=="complexity"))
    print(filter(featureAnalysis, feature=="movCars" | feature == "movCicly" | feature == "parkCars" | feature == "peop" | feature == "diffBuild" | feature == "buildNRec" | feature == "buildDiffAges" | feature == "ligh" | feature == "graff" | feature == "basCol" | feature == "accenCol" | feature == "streeFur" | feature == "tree" | feature == "smallPla"))

    print(filter(qualities, feature=="humanScale"))
    print(filter(featureAnalysis, feature=="movCars" | feature == "movCicly" | feature == "peop" | feature == "ligh" | feature == "streeFur" | feature == "tree" | feature == "smallPla" | feature == "longSight" | feature == "streetWid" | feature == "buildHeight"))

    print(filter(qualities, feature=="imageability"))
    print(filter(featureAnalysis, feature == "peop" | feature == "buildId" | feature == "buildNRec" | feature == "basCol" ))

    print(filter(qualities, feature=="enclosure"))
    print(filter(featureAnalysis, feature=="ligh" | feature == "tree" | feature == "longSight" | feature == "streetWid" | feature == "buildHeight"))

    print(filter(qualities, feature=="coherence"))
    print(filter(featureAnalysis, feature == "peop" | feature == "buildDiffAges" | feature == "ligh" | feature == "basCol" | feature == "accenCol" | feature == "streeFur" | feature == "buildHeight"))

    print(filter(qualities, feature=="linkage"))
    print(filter(featureAnalysis, feature == "movCars" | feature == "longSight" | feature == "streetWid" ))

    print(filter(qualities, feature=="legibility"))
    print(filter(featureAnalysis, feature == "buildId" | feature == "longSight"))

    print(filter(qualities, feature=="transparency"))
    print(filter(featureAnalysis, feature == "sidewalkWid" | feature == "buildHeight"))

    print(filter(qualities, feature=="tidiness"))
    print(filter(featureAnalysis, feature == "graff" | feature == "streeFur" | feature == "debris" | feature == "pavement" | feature == "landscape"))
}


convertSummary <- function(coeffData, size=1000) {
	print( paste( "index feature real random sd lower higher lowerSid higherSid norm" ), quote=FALSE )

	realValue <- as.double(filter(coeffData, variable=="movCars")$value)
	normValue <- as.double(filter(coeffData, variable=="movCarsN")$value)
	randomValue <- as.double(filter(coeffData, variable=="rmovCars")$value)
	sdValue <- as.double(filter(coeffData, variable=="rsdMovCars")$value)
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "movCars", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2) ), quote=FALSE )

	realValue <- filter(coeffData, variable=="parkCars")$value
	normValue <- as.double(filter(coeffData, variable=="parkCarsN")$value)
	randomValue <- filter(coeffData, variable=="rparkCars")$value
	sdValue <- filter(coeffData, variable=="rsdParkCars")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "parkCars", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="movCicly")$value
	normValue <- as.double(filter(coeffData, variable=="movCiclyN")$value)
	randomValue <- filter(coeffData, variable=="rmovCicly")$value
	sdValue <- filter(coeffData, variable=="rsdMovCicly")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "movCicly", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="buildId")$value
	normValue <- as.double(filter(coeffData, variable=="buildIdN")$value)
	randomValue <- filter(coeffData, variable=="rbuildId")$value
	sdValue <- filter(coeffData, variable=="rsdBuildId")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "buildId", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="buildNRec")$value
	normValue <- as.double(filter(coeffData, variable=="buildNRecN")$value)
	randomValue <- filter(coeffData, variable=="rbuildNRec")$value
	sdValue <- filter(coeffData, variable=="rsdBuildNRec")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "buildNRec", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="tree")$value
	normValue <- as.double(filter(coeffData, variable=="treeN")$value)
	randomValue <- filter(coeffData, variable=="rtree")$value
	sdValue <- filter(coeffData, variable=="rsdTree")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "tree", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="smallPla")$value
	normValue <- as.double(filter(coeffData, variable=="smallPlaN")$value)
	randomValue <- filter(coeffData, variable=="rsmallPla")$value
	sdValue <- filter(coeffData, variable=="rsdSmallPla")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "smallPla", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="diffBuild")$value
	normValue <- as.double(filter(coeffData, variable=="diffBuildN")$value)
	randomValue <- filter(coeffData, variable=="rdiffBuild")$value
	sdValue <- filter(coeffData, variable=="rsdDiffBuild")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "diffBuild", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="streeFur")$value
	normValue <- as.double(filter(coeffData, variable=="streeFurN")$value)
	randomValue <- filter(coeffData, variable=="rstreeFur")$value
	sdValue <- filter(coeffData, variable=="rsdStreeFur")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "streeFur", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="basCol")$value
	normValue <- as.double(filter(coeffData, variable=="basColN")$value)
	randomValue <- filter(coeffData, variable=="rbasCol")$value
	sdValue <- filter(coeffData, variable=="rsdBasCol")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "basCol", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="ligh")$value
	normValue <- as.double(filter(coeffData, variable=="lighN")$value)
	randomValue <- filter(coeffData, variable=="rligh")$value
	sdValue <- filter(coeffData, variable=="rsdLigh")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "ligh", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="accenCol")$value
	normValue <- as.double(filter(coeffData, variable=="accenColN")$value)
	randomValue <- filter(coeffData, variable=="raccenCol")$value
	sdValue <- filter(coeffData, variable=="rsdAccenCol")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "accenCol", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="peop")$value
	normValue <- as.double(filter(coeffData, variable=="peopN")$value)
	randomValue <- filter(coeffData, variable=="rpeop")$value
	sdValue <- filter(coeffData, variable=="rsdPeop")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "peop", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="graff")$value
	normValue <- as.double(filter(coeffData, variable=="graffN")$value)
	randomValue <- filter(coeffData, variable=="rgraff")$value
	sdValue <- filter(coeffData, variable=="rsdGraff")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "graff", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="buildDiffAges")$value
	normValue <- as.double(filter(coeffData, variable=="buildDiffAgesN")$value)
	randomValue <- filter(coeffData, variable=="rbuildDiffAges")$value
	sdValue <- filter(coeffData, variable=="rsdBuildDiffAges")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "buildDiffAges", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="streetWid")$value
	normValue <- as.double(filter(coeffData, variable=="streetWidN")$value)
	randomValue <- filter(coeffData, variable=="rstreetWid")$value
	sdValue <- filter(coeffData, variable=="rsdStreetWid")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "streetWid", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="sidewalkWid")$value
	normValue <- as.double(filter(coeffData, variable=="sidewalkWidN")$value)
	randomValue <- filter(coeffData, variable=="rsidewalkWid")$value
	sdValue <- filter(coeffData, variable=="rsdSidewalkWid")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "sidewalkWid", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="debris")$value
	normValue <- as.double(filter(coeffData, variable=="debrisN")$value)
	randomValue <- filter(coeffData, variable=="rdebris")$value
	sdValue <- filter(coeffData, variable=="rsdDebris")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "debris", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="pavement")$value
	normValue <- as.double(filter(coeffData, variable=="pavementN")$value)
	randomValue <- filter(coeffData, variable=="rpavement")$value
	sdValue <- filter(coeffData, variable=="rsdPavement")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "pavement", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="landscape")$value
	normValue <- as.double(filter(coeffData, variable=="landscapeN")$value)
	randomValue <- filter(coeffData, variable=="rlandscape")$value
	sdValue <- filter(coeffData, variable=="rsdLandscape")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "landscape", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propStreetWall")$value
	normValue <- as.double(filter(coeffData, variable=="propStreetWallN")$value)
	randomValue <- filter(coeffData, variable=="rpropStreetWall")$value
	sdValue <- filter(coeffData, variable=="rsdPropStreetWall")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "propStreetWall", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propWind")$value
	normValue <- as.double(filter(coeffData, variable=="propWindN")$value)
	randomValue <- filter(coeffData, variable=="rpropWind")$value
	sdValue <- filter(coeffData, variable=="rsdPropWind")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "propWind", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="longSight")$value
	normValue <- as.double(filter(coeffData, variable=="longSightN")$value)
	randomValue <- filter(coeffData, variable=="rlongSight")$value
	sdValue <- filter(coeffData, variable=="rsdLongSight")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "longSight", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propSkyAhead")$value
	normValue <- as.double(filter(coeffData, variable=="propSkyAheadN")$value)
	randomValue <- filter(coeffData, variable=="rpropSkyAhead")$value
	sdValue <- filter(coeffData, variable=="rsdPropSkyAhead")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "propSkyAhead", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propSkyAcross")$value
	normValue <- as.double(filter(coeffData, variable=="propSkyAcrossN")$value)
	randomValue <- filter(coeffData, variable=="rpropSkyAcross")$value
	sdValue <- filter(coeffData, variable=="rsdPropSkyAcross")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "propSkyAcross", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="buildHeight")$value
	normValue <- as.double(filter(coeffData, variable=="buildHeightN")$value)
	randomValue <- filter(coeffData, variable=="rbuildHeight")$value
	sdValue <- filter(coeffData, variable=="rsdBuildHeight")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "buildHeight", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propActiveUse")$value
	normValue <- as.double(filter(coeffData, variable=="propActiveUseN")$value)
	randomValue <- filter(coeffData, variable=="rpropActiveUse")$value
	sdValue <- filter(coeffData, variable=="rsdPropActiveUse")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, size)
	higher <- randomValue + icOnValues(randomValue, sdValue, size)
	lowerSid <- randomValue - icOnValuesSidak(randomValue, sdValue, size)
	higherSid <- randomValue + icOnValuesSidak(randomValue, sdValue, size)
	print( paste ( "propActiveUse", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2), " ", format(higher, digits=2, nsmall=2), " ", format(lowerSid, digits=2, nsmall=2), " ", format(higherSid, digits=2, nsmall=2), " ", format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
}

#Main
args <- commandArgs(trailingOnly = TRUE)

if (length(args) > 1){
  file1 <- args[1]

  coeffData <- read.table(file1, header=TRUE)   
  convertSummary(coeffData)
}

