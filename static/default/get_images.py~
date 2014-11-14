# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.

import urllib
import urllib2
import re
import json
import string
import glob
import random
import sys

def get_photos_from_file(limit):
    photos = []
    dataFile = open("export.csv", "r")
    lines = dataFile.readlines()
    counter = 0

    for line in lines:
	if counter == 0:
		counter += 1
		continue
	elif counter >= limit:
		break
	data = line.split(",")
	element = {'url_c':  data[2], 'url_a': data[3]}
	photos.append(element)
	
	counter += 1

    dataFile.close()
    return photos

def get_photos(size="big"):
    """
    Gets public photos from Flickr feeds
    :arg string size: Size of the image from Flickr feed.
    :returns: A list of photos.
    :rtype: list
    """
    # Get the ID of the photos and load it in the output var
    # add the 'ids': '25053835@N03' to the values dict if you want to
    # specify a Flickr Person ID
    #print('Contacting Flickr for photos')
    defaultURL = "http://socientize.lsd.ufcg.edu.br/bairros/"
    neighborhoods = ['jt', 'ab', 'jc', 'mi', 'jp', 'nb', 'it', 'lib', 'di', 'uni', 'bod', 'ped']
    photosPerNeighborhood = 5
    #listOfAlmirante = glob.glob('/local/david/pybossa_env/campinaPulse/ruas/almirante/*.jpg')
    #listOfRodrigues = glob.glob('/local/david/pybossa_env/campinaPulse/ruas/rodrigues/*.jpg')
    #listOfFloriano = glob.glob('/local/david/pybossa_env/campinaPulse/ruas/floriano/*.jpg')

    # For each photo ID create its direct URL according to its size:
    # big, medium, small (or thumbnail) + Flickr page hosting the photo
    photos = []
    #numberOfPairs = 10
    #return get_photos_from_file(numberOfPairs)
    #counter = 0	
 
    #Combining each neighborhood with all other neighborhoods
    for ind1 in range(0, len(neighborhoods)):
	for ind2 in range(bairr1+1, len(neighborhoods)):
		neigh1 = neighborhoods[ind1]
		neigh2 = neighborhoods[ind2]
		
		listNeigh1 = glob.glob('/local/david/pybossa_env/campinaPulse/bairros/'+str(neigh1)+'/*.jpg')	    
		listNeigh2 = glob.glob('/local/david/pybossa_env/campinaPulse/bairros/'+str(neigh2)+'/*.jpg')
		
		choosedPhotos1 = random.sample(listNeigh1, photosPerNeighborhood)
		choosedPhotos2 = random.sample(listNeigh2, photosPerNeighborhood)

		for photoIndex in range(0,5):
			choosed1 = choosedPhotos1[photoIndex]
			choosed2 = choosedPhotos2[photoIndex]

			imgUrl_c = defaultURL + choosed1.split("/")[6] + "/" + choosed1.split("/")[7]
			imgUrl_a = defaultURL + choosed2.split("/")[6] + "/" + choosed2.split("/")[7]
			
			element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}
			photos.append(element)
    return photos	
    #while counter < numberOfPairs:
	#Choose streets
	#list1 = random.choice(allPhotos)
	#list2 = random.choice(allPhotos)
	
	#Choose a photo from selected street
	#choosed1 = random.choice(list1)
	#choosed2 = random.choice(list2)
    	
	#while choosed1 == choosed2:
	#	choosed1 = random.choice(list1)
	#	choosed2 = random.choice(list2)
	
	#imgUrl_c = urlPadrao + choosed1.split("/")[6] + "/" + choosed1.split("/")[7]
	#imgUrl_a = urlPadrao + choosed2.split("/")[6] + "/" + choosed2.split("/")[7]
	#print imgUrl_c
	#print imgUrl_a

	#element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}
	#element2 = {'url_c': imgUrl_a, 'url_a': imgUrl_c}
	#if(element in photos or element2 in photos):
	#	continue
	#else:
	#	photos.append(element)
	#	counter = counter + 1
    #for idx, photo in enumerate(output['items']):
    #    print 'Retrieved photo: %s' % idx
    #    imgUrl_m = photo["media"]["m"]
    #    imgUrl_b = string.replace(photo["media"]["m"], "_m.jpg", "_b.jpg")
    #    photos.append({'url_m':  imgUrl_m,
    #                   'url_b': imgUrl_b})
   
