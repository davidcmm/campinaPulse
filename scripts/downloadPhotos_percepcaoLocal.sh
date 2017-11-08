#!/bin/bash
# This script is used to download photos from Google Street View - according to pre-selected places in order to evaluate perceptions of a place!

#design 1: places=( "Rua Inacio Marques da Silva 294" "Rua Inacio Marques da Silva 434" "Rua Inacio Marques da Silva 520" "Rua Edesio Silva 602" "Rua Edesio Silva 522" "Rua Edesio Silva 474" "Rua Edesio Silva 352" "Avenida Prefeito Severino Bezerra Cabral 38" "Avenida Prefeito Severino Bezerra Cabral 218" "Avenida Prefeito Severino Bezerra Cabral 492" "Avenida Prefeito Severino Bezerra Cabral 774" "Rua Cristina Procopio da Silva 62" "Rua Cristina Procopio da Silva 436" "Rua Cristina Procopio da Silva 282" "Rua Cristina Procopio da Silva 64" "Avenida Presidente Getulio Vargas 206" "Avenida Presidente Getulio Vargas 118" "Avenida Presidente Getulio Vargas 280" "Avenida Presidente Getulio Vargas 610" "Rua Manoel P. de Araujo 370" "Rua Manoel P. de Araujo 222" "Rua Manoel P. de Araujo 450" "Vidal de Negreiros 91" "Vidal de Negreiros 48" "Vidal de Negreiros 299" "Vidal de Negreiros 253" "Treze de Maio 132" "Treze de Maio 276" "Treze de Maio 110" "Treze de Maio 338")

#design 2: places=( "R. Edésio Silva 70" "R. Edésio Silva 202" "R. Edésio Silva 306" "R. Edésio Silva 474" "R. Edésio Silva 602" " R. Edésio Silva 650" "R. Edésio Silva 900" "R. Edésio Silva 1136" "R. Edésio Silva 1246" "R. Edésio Silva 1546" "R. Inácio Marquês da Silva 360" "R. Inácio Marquês da Silva 500" "R. Inácio Marquês da Silva 239" "R. Inácio Marquês da Silva 120" "R. Inácio Marquês da Silva 54" "R. Manoel Pereira de Araújo 392" "R. Manoel Pereira de Araújo 370" "R. Manoel Pereira de Araújo 300" "R. Manoel Pereira de Araújo 222" "R. Manoel Pereira de Araújo 188" "R. Maciel Pinheiro 360" "R. Maciel Pinheiro 284" "R. Maciel Pinheiro 248" "R. Maciel Pinheiro 190" "R. Maciel Pinheiro 130" "R. Cristina Procópio Silva 2" "R. Cristina Procópio Silva 66" "R. Cristina Procópio Silva 261" "R. Cristina Procópio Silva 305" "R. Cristina Procópio Silva 436" "Av. Pref. Severino Bezerra Cabral 60" "Av. Pref. Severino Bezerra Cabral 218" "Av. Pref. Severino Bezerra Cabral 832" "Av. Pref. Severino Bezerra Cabral 492" "Av. Pref. Severino Bezerra Cabral 710" "Av. Mal. Floriano Peixoto 913 - " "Avenida Macheral Floriano Peixoto 813 - 826, Centro" "Av. Mal. Floriano Peixoto 691 - 660" "Av. Mal. Floriano Peixoto 549-580" "Av. Mal. Floriano Peixoto 445 - 456" "R. Marquês do Herval 15" "R. Marquês do Herval 30" "R. Marquês do Herval 68" "R. Marquês do Herval 145")
#Edesio: 22 135 203 315
#Inacio: 22 90ou112 203 270ou293
#Manoel: 22 135 203 315 
#Maciel Pinheiro: 360 112 180 270
places=()

for street in "${places[@]}" ; do

	echo $street
	#
	for angle in 10 22 45 67 90 112 135 157 180 203 225 247 270 293 315 337 360 ; do

		streetFullName="$street, Campina Grande"
		#streetFullName="$street"
		echo ">>>>> FULL NAME $streetFullName"
		streetPrefix="${street// /_}"

		wget "http://maps.googleapis.com/maps/api/streetview?size=640x480&location=${streetFullName}&heading=${angle}&fov=90&pitch=0&sensor=false&key=AIzaSyA7EITVT8oaeRJMYTVSPrbJL2Hrb0m3I1k"
		mv streetview* $streetPrefix\_$angle.jpg

	done

done
