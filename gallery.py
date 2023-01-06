from PIL import Image
import photos


class Gallery():
    def __init__(self, pictures):
        self._pictures = []
        for picture in pictures:
            if type(picture) != photos.Photo:
                raise TypeError("The type must be 'Photos'")
            self._pictures.append(picture)

    def addPict(self, picture):
        pass

    def rmvPict(self, picName):
        pass

    def getPict(self, picName):
        pass

    def makeCollage(self):
        pass

    def saveGallery(self, path):
        pass
