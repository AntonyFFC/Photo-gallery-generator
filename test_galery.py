from gallery import Gallery, InvalidPicValueError
import pytest
from photos import Photo, getPhotos, getPhotoWithID
import os
from PIL import Image
from io import BytesIO
import requests
import pytest


def photo():
    data = {
        'id': 'ABC123',
        'width': 800,
        'height': 600,
        'likes': 10,
        'description': 'A beautiful landscape',
        'alt_description': 'A scenic view',
        'urls': {
            'raw': 'http://example.com/raw',
            'full': 'http://example.com/full',
            'regular': 'http://example.com/regular',
            'small': 'http://example.com/small',
            'thumb': 'http://example.com/thumb',
        }
    }
    return Photo(data)


def photoSecond():
    data = {
        'id': 'BCA321',
        'width': 600,
        'height': 500,
        'likes': 5,
        'description': 'A nice landscape',
        'alt_description': 'A cool view',
        'urls': {
            'raw': 'http://example.com/raw',
            'full': 'http://example.com/full',
            'regular': 'http://example.com/regular',
            'small': 'http://example.com/small',
            'thumb': 'http://example.com/thumb',
        }
    }
    return Photo(data)



@pytest.fixture
def testPictures():
    return [photo(), photoSecond()]


@pytest.fixture
def testGallery(testPictures):
    return Gallery(testPictures, "testTitle", "test/Path")


def test_init(testPictures, testGallery):
    assert testGallery.title == "testTitle"
    assert testGallery.path == "test/Path/"
    assert testGallery._pictures == testPictures


def test_settitle(testGallery):
    testGallery.settitle("newTitle")
    assert testGallery.title == "newTitle"


def test_addPict(testGallery):
    newPicture = photoSecond()
    testGallery.addPict(newPicture)
    assert newPicture in testGallery._pictures


def test_rmvPict(testGallery):
    pic = photo()
    testGallery.rmvPict("ABC123")
    assert pic not in testGallery._pictures


def test_getPict(testGallery):
    pic = photoSecond()
    result = testGallery.getPict("BCA321")
    assert result.id == pic.id


def test_initTypeError(testPictures):
    with pytest.raises(TypeError):
        pics= testPictures
        Gallery(pics, 5, "test/path")


def test_settitleTypeError(testPictures):
    with pytest.raises(TypeError):
        pics = testPictures
        gal = Gallery(pics, "title", "test/path")
        gal.settitle(5)


def test_rmvPictTypeError(testGallery):
    with pytest.raises(TypeError):
        testGallery.rmvPict(123)


def test_getPictTypeError(testGallery):
    with pytest.raises(TypeError):
        testGallery.getPict(123)


