library(RSofia)
library(dplyr)

data(irismod)

i.TRAIN <- sample(1:nrow(irismod), 100)
model.logreg <- sofia(Is.Virginica ~ ., data=irismod[i.TRAIN,], learner_type = "logreg-pegasos")#Selecting some lines

p <- predict(model.logreg, newdata=irismod[-1*i.TRAIN,], prediction_type = "logistic")#Predicting for other lines!
table(predicted=p>0.5, actual=irismod[-1*i.TRAIN,]$Is.Virginica)

#Reading input in classifier format
dataCampina <- read.table("classifier_input.dat", header=TRUE, sep="\t")

#Training with all predicors
toTrain <- sample(1:nrow(dataCampina), nrow(dataCampina)*0.8)
model.logreg <- sofia(choice ~ age + gender + income + marital + street_wid1 + mov_cars1 + park_cars1 + 
                        mov_ciclyst1 + landscape1 + build_ident1 + trees1 + build_height1 + diff_build1 + 
                        people1 + graffiti1 + bairro1 + street_wid2 + mov_cars2 + park_cars2 + mov_ciclyst2 + 
                        landscape2 + build_ident2 + trees2 + build_height2 + diff_build2 + people2 + graffiti2 +
                        bairro2, data=dataCampina[toTrain,], learner_type = "logreg-pegasos")#Selecting some lines
p <- predict(model.logreg, newdata = dataCampina[-1*toTrain,], prediction_type = "logistic")#Predicting for other lines!
table(predicted = p>0.5, actual = dataCampina[-1*toTrain,]$choice)

#Training only with image descriptors!
toTrain <- sample(1:nrow(dataCampina), nrow(dataCampina)*0.8)
model.logreg <- sofia(choice ~ street_wid1 + mov_cars1 + park_cars1 + 
                        mov_ciclyst1 + landscape1 + build_ident1 + trees1 + build_height1 + diff_build1 + 
                        people1 + graffiti1 + bairro1 + street_wid2 + mov_cars2 + park_cars2 + mov_ciclyst2 + 
                        landscape2 + build_ident2 + trees2 + build_height2 + diff_build2 + people2 + graffiti2 +
                        bairro2, data=dataCampina[toTrain,], learner_type = "logreg-pegasos")#Selecting some lines
p <- predict(model.logreg, newdata = dataCampina[-1*toTrain,], prediction_type = "logistic")#Predicting for other lines!
table(predicted = p>0.5, actual = dataCampina[-1*toTrain,]$choice)
