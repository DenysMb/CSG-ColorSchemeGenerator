import colorsys
import subprocess
import os
from PIL import Image
from colorthief import ColorThief

darkColorScheme = "/usr/share/color-schemes/BreezeDark.colors"
lightColorScheme = "/usr/share/color-schemes/BreezeLight.colors"
kwinrules = os.path.expanduser("~/.config/kwinrulesrc")
kcolorschemes = os.path.expanduser("~/.local/share/color-schemes")
config = os.path.expanduser(
    "~/.config/plasma-org.kde.plasma.desktop-appletsrc")


def lighten(color, amount=0.5):
    r = color[0]
    g = color[1]
    b = color[2]

    hslColor = colorsys.rgb_to_hls(r, g, b)
    newColor = colorsys.hls_to_rgb(
        hslColor[0], 1 - amount * (1 - hslColor[1]), hslColor[2])

    return f'{",".join(map(str, tuple(map(int, newColor))))}'


def setColorScheme(color):
    r = color[0]
    g = color[1]
    b = color[2]

    if (r*0.299 + g*0.587 + b*0.114) > 186:
        return lightColorScheme
    else:
        return darkColorScheme


def selectColor(willSelectAccent):
    print("Select window color from screen")

    kcolorchooserCommand = 'kcolorchooser --print'

    hexColor = subprocess.check_output(
        kcolorchooserCommand.split(), universal_newlines=True).strip()

    print(f'Window color: {hexColor}')

    rgbTuple = tuple(int(hexColor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    rgbColor = f'{",".join(map(str,rgbTuple))}'

    darkRgbColor = lighten(rgbTuple, 0.9)

    if (willSelectAccent):
        print("Select accent color from screen")

        accentHexColor = subprocess.check_output(
            kcolorchooserCommand.split(), universal_newlines=True).strip()

        print(f'Accent color: {accentHexColor}')

        accentRgbTuple = tuple(int(accentHexColor.lstrip('#')[
                               i:i+2], 16) for i in (0, 2, 4))

        accentRgbColor = f'{",".join(map(str,accentRgbTuple))}'

        return hexColor, rgbTuple, rgbColor, darkRgbColor, accentRgbColor

    return hexColor, rgbTuple, rgbColor, darkRgbColor


def getWallpaper():
    configFile = open(config, "r")

    isInWallpaper = False
    imagePath = ''

    for line in configFile:
        if "[" in line:
            isInWallpaper = False
        if "[Wallpaper]" in line:
            isInWallpaper = True
        if "Image" in line and isInWallpaper:
            imagePath = line[6:].rstrip()
            break

    configFile.close()

    return imagePath


def getPalette(imagePath):
    imageFile = Image.open(imagePath).resize((150, 150))
    imageExtension = imagePath.split('.')[-1]

    resizedImageName = f'/tmp/resized.{imageExtension}'
    imageFile.save(resizedImageName)
    resizedImagePath = os.path.expanduser(resizedImageName)

    colorThief = ColorThief(resizedImagePath)
    palette = colorThief.get_palette(color_count=2)

    return palette
