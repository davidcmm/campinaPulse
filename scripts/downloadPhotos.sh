#!/bin/bash
# This script is used to download photos from Google Street View

for file in `ls *.addr` ; do
	neighborhood=`echo "${file}" | cut -d'.' -f 1`
	mkdir ${neighborhood}
	echo ">>>> Arquivo: ${file}"
	echo ">>>>> Bairro: ${neighborhood}"

	#Download photos of each street location in different positions: 0, 90, 180 and 270 degrees
	while read line ; do 
		streetName=`echo "${line}" | cut -d',' -f 1`
		streetNumber=`echo "${line}" | cut -d',' -f 2`
		if [[ $streetNumber == *-* ]] ; then 
			streetNumber=`echo "${streetNumber}" | cut -d'-' -f 1` 
		fi

		street="${streetName// /_}_${streetNumber// /_}"
		echo ">>>> LINE ${line}"
		echo ">>>> Baixando rua ${streetName} ${street}"

		wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=${line}&heading=0&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
		mv streetview* ${neighborhood}/${street}_0.jpg
		wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=${line}&heading=90&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
		mv streetview* ${neighborhood}/${street}_90.jpg
		wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=${line}&heading=180&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
		mv streetview* ${neighborhood}/${street}_180.jpg
		wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=${line}&heading=270&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
		mv streetview* ${neighborhood}/${street}_270.jpg
	done < $file
done
