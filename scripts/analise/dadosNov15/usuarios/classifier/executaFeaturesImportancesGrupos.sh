#!/bin/bash

for input_file in classifier_input_rnr.dat ; do
#classifier_input_3classes.dat ; do

	outputSpec=''
	if [ ${input_file} == 'classifier_input_lnl.dat' ] ; then
		outputSpec='lnl'
	elif [ ${input_file} == 'classifier_input_rnr.dat' ] ; then
		outputSpec='rnr'
	else
		outputSpec='3classes'
	fi

	echo "#### Only with urban elements features ####" >> classifier_tests_features_importances_${outputSpec}.dat
	echo ">> Masculino" >> classifier_tests_features_importances_${outputSpec}.dat
	python classify.py ${input_file} importances gender-masculino >> classifier_tests_features_importances_${outputSpec}.dat
	echo ">> Feminino" >> classifier_tests_features_importances_${outputSpec}.dat
	python classify.py ${input_file} importances gender-feminino >> classifier_tests_features_importances_${outputSpec}.dat
	echo ">> Jovem" >> classifier_tests_features_importances_${outputSpec}.dat
	python classify.py ${input_file} importances age-jovem >> classifier_tests_features_importances_${outputSpec}.dat
	echo ">> Adulto" >> classifier_tests_features_importances_${outputSpec}.dat
	python classify.py ${input_file} importances age-adulto >> classifier_tests_features_importances_${outputSpec}.dat
	echo ">> Baixa" >> classifier_tests_features_importances_${outputSpec}.dat
	python classify.py ${input_file} importances income-baixa >> classifier_tests_features_importances_${outputSpec}.dat
	echo ">> Media" >> classifier_tests_features_importances_${outputSpec}.dat
	python classify.py ${input_file} importances income-media >> classifier_tests_features_importances_${outputSpec}.dat
	echo ">> Solteiro" >> classifier_tests_features_importances_${outputSpec}.dat
	python classify.py ${input_file} importances marital-solteiro >> classifier_tests_features_importances_${outputSpec}.dat
	echo ">> Casado" >> classifier_tests_features_importances_${outputSpec}.dat
	python classify.py ${input_file} importances marital-casado >> classifier_tests_features_importances_${outputSpec}.dat

done

