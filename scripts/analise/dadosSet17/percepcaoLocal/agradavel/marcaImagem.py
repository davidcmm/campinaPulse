# coding=utf-8
from PIL import Image, ImageDraw, ImageFont
import urllib, cStringIO
import sys
import urllib, json

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

		if best_image != 'equal' or worst_image != 'equal':
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
	image_name = image.split("/")[6]
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

	image_name = image.split("/")[6]
	base.save("piores/"+image_name, "JPEG")

#x, y =  base.size
#bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
#base.show()

# write to stdout
#base.save(sys.stdout, "PNG")


