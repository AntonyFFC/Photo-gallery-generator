from photos import (
    Photo,
    getPhotos,
    getPhotoWithID,
    NoDataError,
    WrongCategoryError,
)
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


def test_photo():
    pic = photo()
    assert pic.id == 'ABC123'
    assert pic.dimensions == (800, 600)
    assert pic.likes == 10
    assert pic.description == 'A beautiful landscape'
    assert pic.alt_description == 'A scenic view'
    assert pic.getContents('raw') == 'http://example.com/raw'
    assert pic.getContents('full') == 'http://example.com/full'
    assert pic.getContents('regular') == 'http://example.com/regular'
    assert pic.getContents('small') == 'http://example.com/small'
    assert pic.getContents('thumb') == 'http://example.com/thumb'


def test_photoNodata():
    with pytest.raises(NoDataError):
        Photo(None)


def test_photoInvalidData():
    with pytest.raises(Exception):
        Photo("invalid data")


def test_photoInvalidID():
    data = {"id": 123}
    with pytest.raises(TypeError):
        _ = Photo(data)


def test_photoInvalidDimensionType():
    data = {
        "id": "ABC123",
        "width": "100",
        "height": 200
        }
    with pytest.raises(TypeError):
        _ = Photo(data)


def test_photoInvalidDimensionValue():
    data = {
        "id": "ABC123",
        "width": 100,
        "height": -200
        }
    with pytest.raises(ValueError):
        _ = Photo(data)


def test_photoInvalidLikesType():
    data = {
        "id": "ABC123",
        "width": 100,
        "height": 200,
        "likes": "10"
        }
    with pytest.raises(TypeError):
        _ = Photo(data)


def test_photoInvalidLikesValue():
    data = {
        "id": "ABC123",
        "width": 100,
        "height": 200,
        "likes": -10
        }
    with pytest.raises(ValueError):
        _ = Photo(data)


def test_photoInvalidDescription():
    data = {
        'id': 'ABC123',
        'width': 800,
        'height': 600,
        'likes': 10,
        'description': 123,
        'alt_description': 'A scenic view',
    }
    with pytest.raises(TypeError):
        _ = Photo(data)


def test_photoInvalidGetContents():
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
            'regular': 513,
            'small': 'http://example.com/small',
            'thumb': 'http://example.com/thumb',
        }
    }
    with pytest.raises(TypeError):
        _ = Photo(data)


def test_setID():
    pic = photo()
    assert pic.id == "ABC123"
    pic.setID("BCA123")
    assert pic.id == "BCA123"


def test_setIDInvalidID():
    pic = photo()
    with pytest.raises(TypeError):
        pic.setID(123)


def test_setLikes():
    pic = photo()
    assert pic.likes == 10
    pic.setLikes(15)
    assert pic.likes == 15


def test_setInvalidLikesType():
    pic = photo()
    assert pic.likes == 10
    with pytest.raises(TypeError):
        pic.setLikes("15")


def test_setInvalidLikesValue():
    pic = photo()
    assert pic.likes == 10
    with pytest.raises(ValueError):
        pic.setLikes(-15)


def test_setDescriptions():
    pic = photo()
    assert pic.description == 'A beautiful landscape'
    assert pic.alt_description == 'A scenic view'
    pic.setDescription('An ugly landscape')
    pic.setAltDescription('An industrial view')
    assert pic.description == 'An ugly landscape'
    assert pic.alt_description == 'An industrial view'


def test_setDescriptionsInvalidType():
    pic = photo()
    assert pic.description == 'A beautiful landscape'
    assert pic.alt_description == 'A scenic view'
    with pytest.raises(TypeError):
        pic.setDescription(513)
    with pytest.raises(TypeError):
        pic.setAltDescription(2137)


def test_getContentsInvalidCategory():
    pic = photo()
    with pytest.raises(WrongCategoryError):
        pic.getContents('invalid')


@pytest.fixture
def mockRequestsGet(mocker):
    data1 = {
        'id': 'ABC',
        'width': 100,
        'height': 200,
        'likes': 5,
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
    data2 = {
        'id': 'DEF',
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
    mock = mocker.patch("requests.get")
    mock.return_value.json.return_value = [data1, data2]
    return mock


def test_getphotos(mockRequestsGet):
    photos = getPhotos()
    assert len(photos) == 2
    assert all(isinstance(photo, Photo) for photo in photos)
    assert photos[1].dimensions == (800, 600)
    assert photos[1].likes == 10
    assert photos[1].description == "A beautiful landscape"
    assert photos[1].getContents('small') == 'http://example.com/small'
    assert mockRequestsGet.called


@pytest.fixture
def mockRequestsGetOne(mocker):
    data = {
        'id': 'ABC',
        'width': 100,
        'height': 200,
        'likes': 5,
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
    mock = mocker.patch("requests.get")
    mock.return_value.json.return_value = data
    return mock


def test_getphotowithid(mockRequestsGetOne):
    photo = getPhotoWithID("ABC")
    assert isinstance(photo, Photo)
    assert photo.likes == 5
    assert photo.dimensions == (100, 200)
    assert mockRequestsGetOne.called
