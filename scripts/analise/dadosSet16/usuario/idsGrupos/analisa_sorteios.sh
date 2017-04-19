#!/bin/bash
#Selects Como é Campina? answers based on users ids, per randomized group, and then computes Q-Scores for selected answers

#python sorteia_grupos.py igual feminino.dat masculino.dat 100 #Creates ids files from second file with same size of first file
#python sorteia_grupos.py desb 60 40 feminino.dat masculino.dat 100 #Creates ids files from each file according to corresponding sizes specified first

#Iterating through each generated men files and comparing to a reference women file
#for file in `ls masculino_*.dat`; do
#
#	currentFile=`echo $file | cut -d \_ -f 2 | cut -d . -f 1`
#	python ../selectRunPerUsers.py ../run100/run.csv $file run > runMasculino_${currentFile}.csv
#	
#	python ../analisaQScore.py runMasculino_${currentFile}.csv 100 ../tasksDef.csv campina
#	mv all.dat allMasculino_${currentFile}.dat
#
#	sort -k 3 -r -o allMasculino_${currentFile}.dat allMasculino_${currentFile}.dat
#
#	python ../encontraInterseccao.py ../all100/allFemininoOrd.dat allMasculino_${currentFile}.dat > intersectionAllFemMas_${currentFile}.dat 
#	python ../preparaHTML.py ../all100/allFemininoOrd.dat intersectionAllFemMas_${currentFile}.dat > allFemininoOrdInter_${currentFile}.dat 
#	python ../preparaHTML.py allMasculino_${currentFile}.dat intersectionAllFemMas_${currentFile}.dat > allMasculinoOrdInter_${currentFile}.dat 
#	rm question.html
#
	#Building all evaluations with only selected men, this means removing men that were not sorted in current group
#	python sorteia_grupos_geral.py masculino masculino_${currentFile}.dat
#	python ../selectRunPerUsers.py ../run100/run.csv diff_masculino_${currentFile}.dat remove > runDiffMasculino_${currentFile}.csv
#	python ../analisaQScore.py runDiffMasculino_${currentFile}.csv 100 ../tasksDef.csv campina
#	mv all.dat allDiffMasculino_${currentFile}.dat
#
#	sort -k 3 -r -o allDiffMasculino_${currentFile}.dat allDiffMasculino_${currentFile}.dat
#done

#Iterating through each generated men and women files
for i in {0..99}; do 

	#currentFile=`echo $file | cut -d \_ -f 2 | cut -d . -f 1`
	python ../selectRunPerUsers.py ../run100/run.csv masculino_${i}.dat run > runMasculino_${i}.csv
	python ../selectRunPerUsers.py ../run100/run.csv feminino_${i}.dat run > runFeminino_${i}.csv
	
	python ../analisaQScore.py runMasculino_${i}.csv 100 ../tasksDef.csv campina
	mv all.dat allMasculino_${i}.dat
	python ../analisaQScore.py runFeminino_${i}.csv 100 ../tasksDef.csv campina
	mv all.dat allFeminino_${i}.dat

	sort -k 3 -r -o allMasculino_${i}.dat allMasculino_${i}.dat
	sort -k 3 -r -o allFeminino_${i}.dat allFeminino_${i}.dat

	python ../encontraInterseccao.py allFeminino_${i}.dat allMasculino_${i}.dat > intersectionAllFemMas_${i}.dat 
	python ../preparaHTML.py allFeminino_${i}.dat intersectionAllFemMas_${i}.dat > allFemininoOrdInter_${i}.dat 
	rm question.html
	python ../preparaHTML.py allMasculino_${i}.dat intersectionAllFemMas_${i}.dat > allMasculinoOrdInter_${i}.dat 
	rm question.html

	#Building all evaluations with only selected users, this means removing users that were not sorted in current group
	python sorteia_grupos_geral.py masculino masculino_${i}.dat
	python sorteia_grupos_geral.py feminino feminino_${i}.dat

	python ../selectRunPerUsers.py ../run100/run.csv diff_masculino_${i}.dat remove > runDiffMasculino_${i}.csv
	python ../selectRunPerUsers.py ../run100/run.csv diff_feminino_${i}.dat remove > runDiffFeminino_${i}.csv

	python ../analisaQScore.py runDiffMasculino_${i}.csv 100 ../tasksDef.csv campina
	mv all.dat allDiffMasculino_${i}.dat
	python ../analisaQScore.py runDiffFeminino_${i}.csv 100 ../tasksDef.csv campina
	mv all.dat allDiffFeminino_${i}.dat

	sort -k 3 -r -o allDiffMasculino_${i}.dat allDiffMasculino_${i}.dat
	sort -k 3 -r -o allDiffFeminino_${i}.dat allDiffFeminino_${i}.dat
done


