import requests


def getPhotos():
    imagesData = requests.get("https://api.unsplash.com/photos/?client_id=74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0").json()
    allImages = []
    for imageData in imagesData:
        image = Photo(imageData)
        allImages.append(image)
    return allImages


def getPhotoWithID(id):
    imageData = requests.get(f"https://api.unsplash.com/photos/{id}?client_id=74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0").json()
    return Photo(imageData)


class Photo:
    def __init__(self, data):
        self._data = data

    def _get(self, key):
        return self._data.get(key)

    def id(self):
        return self._data['id']

    def dimensions(self):
        return self._data['width'], self._data['height']

    def likes(self):
        return self._data['likes']

    # Tu rodzaje to są: 'raw', 'full', 'regular', 'small' i 'thumb'
    def getContents(self, type):
        return self._data["urls"][type]
