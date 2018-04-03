#!/bin/bash

for i in $(seq 20 60); do
	file="../../backupBanco/ranking_predictions/run_80_${i}.csv"

	python compute_elo.py $file ../../backupBanco/tasksDef.csv 10000 10
	mv all_elo.dat ranking_predictions/all_elo_80_10_${i}.dat

	python compute_elo.py $file ../../backupBanco/tasksDef.csv 10000 20
	mv all_elo.dat ranking_predictions/all_elo_80_20_${i}.dat

	python compute_elo.py $file ../../backupBanco/tasksDef.csv 10000 40
	mv all_elo.dat ranking_predictions/all_elo_80_40_${i}.dat
done

for i in $(seq 156 170); do
        file="../../backupBanco/ranking_predictions/run_80_${i}.csv"

        python compute_elo.py $file ../../backupBanco/tasksDef.csv 10000 10
        mv all_elo.dat ranking_predictions/all_elo_80_10_${i}.dat

        python compute_elo.py $file ../../backupBanco/tasksDef.csv 10000 20
        mv all_elo.dat ranking_predictions/all_elo_80_20_${i}.dat

        python compute_elo.py $file ../../backupBanco/tasksDef.csv 10000 40
        mv all_elo.dat ranking_predictions/all_elo_80_40_${i}.dat
done
