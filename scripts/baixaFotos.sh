#!/bin/bash


#Parou em 2682
for numero in `seq 2702 20 9004` ; do

wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=Floriano Peixoto,${numero},Campina Grande&heading=90&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
mv streetview* floriano_${numero}.jpg

done

for numero in `seq 2 20 2248` ; do

wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=Almirante Barroso,${numero},Campina Grande&heading=90&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
mv streetview* almirante_${numero}.jpg

done

for numero in `seq 2 20 1946` ; do

wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=Rodrigues Alves,${numero},Campina Grande&heading=90&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
mv streetview* rodrigues_${numero}.jpg

done
