#https://www.r-bloggers.com/how-to-perform-a-logistic-regression-in-r/
#2nd order interactions: http://stackoverflow.com/questions/22649536/model-matrix-with-all-pairwise-interactions-between-columns
#Assumptions: http://www.statisticssolutions.com/assumptions-of-logistic-regression/ -> no multicollinearity, he independent variables should be independent from each other; 
#Interpret coefficients: http://www.ats.ucla.edu/stat/mult_pkg/faq/general/odds_ratio.htm
#Intercept é o log odds (onde odds é p / (1-p)) para o caso base, por exemplo, jovem, feminino, baixa, solteiro e diferencas das features em 0 -> pode ser um caso hipotetico!
#Moderation x Mediation: http://psych.wisc.edu/henriques/mediator.html ; http://www.uni-kiel.de/psychologie/rexrepos/posts/regressionModMed.html

require(gmodels)
require(vcd)
require(lme4)
library(caret)
library(pscl)
library(DT)
library(ggplot2)
theme_set(theme_bw())
library(GGally)
library(dplyr, warn.conflicts = F)
library(broom)

library(car)
library(readr)

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
raw_data = read_delim(
  "classifier//classifier_input_wodraw.dat",
  delim = "\t",
  col_types = cols(
    .default = col_double(),
    row = col_integer(),
    choice = col_character(),
    question = col_character(),
    photo1 = col_character(),
    photo2 = col_character(),
    choice = col_integer(),
    userID = col_integer(),
    gender = col_character(),
    age = col_character(),
    income = col_character(),
    education = col_character(),
    city = col_character(),
    marital = col_character(),
    graffiti1 = col_character(),
    bairro1 = col_character(),
    graffiti2 = col_character(),
    bairro2 = col_character()
  )
)


data = raw_data %>% 
  mutate( # Recode
    income = if_else(is.na(income), "media", income),
    age_cat = if_else(as.integer(age) >= 25 | is.na(age), "adulto", "jovem"),
    inc_cat = if_else(income %in% c("baixa", "media baixa"),
                      "baixa", 
                      "media"), # substituirá os NA
    choice = if_else(choice == "1", "0", 
                     if_else(choice == "-1", "1", choice)), 
    bair_cat = if_else(bairro1 == bairro2, "mesmo", 
                       paste0(bairro1, "_", bairro2))    
  ) %>% 
  mutate_at( # to factor
    vars(income, age_cat, inc_cat, choice, bair_cat, marital, gender),
    as.factor) %>% 
  mutate( # relevel
    bair_cat = relevel(bair_cat,  "mesmo"),
    marital = relevel(marital,  "solteiro"),
    income = relevel(income,  "baixa"),
    age_cat = relevel(age_cat,  "jovem"),
    gender = relevel(gender,  "feminino"),
    inc_cat = relevel(inc_cat,  "baixa")
  ) 

# Create diff features
data = data %>%
  mutate(
    d_swidth = street_wid1 - street_wid2,
    d_mvcars = mov_cars1 - mov_cars2,
    d_pcars = park_cars1 - park_cars2,
    d_trees = trees1 - trees2,
    d_mvciclyst = mov_ciclyst1 - mov_ciclyst2,
    d_lands = landscape1 - landscape2,
    d_bid = build_ident1 - build_ident2,
    d_bheig = log2(build_height1 + 1) - log2(build_height2 + 1),
    d_dbuild = diff_build1 - diff_build2,
    d_people = people1 - people2,
    d_graff = (graffiti1 == "Yes") - (graffiti2 == "Yes")
  )

# SPLIT + SCALE
agrad <- filter(data, !(question %in% c("seguro?", "seguro"))) %>% 
  mutate_at(vars(40:50), scale)
seg <- filter(data, (question %in% c("seguro?", "seguro")))  %>% 
  mutate_at(vars(40:50), scale)

create_model_w_interact = function(the_data){
  return(glm(
    choice ~ d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff + bair_cat + 
      age_cat:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff) + 
      gender:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff) + 
      inc_cat:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff),
    data = the_data,
    family = binomial()))
}

create_model_wo_profile = function(the_data){
  return(glm(
    choice ~ d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff + bair_cat,
    data = the_data,
    family = binomial()))
}

# mostpleasant_model <- create_model_w_interact(agrad)
# summary(mostpleasant_model)
# #anova(mostpleasant_model, test="Chisq")
# vif(mostpleasant_model)

# coefs_ag = tidy(mostpleasant_model, conf.int = TRUE, exponentiate = TRUE) 
# coefs_ag %>% 
#   mutate_at(vars(-1), prettyNum, digits = 3) %>% 
#   datatable()
# { # fix for what seems like a bug in pR2
#     the_data = agrad
#     pR2(mostpleasant_model)
# }

# safer_model <- create_model_w_interact(seg)
# summary(safer_model)
# #anova(safer_model, test="Chisq")
# vif(safer_model)

# coefs_seg = tidy(safer_model, conf.int = TRUE, exponentiate = TRUE) 
# coefs_seg %>% 
#   mutate_at(vars(-1), prettyNum, digits = 3) %>% 
#   datatable()

# { # fix for what seems like a bug in pR2
#     the_data = seg
#     pR2(safer_model)
# }

#Leave user out
leaveUserOut <- function(dataFrame, threshold){
  allPValues <- matrix(0, nrow=51, ncol=1)
  allCoef <- matrix(0, nrow=51, ncol=1)
  inputFeatures <- c()
  allAccuracies <- c()
  allRecall <- c()
  allPrecision <- c()
  
  for (currentUser in c(unique(dataFrame$userID)[1:20])) { 
    userData <- filter(dataFrame, userID == currentUser)
    notUserData <- filter(dataFrame, userID != currentUser)
    
    #baselineModel_interac <- glm(choice ~ scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + bair_cat + age_cat : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) +    gender : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) + inc_cat : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)), data= notUserData, family = binomial()) 
    baselineModel_interac <- create_model_w_interact(notUserData)
    result <- tidy(baselineModel_interac, conf.int = TRUE) %>% mutate_each(funs(exp), estimate, conf.low, conf.high)
    
    if (mean(allPValues) == 0){
      allPValues[,1] <- result$p.value
      allCoef[,1] <- result$estimate
      inputFeatures <- result$term
    }else{
      allPValues <- cbind(allPValues, result$p.value)
      allCoef <- cbind(allCoef, result$estimate)
    }
    
    #Testing with removed user!
    predictions <- predict(baselineModel_interac, newdata = userData, type = "response") > threshold
    fp <- table(predictions, userData$choice)[2]
    fn <- table(predictions, userData$choice)[3]
    correct_1 <- table(predictions, userData$choice)[4]
    correct_0 <- table(predictions, userData$choice)[1]
    
    print(paste(correct_0, correct_1, fp, fn))
    
    allAccuracies <- append(allAccuracies, (correct_1 + correct_0) / length(predictions))
    allPrecision <- append(allPrecision, (correct_1) / (correct_1 + fp))
    allRecall <- append(allRecall, (correct_1) / (correct_1 + fn))
  }
  
   write.table(allAccuracies, file=paste("accuraciesA", threshold, ".dat"), row.names=FALSE, quote=FALSE)
   write.table(allPrecision, file=paste("precisionA", threshold, ".dat"), row.names=FALSE, quote=FALSE)
   write.table(allRecall, file=paste("recallA", threshold, ".dat"), row.names=FALSE, quote=FALSE)
   write.table(cbind(inputFeatures, allPValues), file=paste("pvaluesA", threshold, ".dat"), row.names=FALSE, quote=FALSE)
   write.table(cbind(inputFeatures, allCoef), file=paste("coefficientsA", threshold, ".dat"), row.names=FALSE, quote=FALSE)
}

leaveUserOut(agrad, 0.5)
leaveUserOut(agrad, 0.6)
leaveUserOut(agrad, 0.7)
#leaveUserOut(seg)

#Safety
#baselineModel_wointerac_seg <- glm(choice ~ age + gender + income + marital + scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + d_catole + d_liberdade + d_centro, data= seg, family = binomial())
#summary(baselineModel_wointerac_seg)
#anova(baselineModel_wointerac_seg, test="Chisq")
#pR2(baselineModel_wointerac_seg)

#Only 3 occurrences of viuvo! Removing this class from interactions!
#age_cat + gender + income + marital + marital * ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff))
# baselineModel_interac_seg <- glm(choice ~ scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + bair_cat + age_cat : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) +    gender : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) + inc_cat : ( scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)), data= seg, family = binomial())#filter(seg, marital != "vi\\u00favo")
# summary(baselineModel_interac_seg)
# anova(baselineModel_interac_seg, test="Chisq")
# pR2(baselineModel_interac_seg)
# exp(baselineModel_interac_seg$coefficients)
# result <- tidy(baselineModel_interac_seg, conf.int = TRUE) %>% 
#   mutate_each(funs(exp), estimate, conf.low, conf.high)
# glance(baselineModel_interac_seg)

#True positive x False Positive
# library(ROCR)
# p <- predict(model, newdata=subset(test,select=c(2,3,4,5,6,7,8)), type="response")
# pr <- prediction(p, test$Survived)
# prf <- performance(pr, measure = "tpr", x.measure = "fpr")
# plot(prf)
# 
# auc <- performance(pr, measure = "auc")
# auc <- auc@y.values[[1]]
# #a model with good predictive ability should have an AUC closer to 1 (1 is ideal) than to 0.5.
# auc
# 
# #Other codes by Nazareno
# lModel <- update(baselineModel, . ~  . + marriage + birth)
# 
# lModel.2 <- update(baselineModel, . ~  . + start_age)
# 
# lModel.3 <- update(baselineModel, . ~  . + start_age + marriage + birth)
# 
# summary(baselineModel)
# summary(lModel)
# compare_glms(baselineModel, lModel)
# 
# summary(lModel.2)
# compare_glms(baselineModel, lModel.2)
# summary(lModel.3)
# compare_glms(lModel.2, lModel.3)
# 
# vif(lModel)
# 
# baselineModel <- glm(mob_change ~ education + gender + start_age,
#                      data = regression_data_u30, 
#                      family = binomial())
# 
# lModel <- update(baselineModel, . ~  . + marriage  + birth)
# 
# summary(baselineModel)
# summary(lModel)
# 
# vif(lModel)
# 
# modelChi <- baselineModel$deviance - lModel$deviance
# chidf <- baselineModel$df.residual - lModel$df.residual
# chisq.prob <- 1 - pchisq(modelChi, chidf)
# modelChi; chidf; chisq.prob
