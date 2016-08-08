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

	if [ ${heur} == 'extra' ]; then

		echo "#### Only with urban elements features ####" >> classifier_testsExtra_${outputSpec}.dat
		echo ">> Masculino" >> classifier_testsExtra_${outputSpec}.dat
		python classify.py ${input_file} train-config gender-masculino >> classifier_testsExtra_${outputSpec}.dat
		echo ">> Feminino" >> classifier_testsExtra_${outputSpec}.dat
		python classify.py ${input_file} train-config gender-feminino >> classifier_testsExtra_${outputSpec}.dat
		echo ">> Jovem" >> classifier_testsExtra_${outputSpec}.dat
		python classify.py ${input_file} train-config age-jovem >> classifier_testsExtra_${outputSpec}.dat
		echo ">> Adulto" >> classifier_testsExtra_${outputSpec}.dat
		python classify.py ${input_file} train-config age-adulto >> classifier_testsExtra_${outputSpec}.dat
		echo ">> Baixa" >> classifier_testsExtra_${outputSpec}.dat
		python classify.py ${input_file} train-config income-baixa >> classifier_testsExtra_${outputSpec}.dat
		echo ">> Media" >> classifier_testsExtra_${outputSpec}.dat
		python classify.py ${input_file} train-config income-media >> classifier_testsExtra_${outputSpec}.dat
		echo ">> Solteiro" >> classifier_testsExtra_${outputSpec}.dat
		python classify.py ${input_file} train-config marital-solteiro >> classifier_testsExtra_${outputSpec}.dat
		echo ">> Casado" >> classifier_testsExtra_${outputSpec}.dat
		python classify.py ${input_file} train-config marital-casado >> classifier_testsExtra_${outputSpec}.dat
		
	elif [ ${heur} == 'knn' ]; then

		echo "#### Only with urban elements features ####" >> classifier_testsKNN_${outputSpec}.dat
		echo ">> Masculino" >> classifier_testsKNN_${outputSpec}.dat
		python classify2.py ${input_file} train-config gender-masculino >> classifier_testsKNN_${outputSpec}.dat
		echo ">> Feminino" >> classifier_testsKNN_${outputSpec}.dat
		python classify2.py ${input_file} train-config gender-feminino >> classifier_testsKNN_${outputSpec}.dat
		echo ">> Jovem" >> classifier_testsKNN_${outputSpec}.dat
		python classify2.py ${input_file} train-config age-jovem >> classifier_testsKNN_${outputSpec}.dat
		echo ">> Adulto" >> classifier_testsKNN_${outputSpec}.dat
		python classify2.py ${input_file} train-config age-adulto >> classifier_testsKNN_${outputSpec}.dat
		echo ">> Baixa" >> classifier_testsKNN_${outputSpec}.dat
		python classify2.py ${input_file} train-config income-baixa >> classifier_testsKNN_${outputSpec}.dat
		echo ">> Media" >> classifier_testsKNN_${outputSpec}.dat
		python classify2.py ${input_file} train-config income-media >> classifier_testsKNN_${outputSpec}.dat
		echo ">> Solteiro" >> classifier_testsKNN_${outputSpec}.dat
		python classify2.py ${input_file} train-config marital-solteiro >> classifier_testsKNN_${outputSpec}.dat
		echo ">> Casado" >> classifier_testsKNN_${outputSpec}.dat
		python classify2.py ${input_file} train-config marital-casado >> classifier_testsKNN_${outputSpec}.dat

	elif [ ${heur} == 'rbf' ]; then

		echo "#### Only with urban elements features ####" >> classifier_testsRBF_${outputSpec}.dat
		echo ">> Masculino" >> classifier_testsRBF_${outputSpec}.dat
		python classify3.py ${input_file} train-config gender-masculino >> classifier_testsRBF_${outputSpec}.dat
		echo ">> Feminino" >> classifier_testsRBF_${outputSpec}.dat
		python classify3.py ${input_file} train-config gender-feminino >> classifier_testsRBF_${outputSpec}.dat
		echo ">> Jovem" >> classifier_testsRBF_${outputSpec}.dat
		python classify3.py ${input_file} train-config age-jovem >> classifier_testsRBF_${outputSpec}.dat
		echo ">> Adulto" >> classifier_testsRBF_${outputSpec}.dat
		python classify3.py ${input_file} train-config age-adulto >> classifier_testsRBF_${outputSpec}.dat
		echo ">> Baixa" >> classifier_testsRBF_${outputSpec}.dat
		python classify3.py ${input_file} train-config income-baixa >> classifier_testsRBF_${outputSpec}.dat
		echo ">> Media" >> classifier_testsRBF_${outputSpec}.dat
		python classify3.py ${input_file} train-config income-media >> classifier_testsRBF_${outputSpec}.dat
		echo ">> Solteiro" >> classifier_testsRBF_${outputSpec}.dat
		python classify3.py ${input_file} train-config marital-solteiro >> classifier_testsRBF_${outputSpec}.dat
		echo ">> Casado" >> classifier_testsRBF_${outputSpec}.dat
		python classify3.py ${input_file} train-config marital-casado >> classifier_testsRBF_${outputSpec}.dat

	elif [ ${heur} == 'linear' ]; then

		echo "#### Only with urban elements features ####" >> classifier_testsLinear_${outputSpec}.dat
		echo ">> Masculino" >> classifier_testsLinear_${outputSpec}.dat
		python classify4.py ${input_file} train-config gender-masculino >> classifier_testsLinear_${outputSpec}.dat
		echo ">> Feminino" >> classifier_testsLinear_${outputSpec}.dat
		python classify4.py ${input_file} train-config gender-feminino >> classifier_testsLinear_${outputSpec}.dat
		echo ">> Jovem" >> classifier_testsLinear_${outputSpec}.dat
		python classify4.py ${input_file} train-config age-jovem >> classifier_testsLinear_${outputSpec}.dat
		echo ">> Adulto" >> classifier_testsLinear_${outputSpec}.dat
		python classify4.py ${input_file} train-config age-adulto >> classifier_testsLinear_${outputSpec}.dat
		echo ">> Baixa" >> classifier_testsLinear_${outputSpec}.dat
		python classify4.py ${input_file} train-config income-baixa >> classifier_testsLinear_${outputSpec}.dat
		echo ">> Media" >> classifier_testsLinear_${outputSpec}.dat
		python classify4.py ${input_file} train-config income-media >> classifier_testsLinear_${outputSpec}.dat
		echo ">> Solteiro" >> classifier_testsLinear_${outputSpec}.dat
		python classify4.py ${input_file} train-config marital-solteiro >> classifier_testsLinear_${outputSpec}.dat
		echo ">> Casado" >> classifier_testsLinear_${outputSpec}.dat
		python classify4.py ${input_file} train-config marital-casado >> classifier_testsLinear_${outputSpec}.dat

	fi
done
