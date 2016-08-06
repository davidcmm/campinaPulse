#!/bin/bash

echo "#### Only with urban elements features ####" >> classifier_output_groups_wo_user_features.dat
echo ">> Masculino" >> classifier_output_groups_wo_user_features.dat
python classify4.py classifier_input.dat importances gender-masculino >> classifier_output_groups_wo_user_features.dat
echo ">> Feminino" >> classifier_output_groups_wo_user_features.dat
python classify4.py classifier_input.dat importances gender-feminino >> classifier_output_groups_wo_user_features.dat
echo ">> Jovem" >> classifier_output_groups_wo_user_features.dat
python classify4.py classifier_input.dat importances age-jovem >> classifier_output_groups_wo_user_features.dat
echo ">> Adulto" >> classifier_output_groups_wo_user_features.dat
python classify4.py classifier_input.dat importances age-adulto >> classifier_output_groups_wo_user_features.dat
echo ">> Baixa" >> classifier_output_groups_wo_user_features.dat
python classify4.py classifier_input.dat importances income-baixa >> classifier_output_groups_wo_user_features.dat
echo ">> Media" >> classifier_output_groups_wo_user_features.dat
python classify4.py classifier_input.dat importances income-media >> classifier_output_groups_wo_user_features.dat
echo ">> Solteiro" >> classifier_output_groups_wo_user_features.dat
python classify4.py classifier_input.dat importances marital-solteiro >> classifier_output_groups_wo_user_features.dat
echo ">> Casado" >> classifier_output_groups_wo_user_features.dat
python classify4.py classifier_input.dat importances marital-casado >> classifier_output_groups_wo_user_features.dat

