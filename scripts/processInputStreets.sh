#!/bin/bash
#This script is used to process latitudes and longitudes from shapefiles and then perform a reverse geocoding in order to obtain the closest human-readable address

if [ $# -lt 1 ]; then
        echo "usage: $0 <shapefiles>"
        exit 1
fi

python extractLatLongSHP.py $*

for file in *.out ; do 
	echo $file 
	while read line ; do 
		echo $line 
		wget https://maps.googleapis.com/maps/api/geocode/json?latlng=${line} -O teste.dat
		IFS=. read -r -a octets <<< "${file}"
		grep "formatted_address" teste.dat | head -n 1 | awk -F ":" '{print $2}' >> "${octets}.addr"
		rm teste.dat
	done < $file
done
