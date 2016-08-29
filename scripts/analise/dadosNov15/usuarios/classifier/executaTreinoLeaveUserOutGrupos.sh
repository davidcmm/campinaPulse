#!/bin/bash

heur=$1

for input_file in classifier_input_wodraw.dat ; do
#classifier_input_lnl.dat classifier_input_rnr.dat ; do

	outputSpec=''
	if [ ${input_file} == 'classifier_input_lnl.dat' ] ; then
		outputSpec='lnl'
	elif [ ${input_file} == 'classifier_input_rnr.dat' ] ; then
		outputSpec='rnr'
	elif [ ${input_file} == 'classifier_input_wodraw.dat' ] ; then
		outputSpec='wodraw'
	else
		outputSpec='3classes'
	fi


	echo "#### Only with urban elements features ####" >> classifier_testsExtra_${outputSpec}.dat
	echo ">> Masculino" >> classifier_testsExtra_userout_${outputSpec}.dat
	python classify.py ${input_file} train-user-out gender-masculino >> classifier_testsExtra_userout_${outputSpec}.dat
	echo ">> Feminino" >> classifier_testsExtra_userout_${outputSpec}.dat
	python classify.py ${input_file} train-user-out gender-feminino >> classifier_testsExtra_userout_${outputSpec}.dat
	echo ">> Jovem" >> classifier_testsExtra_userout_${outputSpec}.dat
	python classify.py ${input_file} train-user-out age-jovem >> classifier_testsExtra_userout_${outputSpec}.dat
	echo ">> Adulto" >> classifier_testsExtra_userout_${outputSpec}.dat
	python classify.py ${input_file} train-user-out age-adulto >> classifier_testsExtra_userout_${outputSpec}.dat
	echo ">> Baixa" >> classifier_testsExtra_userout_${outputSpec}.dat
	python classify.py ${input_file} train-user-out income-baixa >> classifier_testsExtra_userout_${outputSpec}.dat
	echo ">> Media" >> classifier_testsExtra_userout_${outputSpec}.dat
	python classify.py ${input_file} train-user-out income-media >> classifier_testsExtra_userout_${outputSpec}.dat
	echo ">> Solteiro" >> classifier_testsExtra_userout_${outputSpec}.dat
	python classify.py ${input_file} train-user-out marital-solteiro >> classifier_testsExtra_userout_${outputSpec}.dat
	echo ">> Casado" >> classifier_testsExtra_userout_${outputSpec}.dat
	python classify.py ${input_file} train-user-out marital-casado >> classifier_testsExtra_userout_${outputSpec}.dat
	
done
