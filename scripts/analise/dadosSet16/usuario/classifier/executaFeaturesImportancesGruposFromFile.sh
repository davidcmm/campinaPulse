#!/bin/bash

for input_file in classifier_input_wodraw.dat classifier_input_3classes.dat ; do
#classifier_input_rnr.dat ; do
#classifier_input_3classes.dat ; do

	outputSpec=''
	if [ ${input_file} == 'classifier_input_lnl.dat' ] ; then
		outputSpec='lnl'
		importancesFile=''
	elif [ ${input_file} == 'classifier_input_rnr.dat' ] ; then
		outputSpec='rnr'
		importancesFile=''
	elif [ ${input_file} == 'classifier_input_wodraw.dat' ] ; then
		outputSpec='wodraw'
		importancesFile='classifier_tests_features_importances_userout_wodraw.dat '
	else
		outputSpec='3classes'
		importancesFile='classifier_tests_features_importances_userout_3classes.dat '
	fi

	python classify.py ${input_file} importances-file ${importances_File}

done

