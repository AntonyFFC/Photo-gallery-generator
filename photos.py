import requests


class NoDataError(Exception):
    def __init__(self):
        super().__init__("No data given")


class WrongCategoryError(Exception):
    def __init__(self):
        super().__init__("The given category is not possible")


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
        if checker(data):
            self._data = data

    def getData(self):
        return self._data

    def _get(self, key):
        return self._data.get(key)

    @property
    def id(self):
        return self._data['id']

    def setID(self, newID):
        if type(newID) == str:
            self._data['id'] = newID
        else:
            raise TypeError("id has to be a string")

    @property
    def dimensions(self):
        return self._data['width'], self._data['height']

    @property
    def likes(self):
        return self._data['likes']

    def setLikes(self, newLikes):
        if isinstance(newLikes, int):
            if newLikes >= 0:
                self._data['likes'] = newLikes
            else:
                raise ValueError("Likes Cannot be negative")
        else:
            raise TypeError("Likes must be a integers")

    @property
    def description(self):
        return self._data['description']

    @property
    def alt_description(self):
        return self._data['alt_description']

    def setDescription(self, newDescription):
        if not isinstance(newDescription, str):
            raise TypeError("Description Must be a string")
        self._data['description'] = newDescription

    def setAltDescription(self, newDescription):
        if not isinstance(newDescription, str):
            raise TypeError("Description Must be a string")
        self._data['alt_description'] = newDescription

    def getContents(self, category):
        if category not in ['raw', 'full', 'regular', 'small', 'thumb']:
            raise WrongCategoryError()
        return self._data["urls"][category]


def checker(data):
    if not data:
        raise NoDataError()
    if not isinstance(data, dict):
        raise ValueError("Data must be JSON")

    if not isinstance(data['id'], str):
        raise TypeError("id has to be a string")

    keys = ['width', 'height']
    if not all(isinstance(data[k], int) for k in keys):
        raise TypeError("dimensions must be integers")
    if data['width'] <= 0 or data['height'] <= 0:
        raise ValueError("Value must be positive")

    if not isinstance(data['likes'], int):
        raise TypeError("Likes must be integers")
    if data['likes'] < 0:
        raise ValueError("Likes Cannot be negative")

    if not isinstance(data['description'], str):
        raise TypeError("Description Must be a string")

    categories = ['raw', 'full', 'regular', 'small', 'thumb']
    for category in categories:
        if not isinstance(data['urls'][category], str):
            raise TypeError("The contents must be strings")

    return True
