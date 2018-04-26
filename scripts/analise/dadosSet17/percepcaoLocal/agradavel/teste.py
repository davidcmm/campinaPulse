# coding=utf-8
from PIL import Image, ImageDraw, ImageFont
import urllib, cStringIO
import sys
import urllib, json
from os import listdir, mkdir
import pickle
import operator

class MyRectangle(object):
	""" A simple class to represent a rectangle """

	def __init__(self, x_left, y_left, x_right, y_right):
		self.x_left = x_left
		self.y_left = y_left
		self.x_right = x_right
		self.y_right = y_right

	def getBottomLeftCorner(self):
		return [self.x_left, self.y_left] 

	def getWidth(self):
		return self.x_right - self.x_left

	def getHeight(self):
		return self.y_right - self.y_left

	def getAllVertices(self):
		return [[self.x_left, self.y_left], [self.x_right, self.y_left], [self.x_right, self.y_right], [self.x_left, self.y_right]]

	def getMinX(self):
		return self.x_left

	def getMinY(self):
		return self.y_left
	
	def getMaxX(self):
		return self.x_right

	def getMaxY(self):
		return self.y_right

	def __str__(self):
		return "RECT: [(" + str(self.x_left) + "," + str(self.y_left) + "), (" + str(self.x_right) + "," + str(self.y_right) + ")]"   

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

def compute_rectangles(current_marks):
	rectangles = []
	for mark in current_marks:
		if len(mark) > 0:
			minX = min(mark, key=lambda point: point[0])[0]
			maxX = max(mark, key=lambda point: point[0])[0]
			minY = min(mark, key=lambda point: point[1])[1]
			maxY = max(mark, key=lambda point: point[1])[1]

			#Creating rectangle with bottom-left and top-right corners
			if minX != maxX and minY != maxY:
				rectangles.append(MyRectangle(minX, minY, maxX, maxY))
	return rectangles

def intersects(rectangle1, rectangle2): 

	r1_data = rectangle1.getBottomLeftCorner()
	r2_data = rectangle2.getBottomLeftCorner()

	#tw = rectangle1.getWidth()
        #th = rectangle1.getHeight()

        #rw = rectangle2.getWidth()
        #rh = rectangle2.getHeight()

        #tx = r1_data[0]
        #ty = r1_data[1]
        #rx = r2_data[0]
        #ry = r2_data[1]

        #rw += rx;
        #rh += ry;
        #tw += tx;
        #th += ty;

        #return ((rw < rx or rw > tx) and (rh < ry or rh > ty) and (tw < tx or tw > rx) and (th < ty or th > ry))

        #double x0 = getX()
        #double y0 = getY()
        return (r2_data[0] + rectangle2.getWidth() > r1_data[0] and r2_data[1] + rectangle2.getHeight() > r1_data[1] and r2_data[0] < r1_data[0] + rectangle1.getWidth() and r2_data[1] < r1_data[1] + rectangle1.getHeight())

def intersect(rectangle1, rectangle2):
       x1 = max(rectangle1.getMinX(), rectangle2.getMinX())
       y1 = max(rectangle1.getMinY(), rectangle2.getMinY())
       x2 = min(rectangle1.getMaxX(), rectangle2.getMaxX())
       y2 = min(rectangle1.getMaxY(), rectangle2.getMaxY())

       if x1 != x2 and y1 != y2:		
	       return MyRectangle(x1, y1, x2, y2)
       else:
		return None
		

def save_image_rects(image, current_map, path):
	# get an image
	file = cStringIO.StringIO(urllib.urlopen(image).read())
	base = Image.open(file)
	base = base.convert("RGBA")
	#draw = ImageDraw.Draw(base)

	#Black, brown, darkred, violet, darkblue, darkgreen, gold
	colors_map = {1: "black", 2: "brown",  3: "darkred", 4: "violet", 5: "darkblue", 6: "darkgreen", 7: "gold"}

	img_size = (640,480)
	poly_size = (640,480)
	poly_offset = (0,0)
	poly = Image.new('RGB', poly_size )
	pdraw = ImageDraw.Draw(poly, 'RGBA')

	#print str(image_data)
	for level in current_map.keys():
		rects = current_map[level]
		#print ">> RECTS " + str(len(rects))
		for rect in rects:
			color = colors_map[level]
			vertices = rect.getAllVertices()#[[self.x_left, self.y_left], [self.x_right, self.y_left], [self.x_right, self.y_right], [self.x_left, self.y_right]]
	
			pdraw.rectangle([vertices[0][0], vertices[0][1], vertices[2][0], vertices[2][1]], fill=(255,255,255,127), outline=(170,170,170,170))

			#init = vertices[0]
			#end = vertices[3]
			#for y in range(int(init[1]), int(end[1]), 3):
			#	eX, eY = 5, 5 #Size of Bounding Box for ellipse
			#	x = init[0]
				#bbox =  (x - eX/2, y - eY/2, x + eX/2, y + eY/2)			
				#draw.ellipse(bbox, fill=color)
				

			#for index in range(0, len(vertices)-1):
#
#				if index == 0 or index == 2:
#					init = vertices[index]
#					end = vertices[index+1]
#					if index == 2:
#						init = vertices[index+1]
#						end = vertices[index]
#
#					for x in range(int(init[0]), int(end[0]), 3):
#						eX, eY = 5, 5 #Size of Bounding Box for ellipse
#						y = init[1]
#						bbox =  (x - eX/2, y - eY/2, x + eX/2, y + eY/2)			
#						draw.ellipse(bbox, fill=color)#draw.rectangle([10,10, 200, 200]) top-left and bottom-right
#				elif index == 1:
#					init = vertices[index]
#					end = vertices[index+1]
#					for y in range(int(init[1]), int(end[1]), 3):
#						eX, eY = 5, 5 #Size of Bounding Box for ellipse
#						x = init[0]
#						bbox =  (x - eX/2, y - eY/2, x + eX/2, y + eY/2)			
#						draw.ellipse(bbox, fill=color)

	#base.paste(poly, poly_offset, mask=poly)
	poly = poly.convert("RGBA")
	final = Image.blend(base, poly, 0.7)
	image_name = urllib.unquote(image.split("/")[6]).decode('utf8')
	final.save(path+image_name, "JPEG")

#Center of circle given 3 points: http://paulbourke.net/geometry/circlesphere/
# Area and centroid of a polygon: http://paulbourke.net/geometry/polygonmesh/
# Bounding rectangle: [minX, minY, maxX, maxY] http://developer.classpath.org/doc/java/awt/Rectangle-source.html http://grepcode.com/file/repository.grepcode.com/java/root/jdk/openjdk/6-b14/java/awt/Rectangle.java
def evaluate_intersections(images_map, folder):
	intersects_per_level = {}

	images = images_map.keys()
	images.sort()

	for image in images:
	
		#image = "https://contribua.org/bairros/oeste/liberdade/R._Ed%C3%A9sio_Silva_70_203.jpg"
		image_data = images_map[image]
		current_marks = []
		for evaluation in image_data:
			points = evaluation[1]
			#for list_points in points:
			#	print ">>> Tamanho " + str(len(list_points))
			current_marks.extend(compute_rectangles(points))
		
		intersections = []
		level = 0

		#current_marks.sort(key=operator.attrgetter('x_left'))
		#for mark in current_marks:
		#	print ">>> MARKS " + str(mark)

		#while len(current_marks) > 0:
		for index in range(0, len(current_marks)):
			for index2 in range(index+1, len(current_marks)):
				mark1 = current_marks[index]
				mark2 = current_marks[index2]

				if intersects(mark1, mark2):
					intersection = intersect(mark1, mark2)
					#print ">>> CURRENT_INTER " + str(intersection) + " ENTRE " + str(mark1) + " " + str(mark2)	

					if intersection != None:
						intersections.append(intersection)

		#intersections.sort(key=operator.attrgetter('x_left'))
		#for mark in intersections:
		#	print ">>> ALL INTER " + str(mark)

		level = level + 1
		if image in intersects_per_level.keys():
			image_intersects = intersects_per_level[image]
		else:
			image_intersects = {}
		if level in image_intersects.keys():
			level_intersects = image_intersects[level]
		else:
			level_intersects = []
		
		level_intersects.extend(intersections)
		image_intersects[level] = level_intersects
		intersects_per_level[image] = image_intersects

		current_marks = intersections
		intersections = []
		#end while
		#break

	for image in intersects_per_level.keys():
		image_rects_level = intersects_per_level[image]
		#print ">>> INter for " + str(image) + " " + str(len(image_rects_level[1]))
		save_image_rects(image, image_rects_level, folder+"/intersects/")
		print ">>> Terminei imagem " + image
	
		
	
#Creating webpage for marked images
def create_page_for_marked_images(best_images, worst_images, best_map, worst_map, output_filename, best_folder, worst_folder):
	output_file = open(output_filename, "w")
	output_file.write("<meta content=\"text/html; charset=UTF-8\" http-equiv=\"content-type\">")
	output_file.write("<body style=\"overflow:scroll\">\n")

	output_file.write(">>> Para cada imagem temos todas as marcaÃ§Ãµes quando ela foi escolhida como melhor ou pior imagem de um conjunto de 4 fotos. AlÃ©m disso, ao lado do nome de cada imagem temos o nÃºmero de vezes que a imagem foi escolhida como melhor ou pior!")
	
	#Best evaluated images
	output_file.write("<h2> Melhores </h2>")
	output_file.write("<table>\n")
	output_file.write("<tr>\n")
	create_rows(best_images, best_map, best_folder, output_file)
	output_file.write("</tr>\n")
	output_file.write("</table>")

	#Worst evaluated images
	output_file.write("<h2> Piores </h2>")
	output_file.write("<table>\n")
	output_file.write("<tr>\n")
	create_rows(worst_images, worst_map, worst_folder, output_file)
	output_file.write("</tr>\n")
	output_file.write("</table>")

	output_file.write("</body>\n");	
	output_file.close()


if __name__ == "__main__": 

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

			if "Manoel" in best_image:
				print ">>> " + str(user_id) + "\t" + str(best_image.encode("utf8"))

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

	#Iterating through images to add marks and save images
	for image in best_map.keys():
		save_image_marks(image, best_map, "melhores/", 'green')

	#index = 0
	for image in worst_map.keys():
		save_image_marks(image, worst_map, "piores/", 'red')

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

	#Persisting points dictionaries
	best_file = open("./best-dict.pkl", "wb")
	pickle.dump(best_map, best_file, pickle.HIGHEST_PROTOCOL)
	#best_map = pickle.load(best_file)
	best_file.close()
	worst_file = open("./worst-dict.pkl", "wb")
	pickle.dump(worst_map, worst_file, pickle.HIGHEST_PROTOCOL)
	#worst_map = pickle.load(worst_file)
	worst_file.close()
	#users_marks_file = open("./users-dict-marks.pkl", "rb")
	#pickle.dump(users_map, users_marks_file, pickle.HIGHEST_PROTOCOL)
	#users_map = pickle.load(users_marks_file)
	#users_marks_file.close()

	#Creating page for users marks
	create_page_for_marked_images(best_images, worst_images, best_map, worst_map, "markedImages.html", "melhores/", "piores/")

	#Compute intersections of users marks
	evaluate_intersections(best_map, "melhores")
	evaluate_intersections(worst_map, "piores")

	#Retrieving intersects files
	best_images = []
	for filename in listdir("./melhores/intersects/"):
	    if "jpg" in filename:
		    best_images.append(filename)
	best_images.sort()

	worst_images = []
	for filename in listdir("./piores/intersects/"):
	    if "jpg" in filename:
	    	worst_images.append(filename)
	worst_images.sort()

	#Create page for intersects
	create_page_for_marked_images(best_images, worst_images, best_map, worst_map, "markedImages-intersect.html", "melhores/intersects/", "piores/intersects/")

	#x, y =  base.size
	#bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
	#base.show()

	# write to stdout
	#base.save(sys.stdout, "PNG")

