
import random
import sys
import glob

def get_photos(photosToCreate):
    """
    Gets public photos from Flickr feeds
    :arg string size: Size of the image from Flickr feed.
    :returns: A list of photos.
    :rtype: list
    """
    urlPadrao = "http://socientize.lsd.ufcg.edu.br/"
    urlAlmirante = "http://socientize.lsd.ufcg.edu.br/almirante/"
    urlRodrigues = "http://socientize.lsd.ufcg.edu.br/rodrigues/"
    urlFloriano = "http://socientize.lsd.ufcg.edu.br/floriano/"

    listOfAlmirante = glob.glob('/home/pybossa023/pybossa/pybossa/almirante/*.jpg')
    listOfRodrigues = glob.glob('/home/pybossa023/pybossa/pybossa/rodrigues/*.jpg')
    listOfFloriano = glob.glob('/home/pybossa023/pybossa/pybossa/floriano/*.jpg')

    photos = []

    allPhotos = [listOfAlmirante, listOfFloriano, listOfRodrigues]
    counter = 0
    print str(photosToCreate) + " " + str(counter)

    while counter < photosToCreate:
        #Choose streets
        list1 = random.choice(allPhotos)
        list2 = random.choice(allPhotos)

        #Choose a photo from selected street
        choosed1 = random.choice(list1)
        choosed2 = random.choice(list2)

        while choosed1 == choosed2:
                choosed1 = random.choice(list1)
                choosed2 = random.choice(list2)

        imgUrl_c = urlPadrao + choosed1.split("/")[5] + "/" + choosed1.split("/")[6]
        imgUrl_a = urlPadrao + choosed2.split("/")[5] + "/" + choosed2.split("/")[6]
        print imgUrl_c
        print imgUrl_a

        element = {'url_c':  imgUrl_c, 'url_a': imgUrl_a}
        element2 = {'url_c': imgUrl_a, 'url_a': imgUrl_c}
        if(element in photos or element2 in photos):
                continue
        else:
		print element
                photos.append(element)
                counter = counter + 1
    print photos
    return photos

def createCSV(photos):

    file = open("tarefas.csv", "w")
    file.write("question,url_a,url_c\n")
    print photos
    for photo in photos:
	file.write("Qual local lhe parece mais...?,"+photo['url_c']+","+photo['url_a']+"\n")
    file.close()

if __name__ == "__main__":
    if len(sys.argv) < 1:
	print "Uso: <numero de tarefas a serem geradas>"
	sys.exit(1)

    photos = get_photos(int(sys.argv[1]))
    createCSV(photos)
