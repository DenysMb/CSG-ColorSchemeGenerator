import colorsys
import subprocess
import os

dir = os.path.dirname(__file__)
darkColorScheme = f"{dir}/Color-scheme/TemplateDark.colors"
lightColorScheme = f"{dir}/Color-scheme/TemplateLight.colors"
darkKonsoleColorScheme = f"{dir}/Konsole/TemplateDark.colorscheme"
lightKonsoleColorScheme = f"{dir}/Konsole/TemplateLight.colorscheme"
konsoleTemplate = f"{dir}/Konsole/Template.profile"
kwinrules = os.path.expanduser("~/.config/kwinrulesrc")
kcolorschemes = os.path.expanduser("~/.local/share/color-schemes")
konsoleDir = os.path.expanduser("~/.local/share/konsole")
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


def setKonsoleColorScheme(mode):
    if (mode == "light"):
        return (lightKonsoleColorScheme, konsoleTemplate)
    else:
        return (darkKonsoleColorScheme, konsoleTemplate)

def selectColor():
    print("Select window color from screen")

    kcolorchooserCommand = 'kcolorchooser --print'

    hexColor = subprocess.check_output(
        kcolorchooserCommand.split(), universal_newlines=True).strip()

    print(f'Window color: {hexColor}')

    rgbTuple = tuple(int(hexColor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    print("Select accent color from screen")

    accentHexColor = subprocess.check_output(
        kcolorchooserCommand.split(), universal_newlines=True).strip()

    print(f'Accent color: {accentHexColor}')

    accentRgbTuple = tuple(int(accentHexColor.lstrip('#')[
        i:i+2], 16) for i in (0, 2, 4))

    return hexColor, rgbTuple, accentRgbTuple

def generateKonsoleColors(name, mode, palette):
    colorName = name
    colorScheme, colorProfile = setKonsoleColorScheme(mode)
    background1 = lighten(palette, 1)
    background2 = lighten(palette, 1.1)
    background4 = lighten(palette, 0.9)

    createDirectoryCommand = f'mkdir -p {konsoleDir}'
    subprocess.Popen(createDirectoryCommand.split(),
                     stdout=subprocess.PIPE)

    newColorScheme = f'{konsoleDir}/{colorName}.colorscheme'
    newColorProfile = f'{konsoleDir}/{colorName}.profile'

    subprocess.Popen(f'cp {colorScheme} {newColorScheme}'.split(),
                     stdout=subprocess.PIPE).wait()
    subprocess.Popen(f'cp {colorProfile} {newColorProfile}'.split(),
                     stdout=subprocess.PIPE).wait()

    # COLOR SCHEME FILE
    colorSchemeFile = open(newColorScheme, "r")
    colorSchemeLines = colorSchemeFile.readlines()
    colorSchemeFile.close()

    newColorSchemeFile = open(newColorScheme, "w")

    for line in colorSchemeLines:
        if "{BACKGROUND_1}" in line:
            line = line.replace("{BACKGROUND_1}", background1)
        if "{BACKGROUND_2}" in line:
            line = line.replace("{BACKGROUND_2}", background2)
        if "{BACKGROUND_4}" in line:
            line = line.replace("{BACKGROUND_4}", background4)
        if "{NAME}" in line:
            line = line.replace("{NAME}", colorName)
        newColorSchemeFile.write(line)

    newColorSchemeFile.close()

    # PROFILE FILE
    colorProfileFile = open(newColorProfile, "r")
    colorProfileLines = colorProfileFile.readlines()
    colorProfileFile.close()

    newColorProfileFile = open(newColorProfile, "w")

    for line in colorProfileLines:
        if "{NAME}" in line:
            line = line.replace("{NAME}", colorName)
        newColorProfileFile.write(line)

    newColorProfileFile.close()