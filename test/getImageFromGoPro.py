import urllib, re, urlparse
from bs4 import BeautifulSoup

def getImageFromGoPro(workingImageFileString):
    goProImageDirectoryString = "http://10.5.5.9:8080/videos/DCIM/100GOPRO/"
    imageDirectory = urllib.urlopen(goProImageDirectoryString)
    imageDirectorySoup = BeautifulSoup(imageDirectory, "html5lib")
    imageURLs = []
    for i in imageDirectorySoup.findAll('a', attrs={'href': re.compile('(?i)(jpg|png)$')}):
        imageURLs.append(urlparse.urljoin(goProImageDirectoryString, i['href']))
    latestImageURL = max(imageURLs)
    urllib.urlretrieve(latestImageURL, workingImageFileString)
