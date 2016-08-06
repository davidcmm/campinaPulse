#!/bin/bash

echo "#### Only with urban elements features ####" >> classifier_tests_features_importances.dat
echo ">> Masculino" >> classifier_tests_features_importances.dat
python classify4.py classifier_input.dat importances gender-masculino >> classifier_tests_features_importances.dat
echo ">> Feminino" >> classifier_tests_features_importances.dat
python classify4.py classifier_input.dat importances gender-feminino >> classifier_tests_features_importances.dat
echo ">> Jovem" >> classifier_tests_features_importances.dat
python classify4.py classifier_input.dat importances age-jovem >> classifier_tests_features_importances.dat
echo ">> Adulto" >> classifier_tests_features_importances.dat
python classify4.py classifier_input.dat importances age-adulto >> classifier_tests_features_importances.dat
echo ">> Baixa" >> classifier_tests_features_importances.dat
python classify4.py classifier_input.dat importances income-baixa >> classifier_tests_features_importances.dat
echo ">> Media" >> classifier_tests_features_importances.dat
python classify4.py classifier_input.dat importances income-media >> classifier_tests_features_importances.dat
echo ">> Solteiro" >> classifier_tests_features_importances.dat
python classify4.py classifier_input.dat importances marital-solteiro >> classifier_tests_features_importances.dat
echo ">> Casado" >> classifier_tests_features_importances.dat
python classify4.py classifier_input.dat importances marital-casado >> classifier_tests_features_importances.dat

