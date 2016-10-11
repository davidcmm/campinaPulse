#https://www.r-bloggers.com/how-to-perform-a-logistic-regression-in-r/
#2nd order interactions: http://stackoverflow.com/questions/22649536/model-matrix-with-all-pairwise-interactions-between-columns
#Assumptions: http://www.statisticssolutions.com/assumptions-of-logistic-regression/ -> no multicollinearity, he independent variables should be independent from each other; 
#Interpret coefficients: http://www.ats.ucla.edu/stat/mult_pkg/faq/general/odds_ratio.htm
#Intercept é o log odds (onde odds é p / (1-p)) para o caso base, por exemplo, jovem, feminino, baixa, solteiro e diferencas das features em 0 -> pode ser um caso hipotetico!
#Moderation x Mediation: http://psych.wisc.edu/henriques/mediator.html ; http://www.uni-kiel.de/psychologie/rexrepos/posts/regressionModMed.html

library(dplyr)
require(gmodels)
require(vcd)
require(lme4)
library(caret)
library(pscl)

library(ggplot2)
theme_set(theme_bw())
library(GGally)
library(broom)

require("car")
compare_glms <- function(baseline, model){
  modelChi <- baseline$deviance - model$deviance
  chidf <- baseline$df.residual - model$df.residual
  chisq.prob <- 1 - pchisq(modelChi, chidf)
  print(paste(modelChi, chidf, chisq.prob))
}

compare_null <- function(baselineModel){
  modelChi <- baselineModel$null.deviance - baselineModel$deviance
  chidf <- baselineModel$df.null - baselineModel$df.residual
  chisq.prob <- 1 - pchisq(modelChi, chidf)
  print(paste(modelChi, chidf, chisq.prob))
}

#classifier//classifier_input_wodraw.dat
#../../dadosNov15/usuarios/classifier//classifier_input_wodraw.dat
data <- read.table("classifier//classifier_input_wodraw.dat", sep="\t", header=TRUE)

#Replacing empty incomes with most common income
empty <- data$income[7131]#Empty income value!
data$income[data$income == empty] <- "media"

#Creating categories for age and income
data$age_cat <- "adulto"#Most common value
data$age_cat[data$age >= 25] <- "adulto"
data$age_cat[data$age <= 24] <- "jovem"
data$age_cat <- as.factor(data$age_cat)
data$inc_cat <- ""
data$inc_cat[data$income == "baixa" | data$income == "media baixa"] <- "baixa"
data$inc_cat[data$income == "alta" | data$income == "media alta" | data$income == "media"] <- "media"
data$inc_cat <- as.factor(data$inc_cat)

data$choice[data$choice == 1] <- 0
data$choice[data$choice == -1] <- 1
#data$choice[data$choice == -1] <- 0
data$choice <- factor(data$choice)

data$bair_cat <- "mesmo"
data$bair_cat[data$bairro1 == "catole" & data$bairro2 == "liberdade"] <- "cat_lib"
data$bair_cat[data$bairro1 == "catole" & data$bairro2 == "centro"] <- "cat_cen"
data$bair_cat[data$bairro1 == "liberdade" & data$bairro2 == "catole"] <- "lib_cat"
data$bair_cat[data$bairro1 == "liberdade" & data$bairro2 == "centro"] <- "lib_cen"
data$bair_cat[data$bairro1 == "centro" & data$bairro2 == "liberdade"] <- "cen_lib"
data$bair_cat[data$bairro1 == "centro" & data$bairro2 == "catole"] <- "cen_cat"
data$bair_cat <- factor(data$bair_cat)

data$bair_cat <- relevel(data$bair_cat,  "mesmo")
data$marital <- relevel(data$marital,  "solteiro")
data$income <- relevel(data$income,  "baixa")
data$age_cat <- relevel(data$age_cat,  "jovem")
data$gender <- relevel(data$gender,  "feminino")
data$inc_cat <- relevel(data$inc_cat,  "baixa")

agrad <- filter(data, question != "seguro?")
seg <- filter(data, question == "seguro?")

#Differences in features!
agrad$d_swidth = agrad$street_wid1 - agrad$street_wid2
agrad$d_mvcars = agrad$mov_cars1 - agrad$mov_cars2
agrad$d_pcars = agrad$park_cars1 - agrad$park_cars2
agrad$d_trees = agrad$trees1 - agrad$trees2
agrad$d_mvciclyst = agrad$mov_ciclyst1 - agrad$mov_ciclyst2
agrad$d_lands = agrad$landscape1 - agrad$landscape2
agrad$d_bid = agrad$build_ident1 - agrad$build_ident2
agrad$d_bheig = log2(agrad$build_height1+1) - log2(agrad$build_height2+1)
agrad$d_dbuild = agrad$diff_build1 - agrad$diff_build2
agrad$d_people = agrad$people1 - agrad$people2
agrad$graffiti1 <- as.character(agrad$graffiti1)
agrad$graffiti2 <- as.character(agrad$graffiti2)
agrad$graffiti1[agrad$graffiti1 == "No"] <- 0
agrad$graffiti1[agrad$graffiti1 == "Yes"] <- 1
agrad$graffiti2[agrad$graffiti2 == "No"] <- 0
agrad$graffiti2[agrad$graffiti2 == "Yes"] <- 1
agrad$d_graff = as.integer(agrad$graffiti1) - as.integer(agrad$graffiti2)
#dummies <- predict(dummyVars(~ bairro1, data = agrad), newdata = agrad)
#for(level in unique(agrad$bairro1)){
#  agrad[paste("dummy1", level, sep = "_")] <- ifelse(agrad$bairro1 == level, TRUE, FALSE)
#}
#for(level in unique(agrad$bairro2)){
#  agrad[paste("dummy2", level, sep = "_")] <- ifelse(agrad$bairro2 == level, TRUE, FALSE)
#}


seg$d_swidth = seg$street_wid1 - seg$street_wid2
seg$d_mvcars = seg$mov_cars1 - seg$mov_cars2
seg$d_pcars = seg$park_cars1 - seg$park_cars2
seg$d_trees = seg$trees1 - seg$trees2
seg$d_mvciclyst = seg$mov_ciclyst1 - seg$mov_ciclyst2
seg$d_lands = seg$landscape1 - seg$landscape2
seg$d_bid = seg$build_ident1 - seg$build_ident2
seg$d_bheig = log2(seg$build_height1+1) - log2(seg$build_height2+1)
seg$d_dbuild = seg$diff_build1 - seg$diff_build2
seg$d_people = seg$people1 - seg$people2
seg$graffiti1 <- as.character(seg$graffiti1)
seg$graffiti2 <- as.character(seg$graffiti2)
seg$graffiti1[seg$graffiti1 == "No"] <- 0
seg$graffiti1[seg$graffiti1 == "Yes"] <- 1
seg$graffiti2[seg$graffiti2 == "No"] <- 0
seg$graffiti2[seg$graffiti2 == "Yes"] <- 1
seg$d_graff = as.integer(seg$graffiti1) - as.integer(seg$graffiti2)
#dummies <- predict(dummyVars(~ bairro1, data = agrad), newdata = agrad)
#for(level in unique(seg$bairro1)){
#  seg[paste("dummy1", level, sep = "_")] <- ifelse(seg$bairro1 == level, 1, 0)
#}
#for(level in unique(seg$bairro2)){
#  seg[paste("dummy2", level, sep = "_")] <- ifelse(seg$bairro2 == level, 1, 0)
#}

#Regressions!
baselineModel_wointerac <- glm(choice ~ age_cat + gender + income + marital + scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + scale(d_catole) + scale(d_centro) + scale(d_liberdade), data= agrad, family = binomial())
summary(baselineModel_wointerac)
anova(baselineModel_wointerac, test="Chisq")
pR2(baselineModel_wointerac)

#age_cat + gender + income + marital + marital * ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) )
baselineModel_interac <- glm(choice ~ scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + bair_cat + age_cat : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) +    gender : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) + inc_cat : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)), data= agrad, family = binomial())
summary(baselineModel_interac)
anova(baselineModel_interac, test="Chisq")
pR2(baselineModel_interac)
exp(baselineModel_interac$coefficients)
tidy(baselineModel_interac, conf.int = TRUE)#https://github.com/nazareno/ciencia-de-dados-1/blob/master/5-regressao/regressao%20logistica.Rmd
glance(bm)

#Safety
baselineModel_wointerac_seg <- glm(choice ~ age + gender + income + marital + scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + d_catole + d_liberdade + d_centro, data= seg, family = binomial())
summary(baselineModel_wointerac_seg)
anova(baselineModel_wointerac_seg, test="Chisq")
pR2(baselineModel_wointerac_seg)

#Only 3 occurrences of viuvo! Removing this class from interactions!
#age_cat + gender + income + marital + marital * ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff))
baselineModel_interac_seg <- glm(choice ~ scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + bair_cat + age_cat : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) +    gender : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) + inc_cat : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)), data= seg, family = binomial())#filter(seg, marital != "vi\\u00favo")
summary(baselineModel_interac_seg)
anova(baselineModel_interac_seg, test="Chisq")
pR2(baselineModel_interac_seg)
exp(baselineModel_interac_seg$coefficients)


#True positive x False Positive
library(ROCR)
p <- predict(model, newdata=subset(test,select=c(2,3,4,5,6,7,8)), type="response")
pr <- prediction(p, test$Survived)
prf <- performance(pr, measure = "tpr", x.measure = "fpr")
plot(prf)

auc <- performance(pr, measure = "auc")
auc <- auc@y.values[[1]]
#a model with good predictive ability should have an AUC closer to 1 (1 is ideal) than to 0.5.
auc

#Other codes by Nazareno
lModel <- update(baselineModel, . ~  . + marriage + birth)

lModel.2 <- update(baselineModel, . ~  . + start_age)

lModel.3 <- update(baselineModel, . ~  . + start_age + marriage + birth)

summary(baselineModel)
summary(lModel)
compare_glms(baselineModel, lModel)

summary(lModel.2)
compare_glms(baselineModel, lModel.2)
summary(lModel.3)
compare_glms(lModel.2, lModel.3)

vif(lModel)

baselineModel <- glm(mob_change ~ education + gender + start_age,
                     data = regression_data_u30, 
                     family = binomial())

lModel <- update(baselineModel, . ~  . + marriage  + birth)

summary(baselineModel)
summary(lModel)

vif(lModel)

modelChi <- baselineModel$deviance - lModel$deviance
chidf <- baselineModel$df.residual - lModel$df.residual
chisq.prob <- 1 - pchisq(modelChi, chidf)
modelChi; chidf; chisq.prob