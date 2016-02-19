#!/bin/Rscript
# Reads user ids files and mix user ids!

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 1){
  iteration <- args[1]

solteiro <- read.table("solteiro.dat", skip=1)
casado <- read.table("casado.dat", skip=1)
novo <- sample(rbind(solteiro, casado)$V1)
newG1 <- novo[1:nrow(casado)]
newG2 <- novo[(nrow(casado)+1):length(novo)]
write.table(c("[]", newG1), file=paste("casado_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(c("[]", newG2), file=paste("solteiro_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

homem <- read.table("masculino.dat", skip=1)
mulher <- read.table("feminino.dat", skip=1)
novo <- sample(rbind(homem, mulher)$V1)
newG1 <- novo[1:nrow(homem)]
newG2 <- novo[(nrow(homem)+1):length(novo)]
write.table(c("[]", newG1), file=paste("masculino_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(c("[]", newG2), file=paste("feminino_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

baixa <- read.table("baixa.dat", skip=1)
media <- read.table("media.dat", skip=1)
novo <- sample(rbind(baixa, media)$V1)
newG1 <- novo[1:nrow(baixa)]
newG2 <- novo[(nrow(baixa)+1):length(novo)]
write.table(c("[]", newG1), file=paste("baixa_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(c("[]", newG2), file=paste("media_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

jovem <- read.table("jovem.dat", skip=1)
adulto <- read.table("adulto.dat", skip=1)
novo <- sample(rbind(jovem, adulto)$V1)
newG1 <- novo[1:nrow(jovem)]
newG2 <- novo[(nrow(jovem)+1):length(novo)]
write.table(c("[]", newG1), file=paste("jovem_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(c("[]", newG2), file=paste("adulto_", iteration, ".dat", sep=""), row.names=FALSE, col.names=FALSE, quote=FALSE)

}
