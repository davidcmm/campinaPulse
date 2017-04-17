#!/bin/bash
#Selects Como é Campina? answers based on users ids, per randomized group, and then computes Q-Scores for selected answers

for file in `ls masculino_*.dat`; do

	currentFile=`echo $file | cut -d \_ -f 2 | cut -d . -f 1`
	python ../selectRunPerUsers.py ../run100/run.csv $file > runMasculino_${currentFile}.csv
	
	python ../analisaQScore.py runMasculino_${currentFile}.csv 100 ../tasksDef.csv campina
	mv all.dat allMasculino_${currentFile}.dat

done


