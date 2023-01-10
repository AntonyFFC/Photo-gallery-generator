import requests
from random import randint
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk
import re
nltk.download('wordnet')



class NoDataError(Exception):
    def __init__(self):
        super().__init__("No data given")


class WrongCategoryError(Exception):
    def __init__(self):
        super().__init__("The given category is not possible")


def getPhotos(page=1, per_page=10):
    imagesData = requests.get(f"https://api.unsplash.com/photos/?client_id=74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0&page={page}&per_page={per_page}").json()
    allImages = []
    for imageData in imagesData:
        image = Photo(imageData)
        allImages.append(image)
    return allImages


def getPhotoWithID(id):
    imageData = requests.get(f"https://api.unsplash.com/photos/{id}?client_id=74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0").json()
    return Photo(imageData)


def getPhotoWithTopic(topic):
    MatchPhotID = []
    similarVals = []
    laps = 0
    while len(MatchPhotID) < 5 and laps <= 10:
        laps += 1
        phots = getPhotos(laps+randint(0, 500), 30)
        for photo in phots:
            phot = getPhotoWithID(photo.id)
            check, similarVal = checkIfSynonym(phot, topic)
            if check:
                MatchPhotID.append(phot.id)
                similarVals.append(similarVal)
    if MatchPhotID != []:
        sortSimVals, sortPhotID = list(zip(*sorted(zip(similarVals, MatchPhotID))))
    else:
        sortSimVals, sortPhotID = [], []
    return sortSimVals, sortPhotID


def getPhotoWithTopicLight(topic):
    MatchPhotID = []
    similarVals = []
    laps = 0
    while len(MatchPhotID) < 5 and laps <= 10:
        laps += 1
        phots = getPhotos(laps+randint(0, 500), 30)
        for photo in phots:
            if photo.description is None:
                if photo.alt_description is None:
                    continue
                check, similarVal = checkIfSynonym(photo.alt_description, topic)
            else:
                check, similarVal = checkIfSynonym(photo.description, topic)
            if check:
                MatchPhotID.append(photo.id)
                similarVals.append(similarVal)
    if MatchPhotID != []:
        sortSimVals, sortPhotID = list(zip(*sorted(zip(similarVals, MatchPhotID))))
    else:
        sortSimVals, sortPhotID = [], []
    return sortSimVals, sortPhotID


def checkIfSynonym(input, givenTheme):
    lemmatizer = WordNetLemmatizer()
    givenThemeSynonyms = wordnet.synsets(givenTheme)
    categories = ['n', 'v', 'a', 'r', 's']
    if isinstance(input, Photo):
        tags = input.tags_preview
    elif isinstance(input, str):
        tags = re.split(r'[-\s]', input)
    else:
        raise TypeError("The input must be either a Photo or a string")

    if not givenThemeSynonyms:
        for tag in tags:
            if tag.lower() == givenTheme.lower():
                return True, 0.9
        return False, 0

    for tag in tags:
        tag = tag.lower()
        for synset in givenThemeSynonyms:
            themeSynsets = wordnet.synsets(tag)
            for themeSynset in themeSynsets:
                if themeSynset.wup_similarity(synset) > 0.79:
                    return True, themeSynset.wup_similarity(synset)
        for categ in categories:
            givenLemmatized = lemmatizer.lemmatize(givenTheme.lower(), pos=categ)
            tagLemmatized = lemmatizer.lemmatize(tag, pos=categ)
            if givenLemmatized == tagLemmatized:
                return True, 0.8
    return False, 0


class Photo:
    """
    Class Photo. Contains attributes:
    :param data: Photos' data
    :type name: JSON

    :param id: Photos' id
    :type name: str

    :param dimensions: Photos' dimensions
    :type name: tuple

    :param likes: Photos' number of likes
    :type name: int

    :param description: Photos' description
    :type name: str

    :param alt_description: Photos' alternative description
    :type name: str
    """
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

    @property
    def tags(self):
        tags = [tag['title'] for tag in self._data['tags']]
        return tags

    @property
    def tags_preview(self):
        tagsPreview = [tag['title'] for tag in self._data['tags_preview']]
        return tagsPreview

    def savePhoto(self, path):
        pass

    def effect(self, effect):
        pass


def checker(data):
    if not data:
        raise NoDataError()
    if not isinstance(data, dict):
        raise ValueError("Data must be JSON \nthis usually means that unsplash blocked your IP adress")

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

    desc = data['description']
    if not isinstance(desc, str) and desc is not None:
        raise TypeError("Description Must be a string")

    categories = ['raw', 'full', 'regular', 'small', 'thumb']
    for category in categories:
        if not isinstance(data['urls'][category], str):
            raise TypeError("The contents must be strings")

    return True


if __name__ == "__main__":
    simValues, photsIDs = getPhotoWithTopicLight("nature")
    for i, photID in enumerate(photsIDs):
        phot = getPhotoWithID(photID)
        print(f"{phot.tags_preview[0]}: {simValues[i]}")