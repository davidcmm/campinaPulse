# coding=utf-8
from PIL import Image, ImageDraw, ImageFont
import urllib, cStringIO
import sys
import urllib, json
from os import walk
import pickle

#Reading task-run from Contribua
apiUrl = 'https://contribua.org/api/'
projectId = '583'
offset=0
best_map = {}
worst_map = {}

url = apiUrl+'taskrun?project_id='+str(projectId)+'&offset='+str(offset)
response = urllib.urlopen(url)
data = json.loads(response.read())
while len(data) > 0:
	for i in range(0, len(data)):
		current_run = data[i]
		task_id = current_run['id']
		info = current_run['info']
		best_image = info['theMost']
		worst_image = info['theLess']

		if len(best_image) > 0 and len(worst_image) > 0 and (best_image != 'equal' or worst_image != 'equal'):
			best_points = eval(info['markMost'])
			worst_points = eval(info['markLess'])

			best_image = urllib.quote(best_image.encode('utf8'), ':/')
			worst_image = urllib.quote(worst_image.encode('utf8'), ':/')

			if best_image in best_map:
				all_best_points = best_map[best_image]
			else:
				all_best_points = []
			all_best_points.append([task_id, best_points])
			best_map[best_image] = all_best_points
	
			if worst_image in worst_map:
				all_worst_points = worst_map[worst_image]
			else:
				all_worst_points = []
			all_worst_points.append([task_id, worst_points])
			worst_map[worst_image] = all_worst_points
		
	#Requesting next window of data
	offset = offset + len(data)
	url = apiUrl+'taskrun?project_id='+str(projectId)+'&offset='+str(offset)
	response = urllib.urlopen(url)
	data = json.loads(response.read())

#Iterating through images to add marks and save images
for image in best_map.keys():
	# get an image
	file = cStringIO.StringIO(urllib.urlopen(image).read())
	base = Image.open(file)
	draw = ImageDraw.Draw(base)

	image_data = best_map[image]
	#print str(image_data)
	for values in image_data:
		points = values[1]

		for sublist in points:
			for point in sublist:
				x = point[0]
				y = point[1]

				eX, eY = 5, 5 #Size of Bounding Box for ellipse
				bbox =  (x - eX/2, y - eY/2, x + eX/2, y + eY/2)			
				draw.ellipse(bbox, fill='green')
	image_name = urllib.unquote(image.split("/")[6]).decode('utf8')
	base.save("melhores/"+image_name, "JPEG")

#index = 0
for image in worst_map.keys():
	# get an image
	file = cStringIO.StringIO(urllib.urlopen(image).read())
	base = Image.open(file)
	draw = ImageDraw.Draw(base)

	image_data = worst_map[image]
	for values in image_data:
		#if image == "https://contribua.org/bairros/oeste/liberdade/R._Ed%C3%A9sio_Silva_70_135.jpg":
		#	base2 = Image.open(file)
		#	draw2 = ImageDraw.Draw(base2)
		#	index = index + 1
		#else:
		#	base2 = ""

		points = values[1]
		for sublist in points:
			for point in sublist:
				x = point[0]
				y = point[1]

				eX, eY = 5, 5 #Size of Bounding Box for ellipse
				bbox =  (x - eX/2, y - eY/2, x + eX/2, y + eY/2)			
				draw.ellipse(bbox, fill='red')
		
				#if image == "https://contribua.org/bairros/oeste/liberdade/R._Ed%C3%A9sio_Silva_70_135.jpg":
				#	draw2.ellipse(bbox, fill='red')

#		if image == "https://contribua.org/bairros/oeste/liberdade/R._Ed%C3%A9sio_Silva_70_135.jpg":
#			image_name = image.split("/")[6]
#			base2.save("piores/"+image_name+"_"+str(index), "JPEG")

	image_name = urllib.unquote(image.split("/")[6]).decode('utf8')
	base.save("piores/"+image_name, "JPEG")

#Creating webpage for marked images
best_images = []
for (dirpath, dirnames, filenames) in walk("./melhores"):
    best_images.extend(filenames)
best_images.sort()

worst_images = []
for (dirpath, dirnames, filenames) in walk("./piores"):
    worst_images.extend(filenames)
worst_images.sort()

#Persisting points dictionaries
#best_file = open("./best-dict.pkl", "rb")
#pickle.dump(best_map, best_file, pickle.HIGHEST_PROTOCOL)
#best_map = pickle.load(best_file)
#best_file.close()
#worst_file = open("./worst-dict.pkl", "rb")
#pickle.dump(worst_map, worst_file, pickle.HIGHEST_PROTOCOL)
#worst_map = pickle.load(worst_file)
#worst_file.close()

def create_rows(images, current_map, folder, output_file):
	counter = 0
	keys = []
	for key in current_map.keys():#Decoding keys from task-run
		new_key = urllib.unquote(key).decode('utf8')
		keys.append([new_key, key])

	for image in images:
		selected_key = None
		for key_list in keys:
			if image.decode("utf8") in key_list[0]:
				selected_key = key_list[1]
				break

		image_points = len(current_map.get(selected_key))#UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 5: ordinal not in range(128)
		output_file.write("<td><img src=\""+ str(folder) + str(image) + "\" width=\"400\" height=\"300\"></td>\n")
		output_file.write("<td>" + folder + image + " " + str(image_points) + "</td>\n")
		counter += 1

		if counter % 3 == 0:
			output_file.write("</tr>\n")
			output_file.write("<tr>\n")

def create_page_for_marked_images(best_images, worst_images, best_map, worst_map):
	output_file = open("markedImages.html", "w")
	output_file.write("<meta content=\"text/html; charset=UTF-8\" http-equiv=\"content-type\">")
	output_file.write("<body style=\"overflow:scroll\">\n")

	output_file.write(">>> Para cada imagem temos todas as marcações quando ela foi escolhida como melhor ou pior imagem de um conjunto de 4 fotos. Além disso, ao lado do nome de cada imagem temos o número de vezes que a imagem foi escolhida como melhor ou pior!")
	
	#Best evaluated images
	output_file.write("<h2> Melhores </h2>")
	output_file.write("<table>\n")
	output_file.write("<tr>\n")
	create_rows(best_images, best_map, "melhores/", output_file)
	output_file.write("</tr>\n")
	output_file.write("</table>")

	#Worst evaluated images
	output_file.write("<h2> Piores </h2>")
	output_file.write("<table>\n")
	output_file.write("<tr>\n")
	create_rows(worst_images, worst_map, "piores/", output_file)
	output_file.write("</tr>\n")
	output_file.write("</table>")
	
	output_file.write("</body>\n");	
	output_file.close()

create_page_for_marked_images(best_images, worst_images, best_map, worst_map)

#x, y =  base.size
#bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
#base.show()

# write to stdout
#base.save(sys.stdout, "PNG")


