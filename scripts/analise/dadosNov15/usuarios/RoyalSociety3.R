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

    return (data)
}

randomizeCoeff <- function (data, iterations) {
    movCars <- parkCars <- movCicly <- buildId <- buildNRec <- tree <- smallPla <- diffBuild <-streeFur <- basCol <- ligh <-  accenCol <- peop <- graff <- buildDiffAges <- deb <- pav <- land <- propStreetWall <- propWind <- propSkyAhe <- propActiv <- streetW <- sidewalW <- buildHei <- c()
    
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
        
    }    
    
        #Shuffle median and sd
        data$rmovCars <- apply(movCars, 1, median)
        data$rsdmovCars <- apply(movCars, 1, sd)
        data$rparkCars <- apply(parkCars, 1, median)
        data$rsdparkCars <- apply(parkCars, 1, sd)
        data$rmovCicly <- apply(movCicly, 1, median)
        data$rsdmovCicly <- apply(movCicly, 1, sd)
        data$rbuildId <- apply(buildId, 1, median)
        data$rsdbuildId <- apply(buildId, 1, sd)
        data$rbuildNRec <- apply(buildNRec, 1, median)
        data$rsdbuildNRec <- apply(buildNRec, 1, sd)
        data$rtree <- apply(tree, 1, median)
        data$rsdtree <- apply(tree, 1, sd)
        data$rsmallPla <- apply(smallPla, 1, median)
        data$rsdsmallPla <- apply(smallPla, 1, sd)
        data$rdiffBuild <- apply(diffBuild, 1, median)
        data$rsddiffBuild <- apply(diffBuild, 1, sd)
        data$rstreeFur <- apply(streeFur, 1, median)
        data$rsdstreeFur <- apply(streeFur, 1, sd)
        data$rbasCol <- apply(basCol, 1, median)
        data$rsdbasCol <- apply(basCol, 1, sd)
        data$rligh <- apply(ligh, 1, median)
        data$rsdligh <- apply(ligh, 1, sd)
        data$raccenCol <- apply(accenCol, 1, median)
        data$rsdaccenCol <- apply(accenCol, 1, sd)
        data$rpeop <- apply(peop, 1, median)
        data$rsdpeop <- apply(peop, 1, sd)
        
        data$rgraff <- apply(graff, 1, median)
        data$rsdgraff <- apply(graff, 1, sd)
        data$rbuildDiffAges <- apply(buildDiffAges, 1, median)
        data$rsdbuildDiffAges <- apply(buildDiffAges, 1, sd)
        
    return (data)
}

iterations <- 10000

simulateCoefShuffle <- function(agrad.l, iterations){

  cmov <- cpark <- ccic <- cbuiid <- cbuiNR <- ctree <- csmalP <- cdiffB <- cfur <- cbcol <- clig <- cacol <- cgraf <- cdiffA <- cdeb <- cpav <- clan <- cwall <- cwind <- cskyA <- cskyAc <- cstreet <- cside <- cbuiH <- cpeop <- cacti <- 0
  
  agrad.l2 <- randomizeCoeff(agrad.l, iterations)

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
     print(">>>>>>>> One list - top 10 ordered by real world coef and containing real world and shuffle world data")
      print(head(arrange(select_(agrad.l2, "movCars", "rmovCars", "rsdmovCars", "image_url", column1, column2, "diff"), desc(movCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "parkCars", "rparkCars", "rsdparkCars", "image_url", column1, column2, "diff"), desc(parkCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "movCicly", "rmovCicly", "rsdmovCicly", "image_url", column1, column2, "diff"), desc(movCicly)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildId", "rbuildId", "rsdbuildId", "image_url", column1, column2, "diff"), desc(buildId)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildNRec", "rbuildNRec", "rsdbuildNRec", "image_url", column1, column2, "diff"), desc(buildNRec)), n = 10))
      print(head(arrange(select_(agrad.l2, "tree", "rtree", "rsdtree", "image_url", column1, column2, "diff"), desc(tree)), n = 10))
      print(head(arrange(select_(agrad.l2, "smallPla", "rsmallPla", "rsdsmallPla", "image_url", column1, column2, "diff"), desc(smallPla)), n = 10))
      print(head(arrange(select_(agrad.l2, "diffBuild", "rdiffBuild", "rsddiffBuild", "image_url", column1, column2, "diff"), desc(diffBuild)), n = 10))
      print(head(arrange(select_(agrad.l2, "streeFur", "rstreeFur", "rsdstreeFur", "image_url", column1, column2, "diff"), desc(streeFur)), n = 10))
      print(head(arrange(select_(agrad.l2, "basCol", "rbasCol", "rsdbasCol", "image_url", column1, column2, "diff"), desc(basCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "accenCol", "raccenCol", "rsdaccenCol", "image_url", column1, column2, "diff"), desc(accenCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "ligh", "rligh", "rsdligh", "image_url", column1, column2, "diff"), desc(ligh)), n = 10))
      print(head(arrange(select_(agrad.l2, "peop", "rpeop", "rsdpeop", "image_url", column1, column2, "diff"), desc(peop)), n = 10))
      print(head(arrange(select_(agrad.l2, "graff", "rgraff", "rsdgraff", "image_url", column1, column2, "diff"), desc(graff)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildDiffAges", "rbuildDiffAges", "rsdbuildDiffAges", "image_url", column1, column2, "diff"), desc(buildDiffAges)), n = 10))
  
}

printOutputTwoListsPerFeature <- function(agrad.l2, column1, column2){
      print(">>>>>>>> Two lists - top 10 ordered by real world coef ; top 10 ordered by shuffle world")
      print(head(arrange(select_(agrad.l2, "movCars", "image_url", column1, column2, "diff"), desc(movCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "rmovCars", "rsdmovCars", "image_url", column1, column2, "diff"), desc(rmovCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "parkCars", "image_url", column1, column2, "diff"), desc(parkCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "rparkCars", "rsdparkCars", "image_url", column1, column2, "diff"), desc(rparkCars)), n = 10))
      print(head(arrange(select_(agrad.l2, "movCicly", "image_url", column1, column2, "diff"), desc(movCicly)), n = 10))
      print(head(arrange(select_(agrad.l2, "rmovCicly", "rsdmovCicly", "image_url", column1, column2, "diff"), desc(rmovCicly)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildId", "image_url", column1, column2, "diff"), desc(buildId)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildId", "rsdbuildId", "image_url", column1, column2, "diff"), desc(rbuildId)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildNRec", "image_url", column1, column2, "diff"), desc(buildNRec)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildNRec", "rsdbuildNRec", "image_url", column1, column2, "diff"), desc(rbuildNRec)), n = 10))
      print(head(arrange(select_(agrad.l2, "tree", "image_url", column1, column2, "diff"), desc(tree)), n = 10))
      print(head(arrange(select_(agrad.l2, "rtree", "rsdtree", "image_url", column1, column2, "diff"), desc(rtree)), n = 10))
      print(head(arrange(select_(agrad.l2, "smallPla", "image_url", column1, column2, "diff"), desc(smallPla)), n = 10))
      print(head(arrange(select_(agrad.l2, "rsmallPla", "rsdsmallPla", "image_url", column1, column2, "diff"), desc(rsmallPla)), n = 10))
      print(head(arrange(select_(agrad.l2, "diffBuild", "image_url", column1, column2, "diff"), desc(diffBuild)), n = 10))
      print(head(arrange(select_(agrad.l2, "rdiffBuild", "rsddiffBuild", "image_url", column1, column2, "diff"), desc(rdiffBuild)), n = 10))
      print(head(arrange(select_(agrad.l2, "streeFur", "image_url", column1, column2, "diff"), desc(streeFur)), n = 10))
      print(head(arrange(select_(agrad.l2, "rstreeFur", "rsdstreeFur", "image_url", column1, column2, "diff"), desc(rstreeFur)), n = 10))
      print(head(arrange(select_(agrad.l2, "basCol", "image_url", column1, column2, "diff"), desc(basCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbasCol", "rsdbasCol", "image_url", column1, column2, "diff"), desc(rbasCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "accenCol", "image_url", column1, column2, "diff"), desc(accenCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "raccenCol", "rsdaccenCol", "image_url", column1, column2, "diff"), desc(raccenCol)), n = 10))
      print(head(arrange(select_(agrad.l2, "ligh", "image_url", column1, column2, "diff"), desc(ligh)), n = 10))
      print(head(arrange(select_(agrad.l2, "rligh", "rsdligh", "image_url", column1, column2, "diff"), desc(rligh)), n = 10))
      print(head(arrange(select_(agrad.l2, "peop", "image_url", column1, column2, "diff"), desc(peop)), n = 10))
      print(head(arrange(select_(agrad.l2, "rpeop", "rsdpeop", "image_url", column1, column2, "diff"), desc(rpeop)), n = 10))
      print(head(arrange(select_(agrad.l2, "graff", "image_url", column1, column2, "diff"), desc(graff)), n = 10))
      print(head(arrange(select_(agrad.l2, "rgraff", "rsdgraff", "image_url", column1, column2, "diff"), desc(rgraff)), n = 10))
      print(head(arrange(select_(agrad.l2, "buildDiffAges", "image_url", column1, column2, "diff"), desc(buildDiffAges)), n = 10))
      print(head(arrange(select_(agrad.l2, "rbuildDiffAges", "rsdbuildDiffAges", "image_url", column1, column2, "diff"), desc(rbuildDiffAges)), n = 10))
  
}

printOutputTwoListsForAll <- function(agrad.l2){
      print(">>>>>>>> Two lists with all features together - top 10 ordered by real world coef ; top 10 ordered by shuffle world")
      library(reshape)
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
      
      print(">>>>>> Real")
      print( arrange(real, desc(value)) )
      print(">>>>>> Shuffle")
      print( arrange(shuff, desc(value)) )
}

print("################### Married x Single - Pleasantness")

#Casado x Solteiro
agrad.l <- agrad %>% 
    do(arrange(., desc(V3.Casado))) %>% 
    mutate(rank = 1:n()) %>% do(arrange(., desc(V3.Solteiro))) %>% mutate(index = 1:n())

agrad.l <- calcDanieleCoeff(agrad.l)
agrad.l2 <- simulateCoefShuffle(agrad.l,iterations)

printOutputOneListPerFeature(agrad.l2, "V3.Casado", "V3.Solteiro")
printOutputTwoListsPerFeature(agrad.l2, "V3.Casado", "V3.Solteiro")
printOutputTwoListsForAll(agrad.l2)

print("################### Married x Single - Safety")

#Casado x Solteiro
seg.l <- seg %>% 
    do(arrange(., desc(V3.Casado))) %>% 
    mutate(rank = 1:n()) %>% do(arrange(., desc(V3.Solteiro))) %>% mutate(index = 1:n())

seg.l <- calcDanieleCoeff(seg.l)
seg.l2 <- simulateCoefShuffle(seg.l,iterations)

printOutputOneListPerFeature(seg.l2, "V3.Casado", "V3.Solteiro")
printOutputTwoListsPerFeature(seg.l2, "V3.Casado", "V3.Solteiro")
printOutputTwoListsForAll(seg.l2)

