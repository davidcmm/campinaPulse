#!/bin/Rscript

#Reading data
library(ggplot2)
library(gridExtra)
library(dplyr)
library(reshape)
source('analisaICPorFoto.R')
source('convertKendallSummary.R')

facet_names <- list(
  'agrad%C3%A1vel?'="Pleasantness",
  'seguro?'="Safety"
)

facet_labeller <- function(variable,value){
  return(facet_names[value])
}

#dados <- read.table("geral.dat", header=TRUE)
dados <- read.table("geralSetoresAJ.dat", header=TRUE)

#Intervalo de confiança por ponto
temp1 <- dados
qscoreSim <- temp1 [ c(4:103) ]
icData <- apply(qscoreSim, 1, ic)
temp1$distance <- icData

#Subset of columns
dadosSub <- temp1[, c("V2", "V1", "V3", "diag", "hor", "vert", "red", "green", "blue", "grupo", "bairro", "distance", "setor")]

novosDados <- reshape(dadosSub, timevar="grupo", idvar=c("V2", "V1", "diag", "hor", "vert", "red", "green", "blue", "bairro", "setor"), direction="wide")

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

#Summing features values  - left and right
somaValores <- function(dados1, dados2, desvio1, desvio2, uplimit){
    dados1[is.na(dados1)] <- 0
    dados2[is.na(dados2)] <- 0
    
    soma = dados1 + dados2
    desvios = (desvio1 + desvio2)/2
    
    desvio = sd(soma)
#     if (is.na(desvio)){ 
#         valores = rnorm(mean = mean(soma, na.rm = TRUE), sd = mean(desvios, na.rm = TRUE), n = 3)
#         valores <- ifelse(valores < 0, 0, valores)
#         valores <- ifelse(valores > uplimit, uplimit, valores)
#         return (mean(valores))
#     }else{
        soma <- ifelse(soma < 0, 0, soma)
        soma <- ifelse(soma > uplimit, uplimit, soma)
        return (mean(soma))
#     }
  #return (mean(soma))
}

#Mean of features values - left and right
mediaValores <- function(dados1, dados2, desvio1, desvio2, uplimit){
   for (i in 1:length(dados1)){
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
#     if (is.na(desvio)){ 
#         valores = rnorm(mean = mean(soma, na.rm = TRUE), sd = mean(desvios, na.rm = TRUE), n = 3)
#         valores <- ifelse(valores < 0, 0, valores)
#         valores <- ifelse(valores > uplimit, uplimit, valores)
#         return (mean(valores))
#     }else{
        soma <- ifelse(soma < 0, 0, soma)
        soma <- ifelse(soma > uplimit, uplimit, soma)
        return (mean(soma))
#     }
#   return(mean(soma))
}


#Creating values for the cases where only 1 answer was obtained considering the desviations of other features answers
geraValores <- function(lista, question, desvios, uplimit){
   #desvio = sd(lista)
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

#agrad <- filter(temp, V1 == "agrad%C3%A1vel?")
agrad <- filter(temp, V1 == "agradavel?")
seg <- filter(temp, V1 == "seguro?")

#Kendall adaptation to consider weights as the difference in amount of features between images. Using all Qscores computed for each group
kendallWithWeightsSimReal <- function(data, iterations, group1Id, group2Id, question, temp, sector){
	
    data$graffiti <- as.character(data$graffiti)
    data$graffiti[data$graffiti == "No"] <- 0
    data$graffiti[data$graffiti == "Yes"] <- 1
    data$build_diff_ages <- as.character(data$build_diff_ages)
    data$build_diff_ages[data$build_diff_ages == "No"] <- 0
    data$build_diff_ages[data$build_diff_ages == "yes"] <- 1

    if (length(sector) > 1){
	temp <- filter(temp, setor == sector)
    }
    simData1 <- unique(arrange(filter(temp, grupo == group1Id & V1 == question)[ c(1, 4:104) ], V2))
    simData2 <- unique(arrange(filter(temp, grupo == group2Id & V1 == question)[ c(1, 4:104) ], V2))

    #Amount of images
    amountOfItems <- nrow(data)

    featuresMapG1 <- list(movCars = list(c()) , parkCars = list(c()), movCicly= list(c()), buildId = list(c()), buildNRec = list(c()), tree = list(c()), smallPla = list(c()), diffBuild = list(c()), streeFur = list(c()), basCol = list(c()), ligh = list(c()), accenCol = list(c()), peop = list(c()), graff = list(c()), buildDiffAges = list(c()), streetWid = list(c()), sidewalkWid = list(c()), debris = list(c()), pavement = list(c()), landscape = list(c()), propStreetWall = list(c()), propWind = list(c()), longSight = list(c()), propSkyAhead = list(c()), propSkyAcross = list(c()), buildHeight = list(c()), propActiveUse = list(c()), movCarsN = list(c()) , parkCarsN = list(c()), movCiclyN= list(c()), buildIdN = list(c()), buildNRecN = list(c()), treeN = list(c()), smallPlaN = list(c()), diffBuildN = list(c()), streeFurN = list(c()), basColN = list(c()), lighN = list(c()), accenColN = list(c()), peopN = list(c()), graffN = list(c()), buildDiffAgesN = list(c()), streetWidN = list(c()), sidewalkWidN = list(c()), debrisN = list(c()), pavementN = list(c()), landscapeN = list(c()), propStreetWallN = list(c()), propWindN = list(c()), longSightN = list(c()), propSkyAheadN = list(c()), propSkyAcrossN = list(c()), buildHeightN = list(c()), propActiveUseN = list(c()))

     movCarsMaxAllVal <- parkCarsMaxAllVal <- movCiclyMaxAllVal <- buildIdMaxAllVal <- buildNRecMaxAllVal <- treeMaxAllVal <- smallPlaMaxAllVal <- diffBuildMaxAllVal <- streeFurMaxAllVal <- basColMaxAllVal <- lighMaxAllVal <- accenColMaxAllVal <- peopMaxAllVal <- graffMaxAllVal <- buildDiffAgesMaxAllVal <- streetWidMaxAllVal <- sidewalkWidMaxAllVal <- buildHeightMaxAllVal <- longSightMaxAllVal <- c()
    debrisMaxAllVal <- pavementMaxAllVal <- landscapeMaxAllVal <- propStreetWallMaxAllVal <- propWindMaxAllVal <- propSkyAheadMaxAllVal <- propSkyAcrossMaxAllVal <- propActiveUseMaxAllVal <- c()

    for (ind in seq(2, 101)) {
		
	#Original data
	groupCompleteId1 <- paste("V3.", group1Id, sep="")
	groupCompleteId2 <- paste("V3.", group2Id, sep="")
        data <- data %>% do(arrange(., image_url)) 
	data[[groupCompleteId1]] <- as.vector(simData1[,ind])
	data[[groupCompleteId2]] <- as.vector(simData2[,ind])

	sortedData <- data %>% do(arrange(., desc(V3.Masculino))) %>% 
    mutate(rank = 1:n()) %>% do(arrange(., desc(V3.Feminino))) %>% mutate(index = 1:n())
    	data <- arrange(sortedData, rank)
    
	    movCarsOrig <- data[["mov_cars"]]
	    parkCarsOrig <- data[["park_cars"]]
	    movCiclyOrig <- data[["mov_ciclyst"]]
	    buildIdOrig <- data[["build_ident"]] 
	    buildNRecOrig <- data[["build_nrectan"]]
	    treeOrig <- data[["trees"]]
	    smallPlaOrig <- data[["small_planters"]]
	    diffBuildOrig <-data[["diff_build"]]
	    streeFurOrig <- data[["street_furnit"]]
	    basColOrig <- data[["basic_col"]]
	    lighOrig <- data[["lights"]]
	    accenColOrig <-  data[["accent_col"]]
	    peopOrig <- data[["people"]]
	    graffOrig <- data[["graffiti"]]
	    buildDiffAgesOrig <- data[["build_diff_ages"]]
	    streetWidOrig <- data[["street_wid"]]
	    sidewalkWidOrig <- data[["sidewalk_wid"]]
	    buildHeightOrig <- data[["build_height"]]
	    longSightOrig <- data[["long_sight"]]
	    debrisOrig <- data[["debris"]]
	    pavementOrig <- data[["pavement"]]
	    landscapeOrig <- data[["landscape"]]
	    propStreetWallOrig <- data[["prop_street_wall"]]
	    propWindOrig <- data[["prop_wind"]]
	    propSkyAheadOrig <- data[["prop_sky_ahead"]]
	    propSkyAcrossOrig <- data[["prop_sky_across"]]  
	    propActiveUseOrig <- data[["prop_active_use"]]

	    movCars <- parkCars <- movCicly<- buildId <- buildNRec <- tree <- smallPla <- diffBuild <- streeFur <- basCol <- ligh <- accenCol<- peop <- graff <- buildDiffAges <- streetWid <- sidewalkWid <- buildHeight <- longSight <- 0
	    debris <- pavement <- landscape <- propStreetWall <- propWind <- propSkyAhead <- propSkyAcross <-  propActiveUse <- c()
	    
		movCarsMax <- parkCarsMax <- movCiclyMax <- buildIdMax <- buildNRecMax <- treeMax <- smallPlaMax <- diffBuildMax <- streeFurMax <- basColMax <- lighMax <- accenColMax <- peopMax <- graffMax <- buildDiffAgesMax <- streetWidMax <- sidewalkWidMax <- buildHeightMax <- longSightMax <- 0
	    debrisMax <- pavementMax <- landscapeMax <- propStreetWallMax <- propWindMax <- propSkyAheadMax <- propSkyAcrossMax <- propActiveUseMax <- c()

	    #First call, comparing for group 1
	    for( i in seq(1, amountOfItems) ){
		rankLine1 <- data[i,]
		
		if(i+1 <= amountOfItems){
		  
		    for( j in seq(i+1, amountOfItems) ){
		        rankLine2 <- data[j,]
		        
		        if( (rankLine1[["rank"]] < rankLine2[["rank"]]) & (rankLine1[["index"]] > rankLine2[["index"]]) ){
		            #discordantPairs[[length(discordantPairs) + 1]] <- c(i,j)

		            movCars <- movCars + movCarsOrig[i] - movCarsOrig[j]
		            parkCars <- parkCars + parkCarsOrig[i] - parkCarsOrig[j]
		            movCicly <- movCicly + movCiclyOrig[i] - movCiclyOrig[j]
		            buildId <- buildId + buildIdOrig[i] - buildIdOrig[j]
		            buildNRec <- buildNRec + buildNRecOrig[i] - buildNRecOrig[j]
		            tree <- tree + treeOrig[i] - treeOrig[j]
		            smallPla <- smallPla + smallPlaOrig[i] - smallPlaOrig[j]
		            diffBuild <- diffBuild + diffBuildOrig[i] - diffBuildOrig[j]
		            streeFur <- streeFur + streeFurOrig[i] - streeFurOrig[j]
		            basCol <- basCol + basColOrig[i] - basColOrig[j]
		            ligh <- ligh + lighOrig[i] - lighOrig[j]
		            accenCol <- accenCol + accenColOrig[i] - accenColOrig[j]
		            peop <- peop + peopOrig[i] - peopOrig[j]
		            graff <- graff + as.integer(graffOrig[i]) - as.integer(graffOrig[j])
		            buildDiffAges <- buildDiffAges + as.integer(buildDiffAgesOrig[i]) - as.integer(buildDiffAgesOrig[j])
		            
		            streetWid <- streetWid + as.double(streetWidOrig[i]) - as.double(streetWidOrig[j])
		            sidewalkWid <- sidewalkWid + as.double(sidewalkWidOrig[i]) - as.double(sidewalkWidOrig[j])
		            debris <- cbind(debris, as.double(debrisOrig[i]) - as.double(debrisOrig[j]))
		            pavement <- cbind(pavement, as.double(pavementOrig[i]) - as.double(pavementOrig[j])) 
		            landscape <- cbind(landscape, as.double(landscapeOrig[i]) - as.double(landscapeOrig[j]))
		            propStreetWall <- cbind(propStreetWall, as.double(propStreetWallOrig[i]) - as.double(propStreetWallOrig[j]))
		            propWind <- cbind(propWind, as.double(propWindOrig[i]) - as.double(propWindOrig[j]))
		            longSight <- longSight + as.double(longSightOrig[i]) - as.double(longSightOrig[j])
		            propSkyAhead <- cbind(propSkyAhead, as.double(propSkyAheadOrig[i]) - as.double(propSkyAheadOrig[j]))
		            propSkyAcross <- cbind(propSkyAcross, as.double(propSkyAcrossOrig[i]) - as.double(propSkyAcrossOrig[j]))  
		            buildHeight <- buildHeight + as.double(buildHeightOrig[i]) - as.double(buildHeightOrig[j])
		            propActiveUse <- cbind(propActiveUse, as.double(propActiveUseOrig[i]) - as.double(propActiveUseOrig[j]))
		        }  
		        
		        #Accounting differences for max!
		        movCarsMax <- movCarsMax + abs(movCarsOrig[i] - movCarsOrig[j])
		        parkCarsMax <- parkCarsMax + abs(parkCarsOrig[i] - parkCarsOrig[j])
		        movCiclyMax <- movCiclyMax + abs(movCiclyOrig[i] - movCiclyOrig[j])
		        buildIdMax <- buildIdMax + abs(buildIdOrig[i] - buildIdOrig[j])
		        buildNRecMax <- buildNRecMax + abs(buildNRecOrig[i] - buildNRecOrig[j])
		        treeMax <- treeMax + abs(treeOrig[i] - treeOrig[j])
		        smallPlaMax <- smallPlaMax + abs(smallPlaOrig[i] - smallPlaOrig[j])
		        diffBuildMax <- diffBuildMax + abs(diffBuildOrig[i] - diffBuildOrig[j])
		        streeFurMax <- streeFurMax + abs(streeFurOrig[i] - streeFurOrig[j])
		        basColMax <- basColMax + abs(basColOrig[i] - basColOrig[j])
		        lighMax <- lighMax + abs(lighOrig[i] - lighOrig[j])
		        accenColMax <- accenColMax + abs(accenColOrig[i] - accenColOrig[j])
		        peopMax <- peopMax + abs(peopOrig[i] - peopOrig[j])
		        graffMax <- graffMax + abs(as.integer(graffOrig[i]) - as.integer(graffOrig[j]))
		        buildDiffAgesMax <- buildDiffAgesMax + abs(as.integer(buildDiffAgesOrig[i]) - as.integer(buildDiffAgesOrig[j]))
		        
		        streetWidMax <- streetWidMax + abs(as.double(streetWidOrig[i]) - as.double(streetWidOrig[j]))
		        sidewalkWidMax <- sidewalkWidMax + abs(as.double(sidewalkWidOrig[i]) - as.double(sidewalkWidOrig[j]))
		        debrisMax <- cbind(debrisMax, abs(as.double(debrisOrig[i]) - as.double(debrisOrig[j])))
		        pavementMax <- cbind(pavementMax, abs(as.double(pavementOrig[i]) - as.double(pavementOrig[j]))) 
		        landscapeMax <- cbind(landscapeMax, abs(as.double(landscapeOrig[i]) - as.double(landscapeOrig[j])))
		        propStreetWallMax <- cbind(propStreetWallMax, abs(as.double(propStreetWallOrig[i]) - as.double(propStreetWallOrig[j])))
		        propWindMax <- cbind(propWindMax, abs(as.double(propWindOrig[i]) - as.double(propWindOrig[j])))
		        longSightMax <- longSightMax + abs(as.double(longSightOrig[i]) - as.double(longSightOrig[j]))
		        propSkyAheadMax <- cbind(propSkyAheadMax, abs(as.double(propSkyAheadOrig[i]) - as.double(propSkyAheadOrig[j])))
		        propSkyAcrossMax <- cbind(propSkyAcrossMax, abs(as.double(propSkyAcrossOrig[i]) - as.double(propSkyAcrossOrig[j]))) 
		        buildHeightMax <- buildHeightMax + abs(as.double(buildHeightOrig[i]) - as.double(buildHeightOrig[j]))
		        propActiveUseMax <- cbind(propActiveUseMax, abs(as.double(propActiveUseOrig[i]) - as.double(propActiveUseOrig[j])))

		    }
		}
	    }

	    #Real world mean values for grades and proportions
	    if( length(debris) > 0 ){
	      featuresMapG1$movCars[[1]] <- c(featuresMapG1$movCars[[1]], movCars)
	      featuresMapG1$parkCars[[1]] <- c(featuresMapG1$parkCars[[1]], parkCars)
	      featuresMapG1$movCicly[[1]] <- c(featuresMapG1$movCicly[[1]], movCicly)
	      featuresMapG1$buildId[[1]] <- c(featuresMapG1$buildId[[1]], buildId)
	      featuresMapG1$buildNRec[[1]] <- c(featuresMapG1$buildNRec[[1]], buildNRec)
	      featuresMapG1$tree[[1]] <- c(featuresMapG1$tree[[1]], tree)
	      featuresMapG1$smallPla[[1]] <- c(featuresMapG1$smallPla[[1]], smallPla)
	      featuresMapG1$diffBuild[[1]] <- c(featuresMapG1$diffBuild[[1]], diffBuild)
	      featuresMapG1$streeFur[[1]] <- c(featuresMapG1$streeFur[[1]], streeFur)
	      featuresMapG1$basCol[[1]] <- c(featuresMapG1$basCol[[1]], basCol)
	      featuresMapG1$ligh[[1]] <- c(featuresMapG1$ligh[[1]], ligh)
	      featuresMapG1$accenCol[[1]] <- c(featuresMapG1$accenCol[[1]], accenCol)
	      featuresMapG1$peop[[1]] <- c(featuresMapG1$peop[[1]], peop)
	      featuresMapG1$graff[[1]] <- c(featuresMapG1$graff[[1]], graff)
	      featuresMapG1$buildDiffAges[[1]] <- c(featuresMapG1$buildDiffAges[[1]], buildDiffAges)
	      featuresMapG1$streetWid[[1]] <- c(featuresMapG1$streetWid[[1]], streetWid)
	      featuresMapG1$sidewalkWid[[1]] <- c(featuresMapG1$sidewalkWid[[1]], sidewalkWid)
	      featuresMapG1$buildHeight[[1]] <- c(featuresMapG1$buildHeight[[1]], buildHeight)
	      featuresMapG1$longSight[[1]] <- c(featuresMapG1$longSight[[1]], longSight)
	      
	      featuresMapG1$debris[[1]] <- c(featuresMapG1$debris[[1]], .Internal(mean(debris)))
	      featuresMapG1$pavement[[1]] <- c(featuresMapG1$pavement[[1]], .Internal(mean(pavement)))
	      featuresMapG1$landscape[[1]] <- c(featuresMapG1$landscape[[1]], .Internal(mean(landscape)))
	      featuresMapG1$propStreetWall[[1]] <- c(featuresMapG1$propStreetWall[[1]], .Internal(mean(propStreetWall)))
	      featuresMapG1$propWind[[1]] <- c(featuresMapG1$propWind[[1]], .Internal(mean(propWind)))
	      featuresMapG1$propSkyAhead[[1]] <- c(featuresMapG1$propSkyAhead[[1]], .Internal(mean(propSkyAhead)))
	      featuresMapG1$propSkyAcross[[1]] <- c(featuresMapG1$propSkyAcross[[1]], .Internal(mean(propSkyAcross)))
	      featuresMapG1$propActiveUse[[1]] <- c(featuresMapG1$propActiveUse[[1]], .Internal(mean(propActiveUse)))
	    }
	
	    #Saving all max values
	    movCarsMaxAllVal <- c(movCarsMaxAllVal, movCarsMax)
	    parkCarsMaxAllVal <- c(parkCarsMaxAllVal, parkCarsMax)
	    movCiclyMaxAllVal <- c(movCiclyMaxAllVal, movCiclyMax)
	    buildIdMaxAllVal <- c(buildIdMaxAllVal, buildIdMax)
	    buildNRecMaxAllVal <- c(buildNRecMaxAllVal, buildNRecMax)
	    treeMaxAllVal <- c(treeMaxAllVal, treeMax)
	    smallPlaMaxAllVal <- c(smallPlaMaxAllVal, smallPlaMax)
	    diffBuildMaxAllVal <- c(diffBuildMaxAllVal, diffBuildMax)
	    streeFurMaxAllVal <- c(streeFurMaxAllVal, streeFurMax)
	    basColMaxAllVal <- c(basColMaxAllVal, basColMax)
	    lighMaxAllVal <- c(lighMaxAllVal, lighMax)
            accenColMaxAllVal <- c(accenColMaxAllVal, accenColMax)
	    peopMaxAllVal <- c(peopMaxAllVal, peopMax)
	    graffMaxAllVal <- c(graffMaxAllVal, graffMax)
	    buildDiffAgesMaxAllVal <- c(buildDiffAgesMaxAllVal, buildDiffAgesMax)
	    streetWidMaxAllVal <- c(streetWidMaxAllVal, streetWidMax)
	    sidewalkWidMaxAllVal <- c(sidewalkWidMaxAllVal, sidewalkWidMax)
	    buildHeightMaxAllVal <- c(buildHeightMaxAllVal, buildHeightMax)
	    longSightMaxAllVal <- c(longSightMaxAllVal, longSightMax)
	    debrisMaxAllVal <- c(debrisMaxAllVal, .Internal(mean(debrisMax)))
	    pavementMaxAllVal <- c(pavementMaxAllVal, .Internal(mean(pavementMax)))
	    landscapeMaxAllVal <- c(landscapeMaxAllVal, .Internal(mean(landscapeMax)))
	    propStreetWallMaxAllVal <- c(propStreetWallMaxAllVal, .Internal(mean(propStreetWallMax)))
	    propWindMaxAllVal <- c(propWindMaxAllVal, .Internal(mean(propWindMax)))
	    propSkyAheadMaxAllVal <- c(propSkyAheadMaxAllVal, .Internal(mean(propSkyAheadMax)))
	    propSkyAcrossMaxAllVal <- c(propSkyAcrossMaxAllVal, .Internal(mean(propSkyAcrossMax)))
	    propActiveUseMaxAllVal <- c(propActiveUseMaxAllVal, .Internal(mean(propActiveUseMax)))
   }

   #Normalizing real values
    featuresMapG1$movCarsN[[1]] <- mean(movCarsMaxAllVal)#(maxMovCars*den)
    featuresMapG1$parkCarsN[[1]] <-  mean(parkCarsMaxAllVal)#(maxParkCars*den)
    featuresMapG1$movCiclyN[[1]] <-   mean(movCiclyMaxAllVal)#(maxMovCicly*den)
    featuresMapG1$buildIdN[[1]] <-  mean(buildIdMaxAllVal)#(maxBuildId*den)
    featuresMapG1$buildNRecN[[1]] <-  mean(buildNRecMaxAllVal)#(maxBuildNRec*den)
    featuresMapG1$treeN[[1]] <-  mean(treeMaxAllVal)#(maxTree*den)
    featuresMapG1$smallPlaN[[1]] <-  mean(smallPlaMaxAllVal)#(maxSmallPla*den)
    featuresMapG1$diffBuildN[[1]] <-  mean(diffBuildMaxAllVal)#(maxDiffBuild*den)
    featuresMapG1$streeFurN[[1]] <-  mean(streeFurMaxAllVal)#(maxStreeFur*den)
    featuresMapG1$basColN[[1]] <-  mean(basColMaxAllVal)#(maxBasCol*den)
    featuresMapG1$lighN[[1]] <-  mean(lighMaxAllVal)#(maxLigh*den)
    featuresMapG1$accenColN[[1]] <-  mean(accenColMaxAllVal)#(maxAccenCol*den)
    featuresMapG1$peopN[[1]] <-  mean(peopMaxAllVal)#(maxPeop*den)
    featuresMapG1$graffN[[1]] <-  mean(graffMaxAllVal)#(maxGraff*den)
    featuresMapG1$buildDiffAgesN[[1]] <- mean( buildDiffAgesMaxAllVal)#(maxBuildDiffAges*den)
    featuresMapG1$streetWidN[[1]] <-  mean(streetWidMaxAllVal)
    featuresMapG1$sidewalkWidN[[1]] <- mean(sidewalkWidMaxAllVal)
    featuresMapG1$debrisN[[1]] <-  mean(debrisMaxAllVal)
    featuresMapG1$pavementN[[1]] <-  mean(pavementMaxAllVal)
    featuresMapG1$landscapeN[[1]] <- mean(landscapeMaxAllVal)
    featuresMapG1$propStreetWallN[[1]] <-  mean(propStreetWallMaxAllVal)
    featuresMapG1$propWindN[[1]] <-  mean(propWindMaxAllVal)
    featuresMapG1$longSightN[[1]] <-  mean(longSightMaxAllVal)
    featuresMapG1$propSkyAheadN[[1]] <-  mean(propSkyAheadMaxAllVal)
    featuresMapG1$propSkyAcrossN[[1]] <-  mean(propSkyAcrossMaxAllVal)
    featuresMapG1$buildHeightN[[1]] <-  mean(buildHeightMaxAllVal)
    featuresMapG1$propActiveUseN[[1]] <-  mean(propActiveUseMaxAllVal)

	return ( featuresMapG1 )
}

kendallWithWeights <- function(data, iterations, group1Id, group2Id, question, sector){
    
    data$graffiti <- as.character(data$graffiti)
    data$graffiti[data$graffiti == "No"] <- 0
    data$graffiti[data$graffiti == "Yes"] <- 1
    data$build_diff_ages <- as.character(data$build_diff_ages)
    data$build_diff_ages[data$build_diff_ages == "No"] <- 0
    data$build_diff_ages[data$build_diff_ages == "yes"] <- 1
  
    #Amount of images
    amountOfItems <- nrow(data)

    #Maximum comparisons - worst scenario possible between these two groups!
    #data$index2 <- seq(amountOfItems, 1)#Fake index, completely opposite rank!
    
    #Improve? http://stackoverflow.com/questions/6269526/r-applying-a-function-to-all-row-pairs-of-a-matrix-without-for-loop
    featuresMapG1 <- data.frame(movCars = 0 , parkCars = 0, movCicly= 0, buildId = 0, buildNRec = 0, tree = 0, smallPla = 0, diffBuild = 0, streeFur = 0, basCol = 0, ligh = 0, accenCol = 0, peop = 0, graff = 0, buildDiffAges = 0, streetWid = 0, sidewalkWid = 0, debris = 0, pavement = 0, landscape = 0, propStreetWall = 0, propWind = 0, longSight = 0, propSkyAhead = 0, propSkyAcross = 0, buildHeight = 0, propActiveUse = 0, rmovCars = 0, rparkCars = 0, rmovCicly = 0, rbuildId = 0, rbuildNRec = 0, rtree = 0, rsmallPla = 0, rdiffBuild = 0, rstreeFur = 0, rbasCol = 0, rligh = 0, raccenCol = 0, rpeop = 0, rgraff = 0, rbuildDiffAges = 0, rstreetWid = 0, rsidewalkWid = 0, rdebris = 0, rpavement = 0, rlandscape = 0, rpropStreetWall = 0, rpropWind = 0, rlongSight = 0, rpropSkyAhead = 0, rpropSkyAcross = 0, rbuildHeight = 0, rpropActiveUse = 0, rsdMovCars = 0, rsdParkCars = 0, rsdMovCicly = 0, rsdBuildId = 0, rsdBuildNRec = 0, rsdTree = 0, rsdSmallPla = 0, rsdDiffBuild = 0, rsdStreeFur = 0, rsdBasCol = 0, rsdLigh = 0, rsdAccenCol = 0, rsdPeop = 0, rsdGraff = 0, rsdBuildDiffAges = 0, rsdStreetWid = 0, rsdSidewalkWid = 0, rsdDebris = 0, rsdPavement = 0, rsdLandscape = 0, rsdPropStreetWall = 0, rsdPropWind = 0, rsdLongSight = 0, rsdPropSkyAhead = 0, rsdPropSkyAcross = 0, rsdBuildHeight = 0, rsdPropActiveUse = 0, movCarsN = 0 , parkCarsN = 0, movCiclyN= 0, buildIdN = 0, buildNRecN = 0, treeN = 0, smallPlaN = 0, diffBuildN = 0, streeFurN = 0, basColN = 0, lighN = 0, accenColN = 0, peopN = 0, graffN = 0, buildDiffAgesN = 0, streetWidN = 0, sidewalkWidN = 0, debrisN = 0, pavementN = 0, landscapeN = 0, propStreetWallN = 0, propWindN = 0, longSightN = 0, propSkyAheadN = 0, propSkyAcrossN = 0, buildHeightN = 0, propActiveUseN = 0,  rmovCarsN = 0 , rparkCarsN = 0, rmovCiclyN= 0, rbuildIdN = 0, rbuildNRecN = 0, rtreeN = 0, rsmallPlaN = 0, rdiffBuildN = 0, rstreeFurN = 0, rbasColN = 0, rlighN = 0, raccenColN = 0, rpeopN = 0, rgraffN = 0, rbuildDiffAgesN = 0, rstreetWidN = 0, rsidewalkWidN = 0, rdebrisN = 0, rpavementN = 0, rlandscapeN = 0, rpropStreetWallN = 0, rpropWindN = 0, rlongSightN = 0, rpropSkyAheadN = 0, rpropSkyAcrossN = 0, rbuildHeightN = 0, rpropActiveUseN = 0)

	#Original data
    data <- arrange(data, rank)
    
    movCarsOrig <- data[["mov_cars"]]
    parkCarsOrig <- data[["park_cars"]]
    movCiclyOrig <- data[["mov_ciclyst"]]
    buildIdOrig <- data[["build_ident"]] 
    buildNRecOrig <- data[["build_nrectan"]]
    treeOrig <- data[["trees"]]
    smallPlaOrig <- data[["small_planters"]]
    diffBuildOrig <-data[["diff_build"]]
    streeFurOrig <- data[["street_furnit"]]
    basColOrig <- data[["basic_col"]]
    lighOrig <- data[["lights"]]
    accenColOrig <-  data[["accent_col"]]
    peopOrig <- data[["people"]]
    graffOrig <- data[["graffiti"]]
    buildDiffAgesOrig <- data[["build_diff_ages"]]
    streetWidOrig <- data[["street_wid"]]
    sidewalkWidOrig <- data[["sidewalk_wid"]]
    buildHeightOrig <- data[["build_height"]]
    longSightOrig <- data[["long_sight"]]
    debrisOrig <- data[["debris"]]
    pavementOrig <- data[["pavement"]]
    landscapeOrig <- data[["landscape"]]
    propStreetWallOrig <- data[["prop_street_wall"]]
    propWindOrig <- data[["prop_wind"]]
    propSkyAheadOrig <- data[["prop_sky_ahead"]]
    propSkyAcrossOrig <- data[["prop_sky_across"]]  
    propActiveUseOrig <- data[["prop_active_use"]]

    movCars <- parkCars <- movCicly<- buildId <- buildNRec <- tree <- smallPla <- diffBuild <- streeFur <- basCol <- ligh <- accenCol<- peop <- graff <- buildDiffAges <- streetWid <- sidewalkWid <- buildHeight <- longSight <- 0
    debris <- pavement <- landscape <- propStreetWall <- propWind <- propSkyAhead <- propSkyAcross <-  propActiveUse <- c()
    movCarsMax <- parkCarsMax <- movCiclyMax <- buildIdMax <- buildNRecMax <- treeMax <- smallPlaMax <- diffBuildMax <- streeFurMax <- basColMax <- lighMax <- accenColMax <- peopMax <- graffMax <- buildDiffAgesMax <- streetWidMax <- sidewalkWidMax <- buildHeightMax <- longSightMax <- 0
    debrisMax <- pavementMax <- landscapeMax <- propStreetWallMax <- propWindMax <- propSkyAheadMax <- propSkyAcrossMax <- propActiveUseMax <- c()

    mcaT <- new.env()
    pcaT <- new.env()
    mciT <- new.env()
    bidT <- new.env()
    bnrT <- new.env()
    treT <- new.env()
    splT <- new.env()
    dbuT <- new.env()
    sfuT <- new.env()
    bacT <- new.env()
    ligT <- new.env()
    accT <- new.env()
    peoT <- new.env()
    graT <- new.env()
    bdaT <- new.env()
    swiT <- new.env()
    siwiT <- new.env()
    bheT <- new.env()
    lsiT <- new.env()
    debT <- new.env()
    pavT <- new.env()
    lanT <- new.env()
    pswT <- new.env()
    pwiT <- new.env()
    psaT <- new.env()
    psacT <- new.env()
    pactT <- new.env()
    
    #discordantPairs <- list()#Store discordant pairs in order to avoid check and comparisons multiple times!

    #First call, comparing for group 1
    for( i in seq(1, amountOfItems) ){
        rankLine1 <- data[i,]
        
        if(i+1 <= amountOfItems){
          
            for( j in seq(i+1, amountOfItems) ){
                rankLine2 <- data[j,]
                
                if( (rankLine1[["rank"]] < rankLine2[["rank"]]) & (rankLine1[["index"]] > rankLine2[["index"]]) ){
                    #discordantPairs[[length(discordantPairs) + 1]] <- c(i,j)

                    movCars <- movCars + movCarsOrig[i] - movCarsOrig[j]
                    parkCars <- parkCars + parkCarsOrig[i] - parkCarsOrig[j]
                    movCicly <- movCicly + movCiclyOrig[i] - movCiclyOrig[j]
                    buildId <- buildId + buildIdOrig[i] - buildIdOrig[j]
                    buildNRec <- buildNRec + buildNRecOrig[i] - buildNRecOrig[j]
                    tree <- tree + treeOrig[i] - treeOrig[j]
                    smallPla <- smallPla + smallPlaOrig[i] - smallPlaOrig[j]
                    diffBuild <- diffBuild + diffBuildOrig[i] - diffBuildOrig[j]
                    streeFur <- streeFur + streeFurOrig[i] - streeFurOrig[j]
                    basCol <- basCol + basColOrig[i] - basColOrig[j]
                    ligh <- ligh + lighOrig[i] - lighOrig[j]
                    accenCol <- accenCol + accenColOrig[i] - accenColOrig[j]
                    peop <- peop + peopOrig[i] - peopOrig[j]
                    graff <- graff + as.integer(graffOrig[i]) - as.integer(graffOrig[j])
                    buildDiffAges <- buildDiffAges + as.integer(buildDiffAgesOrig[i]) - as.integer(buildDiffAgesOrig[j])
                    
                    streetWid <- streetWid + as.double(streetWidOrig[i]) - as.double(streetWidOrig[j])
                    sidewalkWid <- sidewalkWid + as.double(sidewalkWidOrig[i]) - as.double(sidewalkWidOrig[j])
                    debris <- cbind(debris, as.double(debrisOrig[i]) - as.double(debrisOrig[j]))
                    pavement <- cbind(pavement, as.double(pavementOrig[i]) - as.double(pavementOrig[j])) 
                    landscape <- cbind(landscape, as.double(landscapeOrig[i]) - as.double(landscapeOrig[j]))
                    propStreetWall <- cbind(propStreetWall, as.double(propStreetWallOrig[i]) - as.double(propStreetWallOrig[j]))
                    propWind <- cbind(propWind, as.double(propWindOrig[i]) - as.double(propWindOrig[j]))
                    longSight <- longSight + as.double(longSightOrig[i]) - as.double(longSightOrig[j])
                    propSkyAhead <- cbind(propSkyAhead, as.double(propSkyAheadOrig[i]) - as.double(propSkyAheadOrig[j]))
                    propSkyAcross <- cbind(propSkyAcross, as.double(propSkyAcrossOrig[i]) - as.double(propSkyAcrossOrig[j]))  
                    buildHeight <- buildHeight + as.double(buildHeightOrig[i]) - as.double(buildHeightOrig[j])
                    propActiveUse <- cbind(propActiveUse, as.double(propActiveUseOrig[i]) - as.double(propActiveUseOrig[j]))
                }  
                
                #Accounting differences for max!
                movCarsMax <- movCarsMax + abs(movCarsOrig[i] - movCarsOrig[j])
                parkCarsMax <- parkCarsMax + abs(parkCarsOrig[i] - parkCarsOrig[j])
                movCiclyMax <- movCiclyMax + abs(movCiclyOrig[i] - movCiclyOrig[j])
                buildIdMax <- buildIdMax + abs(buildIdOrig[i] - buildIdOrig[j])
                buildNRecMax <- buildNRecMax + abs(buildNRecOrig[i] - buildNRecOrig[j])
                treeMax <- treeMax + abs(treeOrig[i] - treeOrig[j])
                smallPlaMax <- smallPlaMax + abs(smallPlaOrig[i] - smallPlaOrig[j])
                diffBuildMax <- diffBuildMax + abs(diffBuildOrig[i] - diffBuildOrig[j])
                streeFurMax <- streeFurMax + abs(streeFurOrig[i] - streeFurOrig[j])
                basColMax <- basColMax + abs(basColOrig[i] - basColOrig[j])
                lighMax <- lighMax + abs(lighOrig[i] - lighOrig[j])
                accenColMax <- accenColMax + abs(accenColOrig[i] - accenColOrig[j])
                peopMax <- peopMax + abs(peopOrig[i] - peopOrig[j])
                graffMax <- graffMax + abs(as.integer(graffOrig[i]) - as.integer(graffOrig[j]))
                buildDiffAgesMax <- buildDiffAgesMax + abs(as.integer(buildDiffAgesOrig[i]) - as.integer(buildDiffAgesOrig[j]))
                
                streetWidMax <- streetWidMax + abs(as.double(streetWidOrig[i]) - as.double(streetWidOrig[j]))
                sidewalkWidMax <- sidewalkWidMax + abs(as.double(sidewalkWidOrig[i]) - as.double(sidewalkWidOrig[j]))
                debrisMax <- cbind(debrisMax, abs(as.double(debrisOrig[i]) - as.double(debrisOrig[j])))
                pavementMax <- cbind(pavementMax, abs(as.double(pavementOrig[i]) - as.double(pavementOrig[j]))) 
                landscapeMax <- cbind(landscapeMax, abs(as.double(landscapeOrig[i]) - as.double(landscapeOrig[j])))
                propStreetWallMax <- cbind(propStreetWallMax, abs(as.double(propStreetWallOrig[i]) - as.double(propStreetWallOrig[j])))
                propWindMax <- cbind(propWindMax, abs(as.double(propWindOrig[i]) - as.double(propWindOrig[j])))
                longSightMax <- longSightMax + abs(as.double(longSightOrig[i]) - as.double(longSightOrig[j]))
                propSkyAheadMax <- cbind(propSkyAheadMax, abs(as.double(propSkyAheadOrig[i]) - as.double(propSkyAheadOrig[j])))
                propSkyAcrossMax <- cbind(propSkyAcrossMax, abs(as.double(propSkyAcrossOrig[i]) - as.double(propSkyAcrossOrig[j]))) 
                buildHeightMax <- buildHeightMax + abs(as.double(buildHeightOrig[i]) - as.double(buildHeightOrig[j]))
                propActiveUseMax <- cbind(propActiveUseMax, abs(as.double(propActiveUseOrig[i]) - as.double(propActiveUseOrig[j])))

		#Storing all images features differences
		mcaT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- movCarsOrig[i] - movCarsOrig[j]
		mcaT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- movCarsOrig[j] - movCarsOrig[i]
		pcaT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- parkCarsOrig[i] - parkCarsOrig[j]
		pcaT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- parkCarsOrig[j] - parkCarsOrig[i]
		mciT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- movCiclyOrig[i] - movCiclyOrig[j]
		mciT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- movCiclyOrig[j] - movCiclyOrig[i]
		bidT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- buildIdOrig[i] - buildIdOrig[j]
		bidT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- buildIdOrig[j] - buildIdOrig[i]
		bnrT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- buildNRecOrig[i] - buildNRecOrig[j]
		bnrT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- buildNRecOrig[j] - buildNRecOrig[i]
		treT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- treeOrig[i] - treeOrig[j]
		treT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- treeOrig[j] - treeOrig[i]
		splT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- smallPlaOrig[i] - smallPlaOrig[j]
		splT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- smallPlaOrig[j] - smallPlaOrig[i]
		dbuT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- diffBuildOrig[i] - diffBuildOrig[j]
		dbuT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- diffBuildOrig[j] - diffBuildOrig[i]
		sfuT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- streeFurOrig[i] - streeFurOrig[j]
		sfuT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- streeFurOrig[j] - streeFurOrig[i]
		bacT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- basColOrig[i] - basColOrig[j]
		bacT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- basColOrig[j] - basColOrig[i]
		ligT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- lighOrig[i] - lighOrig[j]
		ligT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- lighOrig[j] - lighOrig[i]
		accT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- accenColOrig[i] - accenColOrig[j]
		accT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- accenColOrig[j] - accenColOrig[i]
		peoT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- peopOrig[i] - peopOrig[j]
		peoT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- peopOrig[j] - peopOrig[i]
		graT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.integer(graffOrig[i]) - as.integer(graffOrig[j])
		graT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.integer(graffOrig[j]) - as.integer(graffOrig[i])
		bdaT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.integer(buildDiffAgesOrig[i]) - as.integer(buildDiffAgesOrig[j])
		bdaT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.integer(buildDiffAgesOrig[j]) - as.integer(buildDiffAgesOrig[i])

		swiT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(streetWidOrig[i]) - as.double(streetWidOrig[j])
		swiT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(streetWidOrig[j]) - as.double(streetWidOrig[i])
		siwiT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(sidewalkWidOrig[i]) - as.double(sidewalkWidOrig[j])
		siwiT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(sidewalkWidOrig[j]) - as.double(sidewalkWidOrig[i])
		bheT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(buildHeightOrig[i]) - as.double(buildHeightOrig[j])
		bheT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(buildHeightOrig[j]) - as.double(buildHeightOrig[i])
		lsiT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(longSightOrig[i]) - as.double(longSightOrig[j])
		lsiT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(longSightOrig[j]) - as.double(longSightOrig[i])
		debT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(debrisOrig[i]) - as.double(debrisOrig[j])
		debT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(debrisOrig[j]) - as.double(debrisOrig[i])
		pavT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(pavementOrig[i]) - as.double(pavementOrig[j])
		pavT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(pavementOrig[j]) - as.double(pavementOrig[i])
		lanT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(landscapeOrig[i]) - as.double(landscapeOrig[j])
		lanT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(landscapeOrig[j]) - as.double(landscapeOrig[i])
		pswT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(propStreetWallOrig[i]) - as.double(propStreetWallOrig[j])
		pswT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(propStreetWallOrig[j]) - as.double(propStreetWallOrig[i])
		pwiT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(propWindOrig[i]) - as.double(propWindOrig[j])
		pwiT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(propWindOrig[j]) - as.double(propWindOrig[i])
		psaT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(propSkyAheadOrig[i]) - as.double(propSkyAheadOrig[j])
		psaT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(propSkyAheadOrig[j]) - as.double(propSkyAheadOrig[i])
		psacT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(propSkyAcrossOrig[i]) - as.double(propSkyAcrossOrig[j])
		psacT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(propSkyAcrossOrig[j]) - as.double(propSkyAcrossOrig[i])
		pactT[[rankLine1[['image_url']]]][[rankLine2[['image_url']]]] <- as.double(propActiveUseOrig[i]) - as.double(propActiveUseOrig[j])
		pactT[[rankLine2[['image_url']]]][[rankLine1[['image_url']]]] <- as.double(propActiveUseOrig[j]) - as.double(propActiveUseOrig[i])
            }
        }
    }

    #Real world mean values for grades and proportions
    if( length(debris) > 0 ){
      featuresMapG1[["movCars"]] <- movCars
      featuresMapG1[["parkCars"]] <- parkCars
      featuresMapG1[["movCicly"]] <- movCicly
      featuresMapG1[["buildId"]] <- buildId
      featuresMapG1[["buildNRec"]] <- buildNRec
      featuresMapG1[["tree"]] <- tree
      featuresMapG1[["smallPla"]] <- smallPla
      featuresMapG1[["diffBuild"]] <- diffBuild
      featuresMapG1[["streeFur"]] <- streeFur
      featuresMapG1[["basCol"]] <- basCol
      featuresMapG1[["ligh"]] <- ligh
      featuresMapG1[["accenCol"]] <- accenCol
      featuresMapG1[["peop"]] <- peop
      featuresMapG1[["graff"]] <- graff
      featuresMapG1[["buildDiffAges"]] <- buildDiffAges
      featuresMapG1[["streetWid"]] <- streetWid
      featuresMapG1[["sidewalkWid"]] <- sidewalkWid
      featuresMapG1[["buildHeight"]] <- buildHeight
      featuresMapG1[["longSight"]] <- longSight
      
      featuresMapG1[["debris"]] <- .Internal(mean(debris))
      featuresMapG1[["pavement"]] <- .Internal(mean(pavement))
      featuresMapG1[["landscape"]]<- .Internal(mean(landscape))
      featuresMapG1[["propStreetWall"]] <- .Internal(mean(propStreetWall))
      featuresMapG1[["propWind"]] <- .Internal(mean(propWind))
      featuresMapG1[["propStreetWall"]] <- .Internal(mean(propStreetWall))
      featuresMapG1[["propWind"]] <- .Internal(mean(propWind))
      featuresMapG1[["propSkyAhead"]] <- .Internal(mean(propSkyAhead))
      featuresMapG1[["propSkyAcross"]] <- .Internal(mean(propSkyAcross))
      featuresMapG1[["propActiveUse"]] <- .Internal(mean(propActiveUse))
    }
    debrisMax <- .Internal(mean(debrisMax))
    pavementMax <- .Internal(mean(pavementMax))
    landscapeMax <- .Internal(mean(landscapeMax))
    propStreetWallMax <- .Internal(mean(propStreetWallMax))
    propWindMax <- .Internal(mean(propWindMax))
    propStreetWallMax <- .Internal(mean(propStreetWallMax))
    propWindMax <- .Internal(mean(propWindMax))
    propSkyAheadMax <- .Internal(mean(propSkyAheadMax))
    propSkyAcrossMax <- .Internal(mean(propSkyAcrossMax))
    propActiveUseMax <- .Internal(mean(propActiveUseMax))
    
    #Random world
    movCars <- parkCars <- movCicly <- buildId <- buildNRec <- tree <- smallPla <- diffBuild <-streeFur <- basCol <- ligh <-  accenCol <- peop <- graff <- buildDiffAges <- streetWid <- sidewalkWid <- longSight <- buildHeight <- debris <- pavement <- landscape <- propStreetWall <- propWind <-  propSkyAhead <- propSkyAcross <- propActiveUse <- c()
    
    for (k in seq(1, iterations)){

	randomData <- filter(read.table(paste("/local/david/pybossa_env/campinaPulse/scripts/analise/dadosNov15/usuarios/samplesIds/geralSetoresAJ_", k, ".dat", sep=""), header=TRUE), V1 == question)
	if (length(sector) > 1){#Filtering when considering only a specific sector!
		randomData <- filter(randomData, setor == sector)
	}
	sub <- randomData[, c("V2", "V3", "grupo", "bairro")]
	newData <- reshape(sub, timevar="grupo", idvar=c("V2", "bairro"), direction="wide")
	amountOfRandData <- nrow(newData)
	if (k %% 20 == 0){
		print(paste("Iteration ", k))
	}

	movCarsR <- parkCarsR <- movCiclyR <- buildIdR <- buildNRecR <- treeR <- smallPlaR <- diffBuildR <- streeFurR <- basColR <- lighR <-  accenColR <- peopR <- graffR <- buildDiffAgesR <- streetWidR <- sidewalkWidR <- longSightR <- buildHeightR <- 0
        debrisR <- pavementR <- landscapeR <- propStreetWallR <- propWindR <- propSkyAheadR <- propSkyAcrossR <- propActiveUseR <- c()

       for( i in seq(1, amountOfRandData) ) {
            rankLine1 <- newData[i,]
            
            if(i+1 <= amountOfRandData){
                for( j in seq(i+1, amountOfRandData) ){
                    rankLine2 <- newData[j,]

		    if ( !is.na(rankLine1[[group1Id]]) & !is.na(rankLine2[[group1Id]]) & !is.na(rankLine1[[group2Id]]) &!is.na(rankLine2[[group2Id]]) ) {                    
		            if ( (rankLine1[[group1Id]] < rankLine2[[group1Id]] & rankLine1[[group2Id]] > rankLine2[[group2Id]]) | (rankLine1[[group1Id]] > rankLine2[[group1Id]] & rankLine1[[group2Id]] < rankLine2[[group2Id]]) ) {

				if( rankLine1[[group1Id]] < rankLine2[[group1Id]] & rankLine1[[group2Id]] > rankLine2[[group2Id]] ) {
						firstImage <- as.character(rankLine2$V2)
						secondImage <- as.character(rankLine1$V2)
	    			   }else {
						firstImage <- as.character(rankLine1$V2)
						secondImage <- as.character(rankLine2$V2)
				  }


			tryCatch(
	  
				    if(!is.null(mcaT[[firstImage]][[secondImage]])) {
					    movCarsR <- movCarsR + mcaT[[firstImage]][[secondImage]]
					    parkCarsR <- parkCarsR +  pcaT[[firstImage]][[secondImage]]
					    movCiclyR <- movCiclyR +  mciT[[firstImage]][[secondImage]]
					    buildIdR <- buildIdR +  bidT[[firstImage]][[secondImage]]
					    buildNRecR <- buildNRecR +  bnrT[[firstImage]][[secondImage]]
					    treeR <- treeR +  treT[[firstImage]][[secondImage]]
					    smallPlaR <- smallPlaR + splT[[firstImage]][[secondImage]]
					    diffBuildR <- diffBuildR +  dbuT[[firstImage]][[secondImage]]
					    streeFurR <- streeFurR +  sfuT[[firstImage]][[secondImage]]
					    basColR <- basColR +  bacT[[firstImage]][[secondImage]]
					    lighR <- lighR + ligT[[firstImage]][[secondImage]]
					    accenColR <- accenColR +  accT[[firstImage]][[secondImage]]
					    peopR <- peopR + peoT[[firstImage]][[secondImage]]
					    graffR <- graffR + graT[[firstImage]][[secondImage]]
					    buildDiffAgesR <- bdaT[[firstImage]][[secondImage]]
						      
					    streetWidR <- streetWidR + swiT[[firstImage]][[secondImage]]
					    sidewalkWidR <- sidewalkWidR + siwiT[[firstImage]][[secondImage]]
					    debrisR <- cbind(debrisR, debT[[firstImage]][[secondImage]])
					    pavementR <- cbind(pavementR, pavT[[firstImage]][[secondImage]])
					    landscapeR <- cbind(landscapeR, lanT[[firstImage]][[secondImage]])
					    propStreetWallR <- cbind(propStreetWallR, pswT[[firstImage]][[secondImage]])
					    propWindR <- cbind(propWindR, pwiT[[firstImage]][[secondImage]])
					    longSightR <- longSightR + lsiT[[firstImage]][[secondImage]]
					    propSkyAheadR <- cbind(propSkyAheadR, psaT[[firstImage]][[secondImage]])
					    propSkyAcrossR <- cbind(propSkyAcrossR, psacT[[firstImage]][[secondImage]])
					    buildHeightR <- buildHeightR + bheT[[firstImage]][[secondImage]]
					    propActiveUseR <- cbind(propActiveUseR, pactT[[firstImage]][[secondImage]])
				},
			error = function(e) 
			  {
			    #print(e$message) # or whatever error handling code you want
			  }
			)
		     }
		}
           }
 	 }
	}
        
        #Binding with previous iterations
        if( length(debrisR) > 0 ) {
            movCars <- cbind(movCars, movCarsR)
            parkCars <- cbind(parkCars, parkCarsR)
            movCicly <- cbind(movCicly, movCiclyR)
            buildId <- cbind(buildId, buildIdR)
            buildNRec <- cbind(buildNRec, buildNRecR)
            tree <- cbind(tree, treeR)
            smallPla <- cbind(smallPla, smallPlaR)
            diffBuild <- cbind(diffBuild, diffBuildR)
            streeFur <- cbind(streeFur, streeFurR)
            basCol <- cbind(basCol, basColR)
            ligh <-  cbind(ligh, lighR)
            accenCol <- cbind(accenCol, accenColR)
            peop <- cbind(peop, peopR)
            graff <- cbind(graff, graffR)
            buildDiffAges <- cbind(buildDiffAges, buildDiffAgesR)
                    
            streetWid <- cbind(streetWid, streetWidR)
            sidewalkWid <- cbind(sidewalkWid, sidewalkWidR)
            longSight <- cbind(longSight, longSightR)
            buildHeight <- cbind(buildHeight, buildHeightR)
            debris <- cbind(debris, .Internal(mean(debrisR)))
            pavement <- cbind(pavement, .Internal(mean(pavementR)))
            landscape <- cbind(landscape, .Internal(mean(landscapeR)))
            propStreetWall <- cbind(propStreetWall, .Internal(mean(propStreetWallR)))
            propWind <- cbind(propWind, .Internal(mean(propWindR)))
            propSkyAhead <- cbind(propSkyAhead, .Internal(mean(propSkyAheadR)))
            propSkyAcross <- cbind(propSkyAcross, .Internal(mean(propSkyAcrossR)))
            propActiveUse <- cbind(propActiveUse, .Internal(mean(propActiveUseR)))
        }
    }
    
    #Random world mean
    if(length(movCars) > 0){
	featuresMapG1[["rmovCars"]] <- .Internal(mean(movCars)) 
	featuresMapG1[["rparkCars"]] <- .Internal(mean(parkCars))
	featuresMapG1[["rmovCicly"]] <- .Internal(mean(movCicly))
	featuresMapG1[["rbuildId"]] <- .Internal(mean(buildId))
	featuresMapG1[["rbuildNRec"]] <- .Internal(mean(buildNRec))
	featuresMapG1[["rtree"]] <- .Internal(mean(tree))
	featuresMapG1[["rsmallPla"]] <- .Internal(mean(smallPla))
	featuresMapG1[["rdiffBuild"]] <- .Internal(mean(diffBuild))
	featuresMapG1[["rstreeFur"]] <- .Internal(mean(streeFur))
	featuresMapG1[["rbasCol"]] <- .Internal(mean(basCol)) 
	featuresMapG1[["rligh"]] <- .Internal(mean(ligh))
	featuresMapG1[["raccenCol"]] <- .Internal(mean(accenCol))
	featuresMapG1[["rpeop"]] <- .Internal(mean(peop))
	featuresMapG1[["rgraff"]] <- .Internal(mean(graff)) 
	featuresMapG1[["rbuildDiffAges"]] <- .Internal(mean(buildDiffAges))

	featuresMapG1[["rstreetWid"]] <- .Internal(mean(streetWid))
	featuresMapG1[["rsidewalkWid"]] <- .Internal(mean(sidewalkWid))
	featuresMapG1[["rlongSight"]] <- .Internal(mean(longSight))
	featuresMapG1[["rbuildHeight"]] <- .Internal(mean(buildHeight))
	featuresMapG1[["rdebris"]] <- .Internal(mean(debris))
	featuresMapG1[["rpavement"]] <- .Internal(mean(pavement))
	featuresMapG1[["rlandscape"]] <- .Internal(mean(landscape))
	featuresMapG1[["rpropStreetWall"]] <- .Internal(mean(propStreetWall))
	featuresMapG1[["rpropWind"]] <- .Internal(mean(propWind))
	featuresMapG1[["rpropSkyAhead"]] <- .Internal(mean(propSkyAhead))
	featuresMapG1[["rpropSkyAcross"]] <- .Internal(mean(propSkyAcross))
	featuresMapG1[["rpropActiveUse"]] <- .Internal(mean(propActiveUse))
    }    

    featuresMapG1[["rsdMovCars"]] <- sd(movCars) 
    featuresMapG1[["rsdParkCars"]] <- sd(parkCars)
    featuresMapG1[["rsdMovCicly"]] <- sd(movCicly)
    featuresMapG1[["rsdBuildId"]] <- sd(buildId) 
    featuresMapG1[["rsdBuildNRec"]] <- sd(buildNRec) 
    featuresMapG1[["rsdTree"]] <- sd(tree)
    featuresMapG1[["rsdSmallPla"]] <- sd(smallPla)
    featuresMapG1[["rsdDiffBuild"]] <- sd(diffBuild)
    featuresMapG1[["rsdStreeFur"]] <- sd(streeFur) 
    featuresMapG1[["rsdBasCol"]] <- sd(basCol) 
    featuresMapG1[["rsdLigh"]] <- sd(ligh)
    featuresMapG1[["rsdAccenCol"]] <- sd(accenCol) 
    featuresMapG1[["rsdPeop"]] <- sd(peop) 
    featuresMapG1[["rsdGraff"]] <- sd(graff) 
    featuresMapG1[["rsdBuildDiffAges"]] <- sd(buildDiffAges)
    
    featuresMapG1[["rsdStreetWid"]] <- sd(streetWid)
    featuresMapG1[["rsdSidewalkWid"]] <- sd(sidewalkWid)
    featuresMapG1[["rsdLongSight"]] <- sd(longSight)
    featuresMapG1[["rsdBuildHeight"]] <- sd(buildHeight)
    featuresMapG1[["rsdDebris"]] <- sd(debris)
    featuresMapG1[["rsdPavement"]] <- sd(pavement)
    featuresMapG1[["rsdLandscape"]] <- sd(landscape)
    featuresMapG1[["rsdPropStreetWall"]] <- sd(propStreetWall)
    featuresMapG1[["rsdPropWind"]] <- sd(propWind)
    featuresMapG1[["rsdPropSkyAhead"]] <- sd(propSkyAhead)
    featuresMapG1[["rsdPropSkyAcross"]] <- sd(propSkyAcross)
    featuresMapG1[["rsdPropActiveUse"]] <- sd(propActiveUse)
    
    #Adding random mean values - normalized
    if(length(movCars) > 0){
	  featuresMapG1[["rmovCarsN"]] <- .Internal(mean(movCars)) / movCarsMax#/ (maxMovCars*den)
          featuresMapG1[["rparkCarsN"]] <- .Internal(mean(parkCars)) / parkCarsMax#/ (maxParkCars*den)
          featuresMapG1[["rmovCiclyN"]] <- .Internal(mean(movCicly)) / movCiclyMax #/ (maxMovCicly*den)
          featuresMapG1[["rbuildIdN"]] <- .Internal(mean(buildId)) / buildIdMax#/ (maxBuildId*den)
          featuresMapG1[["rbuildNRecN"]] <- .Internal(mean(buildNRec)) / buildNRecMax#/ (maxBuildNRec*den)
          featuresMapG1[["rtreeN"]] <- .Internal(mean(tree)) / treeMax#/ (maxTree*den)
          featuresMapG1[["rsmallPlaN"]] <- .Internal(mean(smallPla)) / smallPlaMax#/ (maxSmallPla*den)
          featuresMapG1[["rdiffBuildN"]] <- .Internal(mean(diffBuild)) / diffBuildMax#/ (maxDiffBuild*den)
          featuresMapG1[["rstreeFurN"]] <- .Internal(mean(streeFur)) / streeFurMax#/ (maxStreeFur*den)
          featuresMapG1[["rbasColN"]] <- .Internal(mean(basCol)) / basColMax#/ (maxBasCol*den)
          featuresMapG1[["rlighN"]] <- .Internal(mean(ligh)) / lighMax#/ (maxLigh*den)
          featuresMapG1[["raccenColN"]] <- .Internal(mean(accenCol)) / accenColMax#/ (maxAccenCol*den)
          featuresMapG1[["rpeopN"]] <- .Internal(mean(peop)) / peopMax#/ (maxPeop*den)
          featuresMapG1[["rgraffN"]] <- .Internal(mean(graff)) / graffMax#/ (maxGraff*den)
          featuresMapG1[["rbuildDiffAgesN"]] <- .Internal(mean(buildDiffAges)) / buildDiffAgesMax#/ (maxBuildDiffAges*den)

          featuresMapG1[["rstreetWidN"]] <- .Internal(mean(streetWid)) / streetWidMax
          featuresMapG1[["rsidewalkWidN"]] <- .Internal(mean(sidewalkWid)) / sidewalkWidMax
          featuresMapG1[["rdebrisN"]] <- .Internal(mean(debris)) / debrisMax
          featuresMapG1[["rpavementN"]] <- .Internal(mean(pavement)) / pavementMax
          featuresMapG1[["rlandscapeN"]] <- .Internal(mean(landscape)) / landscapeMax
          featuresMapG1[["rpropStreetWallN"]] <- .Internal(mean(propStreetWall)) / propStreetWallMax
          featuresMapG1[["rpropWindN"]] <- .Internal(mean(propWind)) / propWindMax
          featuresMapG1[["rlongSightN"]] <- .Internal(mean(longSight)) / longSightMax
          featuresMapG1[["rpropSkyAheadN"]] <- .Internal(mean(propSkyAhead)) / propSkyAheadMax
          featuresMapG1[["rpropSkyAcrossN"]] <- .Internal(mean(propSkyAcross)) / propSkyAcrossMax
          featuresMapG1[["rbuildHeightN"]] <- .Internal(mean(buildHeight)) / buildHeightMax
          featuresMapG1[["rpropActiveUseN"]] <- .Internal(mean(propActiveUse)) / propActiveUseMax
    }

    #Normalizing real values
    featuresMapG1[["movCarsN"]] <- featuresMapG1[["movCars"]] / movCarsMax#(maxMovCars*den)
    featuresMapG1[["parkCarsN"]] <- featuresMapG1[["parkCars"]]  / parkCarsMax#(maxParkCars*den)
    featuresMapG1[["movCiclyN"]] <-  featuresMapG1[["movCicly"]] / movCiclyMax#(maxMovCicly*den)
    featuresMapG1[["buildIdN"]] <- featuresMapG1[["buildId"]]/ buildIdMax#(maxBuildId*den)
    featuresMapG1[["buildNRecN"]] <- featuresMapG1[["buildNRec"]] / buildNRecMax#(maxBuildNRec*den)
    featuresMapG1[["treeN"]] <- featuresMapG1[["tree"]] / treeMax#(maxTree*den)
    featuresMapG1[["smallPlaN"]] <- featuresMapG1[["smallPla"]] / smallPlaMax#(maxSmallPla*den)
    featuresMapG1[["diffBuildN"]] <- featuresMapG1[["diffBuild"]] / diffBuildMax#(maxDiffBuild*den)
    featuresMapG1[["streeFurN"]] <- featuresMapG1[["streeFur"]] / streeFurMax#(maxStreeFur*den)
    featuresMapG1[["basColN"]] <- featuresMapG1[["basCol"]] / basColMax#(maxBasCol*den)
    featuresMapG1[["lighN"]] <- featuresMapG1[["ligh"]] / lighMax#(maxLigh*den)
    featuresMapG1[["accenColN"]] <- featuresMapG1[["accenCol"]] / accenColMax#(maxAccenCol*den)
    featuresMapG1[["peopN"]] <- featuresMapG1[["peop"]]  / peopMax#(maxPeop*den)
    featuresMapG1[["graffN"]] <- featuresMapG1[["graff"]]/ graffMax#(maxGraff*den)
    featuresMapG1[["buildDiffAgesN"]] <- featuresMapG1[["buildDiffAges"]] / buildDiffAgesMax#(maxBuildDiffAges*den)
    featuresMapG1[["streetWidN"]] <- featuresMapG1[["streetWid"]] / streetWidMax
    featuresMapG1[["sidewalkWidN"]] <- featuresMapG1[["sidewalkWid"]] / sidewalkWidMax
    featuresMapG1[["debrisN"]] <- featuresMapG1[["debris"]] / debrisMax
    featuresMapG1[["pavementN"]] <- featuresMapG1[["pavement"]] / pavementMax
    featuresMapG1[["landscapeN"]] <- featuresMapG1[["landscape"]] / landscapeMax
    featuresMapG1[["propStreetWallN"]] <- featuresMapG1[["propStreetWall"]] / propStreetWallMax
    featuresMapG1[["propWindN"]] <- featuresMapG1[["propWind"]] / propWindMax
    featuresMapG1[["longSightN"]] <- featuresMapG1[["longSight"]] / longSightMax
    featuresMapG1[["propSkyAheadN"]] <- featuresMapG1[["propSkyAhead"]] / propSkyAheadMax
    featuresMapG1[["propSkyAcrossN"]] <- featuresMapG1[["propSkyAcross"]] / propSkyAcrossMax
    featuresMapG1[["buildHeightN"]] <- featuresMapG1[["buildHeight"]] / buildHeightMax
    featuresMapG1[["propActiveUseN"]] <- featuresMapG1[["propActiveUse"]] / propActiveUseMax
    
    return ( featuresMapG1 )
}

#Calculates maximum denominator for normalization
calcGreatesSum <- function(maxFeature, amountOfImages) {
	sumFeat <- 0
	maxDiff <- amountOfImages - 1
	reuse <- FALSE

	for (i in seq(1, amountOfImages)){
		sumFeat <- sumFeat + maxFeature * (maxDiff)		
		if(maxDiff == 0 | maxDiff == 1){
			maxDiff <- amountOfImages - 1
		}else{
			maxDiff <- maxDiff - 2
		}
	}
	return (sumFeat)
}

iterations <- 10000

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

print("################### Men x Women - Pleasantness")
#Homem x Mulher
agrad.l <- agrad %>% do(arrange(., desc(V3.Masculino))) %>% 
    mutate(rank = 1:n()) %>% do(arrange(., desc(V3.Feminino))) %>% mutate(index = 1:n())

#print(paste(">>>> Kendall Distance ", normalizedKendallTauDistance2(agrad.l$V3.Masculino, agrad.l$V3.Feminino)))
#res <- melt(kendallWithWeights(agrad.l, iterations, "V3.Masculino", "V3.Feminino", "agrad%C3%A1vel?", ""))
#print(res, row.names=FALSE)
#convertSummary(res, iterations)
#res <- kendallWithWeightsSimReal(agrad.l, iterations, "Masculino", "Feminino", "agradavel?", temp1, "")
#print(res)
#analyseICForFeatures(res)

#printOutputOneListPerFeature(agrad.l2, "V3.Masculino", "V3.Feminino")
#printOutputTwoListsPerFeature(agrad.l2, "V3.Masculino", "V3.Feminino")
#printOutputTwoListsAllFeaturesTog(agrad.l2)

print("################### Men x Women - Safety")

#Homem x Mulher
seg.l <- seg %>% 
    do(arrange(., desc(V3.Masculino))) %>% 
    mutate(rank = 1:n()) %>% do(arrange(., desc(V3.Feminino))) %>% mutate(index = 1:n())

print(paste(">>>> Kendall Distance ", normalizedKendallTauDistance2(seg.l$V3.Masculino, seg.l$V3.Feminino)))
res <- melt(kendallWithWeights(seg.l, iterations, "V3.Masculino", "V3.Feminino", "seguro?", ""))
print(res, row.names=FALSE)
convertSummary(res, iterations)
#res <- kendallWithWeightsSimReal(seg.l, iterations, "Masculino", "Feminino", "seguro?", temp1, "")
#print(res)
#analyseICForFeatures(res)

#printOutputOneListPerFeature(seg.l2, "V3.Masculino", "V3.Feminino")
#printOutputTwoListsPerFeature(seg.l2, "V3.Masculino", "V3.Feminino")
#printOutputTwoListsAllFeaturesTog(seg.l2)
