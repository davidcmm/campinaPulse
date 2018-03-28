#!/bin/bash

for i in $(seq 0 499); do
	file="/local/david/pybossa_env/campinaPulse/scripts/analise/dadosSet16/backupBanco/ranking_predictions/run_80_${i}.csv"

	python3 perform_crowdbt_campina.py $file /local/david/pybossa_env/campinaPulse/scripts/analise/dadosSet16/backupBanco/tasksDef.csv ranking 1
	mv allPairwiseComparison.dat /local/david/pybossa_env/campinaPulse/scripts/analise/dadosSet16/usuarios/gavel/ranking_predictions/all_crowdbt_80-lam01-gam01_${i}.dat
done
