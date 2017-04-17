#!/bin/bash
#Selects Como é Campina? answers based on users ids, per randomized group, and then computes Q-Scores for selected answers

python sorteia_grupos.py feminino.dat masculino.dat 100

for file in `ls masculino_*.dat`; do

	currentFile=`echo $file | cut -d \_ -f 2 | cut -d . -f 1`
	#python ../selectRunPerUsers.py ../run100/run.csv $file > runMasculino_${currentFile}.csv
	
	#python ../analisaQScore.py runMasculino_${currentFile}.csv 100 ../tasksDef.csv campina
	#mv all.dat allMasculino_${currentFile}.dat

	#sort -k 3 -r -o allMasculino_${currentFile}.dat allMasculino_${currentFile}.dat

	#python ../encontraInterseccao.py ../all100/allFemininoOrd.dat allMasculino_${currentFile}.dat > intersectionAllFemMas_${currentFile}.dat 
	#python ../preparaHTML.py ../all100/allFemininoOrd.dat intersectionAllFemMas_${currentFile}.dat > allFemininoOrdInter_${currentFile}.dat 
	#python ../preparaHTML.py allMasculino_${currentFile}.dat intersectionAllFemMas_${currentFile}.dat > allMasculinoOrdInter_${currentFile}.dat 
	#rm question.html

	#Building all evaluations with only selected men, this means removing men that were not sorted in current group
	python sorteia_grupos_geral.py masculino masculino_${currentFile}.dat
	python ../selectRunPerUsers.py ../run100/run.csv diff_masculino_${currentFile}.dat > runDiffMasculino_${currentFile}.csv
	python ../analisaQScore.py runDiffMasculino_${currentFile}.csv 100 ../tasksDef.csv campina
	mv all.dat allDiffMasculino_${currentFile}.dat

	sort -k 3 -r -o allDiffMasculino_${currentFile}.dat allDiffMasculino_${currentFile}.dat
done


