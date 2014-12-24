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

def get_photos_votes(size="big"):
    """
    Gets photos from folders
    """
    urlPadrao = "http://socientize.lsd.ufcg.edu.br/bairros/"

    leste = []
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/josep/*.jpg'))
	
    oeste = []
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/liberdade/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/catole/*.jpg'))

    norte = []
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/jardim/*.jpg'))
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/alto/*.jpg'))
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/centro/*.jpg'))

    sul = []
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/bodocongó/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/prata/*.jpg'))

    bairros = [leste[0], oeste[0], oeste[1], norte[0], norte[1], norte[2], sul[0], sul[1]]
    todasFotos.append(leste[0])
    todasFotos.append(oeste[0])
    todasFotos.append(oeste[1])
    todasFotos.append(norte[0])
    todasFotos.append(norte[1])
    todasFotos.append(norte[2])
    todasFotos.append(sul[0])
    todasFotos.append(sul[1])
	
    # For each photo ID create its direct URL according to its size:
    # big, medium, small (or thumbnail) + Flickr page hosting the photo
    photos = []
    paresSorteados = []
    contagemPorFoto = {}
    participacaoPorFoto = 25 #expected 66 * 5
    soma = 0
    terminou = False
    #rand = random.SystemRandom()

    while not terminou:
	foto1 = random.choice(todasFotos)
	cont = 0
	if contagemPorFoto.has_key(foto1):
		cont = contagemPorFoto.get(foto1)
	while cont >= participacaoPorFoto:
		todasFotos.remove(foto1)
 		foto1 = random.choice(todasFotos)
    		if contagemPorFoto.has_key(foto1):
			cont = contagemPorFoto.get(foto1)

	foto2 = random.choice(todasFotos)
	cont = 0
	if contagemPorFoto.has_key(foto2):
		cont = contagemPorFoto.get(foto2)

	if cont >= participacaoPorFoto or [foto1, foto2] in paresSorteados or [foto2, foto1] in paresSorteados:
		if cont >= participacaoPorFoto:
			todasFotos.remove(foto2)
 		continue
	else:
		imgUrl_c = urlPadrao + photos1[photoIndex].split("/")[5] + "/" + photos1[photoIndex].split("/")[6] + "/" + photos1[photoIndex].split("/")[7]
		imgUrl_a = urlPadrao + photos2[photoIndex].split("/")[5] + "/" + photos2[photoIndex].split("/")[6] + "/" + photos2[photoIndex].split("/")[7]
		element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}			
		photos.append(element)
		paresSorteados.append([foto1, foto2])
		soma = soma + 1

	#Finished for all photos?
	if len(todasFotos) == 0:
		terminou = True

    print ">>> Returning with "+str(participacaoPorFoto)+ " " + str(soma)
    return photos

def get_photos_partial(size="big"):
    """
    Gets public photos from Flickr feeds
    :arg string size: Size of the image from Flickr feed.
    :returns: A list of photos.
    :rtype: list
    """
    urlPadrao = "http://socientize.lsd.ufcg.edu.br/bairros/"

    leste = []
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/mirante/*.jpg'))
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/josep/*.jpg'))
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/novab/*.jpg'))
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/santo/*.jpg'))
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/vilac/*.jpg'))
	
    oeste = []
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/itarare/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/liberdade/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/distrito/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/catole/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/cidades/*.jpg'))

    norte = []
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/jardim/*.jpg'))
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/alto/*.jpg'))
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/jardimc/*.jpg'))

    sul = []
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/univ/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/bodocongó/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/pedregal/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/prata/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/serrotao/*.jpg'))

    bairros = [[leste[0], oeste[0], norte[0], sul[0]], [leste[1], oeste[1], norte[1], sul[1]], [leste[2], oeste[2], norte[2], sul[2]]]
	
    photos = []
    expected = 0 #expected 66 * 5
    soma = 0
     
    #Creating pairs for each group of 4 neighborhoods		    	
    for i in range(0, 3):
	grupoAtual = bairros[i]
	for j in range(0, len(grupoAtual)):
		for k in range(j+1, len(grupoAtual)):
			bairro1 = grupoAtual[j]
			bairro2 = grupoAtual[k]

			photos1 = random.sample(bairro1, 5)	
			photos2 = random.sample(bairro2, 5)
			expected = expected + 1

			for photoIndex in range(0, 5):
				imgUrl_c = urlPadrao + photos1[photoIndex].split("/")[5] + "/" + photos1[photoIndex].split("/")[6] + "/" + photos1[photoIndex].split("/")[7]
				imgUrl_a = urlPadrao + photos2[photoIndex].split("/")[5] + "/" + photos2[photoIndex].split("/")[6] + "/" + photos2[photoIndex].split("/")[7]			
				element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}			

				photos.append(element)				
				soma = soma + 1

    #Comparing groups of neighborhoods		    	
    for i in range(0, 3):
	grupoAtual = bairros[i]
	for j in range(i+1, len(bairros)):
		proximoGrupo = bairros[j]
		
		for grupoAtualIndex in range(0, len(grupoAtual)):
			for proximoGrupoIndex in range(0, len(proximoGrupo)):
				bairro1 = grupoAtual[grupoAtualIndex]
				bairro2 = proximoGrupo[proximoGrupoIndex]		
				photos1 = random.sample(bairro1, 5)	
				photos2 = random.sample(bairro2, 5)
				expected = expected + 1

				for photoIndex in range(0, 5):
					imgUrl_c = urlPadrao + photos1[photoIndex].split("/")[5] + "/" + photos1[photoIndex].split("/")[6] + "/" + photos1[photoIndex].split("/")[7]
					imgUrl_a = urlPadrao + photos2[photoIndex].split("/")[5] + "/" + photos2[photoIndex].split("/")[6] + "/" + photos2[photoIndex].split("/")[7]			
					element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}			

					photos.append(element)				
					soma = soma + 1

    print ">>> Returning with "+str(expected)+ " " + str(soma)
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
    urlPadrao = "http://socientize.lsd.ufcg.edu.br/bairros/"
    #urlAlmirante = "http://socientize.lsd.ufcg.edu.br/bairros/almirante/"
    #urlRodrigues = "http://socientize.lsd.ufcg.edu.br/bairros/rodrigues/"
    #urlFloriano = "http://socientize.lsd.ufcg.edu.br/bairros/floriano/"

    leste = []
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/mirante/*.jpg'))
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/josep/*.jpg'))
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/novab/*.jpg'))
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/santo/*.jpg'))
    leste.append(glob.glob('/home/david/Universidade/doutorado/leste/vilac/*.jpg'))
	
    oeste = []
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/itarare/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/liberdade/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/distrito/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/catole/*.jpg'))
    oeste.append(glob.glob('/home/david/Universidade/doutorado/oeste/cidades/*.jpg'))

    norte = []
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/jardim/*.jpg'))
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/alto/*.jpg'))
    norte.append(glob.glob('/home/david/Universidade/doutorado/norte/jardimc/*.jpg'))

    sul = []
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/univ/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/bodocongó/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/pedregal/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/prata/*.jpg'))
    sul.append(glob.glob('/home/david/Universidade/doutorado/sul/serrotao/*.jpg'))

    bairros = [leste[0], leste[1], leste[2], oeste[0], oeste[1], oeste[2], norte[0], norte[1], norte[2], sul[0], sul[1], sul[2]]
	
    # For each photo ID create its direct URL according to its size:
    # big, medium, small (or thumbnail) + Flickr page hosting the photo
    photos = []
    expected = 0 #expected 66 * 5
    soma = 0
    #return get_photos_from_file(numberOfPairs)
	
    for i in range(0, 12):
	for j in range(i+1, 12):
		bairro1 = bairros[i]
		bairro2 = bairros[j]
		
		photos1 = random.sample(bairro1, 5)	
		photos2 = random.sample(bairro2, 5)
		print "Sorteados " + " " + str(len(photos1))
		print "Sorteados " + " " + str(len(photos2))
		expected = expected + 1

		for photoIndex in range(0, 5):
			imgUrl_c = urlPadrao + photos1[photoIndex].split("/")[5] + "/" + photos1[photoIndex].split("/")[6] + "/" + photos1[photoIndex].split("/")[7]
			imgUrl_a = urlPadrao + photos2[photoIndex].split("/")[5] + "/" + photos2[photoIndex].split("/")[6] + "/" + photos2[photoIndex].split("/")[7]			
			element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}			

			photos.append(element)				
			soma = soma + 1

    #for idx, photo in enumerate(output['items']):
    #    print 'Retrieved photo: %s' % idx
    #    imgUrl_m = photo["media"]["m"]
    #    imgUrl_b = string.replace(photo["media"]["m"], "_m.jpg", "_b.jpg")
    #    photos.append({'url_m':  imgUrl_m,
    #                   'url_b': imgUrl_b})
    print ">>> Returning with "+str(expected)+ " " + str(soma)
    return photos
