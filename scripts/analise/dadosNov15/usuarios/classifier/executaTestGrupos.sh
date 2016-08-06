#!/bin/bash

echo "#### Only with urban elements features ####" >> classifier_output_groups_wo_user_features.dat
echo ">> Masculino" >> classifier_output_groups_wo_user_features.dat
python classify.py classifier_input.dat test gender-masculino >> classifier_output_groups_wo_user_features.dat
echo ">> Feminino" >> classifier_output_groups_wo_user_features.dat
python classify.py classifier_input.dat test gender-feminino >> classifier_output_groups_wo_user_features.dat
echo ">> Jovem" >> classifier_output_groups_wo_user_features.dat
python classify.py classifier_input.dat test age-jovem >> classifier_output_groups_wo_user_features.dat
echo ">> Adulto" >> classifier_output_groups_wo_user_features.dat
python classify.py classifier_input.dat test age-adulto >> classifier_output_groups_wo_user_features.dat
echo ">> Baixa" >> classifier_output_groups_wo_user_features.dat
python classify.py classifier_input.dat test income-baixa >> classifier_output_groups_wo_user_features.dat
echo ">> Media" >> classifier_output_groups_wo_user_features.dat
python classify.py classifier_input.dat test income-media >> classifier_output_groups_wo_user_features.dat
echo ">> Solteiro" >> classifier_output_groups_wo_user_features.dat
python classify.py classifier_input.dat test marital-solteiro >> classifier_output_groups_wo_user_features.dat
echo ">> Casado" >> classifier_output_groups_wo_user_features.dat
python classify.py classifier_input.dat test marital-casado >> classifier_output_groups_wo_user_features.dat

