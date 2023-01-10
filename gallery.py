from PIL import Image
import photos
import os
import requests
from io import BytesIO
import math


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
            path = f'{self._path}/'
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
        try:
            self._pictures.append(picture)
        except Exception as e:
            e("Addition not possible")

    def rmvPict(self, picID):
        if not isinstance(picID, str):
            raise TypeError("ID must be a string")
        for i, picture in enumerate(self._pictures):
            if picture.id == picID:
                del self._pictures[i]
        raise IDNotFoundError()

    def getPict(self, picID):
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
                image = requests.get(pics[x+y].getContents("small"))
                imageData = image.content
                im = Image.open(BytesIO(imageData))
                collage.paste(im, (x*boxWidth, y*boxHeight))
        collage.save(f'{self._path}{self.title}/collage.jpg')

    def saveGallery(self):
        for i, pic in enumerate(self._pictures):
            image = requests.get(pic.getContents("full"))
            imageData = image.content
            im = Image.open(BytesIO(imageData))

            im.save(f'{self._path}{self.title}/picture{i}.jpg')


# # URLs of the images
# image_urls = [
#     "https://images.unsplash.com/photo-1661956601031-4cf09efadfce?ixid=MnwzOTAyMjZ8MXwxfGFsbHwxfHx8fHx8Mnx8MTY3MzI5NDQ5Mw&ixlib=rb-4.0.3",
#     "https://images.unsplash.com/photo-1661956601031-4cf09efadfce?ixid=MnwzOTAyMjZ8MXwxfGFsbHwxfHx8fHx8Mnx8MTY3MzI5NDQ5Mw&ixlib=rb-4.0.3",
#     "https://images.unsplash.com/photo-1661956601031-4cf09efadfce?ixid=MnwzOTAyMjZ8MXwxfGFsbHwxfHx8fHx8Mnx8MTY3MzI5NDQ5Mw&ixlib=rb-4.0.3",
# ]

# # Create a new image with the size of the first image
# collage = Image.new("RGB", (1000,8000))

# #  download the images from url and paste in collage
# for i, image_url in enumerate(image_urls):
#     image_data = requests.get(image_url).content
#     image = Image.open(BytesIO(image_data))
#     collage.paste(image, (i * image.width, 0))

# # Save the collage
# collage.save("collage.jpg")
