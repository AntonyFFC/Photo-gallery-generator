from PIL import Image, ImageFilter
from gallery import Gallery
from io import BytesIO
import requests
import photos
from tabulate import tabulate
from colorama import Fore, Style
import os


class invalidInputError(Exception):
    def __init__(self):
        super().__init__("The given input is invalid")


def main():
    printMenu()
    ans = input()
    try:
        functions[ans]()
    except KeyError:
        print("Invalid input")


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


def GenerateGall(gall=None):
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
        photoGalery = generateFunctions[ans](gall)
    except invalidInputError as e:
        raise e("Invalid input")
    retFromGenerate(photoGalery)


def retFromGenerate(photoGalery):
    generateFunctions = {
        '1': GenerateGall,
        '2': MakeGallCol,
    }

    print(Style.BRIGHT + "\nChoose one")
    menuItems2 = [
        [Fore.BLUE + Style.BRIGHT + "'1'" + Style.RESET_ALL,
         Style.BRIGHT + "Generate more photos to this gallery"],
        [Fore.BLUE + Style.BRIGHT + "'2'" + Style.RESET_ALL,
         Style.BRIGHT + "Create a collage out of photos from the gallery"],
        [Fore.BLUE + Style.BRIGHT + "'3'" + Style.RESET_ALL,
         Style.BRIGHT + "Return to main menu screen" + Style.RESET_ALL],
    ]
    print(tabulate(menuItems2, headers=["Option", "Description"]))
    ans = input()
    if ans != '3':
        try:
            newphotoGalery = generateFunctions[ans](photoGalery)
        except invalidInputError as e:
            raise e("Invalid input")
    else:
        main()


def GenerateLight(gall):
    if not gall:
        print(Style.BRIGHT + "\nGive a path for the gallery")
        path = input()
        print(Style.BRIGHT + "\nGive a theme for the photos (for example: 'person', 'city', 'water' etc.)")
        theme = input()
        thisGallery = Gallery([], theme, path)
    else:
        thisGallery = gall
        theme = thisGallery.title
    print("\nAfter each picture there will be a question if you want to add it to the gallery or not")
    simValues, photsIDs = photos.getPhotoWithTopicLight(theme)

    for i, photID in enumerate(reversed(photsIDs[-3:])):
        phot = photos.getPhotoWithID(photID)
        image = requests.get(phot.getContents("small"))
        imageData = image.content
        im = Image.open(BytesIO(imageData))
        im.show()

        print(Style.BRIGHT + "Do you want to add this picture to this gallery? ('Y'-yes 'N'-no)")
        ans = input()
        if ans.lower() == 'n':
            continue
        elif ans.lower() == 'y':
            thisGallery.addPict(phot)
        else:
            raise invalidInputError()
    if not gall:
        thisGallery.saveGallery()
    return thisGallery


def Generate(gall):
    if not gall:
        print(Style.BRIGHT + "\nGive a path for the gallery")
        path = input()
        print(Style.BRIGHT + "\nGive a theme for the photos (for example: 'person', 'city', 'water' etc.)")
        theme = input()
        thisGallery = Gallery([], theme, path)
    else:
        thisGallery = gall
        theme = thisGallery.title
    print("\nAfter each picture there will be a question if you want to add it to the gallery or not")
    simValues, photsIDs = photos.getPhotoWithTopic(theme)

    for i, photID in enumerate(reversed(photsIDs[-3:])):
        phot = photos.getPhotoWithID(photID)
        image = requests.get(phot.getContents("small"))
        imageData = image.content
        im = Image.open(BytesIO(imageData))
        im.show()

        print(Style.BRIGHT + "Do you want to add this picture to this gallery? ('Y'-yes 'N'-no)")
        ans = input()
        if ans.lower() == 'n':
            continue
        elif ans.lower() == 'y':
            thisGallery.addPict(phot)
        else:
            raise invalidInputError()
    if not gall:
        thisGallery.saveGallery()
    return thisGallery


def OpenGall():
    print(Style.BRIGHT + "Give the path for the gallery you want to open")
    path = input()
    pictures = []
    try:
        title = os.path.basename(path)
    except FileNotFoundError:
        raise FileNotFoundError("The gallery path is invalid")

    for file in os.listdir(path):
        if not file.endswith('.jpg'):
            continue
        name, ext = os.path.splitext(os.path.basename(file))
        pictures.append(photos.getPhotoWithID(name))

    thisGallery = Gallery(pictures, title)
    retFromGenerate(thisGallery)


def MakeGallCol(gall):
    print(Style.BRIGHT + "Write the numbers of the pictures you want to use in the collage, max 9 pictures")
    print("Write in the numbers devided by commas ex. 1, 3, 5")
    ans = input()
    indx = [int(item) for item in ans.split(',')]
    gall.makeCollage(indx)


def AddEffect():
    pass


functions = {
    '1': GenerateGall,
    '2': OpenGall,
    '3': MakeGallCol,
    '4': AddEffect
}


if __name__ == "__main__":
    main()
