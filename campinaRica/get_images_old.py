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
    urlPadrao = "http://socientize.lsd.ufcg.edu.br/"
    urlAlmirante = "http://socientize.lsd.ufcg.edu.br/almirante/"
    #urlRodrigues = "http://socientize.lsd.ufcg.edu.br/rodrigues/"
    urlFloriano = "http://socientize.lsd.ufcg.edu.br/floriano/"

    listOfAlmirante = glob.glob('/home/pybossa023/pybossa/pybossa/almirante/*.jpg')
    #listOfRodrigues = glob.glob('/home/pybossa023/pybossa/rodrigues/*.jpg')
    listOfFloriano = glob.glob('/home/pybossa023/pybossa/pybossa/floriano/*.jpg')

    #values = {'nojsoncallback': 1,
    #          'format': "json"}

    #query = url + "?" + urllib.urlencode(values)
    #urlobj = urllib2.urlopen(query)
    #data = urlobj.read()
    #urlobj.close()
    # The returned JSON object by Flickr is not correctly escaped,
    # so we have to fix it see
    # http://goo.gl/A9VNo
    #regex = re.compile(r'\\(?![/u"])')
    #fixed = regex.sub(r"\\\\", data)
    #output = json.loads(fixed)
    #print('Data retrieved from Flickr')

    # For each photo ID create its direct URL according to its size:
    # big, medium, small (or thumbnail) + Flickr page hosting the photo
    photos = []
    numberOfPairs = 30

    allPhotos = [listOfAlmirante, listOfFloriano]
    counter = 0	
	
    #while counter < numberOfPairs:
	#Choose streets
	#list1 = random.choice(allPhotos)
	#list2 = random.choice(allPhotos)
    list1 = listOfAlmirante
    list2 = listOfFloriano
	
	#Choose a photo from selected street
	#choosed1 = random.choice(list1)
	#choosed2 = random.choice(list2)
    	
	#while choosed1 == choosed2:
	#	choosed1 = random.choice(list1)
	#	choosed2 = random.choice(list2)
	
    for i in range(0, 3):
	choosed1 = list1[i]
	for j in range (0, 5):
		choosed2 = list2[j]
		imgUrl_c = urlPadrao + choosed1.split("/")[5] + "/" + choosed1.split("/")[6]
		imgUrl_a = urlPadrao + choosed2.split("/")[5] + "/" + choosed2.split("/")[6]
		print imgUrl_c
		print imgUrl_a
		element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}
		photos.append(element)
    
    for i in range(0,3):
	choosed1 = list1[i]
	for j in range(i+1,3):
		choosed2 = list1[j]
		imgUrl_c = urlPadrao + choosed1.split("/")[5] + "/" + choosed1.split("/")[6]
                imgUrl_a = urlPadrao + choosed2.split("/")[5] + "/" + choosed2.split("/")[6]
                print imgUrl_c
                print imgUrl_a
                element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}
                photos.append(element)

    for i in range(0,5):
        choosed1 = list2[i]
        for j in range(i+1,5):
               choosed2 = list2[j]
               imgUrl_c = urlPadrao + choosed1.split("/")[5] + "/" + choosed1.split("/")[6]
               imgUrl_a = urlPadrao + choosed2.split("/")[5] + "/" + choosed2.split("/")[6]
               print imgUrl_c
               print imgUrl_a
               element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}
               photos.append(element)

	#element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}
	#if(element in photos):
	#	continue
	#else:
	#	photos.append(element)
#		counter = counter + 1
    #for idx, photo in enumerate(output['items']):
    #    print 'Retrieved photo: %s' % idx
    #    imgUrl_m = photo["media"]["m"]
    #    imgUrl_b = string.replace(photo["media"]["m"], "_m.jpg", "_b.jpg")
    #    photos.append({'url_m':  imgUrl_m,
    #                   'url_b': imgUrl_b})
    return photos



