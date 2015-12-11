#!/bin/Rscript

#Reading data
library(ggplot2)
library(gridExtra)
library(dplyr)
source('analisaICPorFoto.R')

facet_names <- list(
  'agrad%C3%A1vel?'="Pleasantness",
  'seguro?'="Safety"
)

facet_labeller <- function(variable,value){
  return(facet_names[value])
}

dados <- read.table("geral.dat", header=TRUE)

#Intervalo de confiança por ponto
temp <- dados
qscoreSim <- temp [ c(4:103) ]
icData <- apply(qscoreSim, 1, ic)
temp$distance <- icData

#Subset of columns
dadosSub <- temp[, c("V2", "V1", "V3", "diag", "hor", "vert", "red", "green", "blue", "grupo", "bairro", "distance")]

novosDados <- reshape(dadosSub, timevar="grupo", idvar=c("V2", "V1", "diag", "hor", "vert", "red", "green", "blue", "bairro"), direction="wide")

#Urban Elements
library(dplyr)
library(texreg)

substituiURL <- function(dadosPorGrupo){
    localData <- lapply(as.character(dadosPorGrupo$image_url), function (x) paste(strsplit(x, split="/", fixed=TRUE)[[1]][6], "/", strsplit(x, split="/", fixed=TRUE)[[1]][7], sep=""))
    local <- unlist(lapply(localData, '[[', 1))
    return (local)
}

#Lendo resultados do CrowdFlower
dadosg1 <- read.csv("regressao100/g1.csv")
dadosg1$image_url <- substituiURL(dadosg1)

dadosg2 <- read.csv("regressao100/g2.csv")
dadosg2$image_url <- substituiURL(dadosg2)

dadosg3 <- read.csv("regressao100/g3.csv")
dadosg3$image_url <- substituiURL(dadosg3)

dadosg4 <- read.csv("regressao100/g4.csv")
dadosg4$image_url <- substituiURL(dadosg4)

dadosg5 <- read.csv("regressao100/g5.csv")
dadosg5$image_url <- substituiURL(dadosg5)

dadosg6 <- read.csv("regressao100/g6.csv")
dadosg6$image_url <- substituiURL(dadosg6)

dadosg7 <- read.csv("regressao100/g7.csv")
dadosg7$image_url <- substituiURL(dadosg7)

dadosg8 <- read.csv("regressao100/g8.csv")
dadosg8$image_url <- substituiURL(dadosg8)

dadosg9 <- read.csv("regressao100/g9.csv")
dadosg9$image_url <- substituiURL(dadosg9)

dadosg10 <- read.csv("regressao100/g10.csv")
dadosg10$image_url <- substituiURL(dadosg10)

dadosg11 <- read.csv("regressao100/g11.csv")
dadosg11$image_url <- substituiURL(dadosg11)

dadosg12 <- read.csv("regressao100/g12.csv")
dadosg12$image_url <- substituiURL(dadosg12)

dadosg13 <- read.csv("regressao100/g13.csv")
dadosg13$image_url <- substituiURL(dadosg13)

#Somando esquerda e direita
somaValores <- function(dados1, dados2, desvio1, desvio2, uplimit){
    dados1[is.na(dados1)] <- 0
    dados2[is.na(dados2)] <- 0
    
    soma = dados1 + dados2
    desvios = (desvio1 + desvio2)/2
    
    
    desvio = sd(soma)
    if (is.na(desvio)){ 
        valores = rnorm(mean = mean(soma, na.rm = TRUE), sd = mean(desvios, na.rm = TRUE), n = 3)
        valores <- ifelse(valores < 0, 0, valores)
        valores <- ifelse(valores > uplimit, uplimit, valores)
        return (mean(valores))
    }else{
        soma <- ifelse(soma < 0, 0, soma)
        soma <- ifelse(soma > uplimit, uplimit, soma)
        return (mean(soma))
    }
}

#Somando esquerda e direita
mediaValores <- function(dados1, dados2, desvio1, desvio2, uplimit){
    for (i in length(dados1)){
       if(is.na(dados1[i])){
         dados1[i] <- dados2[i]
       }
       if(is.na(dados2[i])){
         dados2[i] <- dados1[i]
       }
    }
    
    soma = (dados1 + dados2) / 2
    desvios = (desvio1 + desvio2)/2
    
    
    desvio = sd(soma)
    if (is.na(desvio)){ 
        valores = rnorm(mean = mean(soma, na.rm = TRUE), sd = mean(desvios, na.rm = TRUE), n = 3)
        valores <- ifelse(valores < 0, 0, valores)
        valores <- ifelse(valores > uplimit, uplimit, valores)
        return (mean(valores))
    }else{
        soma <- ifelse(soma < 0, 0, soma)
        soma <- ifelse(soma > uplimit, uplimit, soma)
        return (mean(soma))
    }
}


#Gerando valores para os casos com apenas 1 resposta a partir do desvio obtido em outras respostas para a mesma questão
geraValores <- function(lista, question, desvios, uplimit){
   desvio = sd(lista)
   return (mean(lista, na.rm = TRUE))
}

Mode <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}

#Agrupando por imagem e por questao - G1
by_image <- group_by(dadosg1, image_url)
desvios <- summarise (by_image, 
                  sd1 = sd(question1, na.rm = TRUE),
                  sd2l = sd(question2__left_side, na.rm = TRUE),
                  sd2r = sd(question2__right_side, na.rm = TRUE),
                  sd3 = sd(question3, na.rm = TRUE) )
groupedData1 <- summarise(by_image,
  #count = n(),
  q1 = geraValores(question1, "1", desvios, 100),
  #sdq1 = sd(question1, na.rm = TRUE),
  q2 = mediaValores(question2__left_side, question2__right_side, desvios$sd2l, desvios$sd2r, 100),
  q2_left = geraValores(question2__left_side, "2l", desvios, 100),
  #sdq2_left = sd(question2__left_side, na.rm = TRUE),
  q2_right = geraValores(question2__right_side, "2r", desvios, 100),
  #sdq2_right = sd(question2__right_side, na.rm = TRUE),
  q3 = geraValores(question3, "3", desvios, 100)
  #sdq3 = sd(question3, na.rm = TRUE) 
  )

#Agrupando por imagem e por questao - G2
by_image <- group_by(dadosg2, image_url)
desvios <- summarise (by_image, 
                  sd1 = sd(question1, na.rm = TRUE),
                  sd2l = sd(question2__left_side, na.rm = TRUE),
                  sd2r = sd(question2__right_side, na.rm = TRUE),
                  sd3 = sd(question3, na.rm = TRUE) )
groupedData2 <- summarise(by_image,
  count = n(),
  q1 = geraValores(question1, "1", desvios, 100),
  #sdq1 = sd(question1, na.rm = TRUE),
  q2 = somaValores(question2__left_side, question2__right_side, desvios$sd2l, desvios$sd2r, 200),
  q2_left = geraValores(question2__left_side, "2l", desvios, 100),
  #sdq2_left = sd(question2__left_side, na.rm = TRUE),
  q2_right = geraValores(question2__right_side, "2r", desvios, 100),
  #sdq2_right = sd(question2__right_side, na.rm = TRUE),
  q3 = geraValores(question3, "3", desvios, 100)
  #sdq3 = sd(question3, na.rm = TRUE) 
  )

#Agrupando por imagem e por questao - G3
by_image <- group_by(dadosg3, image_url)
desvios <- summarise (by_image, 
                  sd1l = sd(question1__left_side, na.rm = TRUE),
                  sd1r = sd(question1__right_side, na.rm = TRUE),
                  sd2l = sd(question2__left_side, na.rm = TRUE),
                  sd2r = sd(question2__right_side, na.rm = TRUE),
                  sd3l = sd(question3__left_side, na.rm = TRUE),
                  sd3r = sd(question3__right_side, na.rm = TRUE) )
groupedData3 <- summarise(by_image,
  count = n(),
  q1 = mediaValores(question1__left_side, question1__right_side, desvios$sd1l, desvios$sd1r, 5),
  q1_left = geraValores(question1__left_side, "1l", desvios, 5),
  #sdq1_left = sd(question1__left_side, na.rm = TRUE),
  q1_right = geraValores(question1__right_side, "1r", desvios, 5),
  #sdq1_right = sd(question1__right_side, na.rm = TRUE),
  q2 = mediaValores(question2__left_side, question2__right_side, desvios$sd2l, desvios$sd2r, 5),
  q2_left = geraValores(question2__left_side, "2l", desvios, 5),
  #sdq2_left = sd(question2__left_side, na.rm = TRUE),
  q2_right = geraValores(question2__right_side, "2r", desvios, 5),
  #sdq2_right = sd(question2__right_side, na.rm = TRUE),
  q3 = mediaValores(question3__left_side, question3__right_side, desvios$sd3l, desvios$sd3r, 5),
  q3_left = geraValores(question3__left_side, "3l", desvios, 5),
  #sdq3_left = sd(question3__left_side, na.rm = TRUE),
  q3_right = geraValores(question3__right_side, "3r", desvios, 5)
  #sdq3_right = sd(question3__right_side, na.rm = TRUE)  
  )

#Agrupando por imagem e por questao - G4
by_image <- group_by(dadosg4, image_url)
desvios <- summarise (by_image, 
                  sd1 = sd(question1, na.rm = TRUE),
                  sd2 = sd(question2, na.rm = TRUE))
groupedData4 <- summarise(by_image,
  count = n(),
  q1 = geraValores(question1, "1", desvios, 10),
  #sdq1 = sd(question1, na.rm = TRUE),
  q2 = geraValores(question2, "2", desvios, 10)
  #sdq2 = sd(question2, na.rm = TRUE) 
  )

#Agrupando por imagem e por questao - G5
by_image <- group_by(dadosg5, image_url)
desvios <- summarise (by_image, 
                  sd1 = sd(question1, na.rm = TRUE),
                  sd2 = sd(your_answer_is, na.rm = TRUE))
groupedData5 <- summarise(by_image,
  count = n(),
  q1 = geraValores(question1, "1", desvios, 20),
  #sdq1 = sd(question1, na.rm = TRUE),
  q2 = geraValores(your_answer_is, "2", desvios, 20)
  #sdq2 = sd(question2, na.rm = TRUE) 
  )

#Agrupando por imagem e por questao - G6
by_image <- group_by(dadosg6, image_url)
desvios <- summarise (by_image, 
                  sd1l = sd(question1__left_side, na.rm = TRUE),
                  sd1r = sd(question1__right_side, na.rm = TRUE),
                  sd2l = sd(question2__left_side, na.rm = TRUE),
                  sd2r = sd(question2__right_side, na.rm = TRUE) )
groupedData6 <- summarise(by_image,
  count = n(),
  q1 = mediaValores(question1__left_side, question1__right_side, desvios$sd1l, desvios$sd1r, 1),
  q1_left = geraValores(question1__left_side, "1l", desvios, 1),
  #sdq1_left = sd(question1__left_side, na.rm = TRUE),
  q1_right = geraValores(question1__right_side, "1r", desvios, 1),
  #sdq1_right = sd(question1__right_side, na.rm = TRUE),
  q2 = mediaValores(question2__left_side, question2__right_side, desvios$sd2l, desvios$sd2r, 1),
  q2_left = geraValores(question2__left_side, "2l", desvios, 1),
  #sdq2_left = sd(question2__left_side, na.rm = TRUE),
  q2_right = geraValores(question2__right_side, "2r", desvios, 1)
  #sdq2_right = sd(question2__right_side, na.rm = TRUE) 
  )


#Agrupando por imagem e por questao - G7
by_image <- group_by(dadosg7, image_url)
desvios <- summarise (by_image, 
                  sd1 = sd(question1, na.rm = TRUE),
                  sd2 = sd(question2, na.rm = TRUE),
                  sd3l = sd(question3__left_side, na.rm = TRUE),
                  sd3r = sd(question3__right_side, na.rm = TRUE) )
groupedData7 <- summarise(by_image,
  count = n(),
  q1 = geraValores(question1, "1", desvios, 3),
  #sdq1 = sd(question1, na.rm = TRUE),
  q2 = geraValores(question2, "2", desvios, 1),
  #sdq2 = sd(question2, na.rm = TRUE),
  q3 = mediaValores(question3__left_side, question3__right_side, desvios$sd3l, desvios$sd3r, 1),
  q3_left = geraValores(question3__left_side, "3l", desvios, 1),
  #sdq3_left = sd(question3__left_side, na.rm = TRUE),
  q3_right = geraValores(question3__right_side, "3r", desvios, 1)
  #sdq3_right = sd(question3__right_side, na.rm = TRUE)  
  )

#Agrupando por imagem e por questao - G8
by_image <- group_by(dadosg8, image_url)
desvios <- summarise (by_image, 
                  sd1 = sd(question1, na.rm = TRUE),
                  sd2l = sd(question2__left_side, na.rm = TRUE),
                  sd2r = sd(question2_right_side, na.rm = TRUE),
                  sd3l = sd(question3__left_side, na.rm = TRUE),
                  sd3r = sd(question3_right_side, na.rm = TRUE)
                  )
groupedData8 <- summarise(by_image,
  count = n(),
  q1 = Mode(question1),
  #sdq1 = sd(question1, na.rm = TRUE),
  q2 = somaValores(question2__left_side, question2_right_side, desvios$sd2l, desvios$sd2r, 40),
  q2_left = geraValores(question2__left_side, "2l", desvios, 20),
  #sdq2_left = sd(question2__left_side, na.rm = TRUE),
  q2_right = geraValores(question2_right_side, "2r", desvios, 20),
  #sdq2_right = sd(question2__right_side, na.rm = TRUE)  
  q3 = somaValores(question3__left_side, question3_right_side, desvios$sd3l, desvios$sd3r, 40),
  q3_left = geraValores(question3__left_side, "3l", desvios, 20),
  q3_right = geraValores(question3_right_side, "3r", desvios, 20)
  )

#Agrupando por imagem e por questao - G9
by_image <- group_by(dadosg9, image_url)
desvios <- summarise (by_image, 
                  sd1l = sd(question1__left_side, na.rm = TRUE),
                  sd1r = sd(question1__right_side, na.rm = TRUE) )
groupedData9 <- summarise(by_image,
  count = n(),
  q1 = mediaValores(question1__left_side, question1__right_side, desvios$sd1l, desvios$sd1r, 200),
  q1_left = geraValores(question1__left_side, "1l", desvios, 200),
  #sdq1_left = sd(question1__left_side, na.rm = TRUE),
  q1_right = geraValores(question1__right_side, "1r", desvios, 200)
  #sdq1_right = sd(question1__right_side, na.rm = TRUE)  
  )

#Agrupando por imagem e por questao - G10
by_image <- group_by(dadosg10, image_url)
desvios <- summarise (by_image, 
                  sd1 = sd(question1, na.rm = TRUE),
                  sd2 = sd(question2, na.rm = TRUE),
                  sd3 = sd(question3, na.rm = TRUE))
groupedData10 <- summarise(by_image,
  count = n(),
  q1 = Mode(x = question1),
  #sdq1 = sd(question1, na.rm = TRUE),
  q2 = geraValores(question2, "2", desvios, 50),
  #sdq2 = sd(question2, na.rm = TRUE),
  q3 = geraValores(question3, "3", desvios, 1)
  #sdq3 = sd(question3, na.rm = TRUE)  
  )

#Agrupando por imagem e por questao - G11
by_image <- group_by(dadosg11, image_url)
desvios <- summarise (by_image, 
                  sd2l = sd(question2__left_side, na.rm = TRUE),
                  sd2r = sd(question2__right_side, na.rm = TRUE),
                  sd3l = sd(question3__left_side, na.rm = TRUE),
                  sd3r = sd(question3__right_side, na.rm = TRUE) )
groupedData11 <- summarise(by_image,
  count = n(),
  q2 = somaValores(question2__left_side, question2__right_side, desvios$sd2l, desvios$sd2r, 20),
  q2_left = geraValores(question2__left_side, "2l", desvios, 10),
  #sdq2_left = sd(question2__left_side, na.rm = TRUE),
  q2_right = geraValores(question2__right_side, "2r", desvios, 10),
  #sdq2_right = sd(question2__right_side, na.rm = TRUE),
  q3 = somaValores(question3__left_side, question3__right_side, desvios$sd3l, desvios$sd3r, 80),
  q3_left = geraValores(question3__left_side, "3l", desvios, 40),
  #sdq3_left = sd(question3__left_side, na.rm = TRUE),
  q3_right = geraValores(question3__right_side, "3r", desvios, 40)
  #sdq3_right = sd(question3__right_side, na.rm = TRUE)  
  )

#Agrupando por imagem e por questao - G12
by_image <- group_by(dadosg12, image_url)
desvios <- summarise (by_image, 
                  sd1 = sd(question1, na.rm = TRUE),
                  sd2l = sd(question2__left_side, na.rm = TRUE),
                  sd2r = sd(question2__right_side, na.rm = TRUE),
                  sd3 = sd(question3, na.rm = TRUE))
groupedData12 <- summarise(by_image,
  count = n(),
  q1 = geraValores(question1, "1", desvios, 10),
  #sdq1 = sd(question1, na.rm = TRUE),
  q2 = somaValores(question2__left_side, question2__right_side, desvios$sd2l, desvios$sd2r, 20),
  q2_left = geraValores(question2__left_side, "2l", desvios, 10),
  #sdq2_left = sd(question2__left_side, na.rm = TRUE),
  q2_right = geraValores(question2__right_side, "2r", desvios, 10),
  #sdq2_right = sd(question2__right_side, na.rm = TRUE),
  q3 = geraValores(question3, "3", desvios,10)
  #sdq3 = sd(question3, na.rm = TRUE)  
  )


#Agrupando por imagem e por questao - G13
by_image <- group_by(dadosg13, image_url)
desvios <- summarise (by_image, 
                  sd1l = sd(question1__left_side, na.rm = TRUE),
                  sd1r = sd(question1__right_side, na.rm = TRUE),
                  sd2l = sd(question2__left_side, na.rm = TRUE),
                  sd2r = sd(question2__right_side, na.rm = TRUE) )
groupedData13 <- summarise(by_image,
  count = n(),
  q1 = somaValores(question1__left_side, question1__right_side, desvios$sd1l, desvios$sd1r, 30),
  q1_left = geraValores(question1__left_side, "1l", desvios, 10),
  #sdq1_left = sd(question1__left_side, na.rm = TRUE),
  q1_right = geraValores(question1__right_side, "1r", desvios, 15),
  #sdq1_right = sd(question1__right_side, na.rm = TRUE),
  q2 = mediaValores(question2__left_side, question2__right_side, desvios$sd2l, desvios$sd2r, 1),
  q2_left = geraValores(question2__left_side, "2l", desvios, 1),
  #sdq2_left = sd(question2__left_side, na.rm = TRUE),
  q2_right = geraValores(question2__right_side, "2r", desvios, 1)
  #sdq2_right = sd(question2__right_side, na.rm = TRUE) 
  )


#Renomeando colunas por grupos
renomeiaGrupos <- function(dadosPorGrupo, listaColunas, idGrupo) {
    for (coluna in listaColunas){
        colnames(dadosPorGrupo)[colnames(dadosPorGrupo) == coluna] <- paste(idGrupo, coluna, sep="")
    }
    return(dadosPorGrupo)
}

renomeiaGrupos2 <- function(dadosPorGrupo, listaColunas, novosNomes) {
    for (i in seq(1, length(listaColunas))){
        coluna = listaColunas[i]
        colnames(dadosPorGrupo)[colnames(dadosPorGrupo) == coluna] <- novosNomes[i]
    }
    return(dadosPorGrupo)
}

groupedData1 <- renomeiaGrupos(groupedData1, c("q2_left", "q2_right", "count"), "g1")
groupedData2 <- renomeiaGrupos(groupedData2, c("q2_left", "q2_right", "count"), "g2")
groupedData3 <- renomeiaGrupos(groupedData3, c("q1_left", "q1_right","q2_left", "q2_right","q3_left", "q3_right", "count"), "g3")
groupedData4 <- renomeiaGrupos(groupedData4, c("count"), "g4")
groupedData5 <- renomeiaGrupos(groupedData5, c("count"), "g5")
groupedData6 <- renomeiaGrupos(groupedData6, c("q1_left", "q1_right", "q2_left", "q2_right", "count"), "g6")
groupedData7 <- renomeiaGrupos(groupedData7, c("q3_left", "q3_right", "count"), "g7")
groupedData8 <- renomeiaGrupos(groupedData8, c("q2_left", "q2_right","q3_left", "q3_right", "count"), "g8")
groupedData9 <- renomeiaGrupos(groupedData9, c("q1_left", "q1_right", "count"), "g9")
groupedData10 <- renomeiaGrupos(groupedData10, c("count"), "g10")
groupedData11 <- renomeiaGrupos(groupedData11, c("q2_left", "q2_right","q3_left", "q3_right", "count"), "g11")
groupedData12 <- renomeiaGrupos(groupedData12, c("q2_left", "q2_right", "count"), "g12")
groupedData13 <- renomeiaGrupos(groupedData13, c("q1_left", "q1_right", "q2_left", "q2_right", "count"), "g13")

groupedData1 <- renomeiaGrupos2(groupedData1, c("q1", "q2", "q3"), c("street_wid", "sidewalk_wid", "public_art"))
groupedData2 <- renomeiaGrupos2(groupedData2, c("q1", "q2", "q3"), c("mov_cars", "park_cars", "mov_ciclyst"))
groupedData3 <- renomeiaGrupos2(groupedData3, c("q1", "q2", "q3"), c("debris", "pavement", "landscape"))
groupedData4 <- renomeiaGrupos2(groupedData4, c("q1", "q2"), c("courtyards", "major_landsc"))
groupedData5 <- renomeiaGrupos2(groupedData5, c("q1", "q2"), c("build_ident", "build_nrectan"))
groupedData6 <- renomeiaGrupos2(groupedData6, c("q1", "q2"), c("prop_street_wall", "prop_wind"))
groupedData7 <- renomeiaGrupos2(groupedData7, c("q1", "q2", "q3"), c("long_sight", "prop_sky_ahead", "prop_sky_across"))
groupedData8 <- renomeiaGrupos2(groupedData8, c("q1", "q2", "q3"), c("graffiti", "trees", "small_planters"))
groupedData9 <- renomeiaGrupos2(groupedData9, c("q1"), c("build_height"))
groupedData10 <- renomeiaGrupos2(groupedData10, c("q1", "q2", "q3"), c("build_diff_ages", "diff_build", "prop_hist_build"))
groupedData11 <- renomeiaGrupos2(groupedData11, c("q2", "q3"), c("outdoor_table", "street_furnit"))
groupedData12 <- renomeiaGrupos2(groupedData12, c("q1", "q2", "q3"), c("basic_col", "lights", "accent_col"))
groupedData13 <- renomeiaGrupos2(groupedData13, c("q1","q2"), c("people", "prop_active_use"))

#Regressao
colnames(novosDados)[colnames(novosDados) == "V2"] <- "image_url"
temp <- merge(groupedData1, novosDados, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData2, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData3, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData4, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData5, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData6, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData7, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData8, by.x="image_url", by.y="image_url")
temp<- merge(temp, groupedData9, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData10, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData11, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData12, by.x="image_url", by.y="image_url")
temp <- merge(temp, groupedData13, by.x="image_url", by.y="image_url")

temp$area[temp$bairro == "centro"] <- "norte"
temp$area[temp$bairro == "liberdade"] <- "oeste"
temp$area[temp$bairro == "catole"] <- "oeste"

agrad <- filter(temp, V1 == "agrad%C3%A1vel?")
seg <- filter(temp, V1 == "seguro?")

#Evaluates presence and coefficients for each picture
calcDanieleCoeff <- function (data) {
    data$diff <- data$rank - data$index
    
    data$movCars <- (data$mov_cars * (data$diff/107)) / sum(data$mov_cars)
    data$parkCars <- (data$park_cars * (data$diff/107)) / sum(data$park_cars)
    data$movCicly <- (data$mov_ciclyst * (data$diff/107)) / sum(data$mov_ciclyst)
    data$buildId <- (data$build_ident * (data$diff/107)) / sum(data$build_ident)
    data$buildNRec <- (data$build_nrectan * (data$diff/107)) / sum(data$build_nrectan)
    data$tree <- (data$trees * (data$diff/107)) / sum(data$trees)
    data$smallPla <- (data$small_planters * (data$diff/107)) / sum(data$small_planters)
    data$diffBuild <- (data$diff_build * (data$diff/107)) / sum(data$diff_build)
    data$streeFur <- (data$street_furnit * (data$diff/107)) / sum(data$street_furnit)
    data$basCol <- (data$basic_col * (data$diff/107)) / sum(data$basic_col)
    data$ligh <- (data$lights * (data$diff/107)) / sum(data$lights)
    data$accenCol <- (data$accent_col * (data$diff/107)) / sum(data$accent_col)
    data$peop <- (data$people * (data$diff/107)) / sum(data$people)
    
    data$graffiti <- as.character(data$graffiti)
    data$graffiti[data$graffiti == "No"] <- 0
    data$graffiti[data$graffiti == "Yes"] <- 1
    data$graff <- (data$diff/107 * as.integer(data$graffiti)) / sum(as.integer(data$graffiti))
    data$build_diff_ages <- as.character(data$build_diff_ages)
    data$build_diff_ages[data$build_diff_ages == "No"] <- 0
    data$build_diff_ages[data$build_diff_ages == "yes"] <- 1
    data$buildDiffAges <- (data$diff/107 * as.integer(data$build_diff_ages)) / sum(as.integer(data$build_diff_ages))
    
    data$movCars2 <- (data$mov_cars * abs(data$diff))
    data$parkCars2 <- (data$park_cars * abs(data$diff))
    data$movCicly2 <- (data$mov_ciclyst * abs(data$diff))
    data$buildId2 <- (data$build_ident * abs(data$diff))
    data$buildNRec2 <- (data$build_nrectan * abs(data$diff))
    data$tree2 <- (data$trees * abs(data$diff))
    data$diffBuild2 <- (data$diff_build * abs(data$diff))
    data$streeFur2 <- (data$street_furnit * abs(data$diff))
    data$smallPla2 <- (data$small_planters * abs(data$diff))
    data$basCol2 <- (data$basic_col * abs(data$diff))
    data$ligh2 <- (data$lights * abs(data$diff))
    data$accenCol2 <- (data$accent_col * abs(data$diff))
    data$peop2 <- (data$people * abs(data$diff))
    data$graff2 <- (abs(data$diff) * as.integer(data$graffiti)) 
    data$buildDiffAges2 <- (abs(data$diff) * as.integer(data$build_diff_ages)) 

    size <- length(data)
    data$sumMovCars <- max(data$mov_cars) * (size-1) * size
    data$sumParkCars <- max(data$park_cars)* (size-1) * size
    data$sumMovCicly <- max(data$mov_ciclyst)* (size-1) * size
    data$sumBuildId <- max(data$build_ident)* (size-1) * size
    data$sumBuildNRec <- max(data$build_nrectan)* (size-1) * size
    data$sumTree <- max(data$trees)* (size-1) * size
    data$sumSmallPla <- max(data$small_planters)* (size-1) * size
    data$sumDiffBuild <- max(data$diff_build)* (size-1) * size
    data$sumStreeFur <- max(data$street_furnit)* (size-1) * size
    data$sumBasCol <- max(data$basic_col)* (size-1) * size
    data$sumLigh <-  max(data$lights)* (size-1) * size
    data$sumAccenCol <- max(data$accent_col)* (size-1) * size
    data$sumPeop <- max(data$people)* (size-1) * size
    data$sumGraff <- max(as.integer(data$graffiti))* (size-1) * size
    data$sumBuildDiffAges <- max(as.integer(data$build_diff_ages)) * (size-1) * size

    data$maxMovCars <- max(data$mov_cars)
    data$maxParkCars <- max(data$park_cars)
    data$maxMovCicly <- max(data$mov_ciclyst)
    data$maxBuildId <- max(data$build_ident)
    data$maxBuildNRec <- max(data$build_nrectan)
    data$maxTree <- max(data$trees)
    data$maxSmallPla <- max(data$small_planters)
    data$maxDiffBuild <- max(data$diff_build)
    data$maxStreeFur <- max(data$street_furnit)
    data$maxBasCol <- max(data$basic_col)
    data$maxLigh <- max(data$lights)
    data$maxAccenCol <- max(data$accent_col)
    data$maxPeop <- max(data$people)
    data$maxGraff <- max(as.integer(data$graffiti))
    data$maxBuildDiffAges <- max(as.integer(data$build_diff_ages))
    

    return (data)
}

randomizeCoeff <- function (data, iterations) {
    movCars <- parkCars <- movCicly <- buildId <- buildNRec <- tree <- smallPla <- diffBuild <-streeFur <- basCol <- ligh <-  accenCol <- peop <- graff <- buildDiffAges <- deb <- pav <- land <- propStreetWall <- propWind <- propSkyAhe <- propActiv <- streetW <- sidewalW <- buildHei <- c()
    
    movCars2 <- parkCars2 <- movCicly2 <- buildId2 <- buildNRec2 <- tree2 <- smallPla2 <- diffBuild2 <- streeFur2 <- basCol2 <- ligh2 <-  accenCol2 <- peop2 <- graff2 <- buildDiffAges2 <- deb2 <- pav2 <- land2 <- propStreetWall2 <- propWind2 <- propSkyAhe2 <- propActiv2 <- streetW2 <- sidewalW2 <- buildHei2 <- c()
    
    graffiti <- as.character(data$graffiti)
    graffiti[data$graffiti == "No"] <- 0
    graffiti[data$graffiti == "Yes"] <- 1
    build_diff_ages <- as.character(data$build_diff_ages)
    build_diff_ages[data$build_diff_ages == "No"] <- 0
    build_diff_ages[data$build_diff_ages == "yes"] <- 1
    
    for (i in seq(1, iterations)){#Creating shuffled values
    
        differences <- sample(data$diff)
        
        movCars <- cbind(movCars, (data$mov_cars * differences[2]/107) / sum(data$mov_cars))
        parkCars <- cbind(parkCars, (data$park_cars * differences[3]/107) / sum(data$park_cars))
        movCicly <- cbind(movCicly, (data$mov_ciclyst * differences[4]/107) / sum(data$mov_ciclyst))
        buildId <- cbind(buildId, (data$build_ident * differences[8])/107 / sum(data$build_ident))
        buildNRec <- cbind(buildNRec,(data$build_nrectan * differences[9]/107) / sum(data$build_nrectan))
        tree <- cbind(tree,(data$trees * differences[15]/107) / sum(data$trees))
        smallPla <- cbind(smallPla,(data$small_planters * differences[16]/107) / sum(data$small_planters))
        diffBuild <- cbind(diffBuild,(data$diff_build * differences[19]/107) / sum(data$diff_build))
        streeFur <- cbind(streeFur, (data$street_furnit * differences[20]/107) / sum(data$street_furnit))
        basCol <- cbind(basCol, (data$basic_col * differences[21]/107) / sum(data$basic_col))
        ligh <- cbind(ligh, (data$lights * differences[22]/107) / sum(data$lights))
        accenCol <- cbind(accenCol, (data$accent_col * differences[23]/107) / sum(data$accent_col))
        peop <- cbind(peop, (data$people * differences[24]/107) / sum(data$people))
        
        graff <- cbind(graff, (differences[14]/107 * as.integer(data$graffiti)) / sum(as.integer(data$graffiti)))
        buildDiffAges <- cbind(buildDiffAges, (differences[18]/107 * as.integer(data$build_diff_ages)) / sum(as.integer(data$build_diff_ages)))
        
        movCars2 <- cbind( movCars2, (data$mov_cars * abs(differences[2])) )
        parkCars2 <- cbind(parkCars2, (data$park_cars * abs(differences[3])))
        movCicly2 <- cbind(movCicly2, (data$mov_ciclyst * abs(differences[4])))
        buildId2 <- cbind(buildId2, (data$build_ident * abs(differences[8])))
        buildNRec2 <- cbind(buildNRec2,(data$build_nrectan * abs(differences[9])))
        tree2 <- cbind(tree2,(data$trees * abs(differences[15])))
        smallPla2 <- cbind(smallPla2,(data$small_planters * abs(differences[16])))
        diffBuild2 <- cbind(diffBuild2,(data$diff_build * abs(differences[19])))
        streeFur2 <- cbind(streeFur2, (data$street_furnit * abs(differences[20])))
        basCol2 <- cbind(basCol2, (data$basic_col * abs(differences[21])))
        ligh2 <- cbind(ligh2, (data$lights * abs(differences[22])))
        accenCol2 <- cbind(accenCol2, (data$accent_col * abs(differences[23])))
        peop2 <- cbind(peop2, (data$people * abs(differences[24])))
        
        graff2 <- cbind(graff2, (abs(differences[14]) * as.integer(data$graffiti))) 
        buildDiffAges2 <- cbind(buildDiffAges2, (abs(differences[18]) * as.integer(data$build_diff_ages)))
        
    }    
    
        #Shuffle mean and sd
        data$rmovCars <- apply(movCars, 1, mean)
        data$rsdmovCars <- apply(movCars, 1, sd)
        data$rparkCars <- apply(parkCars, 1, mean)
        data$rsdparkCars <- apply(parkCars, 1, sd)
        data$rmovCicly <- apply(movCicly, 1, mean)
        data$rsdmovCicly <- apply(movCicly, 1, sd)
        data$rbuildId <- apply(buildId, 1, mean)
        data$rsdbuildId <- apply(buildId, 1, sd)
        data$rbuildNRec <- apply(buildNRec, 1, mean)
        data$rsdbuildNRec <- apply(buildNRec, 1, sd)
        data$rtree <- apply(tree, 1, mean)
        data$rsdtree <- apply(tree, 1, sd)
        data$rsmallPla <- apply(smallPla, 1, mean)
        data$rsdsmallPla <- apply(smallPla, 1, sd)
        data$rdiffBuild <- apply(diffBuild, 1, mean)
        data$rsddiffBuild <- apply(diffBuild, 1, sd)
        data$rstreeFur <- apply(streeFur, 1, mean)
        data$rsdstreeFur <- apply(streeFur, 1, sd)
        data$rbasCol <- apply(basCol, 1, mean)
        data$rsdbasCol <- apply(basCol, 1, sd)
        data$rligh <- apply(ligh, 1, mean)
        data$rsdligh <- apply(ligh, 1, sd)
        data$raccenCol <- apply(accenCol, 1, mean)
        data$rsdaccenCol <- apply(accenCol, 1, sd)
        data$rpeop <- apply(peop, 1, mean)
        data$rsdpeop <- apply(peop, 1, sd)
        
        data$rgraff <- apply(graff, 1, mean)
        data$rsdgraff <- apply(graff, 1, sd)
        data$rbuildDiffAges <- apply(buildDiffAges, 1, mean)
        data$rsdbuildDiffAges <- apply(buildDiffAges, 1, sd)

        #Shuffle mean and sd
        data$rmovCars2 <- apply(movCars2, 1, mean)
        data$rsdmovCars2 <- apply(movCars2, 1, sd)
        data$rparkCars2 <- apply(parkCars2, 1, mean)
        data$rsdparkCars2 <- apply(parkCars2, 1, sd)
        data$rmovCicly2 <- apply(movCicly2, 1, mean)
        data$rsdmovCicly2 <- apply(movCicly2, 1, sd)
        data$rbuildId2 <- apply(buildId2, 1, mean)
        data$rsdbuildId2 <- apply(buildId2, 1, sd)
        data$rbuildNRec2 <- apply(buildNRec2, 1, mean)
        data$rsdbuildNRec2 <- apply(buildNRec2, 1, sd)
        data$rtree2 <- apply(tree2, 1, mean)
        data$rsdtree2 <- apply(tree2, 1, sd)
        data$rsmallPla2 <- apply(smallPla2, 1, mean)
        data$rsdsmallPla2 <- apply(smallPla2, 1, sd)
        data$rdiffBuild2 <- apply(diffBuild2, 1, mean)
        data$rsddiffBuild2 <- apply(diffBuild2, 1, sd)
        data$rstreeFur2 <- apply(streeFur2, 1, mean)
        data$rsdstreeFur2 <- apply(streeFur2, 1, sd)
        data$rbasCol2 <- apply(basCol2, 1, mean)
        data$rsdbasCol2 <- apply(basCol2, 1, sd)
        data$rligh2 <- apply(ligh2, 1, mean)
        data$rsdligh2 <- apply(ligh2, 1, sd)
        data$raccenCol2 <- apply(accenCol2, 1, mean)
        data$rsdaccenCol2 <- apply(accenCol2, 1, sd)
        data$rpeop2 <- apply(peop2, 1, mean)
        data$rsdpeop2 <- apply(peop2, 1, sd)
        
        data$rgraff2 <- apply(graff2, 1, mean)
        data$rsdgraff2 <- apply(graff2, 1, sd)
        data$rbuildDiffAges2 <- apply(buildDiffAges2, 1, mean)
        data$rsdbuildDiffAges2 <- apply(buildDiffAges2, 1, sd)
        
    return (data)
}

iterations <- 10000

simulateCoefShuffle <- function(agrad.l, iterations){


  cmov <- cpark <- ccic <- cbuiid <- cbuiNR <- ctree <- csmalP <- cdiffB <- cfur <- cbcol <- clig <- cacol <- cgraf <- cdiffA <- cdeb <- cpav <- clan <- cwall <- cwind <- cskyA <- cskyAc <- cstreet <- cside <- cbuiH <- cpeop <- cacti <- 0
  
  agrad.l2 <- randomizeCoeff(agrad.l, iterations)

  print("### P-values for Coeff - Flavio")
  res <- wilcox.test(agrad.l$movCars2, agrad.l2$rmovCars2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
   cmov = res$p.value

    res <- wilcox.test(agrad.l$parkCars2, agrad.l2$rparkCars2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cpark = res$p.value

    res <- wilcox.test(agrad.l$movCicly2, agrad.l2$rmovCicly2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    ccic = res$p.value

    res <- wilcox.test(agrad.l$buildId2, agrad.l2$rbuildId2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cbuiid = res$p.value

    res <- wilcox.test(agrad.l$buildNRec2, agrad.l2$rbuildNRec2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cbuiNR = res$p.value

    res <- wilcox.test(agrad.l$tree2, agrad.l2$rtree2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    ctree = res$p.value

    res <- wilcox.test(agrad.l$smallPla2, agrad.l2$rsmallPla2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    csmalP= res$p.value

    res <- wilcox.test(agrad.l$diffBuild2, agrad.l2$rdiffBuild2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cdiffB = res$p.value

    res <- wilcox.test(agrad.l$streeFur2, agrad.l2$rstreeFur2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cfur = res$p.value

    res <- wilcox.test(agrad.l$basCol2, agrad.l2$rbasCol2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cbcol = res$p.value

    res <- wilcox.test(agrad.l$ligh2, agrad.l2$rligh2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    clig = res$p.value

    res <- wilcox.test(agrad.l$accenCol2, agrad.l2$raccenCol2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cacol = res$p.value

    res <- wilcox.test(agrad.l$peop2, agrad.l2$rpeop2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cpeop = res$p.value
    
    res <- wilcox.test(agrad.l$graff2, agrad.l2$rgraff2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cgraf = res$p.value

    res <- wilcox.test(agrad.l$buildDiffAges2, agrad.l2$rbuildDiffAges2, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cdiffA = res$p.value

    
  print(paste("P-values - mov cars", cmov)) #/ iterations))
  print(paste("P-values - park cars", cpark)) #/ iterations))
  print(paste("P-values - cyclists", ccic)) #/ iterations))
  print(paste("P-values - build ident", cbuiid)) #/ iterations))
  print(paste("P-values - build n rect", cbuiNR)) #/ iterations))
  print(paste("P-values - trees", ctree)) #/ iterations))
  print(paste("P-values - small planters",csmalP))# / iterations))
  print(paste("P-values - diff buildings", cdiffB)) #/ iterations))
  print(paste("P-values - furniture", cfur)) #/ iterations))
  print(paste("P-values - bas col", cbcol)) #/ iterations))
  print(paste("P-values - acce col", cacol)) #/ iterations))
  print(paste("P-values - lig", clig)) #/ iterations))
  print(paste("P-values - peop", cpeop)) #/ iterations))
  print(paste("P-values - graffiti", cgraf)) #/ iterations))
  print(paste("P-values - build diff ages", cdiffA)) #/ iterations))

print("### P-values for Coeff - Daniele")
  res <- wilcox.test(agrad.l$movCars, agrad.l2$rmovCars, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
   cmov = res$p.value

    res <- wilcox.test(agrad.l$parkCars, agrad.l2$rparkCars, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cpark = res$p.value

    res <- wilcox.test(agrad.l$movCicly, agrad.l2$rmovCicly, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    ccic = res$p.value

    res <- wilcox.test(agrad.l$buildId, agrad.l2$rbuildId, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cbuiid = res$p.value

    res <- wilcox.test(agrad.l$buildNRec, agrad.l2$rbuildNRec, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cbuiNR = res$p.value

    res <- wilcox.test(agrad.l$tree, agrad.l2$rtree, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    ctree = res$p.value

    res <- wilcox.test(agrad.l$smallPla, agrad.l2$rsmallPla, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    csmalP= res$p.value

    res <- wilcox.test(agrad.l$diffBuild, agrad.l2$rdiffBuild, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cdiffB = res$p.value

    res <- wilcox.test(agrad.l$streeFur, agrad.l2$rstreeFur, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cfur = res$p.value

    res <- wilcox.test(agrad.l$basCol, agrad.l2$rbasCol, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cbcol = res$p.value

    res <- wilcox.test(agrad.l$ligh, agrad.l2$rligh, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    clig = res$p.value

    res <- wilcox.test(agrad.l$accenCol, agrad.l2$raccenCol, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cacol = res$p.value

    res <- wilcox.test(agrad.l$peop, agrad.l2$rpeop, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cpeop = res$p.value
    
    res <- wilcox.test(agrad.l$graff, agrad.l2$rgraff, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cgraf = res$p.value

    res <- wilcox.test(agrad.l$buildDiffAges, agrad.l2$rbuildDiffAges, na.action = na.exclude, conf.int = TRUE, paired = TRUE)
    cdiffA = res$p.value

    
  print(paste("P-values - mov cars", cmov)) #/ iterations))
  print(paste("P-values - park cars", cpark)) #/ iterations))
  print(paste("P-values - cyclists", ccic)) #/ iterations))
  print(paste("P-values - build ident", cbuiid)) #/ iterations))
  print(paste("P-values - build n rect", cbuiNR)) #/ iterations))
  print(paste("P-values - trees", ctree)) #/ iterations))
  print(paste("P-values - small planters",csmalP))# / iterations))
  print(paste("P-values - diff buildings", cdiffB)) #/ iterations))
  print(paste("P-values - furniture", cfur)) #/ iterations))
  print(paste("P-values - bas col", cbcol)) #/ iterations))
  print(paste("P-values - acce col", cacol)) #/ iterations))
  print(paste("P-values - lig", clig)) #/ iterations))
  print(paste("P-values - peop", cpeop)) #/ iterations))
  print(paste("P-values - graffiti", cgraf)) #/ iterations))
  print(paste("P-values - build diff ages", cdiffA)) #/ iterations))


  return (agrad.l2)

}

printOutputOneListPerFeature <- function(agrad.l2, column1, column2){
     print(">>>>>>>> One list - top 10 ordered by real world coef and containing real world and shuffle world data - Daniele")
      print(head(arrange(select_(agrad.l2, "movCars", "rmovCars", "rsdmovCars", "maxMovCars", "sumMovCars", "image_url", column1, column2, "diff"), desc(movCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "parkCars", "rparkCars", "rsdparkCars", "maxParkCars","sumParkCars", "image_url", column1, column2, "diff"), desc(parkCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "movCicly", "rmovCicly", "rsdmovCicly", "maxMovCicly", "sumMovCicly", "image_url", column1, column2, "diff"), desc(movCicly)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildId", "rbuildId", "rsdbuildId", "maxBuildId", "sumBuildId","image_url", column1, column2, "diff"), desc(buildId)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildNRec", "rbuildNRec", "rsdbuildNRec", "maxBuildNRec", "sumBuildNRec", "image_url", column1, column2, "diff"), desc(buildNRec)), n = 10))
      print(head(arrange(select_(agrad.l2, "tree", "rtree", "rsdtree", "maxTree", "sumTree", "image_url", column1, column2, "diff"), desc(tree)), n = 10))
      print(head(arrange(select_(agrad.l2, "smallPla", "rsmallPla", "rsdsmallPla", "maxSmallPla","sumSmallPla", "image_url", column1, column2, "diff"), desc(smallPla)), n = 10))
      print(head(arrange(select_(agrad.l2, "diffBuild", "rdiffBuild", "rsddiffBuild", "maxDiffBuild", "sumDiffBuild","image_url", column1, column2, "diff"), desc(diffBuild)), n = 10))
      print(head(arrange(select_(agrad.l2, "streeFur", "rstreeFur", "rsdstreeFur", "maxStreeFur", "sumStreeFur", "image_url", column1, column2, "diff"), desc(streeFur)), n = 10))
      print(head(arrange(select_(agrad.l2, "basCol", "rbasCol", "rsdbasCol", "maxBasCol", "sumBasCol", "image_url", column1, column2, "diff"), desc(basCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "accenCol", "raccenCol", "rsdaccenCol", "maxAccenCol", "sumAccenCol","image_url", column1, column2, "diff"), desc(accenCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "ligh", "rligh", "rsdligh", "maxLigh", "sumLigh","image_url", column1, column2, "diff"), desc(ligh)), n = 10))
      print(head(arrange(select_(agrad.l2, "peop", "rpeop", "rsdpeop", "maxPeop", "sumPeop","image_url", column1, column2, "diff"), desc(peop)), n = 10))
      print(head(arrange(select_(agrad.l2, "graff", "rgraff", "rsdgraff", "maxGraff", "sumGraff","image_url", column1, column2, "diff"), desc(graff)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildDiffAges", "rbuildDiffAges", "rsdbuildDiffAges", "maxBuildDiffAges", "sumBuildDiffAges","image_url", column1, column2, "diff"), desc(buildDiffAges)), n = 10))


     print(">>>>>>>> One list - top 10 ordered by real world coef and containing real world and shuffle world data - Flavio")
      print(head(arrange(select_(agrad.l2, "movCars2", "rmovCars2", "rsdmovCars2", "maxMovCars", "sumMovCars", "image_url", column1, column2, "diff"), desc(movCars2)), n = 10))
      print(head(arrange(select_(agrad.l2, "parkCars2", "rparkCars2", "rsdparkCars2", "maxParkCars", "sumParkCars","image_url", column1, column2, "diff"), desc(parkCars2)), n = 10))
      print(head(arrange(select_(agrad.l2, "movCicly2", "rmovCicly2", "rsdmovCicly2", "maxMovCicly", "sumMovCicly","image_url", column1, column2, "diff"), desc(movCicly2)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildId2", "rbuildId2", "rsdbuildId2", "maxBuildId", "sumBuildId","image_url", column1, column2, "diff"), desc(buildId2)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildNRec2", "rbuildNRec2", "rsdbuildNRec2", "maxBuildNRec", "sumBuildNRec","image_url", column1, column2, "diff"), desc(buildNRec2)), n = 10))
      print(head(arrange(select_(agrad.l2, "tree2", "rtree2", "rsdtree2", "maxTree", "sumTree", "image_url", column1, column2, "diff"), desc(tree2)), n = 10))
      print(head(arrange(select_(agrad.l2, "smallPla2", "rsmallPla2", "rsdsmallPla2", "maxSmallPla", "sumSmallPla","image_url", column1, column2, "diff"), desc(smallPla2)), n = 10))
      print(head(arrange(select_(agrad.l2, "diffBuild2", "rdiffBuild2", "rsddiffBuild2", "maxDiffBuild", "sumDiffBuild","image_url", column1, column2, "diff"), desc(diffBuild2)), n = 10))
      print(head(arrange(select_(agrad.l2, "streeFur2", "rstreeFur2", "rsdstreeFur2", "maxStreeFur", "sumStreeFur", "image_url", column1, column2, "diff"), desc(streeFur2)), n = 10))
      print(head(arrange(select_(agrad.l2, "basCol2", "rbasCol2", "rsdbasCol2", "maxBasCol", "sumBasCol","image_url", column1, column2, "diff"), desc(basCol2)), n = 10))
      print(head(arrange(select_(agrad.l2, "accenCol2", "raccenCol2", "rsdaccenCol2", "maxAccenCol", "sumAccenCol","image_url", column1, column2, "diff"), desc(accenCol2)), n = 10))
      print(head(arrange(select_(agrad.l2, "ligh2", "rligh2", "rsdligh2", "maxLigh",  "sumLigh","image_url", column1, column2, "diff"), desc(ligh2)), n = 10))
      print(head(arrange(select_(agrad.l2, "peop2", "rpeop2", "rsdpeop2", "maxPeop", "sumPeop","image_url", column1, column2, "diff"), desc(peop2)), n = 10))
      print(head(arrange(select_(agrad.l2, "graff2", "rgraff2", "rsdgraff2", "maxGraff", "sumGraff","image_url", column1, column2, "diff"), desc(graff2)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildDiffAges2", "rbuildDiffAges2", "rsdbuildDiffAges2", "maxBuildDiffAges","sumBuildDiffAges", "image_url", column1, column2, "diff"), desc(buildDiffAges2)), n = 10))
  
}

printOutputTwoListsPerFeature <- function(agrad.l2, column1, column2){
      print(">>>>>>>> Two lists - top 10 ordered by real world coef ; top 10 ordered by shuffle world - Daniele")

      print(head(arrange(select_(agrad.l2, "movCars", "maxMovCars", "image_url", column1, column2, "diff"), desc(movCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "rmovCars", "rsdmovCars", "maxMovCars", "image_url", column1, column2, "diff"), desc(rmovCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "parkCars", "maxParkCars", "image_url", column1, column2, "diff"), desc(parkCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "rparkCars", "rsdparkCars", "maxParkCars", "image_url", column1, column2, "diff"), desc(rparkCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "movCicly", "maxMovCicly", "image_url", column1, column2, "diff"), desc(movCicly)), n = 10))
      print(head(arrange(select_(agrad.l2, "rmovCicly", "rsdmovCicly", "maxMovCicly", "image_url", column1, column2, "diff"), desc(rmovCicly)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildId", "maxBuildId", "image_url", column1, column2, "diff"), desc(buildId)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildId", "rsdbuildId", "maxBuildId", "image_url", column1, column2, "diff"), desc(rbuildId)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildNRec", "maxBuildNRec", "image_url", column1, column2, "diff"), desc(buildNRec)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildNRec", "rsdbuildNRec", "maxBuildNRec", "image_url", column1, column2, "diff"), desc(rbuildNRec)), n = 10))
      print(head(arrange(select_(agrad.l2, "tree", "maxTree", "image_url", column1, column2, "diff"), desc(tree)), n = 10))
      print(head(arrange(select_(agrad.l2, "rtree", "rsdtree", "maxTree", "image_url", column1, column2, "diff"), desc(rtree)), n = 10))
      print(head(arrange(select_(agrad.l2, "smallPla", "maxSmallPla", "image_url", column1, column2, "diff"), desc(smallPla)), n = 10))
      print(head(arrange(select_(agrad.l2, "rsmallPla", "rsdsmallPla", "maxSmallPla", "image_url", column1, column2, "diff"), desc(rsmallPla)), n = 10))
      print(head(arrange(select_(agrad.l2, "diffBuild", "maxDiffBuild", "image_url", column1, column2, "diff"), desc(diffBuild)), n = 10))
      print(head(arrange(select_(agrad.l2, "rdiffBuild", "rsddiffBuild", "maxDiffBuild", "image_url", column1, column2, "diff"), desc(rdiffBuild)), n = 10))
      print(head(arrange(select_(agrad.l2, "streeFur", "maxStreeFur", "image_url", column1, column2, "diff"), desc(streeFur)), n = 10))
      print(head(arrange(select_(agrad.l2, "rstreeFur", "rsdstreeFur", "maxStreeFur", "image_url", column1, column2, "diff"), desc(rstreeFur)), n = 10))
      print(head(arrange(select_(agrad.l2, "basCol", "maxBasCol", "image_url", column1, column2, "diff"), desc(basCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbasCol", "rsdbasCol", "maxBasCol", "image_url", column1, column2, "diff"), desc(rbasCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "accenCol", "maxAccenCol", "image_url", column1, column2, "diff"), desc(accenCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "raccenCol", "rsdaccenCol", "maxAccenCol", "image_url", column1, column2, "diff"), desc(raccenCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "ligh", "maxLigh", "image_url", column1, column2, "diff"), desc(ligh)), n = 10))
      print(head(arrange(select_(agrad.l2, "rligh", "rsdligh", "maxLigh", "image_url", column1, column2, "diff"), desc(rligh)), n = 10))
      print(head(arrange(select_(agrad.l2, "peop", "maxPeop", "image_url", column1, column2, "diff"), desc(peop)), n = 10))
      print(head(arrange(select_(agrad.l2, "rpeop", "rsdpeop", "maxPeop", "image_url", column1, column2, "diff"), desc(rpeop)), n = 10))
      print(head(arrange(select_(agrad.l2, "graff", "maxGraff", "image_url", column1, column2, "diff"), desc(graff)), n = 10))
      print(head(arrange(select_(agrad.l2, "rgraff", "rsdgraff", "maxGraff", "image_url", column1, column2, "diff"), desc(rgraff)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildDiffAges", "maxBuildDiffAges", "image_url", column1, column2, "diff"), desc(buildDiffAges)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildDiffAges", "rsdbuildDiffAges", "maxBuildDiffAges", "image_url", column1, column2, "diff"), desc(rbuildDiffAges)), n = 10))


      print(">>>>>>>> Two lists - top 10 ordered by real world coef ; top 10 ordered by shuffle world - Flavio")
      print(head(arrange(select_(agrad.l2, "movCars2", "maxMovCars", "sumMovCars","image_url", column1, column2, "diff"), desc(movCars2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rmovCars2", "rsdmovCars2", "maxMovCars", "sumMovCars", "image_url", column1, column2, "diff"), desc(rmovCars2)), n = 10))
      print(head(arrange(select_(agrad.l2, "parkCars2", "maxParkCars", "sumParkCars","image_url", column1, column2, "diff"), desc(parkCars2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rparkCars2", "rsdparkCars2", "maxParkCars", "sumParkCars","image_url", column1, column2, "diff"), desc(rparkCars2)), n = 10))
      print(head(arrange(select_(agrad.l2, "movCicly2", "maxMovCicly", "sumMovCicly","image_url", column1, column2, "diff"), desc(movCicly2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rmovCicly2", "rsdmovCicly2", "maxMovCicly", "sumMovCicly","image_url", column1, column2, "diff"), desc(rmovCicly2)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildId2", "maxBuildId", "sumBuildId","image_url", column1, column2, "diff"), desc(buildId2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildId2", "rsdbuildId2", "maxBuildId", "sumBuildId","image_url", column1, column2, "diff"), desc(rbuildId2)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildNRec2", "maxBuildNRec", "sumBuildNRec","image_url", column1, column2, "diff"), desc(buildNRec2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildNRec2", "rsdbuildNRec2", "maxBuildNRec", "sumBuildNRec","image_url", column1, column2, "diff"), desc(rbuildNRec2)), n = 10))
      print(head(arrange(select_(agrad.l2, "tree2", "maxTree", "sumTree","image_url", column1, column2, "diff"), desc(tree2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rtree2", "rsdtree2", "maxTree", "sumTree","image_url", column1, column2, "diff"), desc(rtree2)), n = 10))
      print(head(arrange(select_(agrad.l2, "smallPla2", "maxSmallPla", "sumSmallPla","image_url", column1, column2, "diff"), desc(smallPla2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rsmallPla2", "rsdsmallPla2", "maxSmallPla", "sumSmallPla","image_url", column1, column2, "diff"), desc(rsmallPla2)), n = 10))
      print(head(arrange(select_(agrad.l2, "diffBuild2", "maxDiffBuild", "sumDiffBuild","image_url", column1, column2, "diff"), desc(diffBuild2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rdiffBuild2", "rsddiffBuild2", "maxDiffBuild", "sumDiffBuild","image_url", column1, column2, "diff"), desc(rdiffBuild2)), n = 10))
      print(head(arrange(select_(agrad.l2, "streeFur2", "maxStreeFur", "sumStreeFur","image_url", column1, column2, "diff"), desc(streeFur2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rstreeFur2", "rsdstreeFur2", "maxStreeFur", "sumStreeFur","image_url", column1, column2, "diff"), desc(rstreeFur2)), n = 10))
      print(head(arrange(select_(agrad.l2, "basCol2", "maxBasCol", "sumBasCol","image_url", column1, column2, "diff"), desc(basCol2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbasCol2", "rsdbasCol2", "maxBasCol", "sumBasCol","image_url", column1, column2, "diff"), desc(rbasCol2)), n = 10))
      print(head(arrange(select_(agrad.l2, "accenCol2", "maxAccenCol", "sumAccenCol","image_url", column1, column2, "diff"), desc(accenCol2)), n = 10))
      print(head(arrange(select_(agrad.l2, "raccenCol2", "rsdaccenCol2", "maxAccenCol", "sumAccenCol","image_url", column1, column2, "diff"), desc(raccenCol2)), n = 10))
      print(head(arrange(select_(agrad.l2, "ligh2", "maxLigh",  "sumLigh","image_url", column1, column2, "diff"), desc(ligh2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rligh2", "rsdligh2", "maxLigh", "sumLigh","image_url", column1, column2, "diff"), desc(rligh2)), n = 10))
      print(head(arrange(select_(agrad.l2, "peop2", "maxPeop", "sumPeop","image_url", column1, column2, "diff"), desc(peop2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rpeop2", "rsdpeop2", "maxPeop", "sumPeop","image_url", column1, column2, "diff"), desc(rpeop2)), n = 10))
      print(head(arrange(select_(agrad.l2, "graff2", "maxGraff","sumGraff", "image_url", column1, column2, "diff"), desc(graff2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rgraff2", "rsdgraff2", "maxGraff", "sumGraff","image_url", column1, column2, "diff"), desc(rgraff2)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildDiffAges2", "maxBuildDiffAges", "sumBuildDiffAges","image_url", column1, column2, "diff"), desc(buildDiffAges2)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildDiffAges2", "rsdbuildDiffAges2", "maxBuildDiffAges", "sumBuildDiffAges","image_url", column1, column2, "diff"), desc(rbuildDiffAges2)), n = 10))
  
}

printOutputTwoListsAllFeaturesTog <- function(agrad.l2){
      library(reshape)

      print(">>>>>>>> One list with all features together with Daniele coeff - real world and shuffle world")
      all <- melt(select(agrad.l2, movCars, parkCars, movCicly, buildId, buildNRec, tree, smallPla, diffBuild, streeFur, basCol, ligh, accenCol, peop, graff, buildDiffAges, image_url), id=c("image_url"))
      
      all$random <- 0
      all[all$variable == "movCars",]$random<- sum(agrad.l2$rmovCars)
      all[all$variable == "parkCars",]$random<- sum(agrad.l2$rparkCars)
      all[all$variable == "movCicly",]$random<- sum(agrad.l2$rmovCicly)
      all[all$variable == "buildId",]$random<- sum(agrad.l2$rbuildId)
      all[all$variable == "buildNRec",]$random<- sum(agrad.l2$rbuildNRec)
      all[all$variable == "tree",]$random<- sum(agrad.l2$rtree)
      all[all$variable == "smallPla",]$random<- sum(agrad.l2$rsmallPla)
      all[all$variable == "diffBuild",]$random<- sum(agrad.l2$rdiffBuild)
      all[all$variable == "streeFur",]$random<- sum(agrad.l2$rstreeFur)
      all[all$variable == "basCol",]$random<- sum(agrad.l2$rbasCol)
      all[all$variable == "accenCol",]$random<- sum(agrad.l2$raccenCol)
      all[all$variable == "peop",]$random<- sum(agrad.l2$rpeop)
      all[all$variable == "buildDiffAges",]$random<- sum(agrad.l2$rbuildDiffAges)
      all[all$variable == "graff",]$random<- sum(agrad.l2$rgraff)
      all[all$variable == "ligh",]$random<- sum(agrad.l2$rligh)
      all$sd <- 0
      all[all$variable == "movCars",]$sd <- agrad.l2$rsdmovCars
      all[all$variable == "parkCars",]$sd <- agrad.l2$rsdparkCars
      all[all$variable == "movCicly",]$sd <- agrad.l2$rsdmovCicly
      all[all$variable == "buildId",]$sd <- agrad.l2$rsdbuildId
      all[all$variable == "buildNRec",]$sd <- agrad.l2$rsdbuildNRec
      all[all$variable == "tree",]$sd <- agrad.l2$rsdtree
      all[all$variable == "smallPla",]$sd <- agrad.l2$rsdsmallPla
      all[all$variable == "diffBuild",]$sd <- agrad.l2$rsddiffBuild
      all[all$variable == "streeFur",]$sd <- agrad.l2$rsdstreeFur
      all[all$variable == "basCol",]$sd <- agrad.l2$rsdbasCol
      all[all$variable == "accenCol",]$sd <- agrad.l2$rsdaccenCol
      all[all$variable == "peop",]$sd <- agrad.l2$rsdpeop
      all[all$variable == "buildDiffAges",]$sd <- agrad.l2$rsdbuildDiffAges
      all[all$variable == "graff",]$sd <- agrad.l2$rsdgraff
      all[all$variable == "ligh",]$sd <- agrad.l2$rsdligh

      print("### All")
      print("##### Summary")
      print( all %>% group_by(variable) %>% summarise( som=sum(value), rand=mean(random), std=mean(sd) ) %>% arrange(desc(som)) )
      print("##### List")
      print( arrange(all, desc(value)) )
      
      print(">>>>>>>> Two lists with all features together with Daniele coeff - real world and shuffle world")
      real <- melt(select(agrad.l2, movCars, parkCars, movCicly, buildId, buildNRec, tree, smallPla, diffBuild, streeFur, basCol, ligh, accenCol, peop, graff, buildDiffAges, image_url), id=c("image_url"))
      
      shuff <- melt(select(agrad.l2, rmovCars, rparkCars, rmovCicly, rbuildId, rbuildNRec, rtree, rsmallPla, rdiffBuild, rstreeFur, rbasCol, rligh, raccenCol, rpeop, rgraff, rbuildDiffAges, image_url), id=c("image_url"))
      shuff$sd <- 0
      shuff[shuff$variable == "rmovCars",]$sd <- agrad.l2$rsdmovCars
      shuff[shuff$variable == "rparkCars",]$sd <- agrad.l2$rsdparkCars
      shuff[shuff$variable == "rmovCicly",]$sd <- agrad.l2$rsdmovCicly
      shuff[shuff$variable == "rbuildId",]$sd <- agrad.l2$rsdbuildId
      shuff[shuff$variable == "rbuildNRec",]$sd <- agrad.l2$rsdbuildNRec
      shuff[shuff$variable == "rtree",]$sd <- agrad.l2$rsdtree
      shuff[shuff$variable == "rsmallPla",]$sd <- agrad.l2$rsdsmallPla
      shuff[shuff$variable == "rdiffBuild",]$sd <- agrad.l2$rsddiffBuild
      shuff[shuff$variable == "rstreeFur",]$sd <- agrad.l2$rsdstreeFur
      shuff[shuff$variable == "rbasCol",]$sd <- agrad.l2$rsdbasCol
      shuff[shuff$variable == "raccenCol",]$sd <- agrad.l2$rsdaccenCol
      shuff[shuff$variable == "rpeop",]$sd <- agrad.l2$rsdpeop
      shuff[shuff$variable == "rbuildDiffAges",]$sd <- agrad.l2$rsdbuildDiffAges
      shuff[shuff$variable == "rgraff",]$sd <- agrad.l2$rsdgraff
      shuff[shuff$variable == "rligh",]$sd <- agrad.l2$rsdligh

      print("### Real")
      print("##### Summary")
      print( real %>% group_by(variable) %>% summarise( som=sum(value) ) %>% arrange(desc(som)) )
      print("##### List")
      print( arrange(real, desc(value)) )
      print("### Shuffle")
      print("##### Summary")
      print( shuff %>% group_by(variable) %>% summarise( som=sum(value), std=mean(sd) ) %>% arrange(desc(som)) )
      print("##### List")
      print( arrange(shuff, desc(value)) )

       print(">>>>>>>> One list with all features together with Flavio coeff - real world and shuffle world")
       all <- melt(select(agrad.l2, movCars2, parkCars2, movCicly2, buildId2, buildNRec2, tree2, smallPla2, diffBuild2, streeFur2, basCol2, ligh2, accenCol2, peop2, graff2, buildDiffAges2, image_url), id=c("image_url"))
      
      all$sumDen <- 0
      all[all$variable == "movCars2",]$sumDen <- agrad.l2$sumMovCars
      all[all$variable == "parkCars2",]$sumDen <- agrad.l2$sumParkCars
      all[all$variable == "movCicly2",]$sumDen <- agrad.l2$sumMovCicly
      all[all$variable == "buildId2",]$sumDen <- agrad.l2$sumBuildId
      all[all$variable == "buildNRec2",]$sumDen <- agrad.l2$sumBuildNRec
      all[all$variable == "tree2",]$sumDen <- agrad.l2$sumTree
      all[all$variable == "smallPla2",]$sumDen <- agrad.l2$sumSmallPla
      all[all$variable == "diffBuild2",]$sumDen <- agrad.l2$sumDiffBuild
      all[all$variable == "streeFur2",]$sumDen <- agrad.l2$sumStreeFur
      all[all$variable == "basCol2",]$sumDen <- agrad.l2$sumBasCol
      all[all$variable == "accenCol2",]$sumDen <- agrad.l2$sumAccenCol
      all[all$variable == "peop2",]$sumDen <- agrad.l2$sumPeop
      all[all$variable == "buildDiffAges2",]$sumDen <- agrad.l2$sumBuildDiffAges
      all[all$variable == "graff2",]$sumDen <- agrad.l2$sumGraff
      all[all$variable == "ligh2",]$sumDen <- agrad.l2$sumLigh

      all$random <- 0
      all[all$variable == "movCars2",]$random<- sum(agrad.l2$rmovCars2)
      all[all$variable == "parkCars2",]$random<- sum(agrad.l2$rparkCars2)
      all[all$variable == "movCicly2",]$random<- sum(agrad.l2$rmovCicly2)
      all[all$variable == "buildId2",]$random<- sum(agrad.l2$rbuildId2)
      all[all$variable == "buildNRec2",]$random<- sum(agrad.l2$rbuildNRec2)
      all[all$variable == "tree2",]$random<- sum(agrad.l2$rtree2)
      all[all$variable == "smallPla2",]$random<- sum(agrad.l2$rsmallPla2)
      all[all$variable == "diffBuild2",]$random<- sum(agrad.l2$rdiffBuild2)
      all[all$variable == "streeFur2",]$random<- sum(agrad.l2$rstreeFur2)
      all[all$variable == "basCol2",]$random<- sum(agrad.l2$rbasCol2)
      all[all$variable == "accenCol2",]$random<- sum(agrad.l2$raccenCol2)
      all[all$variable == "peop2",]$random<- sum(agrad.l2$rpeop2)
      all[all$variable == "buildDiffAges2",]$random<- sum(agrad.l2$rbuildDiffAges2)
      all[all$variable == "graff2",]$random<- sum(agrad.l2$rgraff2)
      all[all$variable == "ligh2",]$random<- sum(agrad.l2$rligh2)
      all$sd <- 0
      all[all$variable == "movCars2",]$sd <- agrad.l2$rsdmovCars2
      all[all$variable == "parkCars2",]$sd <- agrad.l2$rsdparkCars2
      all[all$variable == "movCicly2",]$sd <- agrad.l2$rsdmovCicly2
      all[all$variable == "buildId2",]$sd <- agrad.l2$rsdbuildId2
      all[all$variable == "buildNRec2",]$sd <- agrad.l2$rsdbuildNRec2
      all[all$variable == "tree2",]$sd <- agrad.l2$rsdtree2
      all[all$variable == "smallPla2",]$sd <- agrad.l2$rsdsmallPla2
      all[all$variable == "diffBuild2",]$sd <- agrad.l2$rsddiffBuild2
      all[all$variable == "streeFur2",]$sd <- agrad.l2$rsdstreeFur2
      all[all$variable == "basCol2",]$sd <- agrad.l2$rsdbasCol2
      all[all$variable == "accenCol2",]$sd <- agrad.l2$rsdaccenCol2
      all[all$variable == "peop2",]$sd <- agrad.l2$rsdpeop2
      all[all$variable == "buildDiffAges2",]$sd <- agrad.l2$rsdbuildDiffAges2
      all[all$variable == "graff2",]$sd <- agrad.l2$rsdgraff2
      all[all$variable == "ligh2",]$sd <- agrad.l2$rsdligh2
      print("### All")
      print("##### Summary")
      print( all %>% group_by(variable) %>% summarise( som=sum(value)/mean(sumDen), rand=mean(random)/mean(sumDen), std=mean(sd)/mean(sumDen) ) %>% arrange(desc(som)) )
      print("##### List")
      print( arrange(all, desc(value)) )
      
      print(">>>>>>>> Two lists with all features together Flavio coeff - real world and shuffle world")
      real <- melt(select(agrad.l2, movCars2, parkCars2, movCicly2, buildId2, buildNRec2, tree2, smallPla2, diffBuild2, streeFur2, basCol2, ligh2, accenCol2, peop2, graff2, buildDiffAges2, image_url), id=c("image_url"))
      real$sumDen <- 0
      real[real$variable == "movCars2",]$sumDen <- agrad.l2$sumMovCars
      real[real$variable == "parkCars2",]$sumDen <- agrad.l2$sumParkCars
      real[real$variable == "movCicly2",]$sumDen <- agrad.l2$sumMovCicly
      real[real$variable == "buildId2",]$sumDen <- agrad.l2$sumBuildId
      real[real$variable == "buildNRec2",]$sumDen <- agrad.l2$sumBuildNRec
      real[real$variable == "tree2",]$sumDen <- agrad.l2$sumTree
      real[real$variable == "smallPla2",]$sumDen <- agrad.l2$sumSmallPla
      real[real$variable == "diffBuild2",]$sumDen <- agrad.l2$sumDiffBuild
      real[real$variable == "streeFur2",]$sumDen <- agrad.l2$sumStreeFur
      real[real$variable == "basCol2",]$sumDen <- agrad.l2$sumBasCol
      real[real$variable == "accenCol2",]$sumDen <- agrad.l2$sumAccenCol
      real[real$variable == "peop2",]$sumDen <- agrad.l2$sumPeop
      real[real$variable == "buildDiffAges2",]$sumDen <- agrad.l2$sumBuildDiffAges
      real[real$variable == "graff2",]$sumDen <- agrad.l2$sumGraff
      real[real$variable == "ligh2",]$sumDen <- agrad.l2$sumLigh
      
      shuff <- melt(select(agrad.l2, rmovCars2, rparkCars2, rmovCicly2, rbuildId2, rbuildNRec2, rtree2, rsmallPla2, rdiffBuild2, rstreeFur2, rbasCol2, rligh2, raccenCol2, rpeop2, rgraff2, rbuildDiffAges2, image_url), id=c("image_url"))
      shuff$sd <- 0
      shuff[shuff$variable == "rmovCars2",]$sd <- agrad.l2$rsdmovCars2
      shuff[shuff$variable == "rparkCars2",]$sd <- agrad.l2$rsdparkCars2
      shuff[shuff$variable == "rmovCicly2",]$sd <- agrad.l2$rsdmovCicly2
      shuff[shuff$variable == "rbuildId2",]$sd <- agrad.l2$rsdbuildId2
      shuff[shuff$variable == "rbuildNRec2",]$sd <- agrad.l2$rsdbuildNRec2
      shuff[shuff$variable == "rtree2",]$sd <- agrad.l2$rsdtree2
      shuff[shuff$variable == "rsmallPla2",]$sd <- agrad.l2$rsdsmallPla2
      shuff[shuff$variable == "rdiffBuild2",]$sd <- agrad.l2$rsddiffBuild2
      shuff[shuff$variable == "rstreeFur2",]$sd <- agrad.l2$rsdstreeFur2
      shuff[shuff$variable == "rbasCol2",]$sd <- agrad.l2$rsdbasCol2
      shuff[shuff$variable == "raccenCol2",]$sd <- agrad.l2$rsdaccenCol2
      shuff[shuff$variable == "rpeop2",]$sd <- agrad.l2$rsdpeop2
      shuff[shuff$variable == "rbuildDiffAges2",]$sd <- agrad.l2$rsdbuildDiffAges2
      shuff[shuff$variable == "rgraff2",]$sd <- agrad.l2$rsdgraff2
      shuff[shuff$variable == "rligh2",]$sd <- agrad.l2$rsdligh2

      shuff$sumDen <- 0
      shuff[shuff$variable == "rmovCars2",]$sumDen <- agrad.l2$sumMovCars
      shuff[shuff$variable == "rparkCars2",]$sumDen <- agrad.l2$sumParkCars
      shuff[shuff$variable == "rmovCicly2",]$sumDen <- agrad.l2$sumMovCicly
      shuff[shuff$variable == "rbuildId2",]$sumDen <- agrad.l2$sumBuildId
      shuff[shuff$variable == "rbuildNRec2",]$sumDen <- agrad.l2$sumBuildNRec
      shuff[shuff$variable == "rtree2",]$sumDen <- agrad.l2$sumTree
      shuff[shuff$variable == "rsmallPla2",]$sumDen <- agrad.l2$sumSmallPla
      shuff[shuff$variable == "rdiffBuild2",]$sumDen <- agrad.l2$sumDiffBuild
      shuff[shuff$variable == "rstreeFur2",]$sumDen <- agrad.l2$sumStreeFur
      shuff[shuff$variable == "rbasCol2",]$sumDen <- agrad.l2$sumBasCol
      shuff[shuff$variable == "raccenCol2",]$sumDen <- agrad.l2$sumAccenCol
      shuff[shuff$variable == "rpeop2",]$sumDen <- agrad.l2$sumPeop
      shuff[shuff$variable == "rbuildDiffAges2",]$sumDen <- agrad.l2$sumBuildDiffAges
      shuff[shuff$variable == "rgraff2",]$sumDen <- agrad.l2$sumGraff
      shuff[shuff$variable == "rligh2",]$sumDen <- agrad.l2$sumLigh
 
      
      print("### Real")
      print("##### Summary")
      print( real %>% group_by(variable) %>% summarise( som=sum(value)/(mean(sumDen)) ) %>% arrange(desc(som)) )
      print("##### List")
      print( arrange(real, desc(value)) )
      print("### Shuffle")
      print("##### Summary")
      print( shuff %>% group_by(variable) %>% summarise( som=sum(value)/(mean(sumDen)), std=mean(sd) ) %>% arrange(desc(som)) )
      print("##### List")
      print( arrange(shuff, desc(value)) )
}

mergeSort <- function(x){
  if(length(x) == 1){
    inv <- 0
  } else {
    n <- length(x)
    n1 <- ceiling(n/2)
    n2 <- n-n1
    y1 <- mergeSort(x[1:n1])
    y2 <- mergeSort(x[n1+1:n2])
    inv <- y1$inversions + y2$inversions
    x1 <- y1$sortedVector
    x2 <- y2$sortedVector
    i1 <- 1
    i2 <- 1
    while(i1+i2 <= n1+n2+1){
      if(i2 > n2 || (i1 <= n1 && x1[i1] <= x2[i2])){
        x[i1+i2-1] <- x1[i1]
        i1 <- i1 + 1
      } else {
        inv <- inv + n1 + 1 - i1
        x[i1+i2-1] <- x2[i2]
        i2 <- i2 + 1
      }
    }
  }
  return (list(inversions=inv,sortedVector=x))
}

numberOfInversions <- function(x){
  r <- mergeSort(x)
  return (r$inversions)
}

normalizedKendallTauDistance2 <- function(data1, data2){
  x <- data1
  y <- data2
  
  tau = numberOfInversions(order(x)[rank(y)])
  nItens = length(x)
  maxNumberOfInverstions <- (nItens*(nItens-1))/2
  normalized = tau/maxNumberOfInverstions

  print (normalized)
}

print("################### Married x Single - Pleasantness")

#Casado x Solteiro
agrad.l <- agrad %>% 
    do(arrange(., desc(V3.Casado))) %>% 
    mutate(rank = 1:n()) %>% do(arrange(., desc(V3.Solteiro))) %>% mutate(index = 1:n())

agrad.l <- calcDanieleCoeff(agrad.l)
agrad.l2 <- simulateCoefShuffle(agrad.l,iterations)

print(paste(">>>> Kendall Distance ", normalizedKendallTauDistance2(agrad.l$V3.Casado, agrad.l$V3.Solteiro)))

printOutputOneListPerFeature(agrad.l2, "V3.Casado", "V3.Solteiro")
printOutputTwoListsPerFeature(agrad.l2, "V3.Casado", "V3.Solteiro")
printOutputTwoListsAllFeaturesTog(agrad.l2)

print("################### Married x Single - Safety")

#Casado x Solteiro
seg.l <- seg %>% 
    do(arrange(., desc(V3.Casado))) %>% 
    mutate(rank = 1:n()) %>% do(arrange(., desc(V3.Solteiro))) %>% mutate(index = 1:n())

seg.l <- calcDanieleCoeff(seg.l)
seg.l2 <- simulateCoefShuffle(seg.l,iterations)

print(paste(">>>> Kendall Distance ", normalizedKendallTauDistance2(seg.l$V3.Casado, seg.l$V3.Solteiro)))

printOutputOneListPerFeature(seg.l2, "V3.Casado", "V3.Solteiro")
printOutputTwoListsPerFeature(seg.l2, "V3.Casado", "V3.Solteiro")
printOutputTwoListsAllFeaturesTog(seg.l2)


