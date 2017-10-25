# coding=utf-8
from PIL import Image, ImageDraw, ImageFont
import urllib, cStringIO
import sys
import urllib, json
from os import listdir, mkdir
import pickle

#Reading task-run from Contribua
apiUrl = 'https://contribua.org/api/'
projectId = '583'
offset=0
best_map = {}
worst_map = {}
users_map = {}

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
		user_id = current_run['user_id']

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

			#Persisting per user
			if user_id in users_map:
				users_marks = users_map[user_id]
			else:
				users_marks = {"best": {}, "worst":{}}
			if best_image in users_marks['best']:
				best_marks = users_marks['best'][best_image]
			else:
				best_marks = []
			best_marks.append([task_id, best_points.sort()])
			users_marks['best'][best_image] = best_marks
			users_map[user_id] = users_marks

			if worst_image in users_marks['worst']:
				worst_marks = users_marks['worst'][worst_image]
			else:
				worst_marks = []
			worst_marks.extend([task_id, worst_points.sort()])
			users_marks['worst'][worst_image] = worst_marks
			users_map[user_id] = users_marks
			
		
	#Requesting next window of data
	offset = offset + len(data)
	url = apiUrl+'taskrun?project_id='+str(projectId)+'&offset='+str(offset)
	response = urllib.urlopen(url)
	data = json.loads(response.read())


def save_image_marks(image, current_map, path, color):
	# get an image
	file = cStringIO.StringIO(urllib.urlopen(image).read())
	base = Image.open(file)
	draw = ImageDraw.Draw(base)

	image_data = current_map[image]
	#print str(image_data)
	for values in image_data:
		points = values[1]

		for sublist in points:
			for point in sublist:
				x = point[0]
				y = point[1]

				eX, eY = 5, 5 #Size of Bounding Box for ellipse
				bbox =  (x - eX/2, y - eY/2, x + eX/2, y + eY/2)			
				draw.ellipse(bbox, fill=color)
	image_name = urllib.unquote(image.split("/")[6]).decode('utf8')
	base.save(path+image_name, "JPEG")

#Iterating through images to add marks and save images
for image in best_map.keys():
	save_image_marks(image, best_map, "melhores/", 'green')

#index = 0
for image in worst_map.keys():
	save_image_marks(image, worst_map, "piores/", 'red')

#for user_id in users_map.keys():
#	user_data = users_map[user_id]
#	user_best = user_data['best']
#	for image in user_best.keys():
#		mkdir('melhores/'+str(user_id))
#		save_image_marks(image, user_best, "melhores/"+str(user_id), "green")
#
#	user_worst = user_data['worst']
#	for image in user_worst.keys():
#		mkdir('piores/'+str(user_id))
#		save_image_marks(image, user_worst, "piores/"+str(user_id), "red")

#Reading all best and worst marked images filenames
best_images = []
for filename in listdir("./melhores/"):
    if "jpg" in filename:
	    best_images.append(filename)
best_images.sort()

worst_images = []
for filename in listdir("./piores/"):
    if "jpg" in filename:
    	worst_images.append(filename)
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

#Build rows of best and worst images evaluations for a certain user
def evaluate_user_rows(user_id, user_data, best_dir, worst_dir, output_file):
	output_file.write("<h3> Usuário " + str(user_id) +" </h3>")
	output_file.write("<h4> Melhores </h4>")
	best_images = user_data['best']
	for image in best_images.keys():
		image_data = best_images[image]
		tasks_ids = image_data.keys()
		#Comparing each of three marks of the user
		for i in [0,1,2]:		
			distance = 0
			for i in range(1, len(tasks_ids)):
				print ""
	
#Creating webpage for marked images
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

	#Per user marks
	#output_file.write("<h2> Por usuário </h2>")
	#for user_id in users_map.keys():
	#	user_data = users_map[user_id]
	#	create_user_rows(user_id, user_data, "melhores/", "piores/", output_file)

	output_file.write("</body>\n");	
	output_file.close()

create_page_for_marked_images(best_images, worst_images, best_map, worst_map)

#x, y =  base.size
#bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
#base.show()

# write to stdout
#base.save(sys.stdout, "PNG")


#Center of circle given 3 points: http://paulbourke.net/geometry/circlesphere/
# Area and centroid of a polygon: http://paulbourke.net/geometry/polygonmesh/
# Bounding rectangle: [minX, minY, maxX, maxY] http://developer.classpath.org/doc/java/awt/Rectangle-source.html http://grepcode.com/file/repository.grepcode.com/java/root/jdk/openjdk/6-b14/java/awt/Rectangle.java


