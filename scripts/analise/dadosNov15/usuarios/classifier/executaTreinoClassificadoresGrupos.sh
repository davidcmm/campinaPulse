#!/bin/bash

heur=$1

if [ ${heur} == 'extra' ]; then

	#echo "#### Only with urban elements features ####"
	#echo ">> Masculino" >> classifier_testsExtra.dat
	#python classify.py classifier_input.dat train-config gender-masculino >> classifier_testsExtra.dat
	#echo ">> Feminino" >> classifier_testsExtra.dat
	#python classify.py classifier_input.dat train-config gender-feminino >> classifier_testsExtra.dat
	echo ">> Jovem" >> classifier_testsExtra.dat
	python classify.py classifier_input.dat train-config age-jovem >> classifier_testsExtra.dat
	echo ">> Adulto" >> classifier_testsExtra.dat
	python classify.py classifier_input.dat train-config age-adulto >> classifier_testsExtra.dat
	echo ">> Baixa" >> classifier_testsExtra.dat
	python classify.py classifier_input.dat train-config income-baixa >> classifier_testsExtra.dat
	echo ">> Media" >> classifier_testsExtra.dat
	python classify.py classifier_input.dat train-config income-media >> classifier_testsExtra.dat
	echo ">> Solteiro" >> classifier_testsExtra.dat
	python classify.py classifier_input.dat train-config marital-solteiro >> classifier_testsExtra.dat
	echo ">> Casado" >> classifier_testsExtra.dat
	python classify.py classifier_input.dat train-config marital-casado >> classifier_testsExtra.dat
        
elif [ ${heur} == 'knn' ]; then

	echo "#### Only with urban elements features ####"
	echo ">> Masculino" >> classifier_testsKNN.dat
	python classify2.py classifier_input.dat train-config gender-masculino >> classifier_testsKNN.dat
	echo ">> Feminino" >> classifier_testsKNN.dat
	python classify2.py classifier_input.dat train-config gender-feminino >> classifier_testsKNN.dat
	echo ">> Jovem" >> classifier_testsKNN.dat
	python classify2.py classifier_input.dat train-config age-jovem >> classifier_testsKNN.dat
	echo ">> Adulto" >> classifier_testsKNN.dat
	python classify2.py classifier_input.dat train-config age-adulto >> classifier_testsKNN.dat
	echo ">> Baixa" >> classifier_testsKNN.dat
	python classify2.py classifier_input.dat train-config income-baixa >> classifier_testsKNN.dat
	echo ">> Media" >> classifier_testsKNN.dat
	python classify2.py classifier_input.dat train-config income-media >> classifier_testsKNN.dat
	echo ">> Solteiro" >> classifier_testsKNN.dat
	python classify2.py classifier_input.dat train-config marital-solteiro >> classifier_testsKNN.dat
	echo ">> Casado" >> classifier_testsKNN.dat
	python classify2.py classifier_input.dat train-config marital-casado >> classifier_testsKNN.dat

elif [ ${heur} == 'rbf' ]; then

	echo "#### Only with urban elements features ####"
	echo ">> Masculino" >> classifier_testsRBF.dat
	python classify3.py classifier_input.dat train-config gender-masculino >> classifier_testsRBF.dat
	echo ">> Feminino" >> classifier_testsRBF.dat
	python classify3.py classifier_input.dat train-config gender-feminino >> classifier_testsRBF.dat
	echo ">> Jovem" >> classifier_testsRBF.dat
	python classify3.py classifier_input.dat train-config age-jovem >> classifier_testsRBF.dat
	echo ">> Adulto" >> classifier_testsRBF.dat
	python classify3.py classifier_input.dat train-config age-adulto >> classifier_testsRBF.dat
	echo ">> Baixa" >> classifier_testsRBF.dat
	python classify3.py classifier_input.dat train-config income-baixa >> classifier_testsRBF.dat
	echo ">> Media" >> classifier_testsRBF.dat
	python classify3.py classifier_input.dat train-config income-media >> classifier_testsRBF.dat
	echo ">> Solteiro" >> classifier_testsRBF.dat
	python classify3.py classifier_input.dat train-config marital-solteiro >> classifier_testsRBF.dat
	echo ">> Casado" >> classifier_testsRBF.dat
	python classify3.py classifier_input.dat train-config marital-casado >> classifier_testsRBF.dat

elif [ ${heur} == 'linear' ]; then

	echo "#### Only with urban elements features ####"
	echo ">> Masculino" >> classifier_testsLinear.dat
	python classify4.py classifier_input.dat train-config gender-masculino >> classifier_testsLinear.dat
	echo ">> Feminino" >> classifier_testsLinear.dat
	python classify4.py classifier_input.dat train-config gender-feminino >> classifier_testsLinear.dat
	echo ">> Jovem" >> classifier_testsLinear.dat
	python classify4.py classifier_input.dat train-config age-jovem >> classifier_testsLinear.dat
	echo ">> Adulto" >> classifier_testsLinear.dat
	python classify4.py classifier_input.dat train-config age-adulto >> classifier_testsLinear.dat
	echo ">> Baixa" >> classifier_testsLinear.dat
	python classify4.py classifier_input.dat train-config income-baixa >> classifier_testsLinear.dat
	echo ">> Media" >> classifier_testsLinear.dat
	python classify4.py classifier_input.dat train-config income-media >> classifier_testsLinear.dat
	echo ">> Solteiro" >> classifier_testsLinear.dat
	python classify4.py classifier_input.dat train-config marital-solteiro >> classifier_testsLinear.dat
	echo ">> Casado" >> classifier_testsLinear.dat
	python classify4.py classifier_input.dat train-config marital-casado >> classifier_testsLinear.dat

fi

