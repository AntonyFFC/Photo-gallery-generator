from PIL import Image
import photos
import os
import requests
from io import BytesIO


class IDNotFoundError(Exception):
    def __init__(self):
        super().__init__("No such id in gallery")


class InvalidPicValueError(Exception):
    def __init__(self):
        super().__init__("The number of pictures given is invalid")


class Gallery():
    """
    Class Gallery. Contains attributes:
    :param pictures: A list of the gallery's pictures
    :type name: list

    :param title: the title of the gallery
    :type name: str

    :param path: the path of the gallery
    :type name: str
    """
    def __init__(self, pictures, title="", path=""):
        self._pictures = []
        self._path = path
        if not isinstance(title, str):
            raise TypeError("The title must be a string")
        self._title = title
        if self._path != "":
            self._path = f'{self._path}/'
        os.makedirs(f'{self._path}{self._title}', exist_ok=True)
        for picture in pictures:
            if type(picture) != photos.Photo:
                raise TypeError("The type must be 'Photos'")
            self._pictures.append(picture)

    @property
    def title(self):
        return self._title

    def settitle(self, newtitle):
        if not isinstance(newtitle, str):
            raise TypeError("The title must be a string")
        self._title = newtitle

    @property
    def path(self):
        return self._path

    def addPict(self, picture):
        """Adds an image from the gallery with the given ID"""
        try:
            self._pictures.append(picture)
        except Exception as e:
            e("Addition not possible")

    def rmvPict(self, picID):
        """Removes an image from the gallery with the given ID"""
        if not isinstance(picID, str):
            raise TypeError("ID must be a string")
        for i, picture in enumerate(self._pictures):
            if picture.id == picID:
                del self._pictures[i]
                return
        raise IDNotFoundError()

    def getPict(self, picID):
        """Returns an image from the gallery with the given ID"""
        if not isinstance(picID, str):
            raise TypeError("ID must be a string")
        for i, picture in enumerate(self._pictures):
            if picture.id == picID:
                return self._pictures[i]
        raise IDNotFoundError()

    def makeCollage(self, picNumbers=[0, 1, 2, 3]):
        """Creates a collage out of given photos with max 9 photos"""
        widths = []
        heights = []
        pics = []
        for i in picNumbers:
            pics.append(self._pictures[i])
            widths.append(self._pictures[i].dimensions[0])
            heights.append(self._pictures[i].dimensions[1])

        if len(picNumbers) == 2:
            rows = 2
            cols = 1
        elif len(picNumbers) < 5:
            rows = 2
            cols = 2
        elif len(picNumbers) < 7:
            rows = 2
            cols = 3
        elif len(picNumbers) < 10:
            rows = 3
            cols = 3
        else:
            raise InvalidPicValueError()
        boxWidth = max(widths)
        boxHeight = max(heights)

        collage = Image.new("RGB", (boxWidth*cols, boxHeight*rows))

        for y in range(rows):
            for x in range(cols):
                image = requests.get(pics[x+y].getContents("full"))
                imageData = image.content
                im = Image.open(BytesIO(imageData))
                collage.paste(im, (x*boxWidth, y*boxHeight))
        collage.save(f'{self._path}{self.title}/collage.jpg')
        return collage

    def saveGallery(self):
        """Saves each photo of the gallery into a folder of the photogallery"""
        for i, pic in enumerate(self._pictures):
            pic.savePhoto(self)
