import requests
from random import randint
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


def getCollectionsWithTopic(topic):
    MatchColID = []
    similarVals = []
    laps = 0
    while len(MatchColID) < 5 and laps <= 20:
        laps += 1
        colls = requests.get(f"https://api.unsplash.com/collections?client_id=74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0&page={laps}&per_page=30").json()
        for coll in colls:
            check, similarVal = checkIfSynonym(coll, topic)
            if check:
                MatchColID.append(coll['id'])
                similarVals.append(similarVal)
    if MatchColID != []:
        sortSimVals, sortID = list(zip(*sorted(zip(similarVals, MatchColID))))
    else:
        sortSimVals, sortID = [], []
    return sortSimVals, sortID


def getCollectionWithID(id):
    return requests.get(f"https://api.unsplash.com/collections/{id}?client_id=74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0").json()


def checkIfSynonym(collection, givenTheme):
    lemmatizer = WordNetLemmatizer()
    givenThemeSynonyms = wordnet.synsets(givenTheme)
    categories = ['n', 'v', 'a', 'r', 's']

    tags = [tag['title'] for tag in collection['tags']]

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


def getaPhotoFromCollection(collectionID, number):
    topic = requests.get(f"https://api.unsplash.com/topics/{collectionID}?client_id=74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0").json()
    photos = requests.get(f"https://api.unsplash.com/topics/{collectionID}/photos?client_id=74i4_wzXS1aC5JPj89c6p7gfVPo1GBlXwVtapdLtvE0").json()
    start = randint(0, topic['total_photos']-number-1)
    pictures = []
    for i in range(number):
        pictures.append(photos[start+i])
    return pictures


# if __name__ == "__main__":
#     simValues, collIDs = getCollectionsWithTopic("happy")
#     for i, collID in enumerate(collIDs):
#         coll = getCollectionWithID(collID)
#         print(f"{coll['title']}: {simValues[i]}")