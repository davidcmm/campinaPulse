#!/bin/Rscript
# Combines the set of files with QScores and image characteristics into a single file

#Reading social groups data
solteiro <- read.table("allSolteiroOrdInter.dat")
casado <- read.table("allCasadoOrdInter.dat")
masculino <- read.table("allMasculinoOrdInter.dat")
feminino <- read.table("allFemininoOrdInter.dat")
jovem <- read.table("allJovemOrdInter.dat")
adulto <- read.table("allAdultoOrdInter.dat")
#menorMed <- read.table("allMenorMedianOrdInter.dat")
#maiorMed <- read.table("allMaiorMedianOrdInter.dat")
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
#menorMed$grupo <- "MenorMed"
#maiorMed$grupo <- "MaiorMed"
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

#Reading IBGE sectors
ibge <- read.table("setores_censitarios.dat", header=TRUE)

newFrame <- rbind(solteiro, casado, masculino, feminino, jovem, adulto, media, baixa, medio, pos, nliberdade,
      liberdade, ncatole, catole, ncentro, centro, general)
novoV2 <- lapply(as.character(newFrame$V2), function (x) paste(strsplit(x, split="/", fixed=TRUE)[[1]][6], "/", strsplit(x, split="/", fixed=TRUE)[[1]][7], sep=""))
local <- unlist(lapply(novoV2, '[[', 1))
newFrame$V2 <- local

temp <- merge(newFrame, segRGB[,c("foto", "red", "green", "blue", "hor", "vert", "diag")], by.x="V2", by.y="foto")
temp1 <- merge(temp, ibge, by.x = "V2", by.y = "foto")
final <- temp1[with(temp1, order(V2)),]
final2 <- temp[with(temp, order(V2)),]

temp1 <- lapply(as.character(final$V2), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][1])
neigs1 <- unlist(lapply(temp1, '[[', 1))
final$bairro <- neigs1

temp <- lapply(as.character(final2$V2), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][1])
neigs2 <- unlist(lapply(temp, '[[', 1))
final2$bairro <- neigs2

write.table(final, file="geralSetores.dat", sep=" ", quote=FALSE, row.names=FALSE)
write.table(final2, file="geralRank.dat", sep=" ", quote=FALSE, row.names=FALSE)

