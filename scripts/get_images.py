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
from sets import Set

def escolhe_pontos():
    leste = [[]]
    #leste[0] = glob.glob('/home/david/Universidade/doutorado/leste/josep/*.jpg')
	
    oeste = [[], []]
    oeste[0] = glob.glob('/home/david/Universidade/doutorado/oeste/liberdade/*.jpg')
    oeste[1] = glob.glob('/home/david/Universidade/doutorado/oeste/catole/*.jpg')

    norte = [[], [], []]
    #norte[0] = glob.glob('/home/david/Universidade/doutorado/norte/jardim/*.jpg')
    #norte[1] = glob.glob('/home/david/Universidade/doutorado/norte/alto/*.jpg')
    norte[0] = glob.glob('/home/david/Universidade/doutorado/norte/centro/*.jpg')

    #sul = [[], []]
    #sul[0] = glob.glob('/home/david/Universidade/doutorado/sul/bodocongo/*.jpg')
    #sul[1] = glob.glob('/home/david/Universidade/doutorado/sul/prata/*.jpg')

    #leste[0] = recupera_lugar_unico(leste[0])
    oeste[0] = recupera_lugar_unico(oeste[0])
    oeste[1] = recupera_lugar_unico(oeste[1])
    norte[0] = recupera_lugar_unico(norte[0])
    #norte[1] = recupera_lugar_unico(norte[1])
    #norte[2] = recupera_lugar_unico(norte[2])
    #sul[0] = recupera_lugar_unico(sul[0])
    #sul[1] = recupera_lugar_unico(sul[1])

    #print "JOSEP " + str(len(leste[0]))
    #print "LIB " + str(len(oeste[0]))
    #print "CAT " + str(len(oeste[1]))
    #print "JAR " + str(len(norte[0]))
    #print "ALTO " + str(len(norte[1]))
    #print "CEN " + str(len(norte[2])) + str(norte[2])
    #print "BOD " + str(len(sul[0]))
    #print "PRA " + str(len(sul[1])) + str(sul[1])

    #return [random.sample(leste[0], 12), random.sample(oeste[0], 12), random.sample(oeste[1], 12), random.sample(norte[0], 12), random.sample(norte[1], 12), random.sample(norte[2], 12), random.sample(sul[0], 12), random.sample(sul[1], 12)]
    resultado = []
    #resultado.append(leste[0])
    resultado.append(oeste[0])
    resultado.append(oeste[1])
    resultado.append(norte[0])
    return resultado

def escolhe_fotos(pontos):
    #print pontos
    todasFotos = []
    for listaBairro in pontos:
	for ponto in listaBairro:
		fotos = glob.glob(ponto+'*.jpg')       	   
		#print "Fotos " + str(fotos) + " " + str(ponto)
		#escolhida = random.choice(fotos)
		#print "Escolhida " + str(escolhida)
		#todasFotos.append(escolhida)
		for foto in fotos:
			todasFotos.append(foto)
    return todasFotos
		

def recupera_lugar_unico(places):
    newPlaces = []
    for place in places:
	if len(place) > 0:
		dados = place.split("__")
		newPlaces.append(dados[0]+"__"+dados[1].split("_")[0])
    return Set(newPlaces)


def get_photos_votes(size="big"):
    """
    Gets photos from folders
    """
    urlPadrao = "http://socientize.lsd.ufcg.edu.br/bairros/"
    
    pontos = escolhe_pontos()
    todasFotos = escolhe_fotos(pontos)[0:10]
    print str(todasFotos)

    # For each photo ID create its direct URL according to its size:
    # big, medium, small (or thumbnail) + Flickr page hosting the photo
    photos = []
    paresSorteados = []
    contagemPorFoto = {}
    participacaoPorFoto = 6 #expected 66 * 5
    soma = 0
    fotosOriginais = list(todasFotos)
    
    #rand = random.SystemRandom()

    while len(todasFotos) > 0:
	#Escolhendo foto1
	foto1 = random.choice(todasFotos)
	cont = 0
	if contagemPorFoto.has_key(foto1):
		cont = contagemPorFoto.get(foto1)
	while cont >= participacaoPorFoto:
 		foto1 = random.choice(todasFotos)
		cont = 0
    		if contagemPorFoto.has_key(foto1):
			cont = contagemPorFoto.get(foto1)

	#Escolhendo foto2
	if len(todasFotos) <= 10:#Evitando loop com poucas fotos sem pares disponiveis
		foto2 = random.choice(fotosOriginais)#Escolhendo foto2
		while foto2 == foto1:
			foto2 = random.choice(fotosOriginais)
	else:
		foto2 = random.choice(todasFotos)
		while foto2 == foto1:
			foto2 = random.choice(todasFotos)

	cont2 = 0
	if contagemPorFoto.has_key(foto2):
		cont2 = contagemPorFoto.get(foto2)

	#Par de fotos já foi sorteado ou foto2 já atingiu a cota mínima!
	if (foto2 in todasFotos and cont2 >= participacaoPorFoto) or [foto1, foto2] in paresSorteados or [foto2, foto1] in paresSorteados:
		#print "Pulando com " + str(foto1) + " " + str(foto2) + str(cont) + " " + str(cont2)
		continue
	else:
		#Criando tarefa
		imgUrl_c = urlPadrao + foto1.split("/")[5] + "/" + foto1.split("/")[6] + "/" + foto1.split("/")[7]
		imgUrl_a = urlPadrao + foto2.split("/")[5] + "/" + foto2.split("/")[6] + "/" + foto2.split("/")[7]
		element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}			
		photos.append(element)
		paresSorteados.append([foto1, foto2])

		soma = soma + 1
		cont = cont + 1
		cont2 = cont2 + 1
		contagemPorFoto[foto1] = cont
		contagemPorFoto[foto2] = cont2
		if cont >= participacaoPorFoto and foto1 in todasFotos:
			todasFotos.remove(foto1)
		if cont2 >= participacaoPorFoto and foto2 in todasFotos:
			todasFotos.remove(foto2)
		#print "Sorteou : " + str(element) + str(len(todasFotos))

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
