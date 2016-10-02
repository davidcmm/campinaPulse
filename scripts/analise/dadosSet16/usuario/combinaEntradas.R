#!/bin/Rscript
# Combines the set of files with QScores and image characteristics into a single file

#Reading social groups data
solteiro <- read.table("all100/allSolteiroOrdInter.dat")
casado <- read.table("all100/allCasadoOrdInter.dat")
masculino <- read.table("all100/allMasculinoOrdInter.dat")
feminino <- read.table("all100/allFemininoOrdInter.dat")
jovem <- read.table("all100/allJovemOrdInter.dat")
adulto <- read.table("all100/allAdultoOrdInter.dat")
#jovem <- read.table("allJovem24OrdInter.dat")
#adulto <- read.table("allAdulto25OrdInter.dat")
#menorMed <- read.table("allMenorMedianOrdInter.dat")
#maiorMed <- read.table("allMaiorMedianOrdInter.dat")
media <- read.table("all100/allMediaOrdInter.dat")
baixa <- read.table("all100/allBaixaOrdInter.dat")
medio <- read.table("all100/allMedioOrdInter.dat")
pos <- read.table("all100/allPosOrdInter.dat")
liberdade <- read.table("all100/allLiberdadeOrdInter.dat")
nliberdade <- read.table("all100/allNotLiberdadeOrdInter.dat")
centro <- read.table("all100/allCentroOrdInter.dat")
ncentro <- read.table("all100/allNotCentroOrdInter.dat")
catole <- read.table("all100/allCatoleOrdInter.dat")
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
general <- read.table("all100/all_ordenado.dat")
general$grupo <- "Geral"

#Reading images characteristics
segRGB <- read.table("inputCorrelacaoRegressao100/rgbQScoreSegAll.dat", header=TRUE)

#Reading IBGE sectors
ibge <- read.table("setores_censitarios.dat", header=TRUE)

newFrame <- rbind(solteiro, casado, masculino, feminino, jovem, adulto, media, baixa, general)
                  #, medio, pos, nliberdade,
                  #liberdade, ncatole, catole, ncentro, centro, general)
#newFrame2 <- rbind(catole, centro, ncentro, ncatole, liberdade, nliberdade, general)
novoV2 <- lapply(as.character(newFrame$V2), function (x) paste(strsplit(x, split="/", fixed=TRUE)[[1]][6], "/", strsplit(x, split="/", fixed=TRUE)[[1]][7], sep=""))
local <- unlist(lapply(novoV2, '[[', 1))
newFrame$V2 <- local
newFrame <- rbind(solteiro, casado, masculino, feminino, jovem, adulto, media, baixa, medio, pos, newFrame2)

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

#write.table(final, file="geral.dat", sep=" ", quote=FALSE, row.names=FALSE)
write.table(final, file="geralSetoresAJ.dat", sep=" ", quote=FALSE, row.names=FALSE)
write.table(final2, file="geralRankAJ.dat", sep=" ", quote=FALSE, row.names=FALSE)

