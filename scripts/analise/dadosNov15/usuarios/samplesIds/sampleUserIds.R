#!/bin/Rscript
# Reads user ids files and mix user ids!

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 1){
  iteration <- args[1]

#solteiro <- read.table("solteiro.dat", skip=1)
#casado <- read.table("casado.dat", skip=1)
#novo <- sample(rbind(solteiro, casado)$V1)
#newG1 <- novo[1:nrow(casado)]
#newG2 <- novo[(nrow(casado)+1):length(novo)]
#write.table(c("[]", newG1), file=paste("casado_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
#write.table(c("[]", newG2), file=paste("solteiro_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

#homem <- read.table("masculino.dat", skip=1)
#mulher <- read.table("feminino.dat", skip=1)
#novo <- sample(rbind(homem, mulher)$V1)
#newG1 <- novo[1:nrow(homem)]
#newG2 <- novo[(nrow(homem)+1):length(novo)]
#write.table(c("[]", newG1), file=paste("masculino_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
#write.table(c("[]", newG2), file=paste("feminino_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

#baixa <- read.table("baixa.dat", skip=1)
#media <- read.table("media.dat", skip=1)
#novo <- sample(rbind(baixa, media)$V1)
#newG1 <- novo[1:nrow(baixa)]
#newG2 <- novo[(nrow(baixa)+1):length(novo)]
#write.table(c("[]", newG1), file=paste("baixa_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
#write.table(c("[]", newG2), file=paste("media_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

#jovem <- read.table("jovem.dat", skip=1)
#adulto <- read.table("adulto.dat", skip=1)
#novo <- sample(rbind(jovem, adulto)$V1)
#newG1 <- novo[1:nrow(jovem)]
#newG2 <- novo[(nrow(jovem)+1):length(novo)]
#write.table(c("[]", newG1), file=paste("jovem_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
#write.table(c("[]", newG2), file=paste("adulto_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

centro <- read.table("centro.dat", skip=1)
notcentro <- read.table("notcentro.dat", skip=1)
novo <- sample(rbind(centro, notcentro)$V1)
newG1 <- novo[1:nrow(centro)]
newG2 <- novo[(nrow(notcentro)+1):length(novo)]
write.table(c("[]", newG1), file=paste("centro_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(c("[]", newG2), file=paste("notcentro_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

catole <- read.table("catole.dat", skip=1)
notcatole <- read.table("notcatole.dat", skip=1)
novo <- sample(rbind(catole, notcatole)$V1)
newG1 <- novo[1:nrow(catole)]
newG2 <- novo[(nrow(notcatole)+1):length(novo)]
write.table(c("[]", newG1), file=paste("catole_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(c("[]", newG2), file=paste("notcatole_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

liberdade <- read.table("liberdade.dat", skip=1)
notliberdade <- read.table("notliberdade.dat", skip=1)
novo <- sample(rbind(liberdade, notliberdade)$V1)
newG1 <- novo[1:nrow(liberdade)]
newG2 <- novo[(nrow(notliberdade)+1):length(novo)]
write.table(c("[]", newG1), file=paste("liberdade_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(c("[]", newG2), file=paste("notliberdade_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)


}
