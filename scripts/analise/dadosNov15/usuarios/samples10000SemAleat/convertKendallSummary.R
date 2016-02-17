#!/bin/Rscript
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


convertSummary <- function(coeffData) {
	print( paste( "index feature real random sd lower higher norm" ), quote=FALSE )

	realValue <- as.double(filter(coeffData, variable=="movCars")$value)
	normValue <- as.double(filter(coeffData, variable=="movCarsN")$value)
	randomValue <- as.double(filter(coeffData, variable=="rmovCars")$value)
	sdValue <- as.double(filter(coeffData, variable=="rsdMovCars")$value)
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "movCars", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2) ), quote=FALSE )

	realValue <- filter(coeffData, variable=="parkCars")$value
	normValue <- as.double(filter(coeffData, variable=="parkCarsN")$value)
	randomValue <- filter(coeffData, variable=="rparkCars")$value
	sdValue <- filter(coeffData, variable=="rsdParkCars")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "parkCars", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="movCicly")$value
	normValue <- as.double(filter(coeffData, variable=="movCiclyN")$value)
	randomValue <- filter(coeffData, variable=="rmovCicly")$value
	sdValue <- filter(coeffData, variable=="rsdMovCicly")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "movCicly", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="buildId")$value
	normValue <- as.double(filter(coeffData, variable=="buildIdN")$value)
	randomValue <- filter(coeffData, variable=="rbuildId")$value
	sdValue <- filter(coeffData, variable=="rsdBuildId")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "buildId", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="buildNRec")$value
	normValue <- as.double(filter(coeffData, variable=="buildNRecN")$value)
	randomValue <- filter(coeffData, variable=="rbuildNRec")$value
	sdValue <- filter(coeffData, variable=="rsdBuildNRec")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "buildNRec", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="tree")$value
	normValue <- as.double(filter(coeffData, variable=="treeN")$value)
	randomValue <- filter(coeffData, variable=="rtree")$value
	sdValue <- filter(coeffData, variable=="rsdTree")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "tree", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="smallPla")$value
	normValue <- as.double(filter(coeffData, variable=="smallPlaN")$value)
	randomValue <- filter(coeffData, variable=="rsmallPla")$value
	sdValue <- filter(coeffData, variable=="rsdSmallPla")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "smallPla", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="diffBuild")$value
	normValue <- as.double(filter(coeffData, variable=="diffBuildN")$value)
	randomValue <- filter(coeffData, variable=="rdiffBuild")$value
	sdValue <- filter(coeffData, variable=="rsdDiffBuild")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "diffBuild", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="streeFur")$value
	normValue <- as.double(filter(coeffData, variable=="streeFurN")$value)
	randomValue <- filter(coeffData, variable=="rstreeFur")$value
	sdValue <- filter(coeffData, variable=="rsdStreeFur")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "streeFur", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="basCol")$value
	normValue <- as.double(filter(coeffData, variable=="basColN")$value)
	randomValue <- filter(coeffData, variable=="rbasCol")$value
	sdValue <- filter(coeffData, variable=="rsdBasCol")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "basCol", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="ligh")$value
	normValue <- as.double(filter(coeffData, variable=="lighN")$value)
	randomValue <- filter(coeffData, variable=="rligh")$value
	sdValue <- filter(coeffData, variable=="rsdLigh")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "ligh", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="accenCol")$value
	normValue <- as.double(filter(coeffData, variable=="accenColN")$value)
	randomValue <- filter(coeffData, variable=="raccenCol")$value
	sdValue <- filter(coeffData, variable=="rsdAccenCol")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "accenCol", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="peop")$value
	normValue <- as.double(filter(coeffData, variable=="peopN")$value)
	randomValue <- filter(coeffData, variable=="rpeop")$value
	sdValue <- filter(coeffData, variable=="rsdPeop")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "peop", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="graff")$value
	normValue <- as.double(filter(coeffData, variable=="graffN")$value)
	randomValue <- filter(coeffData, variable=="rgraff")$value
	sdValue <- filter(coeffData, variable=="rsdGraff")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "graff", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )

	realValue <- filter(coeffData, variable=="buildDiffAges")$value
	normValue <- as.double(filter(coeffData, variable=="buildDiffAgesN")$value)
	randomValue <- filter(coeffData, variable=="rbuildDiffAges")$value
	sdValue <- filter(coeffData, variable=="rsdBuildDiffAges")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "buildDiffAges", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="streetWid")$value
	normValue <- as.double(filter(coeffData, variable=="streetWidN")$value)
	randomValue <- filter(coeffData, variable=="rstreetWid")$value
	sdValue <- filter(coeffData, variable=="rsdStreetWid")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "streetWid", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="sidewalkWid")$value
	normValue <- as.double(filter(coeffData, variable=="sidewalkWidN")$value)
	randomValue <- filter(coeffData, variable=="rsidewalkWid")$value
	sdValue <- filter(coeffData, variable=="rsdSidewalkWid")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "sidewalkWid", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="debris")$value
	normValue <- as.double(filter(coeffData, variable=="debrisN")$value)
	randomValue <- filter(coeffData, variable=="rdebris")$value
	sdValue <- filter(coeffData, variable=="rsdDebris")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "debris", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="pavement")$value
	normValue <- as.double(filter(coeffData, variable=="pavementN")$value)
	randomValue <- filter(coeffData, variable=="rpavement")$value
	sdValue <- filter(coeffData, variable=="rsdPavement")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "pavement", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="landscape")$value
	normValue <- as.double(filter(coeffData, variable=="landscapeN")$value)
	randomValue <- filter(coeffData, variable=="rlandscape")$value
	sdValue <- filter(coeffData, variable=="rsdLandscape")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "landscape", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propStreetWall")$value
	normValue <- as.double(filter(coeffData, variable=="propStreetWallN")$value)
	randomValue <- filter(coeffData, variable=="rpropStreetWall")$value
	sdValue <- filter(coeffData, variable=="rsdPropStreetWall")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "propStreetWall", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propWind")$value
	normValue <- as.double(filter(coeffData, variable=="propWindN")$value)
	randomValue <- filter(coeffData, variable=="rpropWind")$value
	sdValue <- filter(coeffData, variable=="rsdPropWind")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "propWind", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="longSight")$value
	normValue <- as.double(filter(coeffData, variable=="longSightN")$value)
	randomValue <- filter(coeffData, variable=="rlongSight")$value
	sdValue <- filter(coeffData, variable=="rsdLongSight")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "longSight", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propSkyAhead")$value
	normValue <- as.double(filter(coeffData, variable=="propSkyAheadN")$value)
	randomValue <- filter(coeffData, variable=="rpropSkyAhead")$value
	sdValue <- filter(coeffData, variable=="rsdPropSkyAhead")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "propSkyAhead", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propSkyAcross")$value
	normValue <- as.double(filter(coeffData, variable=="propSkyAcrossN")$value)
	randomValue <- filter(coeffData, variable=="rpropSkyAcross")$value
	sdValue <- filter(coeffData, variable=="rsdPropSkyAcross")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "propSkyAcross", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="buildHeight")$value
	normValue <- as.double(filter(coeffData, variable=="buildHeightN")$value)
	randomValue <- filter(coeffData, variable=="rbuildHeight")$value
	sdValue <- filter(coeffData, variable=="rsdBuildHeight")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "buildHeight", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
	realValue <- filter(coeffData, variable=="propActiveUse")$value
	normValue <- as.double(filter(coeffData, variable=="propActiveUseN")$value)
	randomValue <- filter(coeffData, variable=="rpropActiveUse")$value
	sdValue <- filter(coeffData, variable=="rsdPropActiveUse")$value
	lower <- randomValue - icOnValues(randomValue, sdValue, 1000)
	higher <- randomValue + icOnValues(randomValue, sdValue, 1000)
	print( paste ( "propActiveUse", format(realValue, digits=2, nsmall=2), " ", format(randomValue, digits=2, nsmall=2) , " ", format(sdValue, digits=2, nsmall=2) , " ", format(lower, digits=2, nsmall=2) , format(higher, digits=2, nsmall=2), format(normValue, digits=2, nsmall=2)  ), quote=FALSE  )
  
}

#Main
args <- commandArgs(trailingOnly = TRUE)

if (length(args) > 1){
  file1 <- args[1]

  coeffData <- read.table(file1, header=TRUE)   
  convertSummary(coeffData)
}

