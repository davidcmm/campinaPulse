#!/bin/bash

for i in $(seq 0 499); do
	file="../../backupBanco/ranking_predictions/run_80_${i}.csv"

	python ../analisaQScore.py $file 100 ../../backupBanco/tasksDef.csv campina
	mv all.dat ranking_predictions/all_qscore_80_${i}.dat
	mv all.dat-maxdiff ranking_predictions/all.dat-maxdiff_80_${i}
done
