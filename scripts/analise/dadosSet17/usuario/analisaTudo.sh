#!/bin/bash


#### COMPUTING PERCEPTIONS FOR A STREET
sed -i -e 's/^/N/g' ../backupBanco/run.csv #Adding identifier in the beggining of each line
sed -i -e 's/""/"/g' ../backupBanco/run.csv 
sed -i -e 's/""/"/g' ../backupBanco/tasksDef.csv

#Creating folders for groups
mkdir idsGerais
mkdir idsCampina
mkdir idsNotCampina 

#Separating all users into groups
python analisaUsuarios.py run.csv run.csv

python separaGrupo.py separa usersInfo.dat users_notcampina_campina.dat
sort -t "|" -k 1 -g -o usersInfo.dat usersInfo.dat

mv campina.dat casado.dat adulto.dat baixa.dat catole.dat centro.dat feminino.dat jovem.dat liberdade.dat masculino.dat media.dat medio.dat notcampina.dat notcatole.dat notcentro.dat notliberdade.dat posgrad.dat solteiro.dat usersInfo*.dat usersNAnswered.dat usersPhotos* idsGerais/

#Must run in percepcaoLocal/agradavel folder
python marcaImagem.py #All users
python marcaImagem.py ../../usuario/idsGrupos/notcampina.dat notcampina > debug.dat #Only users of notcampina group
python marcaImagem.py ../../usuario/idsGrupos/campina.dat campina > debug.dat #Only users of campina group

#Split users
python selectRunPerUsers.py ../backupBanco/run.csv ../backupBanco/notcampina.dat > run100/runnotCampina.csv
python selectRunPerUsers.py ../backupBanco/run.csv ../backupBanco/campina.dat > run100/runCampina.csv

python selectRunPerUsers.py ../backupBanco/run.csv ../backupBanco/masculino.dat > run100/runMasculino.csv
python selectRunPerUsers.py ../backupBanco/run.csv ../backupBanco/feminino.dat > run100/runFeminino.csv
python selectRunPerUsers.py ../backupBanco/run.csv ../backupBanco/jovem.dat > run100/runJovem.csv
python selectRunPerUsers.py ../backupBanco/run.csv ../backupBanco/adulto.dat > run100/runAdulto.csv
python selectRunPerUsers.py ../backupBanco/run.csv ../backupBanco/media.dat > run100/runMedia.csv
python selectRunPerUsers.py ../backupBanco/run.csv ../backupBanco/baixa.dat > run100/runBaixa.csv

cp ../backupBanco/media.dat ../backupBanco/baixa.dat ../backupBanco/adulto.dat ../backupBanco/jovem.dat ../backupBanco/feminino.dat ../backupBanco/masculino.dat ../backupBanco/campina.dat ../backupBanco/notcampina.dat idsGrupos 

#Separating subgroups - Run in backupBanco folder
python analisaUsuarios.py ../usuario/run100/runCampina.csv ../usuario/run100/runCampina.csv

python separaGrupo.py separa usersInfo.dat users_notcampina_campina.dat
sort -t "|" -k 1 -g -o usersInfo.dat usersInfo.dat

mv campina.dat casado.dat adulto.dat baixa.dat catole.dat centro.dat feminino.dat jovem.dat liberdade.dat masculino.dat media.dat medio.dat notcampina.dat notcatole.dat notcentro.dat notliberdade.dat posgrad.dat solteiro.dat usersInfo*.dat usersNAnswered.dat usersPhotos* idsCampina/

python analisaUsuarios.py ../usuario/run100/runnotCampina.csv ../usuario/run100/runnotCampina.csv

python separaGrupo.py separa usersInfo.dat users_notcampina_campina.dat
sort -t "|" -k 1 -g -o usersInfo.dat usersInfo.dat

mv campina.dat casado.dat adulto.dat baixa.dat catole.dat centro.dat feminino.dat jovem.dat liberdade.dat masculino.dat media.dat medio.dat notcampina.dat notcatole.dat notcentro.dat notliberdade.dat posgrad.dat solteiro.dat usersInfo*.dat usersNAnswered.dat usersPhotos* idsNotCampina/

#Analyze Q-Score
python analisaQScore.py ../backupBanco/run.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allGeral.dat
rm all.dat

python analisaQScore.py run100/runnotCampina.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allNotCampina.dat
rm all.dat
python analisaQScore.py run100/runCampina.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allCampina.dat
rm all.dat
python analisaQScore.py run100/runMasculino.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allMasculino.dat
rm all.dat
python analisaQScore.py run100/runFeminino.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allFeminino.dat
rm all.dat
python analisaQScore.py run100/runJovem.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allJovem.dat
rm all.dat
python analisaQScore.py run100/runAdulto.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allAdulto.dat
rm all.dat
python analisaQScore.py run100/runMedia.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allMedia.dat
rm all.dat
python analisaQScore.py run100/runBaixa.csv 100 ../backupBanco/tasksDef.csv campina
grep agrad all.dat > all100/allBaixa.dat
rm all.dat

#Sorting by mean Q-Score per photo
sort -k 3 -r all100/allGeral.dat > all100/all_ordenado.dat

sort -k 3 -r all100/allCampina.dat > all100/all_campina_ordenado.dat
sort -k 3 -r all100/allNotCampina.dat > all100/all_notcampina_ordenado.dat
sort -k 3 -r all100/allMedia.dat > all100/all_media_ordenado.dat
sort -k 3 -r all100/allBaixa.dat > all100/all_baixa_ordenado.dat
sort -k 3 -r all100/allFeminino.dat > all100/all_feminino_ordenado.dat
sort -k 3 -r all100/allMasculino.dat > all100/all_masculino_ordenado.dat
sort -k 3 -r all100/allJovem.dat > all100/all_jovem_ordenado.dat
sort -k 3 -r all100/allAdulto.dat > all100/all_adulto_ordenado.dat

#Finding intersections between evaluated photos of different groups
python encontraInterseccao.py all100/all_campina_ordenado.dat all100/all_notcampina_ordenado.dat > all100/intersection_all_campina_notcampina.dat 
python encontraInterseccao.py all100/all_media_ordenado.dat all100/all_media_ordenado.dat > all100/intersection_all_baixa_media.dat 
python encontraInterseccao.py all100/all_feminino_ordenado.dat all100/all_masculino_ordenado.dat > all100/intersection_all_feminino_masculino.dat
python encontraInterseccao.py all100/all_jovem_ordenado.dat all100/all_adulto_ordenado.dat > all100/intersection_all_jovem_adulto.dat

#Preparing html pages and sorted intersection files
python preparaHTML.py all100/all_ordenado.dat
rm questionFilter.html
mv question.html rankings100/question.html

python preparaHTML.py all100/all_campina_ordenado.dat all100/intersection_all_campina_notcampina.dat > all100/all_campina_ordInter.dat 
rm questionFilter.html
mv question.html rankings100/questionCampina.html
python preparaHTML.py all100/all_notcampina_ordenado.dat all100/intersection_all_campina_notcampina.dat > all100/all_notcampina_ordInter.dat 
rm questionFilter.html
mv question.html rankings100/questionNotCampina.html

python preparaHTML.py all100/all_jovem_ordenado.dat all100/intersection_all_jovem_adulto.dat > all100/all_jovem_ordInter.dat 
rm questionFilter.html
mv question.html rankings100/questionAllJovem.html
python preparaHTML.py all100/all_adulto_ordenado.dat all100/intersection_all_jovem_adulto.dat > all100/all_adulto_ordInter.dat 
rm questionFilter.html
mv question.html rankings100/questionAllAdulto.html

python preparaHTML.py all100/all_baixa_ordenado.dat all100/intersection_all_baixa_media.dat > all100/all_baixa_ordInter.dat 
rm questionFilter.html
mv question.html rankings100/questionAllBaixa.html
python preparaHTML.py all100/all_media_ordenado.dat all100/intersection_all_baixa_media.dat > all100/all_media_ordInter.dat 
rm questionFilter.html
mv question.html rankings100/questionAllMedia.html

python preparaHTML.py all100/all_feminino_ordenado.dat all100/intersection_all_feminino_masculino.dat > all100/all_feminino_ordInter.dat 
rm questionFilter.html
mv question.html rankings100/questionAllFeminino.html
python preparaHTML.py all100/all_masculino_ordenado.dat all100/intersection_all_feminino_masculino.dat > all100/all_masculino_ordInter.dat 
rm questionFilter.html
mv question.html rankings100/questionAllMasculino.html

#Analyzing Per Street
python analisaPorRua.py all100/all_ordenado.dat
mv qscores-df.csv qscores-df-geral.csv
mv qscores-df-summary.dat qscores-df-summary-geral.dat

python analisaPorRua.py all100/all_campina_ordenado.dat
mv qscores-df.csv qscores-df-campina.csv
mv qscores-df-summary.dat qscores-df-summary-campina.dat

python analisaPorRua.py all100/all_notcampina_ordenado.dat
mv qscores-df.csv qscores-df-notcampina.csv
mv qscores-df-summary.dat qscores-df-summary-notcampina.dat
