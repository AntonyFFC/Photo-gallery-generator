from unsplash.api import Api
from unsplash.auth import Auth
from PIL import Image, ImageFilter
from gallery import Gallery
from io import BytesIO
import requests
import photos


def main():
    pic = photos.getPhotoWithID('04X1Yp9hNH8')

    image = requests.get(pic.getContents("small"))

    imageData = image.content

    im = Image.open(BytesIO(imageData))
    im.show()


if __name__ == "__main__":
    main()