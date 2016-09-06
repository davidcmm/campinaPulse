#!/bin/bash

input_file=$1

#for input_file in classifier_input_wodraw.dat ; do
#classifier_input_lnl.dat classifier_input_rnr.dat ; do

echo "Arquivo de entrada ${input_file}"

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


echo "#### Leave User out with other groups properties in input and mean classif config ####" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
echo ">> Masculino" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
python classify.py ${input_file} train-user-out gender-masculino >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
echo ">> Feminino" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
python classify.py ${input_file} train-user-out gender-feminino >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
echo ">> Jovem" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
python classify.py ${input_file} train-user-out age-jovem >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
echo ">> Adulto" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
python classify.py ${input_file} train-user-out age-adulto >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
echo ">> Baixa" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
python classify.py ${input_file} train-user-out income-baixa >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
echo ">> Media" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
python classify.py ${input_file} train-user-out income-media >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
echo ">> Solteiro" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
python classify.py ${input_file} train-user-out marital-solteiro >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
echo ">> Casado" >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
python classify.py ${input_file} train-user-out marital-casado >> classifier_output_groups_userout_w_user_features_${outputSpec}.dat
	
#done
