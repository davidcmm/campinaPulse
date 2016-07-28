library(RSofia)

data(irismod)

i.TRAIN <- sample(1:nrow(irismod), 100)
model.logreg <- sofia(Is.Virginica ~ ., data=irismod[i.TRAIN,], learner_type = "logreg-pegasos")#Selecting some lines

p <- predict(model.logreg, newdata=irismod[-1*i.TRAIN,], prediction_type = "logistic")#Predicting for other lines!
table(predicted=p>0.5, actual=irismod[-1*i.TRAIN,]$Is.Virginica)
