#!/bin/Rscript
# Combines the set of files with QScores and image characteristics into a single file

#Reading social groups data
solteiro <- read.table("allSolteiroOrdInter.dat")
casado <- read.table("allCasadoOrdInter.dat")
masculino <- read.table("allMasculinoOrdInter.dat")
feminino <- read.table("allFemininoOrdInter.dat")
jovem <- read.table("allJovemOrdInter.dat")
adulto <- read.table("allAdultoOrdInter.dat")
media <- read.table("allMediaOrdInter.dat")
baixa <- read.table("allBaixaOrdInter.dat")
medio <- read.table("allMedioOrdInter.dat")
pos <- read.table("allPosOrdInter.dat")
liberdade <- read.table("allLiberdadeOrdInter.dat")
nliberdade <- read.table("allNotLiberdadeOrdInter.dat")
centro <- read.table("allCentroOrdInter.dat")
ncentro <- read.table("allNotCentroOrdInter.dat")
catole <- read.table("allCatoleOrdInter.dat")
ncatole <- read.table("allNotCatoleOrdInter.dat")

solteiro$grupo <- "Solteiro"
casado$grupo <- "Casado"
masculino$grupo <- "Masculino"
feminino$grupo <- "Feminino"
jovem$grupo <- "Jovem"
adulto$grupo <- "Adulto"
media$grupo <- "Media"
baixa$grupo <- "Baixa"
medio$grupo <- "Medio"
pos$grupo <- "Pos"
nliberdade$grupo <- "NCLiberdade"
liberdade$grupo <- "CLiberdade"
ncatole$grupo <- "NCCatole"
catole$grupo <- "CCatole"
ncentro$grupo <- "NCCentro"
centro$grupo <- "CCentro"

#Reading general data
general <- read.table("all_ordenado.dat")
general$grupo <- "Geral"

#Reading images characteristics
segRGB <- read.table("inputCorrelacaoRegressao100/rgbQScoreSegAll.dat", header=TRUE)

newFrame <- rbind(solteiro, casado, masculino, feminino, jovem, adulto, media, baixa, medio, pos, nliberdade,
      liberdade, ncatole, catole, ncentro, centro, general)

temp <- merge(newFrame, segRGB[,c("foto", "red", "green", "blue", "hor", "vert", "diag")], by.x="V2", by.y="foto")
final <- temp[with(temp, order(V2)),]

temp1 <- lapply(as.character(final$V2), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][1])
neigs1 <- unlist(lapply(temp1, '[[', 1))
final$bairro <- neigs1

write.table(final, file="geral.dat", sep=" ", quote=FALSE, row.names=FALSE)


