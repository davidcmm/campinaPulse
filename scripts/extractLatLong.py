# This script is used to parse latitude and longitude from shapefiles (.shp)
#

import shapefile
import sys

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print "Error! Usage: list of shapefiles!"
	
	for i in range(1, len(sys.argv)):
		currentArg = sys.argv[i]
		sf = shapefile.Reader(currentArg)
		shapes = sf.shapes()
		output = open(currentArg+".out", "w")

		for j in range(0, len(shapes)):
			output.write(str(shapes[j].points[0][1])+","+str(shapes[j].points[0][0])+"\n")
		output.close()
