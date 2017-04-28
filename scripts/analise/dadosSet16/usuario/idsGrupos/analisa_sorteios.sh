#!/bin/bash
#Selects Como é Campina? answers based on users ids, per randomized group, and then computes Q-Scores for selected answers

#for group in "masculino-feminino"; do #"jovem-adulto" "media-baixa" ; do #"masculino-feminino" "jovem-adulto" "media-baixa"
#
#	group1=`echo $group | cut -d \- -f 1`
#	group2=`echo $group | cut -d \- -f 2`
#
#	for desb in "60-15" ; do #"60-40" "15-60" "40-60" ; do
#
#		size1=`echo $desb | cut -d \- -f 1`
#		size2=`echo $desb | cut -d \- -f 2`
#
#		mkdir ${group1}${size1}_${group2}${size2}
#	
#		#python sorteia_grupos.py igual feminino.dat masculino.dat 100 #Creates ids files from second file with same size of first file
#		python sorteia_grupos.py desb ${size2} ${size1} ${group2}.dat ${group1}.dat 100 #Creates ids files from each file according to corresponding sizes specified first
#
#		#Iterating through each generated men files and comparing to a reference women file
#		#for file in `ls masculino_*.dat`; do
#		#
#		#	currentFile=`echo $file | cut -d \_ -f 2 | cut -d . -f 1`
#		#	python ../selectRunPerUsers.py ../run100/run.csv $file run > runMasculino_${currentFile}.csv
#		#	
#		#	python ../analisaQScore.py runMasculino_${currentFile}.csv 100 ../tasksDef.csv campina
#		#	mv all.dat allMasculino_${currentFile}.dat
#		#
#		#	sort -k 3 -r -o allMasculino_${currentFile}.dat allMasculino_${currentFile}.dat
#		#
#		#	python ../encontraInterseccao.py ../all100/allFemininoOrd.dat allMasculino_${currentFile}.dat > intersectionAllFemMas_${currentFile}.dat 
#		#	python ../preparaHTML.py ../all100/allFemininoOrd.dat intersectionAllFemMas_${currentFile}.dat > allFemininoOrdInter_${currentFile}.dat 
#		#	python ../preparaHTML.py allMasculino_${currentFile}.dat intersectionAllFemMas_${currentFile}.dat > allMasculinoOrdInter_${currentFile}.dat 
#		#	rm question.html
#		#
#			#Building all evaluations with only selected men, this means removing men that were not sorted in current group
#		#	python sorteia_grupos_geral.py masculino masculino_${currentFile}.dat
#		#	python ../selectRunPerUsers.py ../run100/run.csv homMul_95/diff_masculino_${currentFile}.dat remove > homMul_95/runDiffMasculino_${currentFile}.csv
#		#	python ../analisaQScore.py homMul_95/runDiffMasculino_${currentFile}.csv 100 ../tasksDef.csv campina
#		#	mv all.dat homMul_95/allDiffMasculino_${currentFile}.dat
#		#
#		#	sort -k 3 -r -o homMul_95/allDiffMasculino_${currentFile}.dat homMul_95/allDiffMasculino_${currentFile}.dat
#		#done
#
#		#Iterating through each generated men and women files
#		for i in {0..99}; do 
#
#			#currentFile=`echo $file | cut -d \_ -f 2 | cut -d . -f 1`
#			python ../selectRunPerUsers.py ../run100/run.csv ${group1}_${i}.dat run > run${group1}_${i}.csv
#			python ../selectRunPerUsers.py ../run100/run.csv ${group2}_${i}.dat run > run${group2}_${i}.csv
#	
#			python ../analisaQScore.py run${group1}_${i}.csv 100 ../tasksDef.csv campina
#			mv all.dat all${group1}_${i}.dat
#			python ../analisaQScore.py run${group2}_${i}.csv 100 ../tasksDef.csv campina
#			mv all.dat all${group2}_${i}.dat
#
#			sort -k 3 -r -o all${group1}_${i}.dat all${group1}_${i}.dat
#			sort -k 3 -r -o all${group2}_${i}.dat all${group2}_${i}.dat
#
#			python ../encontraInterseccao.py all${group2}_${i}.dat all${group1}_${i}.dat > intersectionAll${group2}${group1}_${i}.dat 
#			python ../preparaHTML.py all${group2}_${i}.dat intersectionAll${group2}${group1}_${i}.dat > all${group2}OrdInter_${i}.dat 
#			rm question.html
#			python ../preparaHTML.py all${group1}_${i}.dat intersectionAll${group2}${group1}_${i}.dat > all${group1}OrdInter_${i}.dat 
#			rm question.html
#
#			#Building all evaluations with only selected men, this means removing men that were not sorted in current group
#			python sorteia_grupos_geral.py ${group1} ${group1}_${i}.dat
#			python sorteia_grupos_geral.py ${group2} ${group2}_${i}.dat
#
#			python ../selectRunPerUsers.py ../run100/run.csv diff_${group1}_${i}.dat diff_${group2}_${i}.dat remove > runDiff${group2}${group1}_${i}.csv
#			#python ../selectRunPerUsers.py ../run100/run.csv diff_feminino_${i}.dat remove > runDiffFeminino_${i}.csv
#
#			python ../analisaQScore.py runDiff${group2}${group1}_${i}.csv 100 ../tasksDef.csv campina
#			mv all.dat allDiff${group2}${group1}_${i}.dat
#			#python ../analisaQScore.py runDiffFeminino_${i}.csv 100 ../tasksDef.csv campina
#			#mv all.dat allDiffFeminino_${i}.dat
#
#			sort -k 3 -r -o allDiff${group2}${group1}_${i}.dat allDiff${group2}${group1}_${i}.dat
#			#sort -k 3 -r -o allDiffFeminino_${i}.dat allDiffFeminino_${i}.dat
#		done
#		mv run*_*.csv all*_*.dat intersectionAll*.dat diff_*.dat ${group1}_*.dat ${group2}_*.dat ${group1}${size1}_${group2}${size2}
#	done
#done

#Creating files to be used for logit models
for folder in "hom60_mul15" "hom40_mul60" "hom95_mul95" "hom15_mul60" "jovem15_adulto60" "jovem40_adulto60" "jovem60_adulto40" "jovem60_adulto15" "media15_baixa60" "media40_baixa60" "media60_baixa40" "media60_baixa15" ; do

	if [[ $folder =~ .*hom.* ]] ; then 
		group1="masculino"
		group2="feminino" 
        elif [[ $folder =~ .*jovem.* ]] ; then 
		group1="jovem"
		group2="adulto"
        elif [[ $folder =~ .*baixa.* ]] ; then 
		group1="baixa"
		group2="media"  
	fi

	for i in {0..99}; do
	#for runFile in `ls ${folder}/runmasculino_*.csv` ; do
		runFile1="${folder}/run${group1}_${i}.csv"
		runFile2="${folder}/run${group2}_${i}.csv"

		cat $runFile1 $runFile2 >> runMerged_${i}.csv
		runFile="runMerged_${i}.csv"

		python ../classifier/createInputForClassification.py create $runFile ../tasksDef.csv ../usersInfo.dat ../classifier/images_description.dat > classifier_input_3classes.dat 
		python ../classifier/createInputForClassification.py convert $runFile ../tasksDef.csv ../usersInfo.dat ../classifier/images_description.dat 
		mv classifier_input_3classes.dat $folder/runMerged_${i}_3classes.dat
		mv classifier_input_wodraw.dat $folder/runMerged_${i}_wodraw.dat
	done
done


