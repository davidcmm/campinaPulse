library(ggplot2)
theme_set(theme_bw())
library(dplyr)
library(reshape2)

source('analisaICPorFoto.R')

dados <- read.table("geral.dat", header=TRUE)

dadosCopy <- dados

#Intervalo de confiança por ponto
# <nazareno> Não estou usando por agora.
qscoreSim <- dadosCopy [ c(4:103) ]
icData <- apply(qscoreSim, 1, ic)
dadosCopy$distance <- icData

dadosCopy <- select(dadosCopy, V2, V1, V3, grupo, bairro)

dados_pro_plot <- function(data, grupo1, grupo2, pergunta){
  grupos_e_pergunta.index <- (data$grupo == grupo1 | dadosCopy$grupo == grupo2) & dadosCopy$V1==pergunta
  dados_CS_S.l <- dadosCopy[grupos_e_pergunta.index,]
  names(dados_CS_S.l) <- c("Local", "Pergunta", "QScore", "grupo", "bairro")
  
  # Qscore > rank
  dados_CS_S.l <- dados_CS_S.l %>% 
    group_by(grupo) %>% 
    do(arrange(., desc(QScore))) %>% 
    group_by(grupo, bairro) %>% 
    mutate(rank = 1:n())
  
  dados_CS_S.l$QScore <- NULL
  
  # long to wide
  dados_CS_S <- dcast(dados_CS_S.l, Local + bairro + Pergunta ~ grupo, value.var = "rank")
  # ordenar e colocar indices (deve haver uma forma melhor)
  dados_CS_S <- dados_CS_S %>% 
    group_by(bairro) %>% 
    do(arrange(., Casado)) %>% 
    group_by(bairro) %>% 
    mutate(index = 1:n())
  
  # back to long
  dados_CS_S.l <- melt(dados_CS_S, id.vars = names(dados_CS_S)[c(-4, -5)])
  names(dados_CS_S.l)[5] <- "grupo"
  names(dados_CS_S.l)[6] <- "rank"
  dados_CS_S.l
}

#Seguro
grupo1 <- 'Casado'
grupo2 <- 'Solteiro'
pergunta <- 'seguro?'

osdados <- dados_pro_plot(dadosCopy, grupo1, grupo2, pergunta)

w = 8
h = 2.7
pdf("casados-solteiros-seguro.pdf", width = w, height = h)
ggplot(osdados, aes(x=index, y = rank, colour=grupo, fill = grupo)) + 
  geom_point(alpha = 0.7, size=1.7) + 
  geom_line(aes(group = index), colour = "grey80") + 
  xlab("Local") + 
  ylab("rank") + 
  scale_y_reverse(limits = c(39, 1)) + 
  facet_grid(. ~ bairro)
  #scale_x_discrete(breaks=seq(1, 36, by=5))
dev.off()

pergunta <- 'agrad%C3%A1vel?'

osdados <- dados_pro_plot(dadosCopy, grupo1, grupo2, pergunta)

pdf("casados-solteiros-agradavel.pdf", width = w, height = h)
ggplot(osdados, aes(x=index, y = rank, colour=grupo, fill = grupo)) + 
  geom_point(alpha = 0.7, size=1.7) + 
  geom_line(aes(group = index), colour = "grey80") + 
  xlab("Local") + 
  ylab("rank") + 
  scale_y_reverse(limits = c(39, 1)) + 
  facet_grid(. ~ bairro)
#scale_x_discrete(breaks=seq(1, 36, by=5))
dev.off()
