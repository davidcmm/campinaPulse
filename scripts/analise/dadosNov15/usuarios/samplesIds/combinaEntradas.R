#!/bin/Rscript
# Combines the set of files with QScores and image characteristics into a single file

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 1){
        iteration <- args[1]

	#Reading social groups data
	#solteiro <- read.table(paste("allSolteiroOrdInter_", iteration,".dat", sep=""))
	#casado <- read.table(paste("allCasadoOrdInter_", iteration,".dat", sep=""))
	#masculino <- read.table(paste("allMasculinoOrdInter_", iteration,".dat", sep=""))
	#feminino <- read.table(paste("allFemininoOrdInter_", iteration,".dat", sep=""))
	#jovem <- read.table(paste("allJovemOrdInter_", iteration,".dat", sep=""))
	#adulto <- read.table(paste("allAdultoOrdInter_", iteration,".dat", sep=""))
	#media <- read.table(paste("allMediaOrdInter_", iteration,".dat", sep=""))
	#baixa <- read.table(paste("allBaixaOrdInter_", iteration,".dat", sep=""))
	centro <- read.table(paste("allCentroOrdInter_", iteration,".dat", sep=""))
	notcentro <- read.table(paste("allNotCentroOrdInter_", iteration,".dat", sep=""))
	catole <- read.table(paste("allCatoleOrdInter_", iteration,".dat", sep=""))
	notcatole <- read.table(paste("allNotCatoleOrdInter_", iteration,".dat", sep=""))
	liberdade <- read.table(paste("allLiberdadeOrdInter_", iteration,".dat", sep=""))
	notliberdade <- read.table(paste("allNotLiberdadeOrdInter_", iteration,".dat", sep=""))

	#solteiro$grupo <- "Solteiro"
	#casado$grupo <- "Casado"
	#masculino$grupo <- "Masculino"
	#feminino$grupo <- "Feminino"
	#jovem$grupo <- "Jovem"
	#adulto$grupo <- "Adulto"
	#media$grupo <- "Media"
	#baixa$grupo <- "Baixa"
	centro$grupo <- "CCentro"
	notcentro$grupo <- "NCCentro"
	catole$grupo <- "CCatole"
	notcatole$grupo <- "NCCatole"
	liberdade$grupo <- "CLiberdade"
	notliberdade$grupo <- "NCLiberdade"

	#Reading IBGE sectors
	ibge <- read.table("../setores_censitarios.dat", header=TRUE)

	newFrame <- rbind(centro, notcentro, catole, notcatole, liberdade, notliberdade)#rbind(solteiro, casado, masculino, feminino, jovem, adulto, media, baixa)
	novoV2 <- lapply(as.character(newFrame$V2), function (x) paste(strsplit(x, split="/", fixed=TRUE)[[1]][6], "/", strsplit(x, split="/", fixed=TRUE)[[1]][7], sep=""))
	local <- unlist(lapply(novoV2, '[[', 1))
	newFrame$V2 <- local

	temp1 <- merge(newFrame, ibge, by.x = "V2", by.y = "foto")
	final <- temp1[with(temp1, order(V2)),]

	temp1 <- lapply(as.character(final$V2), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][1])
	neigs1 <- unlist(lapply(temp1, '[[', 1))
	final$bairro <- neigs1

	#write.table(final, file="geral.dat", sep=" ", quote=FALSE, row.names=FALSE)
	write.table(final, file=paste("geralSetores2AJ_", iteration, ".dat", sep=""), sep=" ", quote=FALSE, row.names=FALSE, col.names=FALSE, append=TRUE)
}
