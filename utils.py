import colorsys
import subprocess
import os
from PIL import Image
from colorthief import ColorThief

dir = os.path.dirname(__file__)
darkColorScheme = f"{dir}/TemplateDark.colors"
lightColorScheme = f"{dir}/TemplateLight.colors"
kwinrules = os.path.expanduser("~/.config/kwinrulesrc")
kcolorschemes = os.path.expanduser("~/.local/share/color-schemes")
config = os.path.expanduser(
    "~/.config/plasma-org.kde.plasma.desktop-appletsrc")


def lighten(color, amount=0.5):
    r = color[0]
    g = color[1]
    b = color[2]

    hslColor = colorsys.rgb_to_hls(r, g, b)

    newR = hslColor[0] if hslColor[0] <= 255 else 255
    newG = 1 - amount * (1 - hslColor[1])
    newB = hslColor[2]

    colorTuple = colorsys.hls_to_rgb(newR, newG, newB)

    colorList = list(colorTuple)
    colorList[:] = [x if x <= 255 else 255 for x in colorList]
    colorTuple = tuple(colorList)

    return f'{",".join(map(str, tuple(map(int, colorTuple))))}'


def setColorScheme(color):
    r = color[0]
    g = color[1]
    b = color[2]

    if (r*0.299 + g*0.587 + b*0.114) > 186:
        return (lightColorScheme, "light")
    else:
        return (darkColorScheme, "dark")


def selectColor(willSelectAccent):
    print("Select window color from screen")

    kcolorchooserCommand = 'kcolorchooser --print'

    hexColor = subprocess.check_output(
        kcolorchooserCommand.split(), universal_newlines=True).strip()

    print(f'Window color: {hexColor}')

    rgbTuple = tuple(int(hexColor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    accentRgbTuple = (61, 174, 233)

    if (willSelectAccent):
        print("Select accent color from screen")

        accentHexColor = subprocess.check_output(
            kcolorchooserCommand.split(), universal_newlines=True).strip()

        print(f'Accent color: {accentHexColor}')

        accentRgbTuple = tuple(int(accentHexColor.lstrip('#')[
                               i:i+2], 16) for i in (0, 2, 4))

        return hexColor, rgbTuple, accentRgbTuple

    return hexColor, rgbTuple, accentRgbTuple
