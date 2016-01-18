#!/bin/Rscript
library(dplyr)

ic <- function(mean, sd, n) { 
	return (sd/sqrt(n)*qnorm(1-(0.05/2)))#95% confidence interval, significance level of 0.05 (alpha) - sample 100
}

coeffData <- read.table("teste.dat", header=TRUE)

print( paste( "index feature real random sd lower higher" ), quote=FALSE )

realValue <- as.double(filter(coeffData, variable=="movCars")$value)
randomValue <- as.double(filter(coeffData, variable=="rmovCars")$value)
sdValue <- as.double(filter(coeffData, variable=="rsdMovCars")$value)
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "movCars", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE )

realValue <- filter(coeffData, variable=="parkCars")$value
randomValue <- filter(coeffData, variable=="rparkCars")$value
sdValue <- filter(coeffData, variable=="rsdParkCars")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "parkCars", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="movCicly")$value
randomValue <- filter(coeffData, variable=="rmovCicly")$value
sdValue <- filter(coeffData, variable=="rsdMovCicly")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "movCicly", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="buildId")$value
randomValue <- filter(coeffData, variable=="rbuildId")$value
sdValue <- filter(coeffData, variable=="rsdBuildId")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "buildId", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="buildNRec")$value
randomValue <- filter(coeffData, variable=="rbuildNRec")$value
sdValue <- filter(coeffData, variable=="rsdBuildNRec")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "buildNRec", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="tree")$value
randomValue <- filter(coeffData, variable=="rtree")$value
sdValue <- filter(coeffData, variable=="rsdTree")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "tree", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="smallPla")$value
randomValue <- filter(coeffData, variable=="rsmallPla")$value
sdValue <- filter(coeffData, variable=="rsdSmallPla")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "smallPla", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="diffBuild")$value
randomValue <- filter(coeffData, variable=="rdiffBuild")$value
sdValue <- filter(coeffData, variable=="rsdDiffBuild")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "diffBuild", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="streeFur")$value
randomValue <- filter(coeffData, variable=="rstreeFur")$value
sdValue <- filter(coeffData, variable=="rsdStreeFur")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "streeFur", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="basCol")$value
randomValue <- filter(coeffData, variable=="rbasCol")$value
sdValue <- filter(coeffData, variable=="rsdBasCol")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "basCol", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="ligh")$value
randomValue <- filter(coeffData, variable=="rligh")$value
sdValue <- filter(coeffData, variable=="rsdLigh")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "ligh", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="accenCol")$value
randomValue <- filter(coeffData, variable=="raccenCol")$value
sdValue <- filter(coeffData, variable=="rsdAccenCol")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "accenCol", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="peop")$value
randomValue <- filter(coeffData, variable=="rpeop")$value
sdValue <- filter(coeffData, variable=="rsdPeop")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "peop", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="graff")$value
randomValue <- filter(coeffData, variable=="rgraff")$value
sdValue <- filter(coeffData, variable=="rsdGraff")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "graff", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )

realValue <- filter(coeffData, variable=="buildDiffAges")$value
randomValue <- filter(coeffData, variable=="rbuildDiffAges")$value
sdValue <- filter(coeffData, variable=="rsdBuildDiffAges")$value
lower <- randomValue - ic(randomValue, sdValue, 1000)
higher <- randomValue + ic(randomValue, sdValue, 1000)
print( paste ( "buildDiffAges", realValue, " ",  randomValue, " ",  sdValue, " ", lower, higher ), quote=FALSE  )
