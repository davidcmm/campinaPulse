library(ggplot2)
theme_set(theme_bw())
library(GGally)
library(pscl)
library(dplyr, warn.conflicts = FALSE)
library(broom)

titanic <- read.csv("logit/exemplo_naza/titanic3.csv")
titanic <- select(titanic, pclass, survived, sex, age, fare)
titanic$pclass <- as.factor(titanic$pclass)
titanic$survived <- as.factor(titanic$survived)
titanic <- na.omit(titanic)

ggpairs(titanic)

# Parece haver uma relação entre fare e survived
ggplot(titanic, aes(x = survived, y = fare)) + 
  geom_violin(fill = "lightblue") + 
  geom_point(position = position_jitter(.2), alpha = .3) + 
  scale_y_log10()

# Seria possível passar uma regressão linear?
ggplot(titanic, aes(x = fare, y = survived)) + 
  scale_x_log10() + 
  geom_count(alpha = .5)

# Um preditor numérico
x = -20:20

minha_logit = function(b0, b1, x){
  return(exp(b0 + b1 * x) / (1 + exp(b0 + b1 * x)))
}

# Usando uma função Logit qualquer
py_dado_x = minha_logit(1.2, 1.3, x)

data.frame(x, py_dado_x) %>% 
  ggplot(aes(x, py_dado_x)) + 
  geom_point() + 
  geom_line()

# coeficiente negativo: 
py_dado_x = minha_logit(1.2, -1.3, x)

data.frame(x, py_dado_x) %>% 
  ggplot(aes(x, py_dado_x)) + 
  geom_point() + 
  geom_line()

titanic = titanic %>% 
  filter(fare > 0) %>% 
  mutate(logFare = log(fare))

bm <- glm(survived ~ logFare, 
          data = titanic, 
          family = "binomial")

tidy(bm, conf.int = TRUE)
# EXPONENCIANDO:
tidy(bm, conf.int = TRUE, exponentiate = TRUE)
## Como aqui y = exp(b0)*exp(b1*x1), aumentar em uma unidade x, faz com que y seja multiplicado por exp(b1), que é o coeficiente acima

# Não existe um R^2 aqui
glance(bm)
# Pseudo R^2:
pR2(bm)

expectativa_realidade = augment(bm, type.predict = "response") 

expectativa_realidade %>% 
  mutate(survivedNum = ifelse(survived == "1", 1, 0)) %>% 
  ggplot(aes(x = logFare)) + 
  geom_count(aes(y = survivedNum), alpha = 0.5) + 
  geom_line(aes(y = .fitted))

bm <- glm(survived ~ pclass, 
          data = titanic, 
          family = "binomial")
tidy(bm, conf.int = TRUE)
glance(bm)
pR2(bm)
#summary(bm)

#Fit relacionando preferências e gêneros
x = read_csv("data/gender_prefs_speeddating.csv")
gendermodel = glm(gender ~ sport, 
                  data = select(x, -iid), 
                  family = "binomial")
tidy(gendermodel, conf.int = TRUE, exponentiate = TRUE)
glance(gendermodel)
pR2(gendermodel)

expectativa_realidade = augment(gendermodel, 
                                type.predict = "response") 

expectativa_realidade %>% 
  mutate(genderNum = ifelse(gender == "1", 1, 0)) %>% 
  ggplot(aes(x = sports)) + 
  geom_count(aes(y = genderNum), alpha = 0.5) + 
  geom_line(aes(y = .fitted))

expectativa_realidade = expectativa_realidade %>% 
  mutate(categoria_prevista = ifelse(.fitted > .5, "1", "0"))

table(expectativa_realidade$categoria_prevista, expectativa_realidade$gender)

#Multivariada:
bm <- glm(survived ~ pclass + sex + age + sex*age, 
          data = titanic, 
          family = "binomial")

tidy(bm, conf.int = TRUE, exponentiate = TRUE)
pR2(bm)

library(tidyr)
library(modelr) # devtools::install_github("hadley/modelr")

m = titanic %>% 
  data_grid(pclass, sex, age, survived)
mm = augment(bm, newdata = m, type.predict = "response")

ggplot(mm, aes(x = age, colour = pclass)) + 
  geom_line(aes(y = .fitted)) +  
  facet_grid(.~sex) 

predictions <- predict(bm, type = "response") > .5
true_survivals <- titanic$survived == 1

table(predictions, true_survivals)

require(vcd)
mosaic(table(predictions, true_survivals))

erro <- sum((predictions != true_survivals)) / NROW(predictions)

#ROC Curve: https://onlinecourses.science.psu.edu/stat504/node/163
#Most common value to accept as true (1): 0.5
#The ROC of random guessing lies on the diagonal line. 
#The ROC of a perfect diagnostic technique is a point at the upper left corner of the graph
library(pROC)
g <- roc(survived ~ .fitted, data = mm)
plot(g) 

library(ROCR)
p <- predict(model, newdata=subset(test,select=c(2,3,4,5,6,7,8)), type="response")
pr <- prediction(p, test$Survived)
pr <- prediction(predict(bm, type = "response"), titanic$survived)
prf <- performance(pr, measure = "tpr", x.measure = "fpr")
plot(prf)
