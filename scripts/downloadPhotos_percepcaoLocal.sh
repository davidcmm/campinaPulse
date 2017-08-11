#!/bin/bash
# This script is used to download photos from Google Street View - according to pre-selected places in order to evaluate perceptions of a place!

#Pleasantness -> "Rua Inacio Marques da Silva 294" "Rua Inacio Marques da Silva 434" "Rua Inacio Marques da Silva 520"
places=( "Rua Edesio Silva 602" "Rua Edesio Silva 522" "Rua Edesio Silva 474" "Rua Edesio Silva 352" "Avenida Prefeito Severino Bezerra Cabral 38" "Avenida Prefeito Severino Bezerra Cabral 218" "Avenida Prefeito Severino Bezerra Cabral 492" "Avenida Prefeito Severino Bezerra Cabral 774" "Rua Cristina Procopio da Silva 62" "Rua Cristina Procopio da Silva 436" "Rua Cristina Procopio da Silva 282" "Rua Cristina Procopio da Silva 64" "Avenida Presidente Getulio Vargas 206" "Avenida Presidente Getulio Vargas 118" "Avenida Presidente Getulio Vargas 280" "Avenida Presidente Getulio Vargas 610" "Rua Manoel P. de Araujo 370" "Rua Manoel P. de Araujo 222" "Rua Manoel P. de Araujo 450" "Vidal de Negreiros 91" "Vidal de Negreiros 48" "Vidal de Negreiros 299" "Vidal de Negreiros 253" "Treze de Maio 132" "Treze de Maio 276" "Treze de Maio 110" "Treze de Maio 338")
for street in "${places[@]}" ; do

	for angle in 22 45 67 90 112 135 157 180 203 225 247 270 293 315 337 360 ; do

		streetFullName="$street, Campina Grande"
		streetPrefix="${street// /_}"

		wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=${streetFullName}&heading=${angle}&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
		mv streetview* $streetPrefix\_$angle.jpg

	done

done
