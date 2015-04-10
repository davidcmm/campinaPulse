#!/bin/bash
# This script receives a file containing streets and QScores in order to look for the latitude and longitude of each street

if [ $# -lt 1 ]; then
        echo "usage: $0 <streets and qscore file>"
        exit 1
fi

echo "Chamando python $1" 
python extractLatLongStreet.py $1 > streetNames.dat

while read line ; do 
	street=`echo $line | awk -F "+" '{print $2}'`
	echo $street
	wget "https://maps.googleapis.com/maps/api/geocode/json?address=${street}" -O teste.dat
	lat=`grep "lat" teste.dat | head -n 1 | awk -F ":" '{print $2}'`
	long=`grep "lng" teste.dat | head -n 1 | awk -F ":" '{print $2}'`
	
	echo "$line+$lat+$long" >> streetsQScoresLatLong.dat
done < streetNames.dat

rm teste.dat
