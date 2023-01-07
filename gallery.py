from PIL import Image
import photos


class IDNotFoundError(Exception):
    def __init__(self):
        super().__init__("No such id in gallery")


class Gallery():
    """
    Class Gallery. Contains attributes:
    :param pictures: A list of the gallery's pictures
    :type name: list

    :param title: the title of the gallery
    :type name: str
    """
    def __init__(self, pictures, title=""):
        self._pictures = []
        for picture in pictures:
            if type(picture) != photos.Photo:
                raise TypeError("The type must be 'Photos'")
            self._pictures.append(picture)
        if not isinstance(title, str):
            raise TypeError("The title must be a string")
        self._title = title

    @property
    def title(self):
        return self._title

    def settitle(self, newtitle):
        if not isinstance(newtitle, str):
            raise TypeError("The title must be a string")
        self._title = newtitle

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

    def makeCollage(self):
        """Creates a collage with a maximum of the first 10 photos"""
        if len(self._pictures) > 10:
            pics = self._pictures[:10]
        else:
            pics = self._pictures

    def saveGallery(self, path):
        pass
