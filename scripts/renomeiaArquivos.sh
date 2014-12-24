#!/bin/bash


for file in *; do
	newname=`echo "$file" | iconv -t 'ascii//TRANSLIT'`
	mv "$file" "$newname"

done
