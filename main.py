from unsplash.api import Api
from unsplash.auth import Auth
from PIL import Image, ImageFilter
from gallery import Gallery
from io import BytesIO
import requests
import photos
from tabulate import tabulate
from colorama import Fore, Style


def main():
    printMenu()
    ans = input()
    try:
        functions[ans]()
    except KeyError:
        print("Invalid input")
    # pic = photos.getPhotoWithID('04X1Yp9hNH8')

    # image = requests.get(pic.getContents("small"))

    # imageData = image.content

    # im = Image.open(BytesIO(imageData))
    # im.show()


def printMenu():
    DescriptionTxt = """
    Welcome to the PhotoGallery Generator
    Choose your action by typing one of the options below:
    """
    print(Style.BRIGHT + DescriptionTxt)
    menuItems = [
        [Fore.BLUE + Style.BRIGHT + "'1'" + Style.RESET_ALL,
         Style.BRIGHT + "Generate new photogallery"],
        [Fore.BLUE + Style.BRIGHT + "'2'" + Style.RESET_ALL,
         Style.BRIGHT + "Open an existing photogallery" + Style.RESET_ALL],
        [Fore.BLUE + Style.BRIGHT + "'3'" + Style.RESET_ALL,
         Style.BRIGHT + "Make a collage out of photos from a photogallery"
         + Style.RESET_ALL],
        [Fore.BLUE + Style.BRIGHT + "'4'" + Style.RESET_ALL,
         Style.BRIGHT + "Add an effect to a photo from a photogallery"
         + Style.RESET_ALL],
    ]
    print(tabulate(menuItems, headers=["Option", "Description"]))


def GenerateNewGall():
    generateFunctions = {
        '1': GenerateLight,
        '2': Generate,
    }

    print(Style.BRIGHT + "\nChoose One")
    menuItems = [
        [Fore.BLUE + Style.BRIGHT + "'1'" + Style.RESET_ALL,
         Style.BRIGHT + "Generate photogallery using only a few photo requests (less precise)"],
        [Fore.BLUE + Style.BRIGHT + "'2'" + Style.RESET_ALL,
         Style.BRIGHT + "Generate photogallery using only a lot of photo requests (more precise)" + Style.RESET_ALL],
    ]
    print(tabulate(menuItems, headers=["Option", "Description"]))
    ans = input()
    try:
        generateFunctions[ans]()
    except KeyError:
        print("Invalid input")


def GenerateLight():
    print(Style.BRIGHT + "\nAfter each picture there will be a question if you want to add it to the gallery or not")
    print(Style.BRIGHT + "Give a theme for the photos (for example: 'nature', 'city', 'water')")
    theme = input()
    simValues, photsIDs = photos.getPhotoWithTopicLight(theme)
    for i, photID in enumerate(photsIDs):
        phot = photos.getPhotoWithID(photID)
        image = requests.get(phot.getContents("small"))
        imageData = image.content
        im = Image.open(BytesIO(imageData))
        im.show()


def Generate():
    print(Style.BRIGHT + "\nAfter each picture there will be a question if you want to add it to the gallery or not")
    print(Style.BRIGHT + "Give a theme for the photos (for example: 'nature', 'city', 'water')")
    theme = input()
    simValues, photsIDs = photos.getPhotoWithTopic(theme)
    for i, photID in enumerate(photsIDs):
        phot = photos.getPhotoWithID(photID)
        image = requests.get(phot.getContents("small"))
        imageData = image.content
        im = Image.open(BytesIO(imageData))
        im.show()


def OpenGall():
    pass


def MakeGallCol():
    pass


def AddEffect():
    pass


functions = {
    '1': GenerateNewGall,
    '2': OpenGall,
    '3': MakeGallCol,
    '4': AddEffect
}


if __name__ == "__main__":
    main()
