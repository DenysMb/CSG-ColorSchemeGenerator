import subprocess
from utils import selectColor, setColorScheme, kcolorschemes, lighten

prefix = "CSG-"

createDirectoryCommand = f'mkdir -p {kcolorschemes}'
subprocess.Popen(createDirectoryCommand.split(), stdout=subprocess.PIPE)

hexColor, rgbTuple, accentRgbTuple = selectColor(True)

defaultName = f'{prefix}{hexColor.lstrip("#")}'.upper()

customName = input(
    f"Write a name for the colorscheme or leave it blank to use the default name ({defaultName}): ")

colorName = customName if len(customName.strip()) else defaultName

newColorScheme = f'{kcolorschemes}/{colorName}.colors'
newColorSchemeNoHeader = f'{kcolorschemes}/{colorName}-NoHeader.colors'
newColorSchemeDarkHeader = f'{kcolorschemes}/{colorName}-DarkHeader.colors'
newColorSchemePlain = f'{kcolorschemes}/{colorName}-Plain.colors'

colorScheme, mode = setColorScheme(rgbTuple)

subprocess.Popen(f'cp {colorScheme} {newColorScheme}'.split(),
                 stdout=subprocess.PIPE).wait()
subprocess.Popen(
    f'cp {colorScheme} {newColorSchemeNoHeader}'.split(), stdout=subprocess.PIPE).wait()
subprocess.Popen(
    f'cp {colorScheme} {newColorSchemeDarkHeader}'.split(), stdout=subprocess.PIPE).wait()
subprocess.Popen(
    f'cp {colorScheme} {newColorSchemePlain}'.split(), stdout=subprocess.PIPE).wait()

# SET COLORS

background1 = lighten(rgbTuple, 1)
background2 = lighten(rgbTuple, 1.1)
background3 = lighten(rgbTuple, 0.8)
background4 = lighten(rgbTuple, 0.9)
background5 = lighten(rgbTuple, 1.2)
background6 = lighten(rgbTuple, 1.2)
accent1 = lighten(accentRgbTuple, 1)
accent2 = lighten(accentRgbTuple, 0.9)
accent3 = lighten(accentRgbTuple, 1.1)
header1 = background2
header2 = background1
header3 = background4

# NORMAL STYLE
colorSchemeFile = open(newColorScheme, "r")
colorSchemeLines = colorSchemeFile.readlines()
colorSchemeFile.close()

newColorSchemeFile = open(newColorScheme, "w")

for line in colorSchemeLines:
    if "{BACKGROUND_1}" in line:
        line = line.replace("{BACKGROUND_1}", background1)
    if "{BACKGROUND_2}" in line:
        line = line.replace("{BACKGROUND_2}", background2)
    if "{BACKGROUND_3}" in line:
        line = line.replace("{BACKGROUND_3}", background3)
    if "{BACKGROUND_4}" in line:
        line = line.replace("{BACKGROUND_4}", background4)
    if "{BACKGROUND_5}" in line:
        line = line.replace("{BACKGROUND_5}", background5)
    if "{BACKGROUND_6}" in line:
        line = line.replace("{BACKGROUND_6}", background6)
    if "{ACCENT_1}" in line:
        line = line.replace("{ACCENT_1}", accent1)
    if "{ACCENT_2}" in line:
        line = line.replace("{ACCENT_2}", accent2)
    if "{ACCENT_3}" in line:
        line = line.replace("{ACCENT_3}", accent3)
    if "{HEADER_1}" in line:
        line = line.replace("{HEADER_1}", header1)
    if "{HEADER_2}" in line:
        line = line.replace("{HEADER_2}", header2)
    if "{NAME}" in line:
        line = line.replace("{NAME}", colorName)
    newColorSchemeFile.write(line)

newColorSchemeFile.close()

# NO HEADER STYLE
colorSchemeFileNoHeader = open(newColorSchemeNoHeader, "r")
colorSchemeNoHeaderLines = colorSchemeFileNoHeader.readlines()
colorSchemeFileNoHeader.close()

newColorSchemeFileNoHeader = open(newColorSchemeNoHeader, "w")

for line in colorSchemeNoHeaderLines:
    if "{BACKGROUND_1}" in line:
        line = line.replace("{BACKGROUND_1}", background1)
    if "{BACKGROUND_2}" in line:
        line = line.replace("{BACKGROUND_2}", background2)
    if "{BACKGROUND_3}" in line:
        line = line.replace("{BACKGROUND_3}", background3)
    if "{BACKGROUND_4}" in line:
        line = line.replace("{BACKGROUND_4}", background4)
    if "{BACKGROUND_5}" in line:
        line = line.replace("{BACKGROUND_5}", background5)
    if "{BACKGROUND_6}" in line:
        line = line.replace("{BACKGROUND_6}", background6)
    if "{ACCENT_1}" in line:
        line = line.replace("{ACCENT_1}", accent1)
    if "{ACCENT_2}" in line:
        line = line.replace("{ACCENT_2}", accent2)
    if "{ACCENT_3}" in line:
        line = line.replace("{ACCENT_3}", accent3)
    if "{HEADER_1}" in line:
        line = line.replace(
            "{HEADER_1}", header2 if mode == "dark" else header1)
    if "{HEADER_2}" in line:
        line = line.replace(
            "{HEADER_2}", header2 if mode == "dark" else header1)
    if "{NAME}" in line:
        line = line.replace("{NAME}", f'{colorName}-NoHeader')
    newColorSchemeFileNoHeader.write(line)

newColorSchemeFileNoHeader.close()

# PLAIN STYLE
colorSchemeFilePlain = open(newColorSchemePlain, "r")
colorSchemePlainLines = colorSchemeFilePlain.readlines()
colorSchemeFilePlain.close()

newColorSchemeFilePlain = open(newColorSchemePlain, "w")

for line in colorSchemePlainLines:
    if "{BACKGROUND_1}" in line:
        line = line.replace(
            "{BACKGROUND_1}", background1 if mode == "dark" else background2)
    if "{BACKGROUND_2}" in line:
        line = line.replace(
            "{BACKGROUND_2}", background1 if mode == "dark" else background2)
    if "{BACKGROUND_3}" in line:
        line = line.replace(
            "{BACKGROUND_3}", background1 if mode == "dark" else background2)
    if "{BACKGROUND_4}" in line:
        line = line.replace(
            "{BACKGROUND_4}", background1 if mode == "dark" else background2)
    if "{BACKGROUND_5}" in line:
        line = line.replace(
            "{BACKGROUND_5}", background1 if mode == "dark" else background2)
    if "{BACKGROUND_6}" in line:
        line = line.replace(
            "{BACKGROUND_6}", background1 if mode == "dark" else background2)
    if "{ACCENT_1}" in line:
        line = line.replace("{ACCENT_1}", accent1)
    if "{ACCENT_2}" in line:
        line = line.replace("{ACCENT_2}", accent2)
    if "{ACCENT_3}" in line:
        line = line.replace("{ACCENT_3}", accent3)
    if "{HEADER_1}" in line:
        line = line.replace(
            "{HEADER_1}", background1 if mode == "dark" else background2)
    if "{HEADER_2}" in line:
        line = line.replace(
            "{HEADER_2}", background1 if mode == "dark" else background2)
    if "{NAME}" in line:
        line = line.replace("{NAME}", f'{colorName}-Plain')
    newColorSchemeFilePlain.write(line)

newColorSchemeFilePlain.close()

# DARK HEADER STYLE
colorSchemeFileDarkHeader = open(newColorSchemeDarkHeader, "r")
colorSchemeDarkHeaderLines = colorSchemeFileDarkHeader.readlines()
colorSchemeFileDarkHeader.close()

newColorSchemeFileDarkHeader = open(newColorSchemeDarkHeader, "w")

for line in colorSchemeDarkHeaderLines:
    if "{BACKGROUND_1}" in line:
        line = line.replace("{BACKGROUND_1}", background1)
    if "{BACKGROUND_2}" in line:
        line = line.replace("{BACKGROUND_2}", background2)
    if "{BACKGROUND_3}" in line:
        line = line.replace("{BACKGROUND_3}", background3)
    if "{BACKGROUND_4}" in line:
        line = line.replace("{BACKGROUND_4}", background4)
    if "{BACKGROUND_5}" in line:
        line = line.replace("{BACKGROUND_5}", background5)
    if "{BACKGROUND_6}" in line:
        line = line.replace("{BACKGROUND_6}", background6)
    if "{ACCENT_1}" in line:
        line = line.replace("{ACCENT_1}", accent1)
    if "{ACCENT_2}" in line:
        line = line.replace("{ACCENT_2}", accent2)
    if "{ACCENT_3}" in line:
        line = line.replace("{ACCENT_3}", accent3)
    if "{HEADER_1}" in line:
        line = line.replace(
            "{HEADER_1}", header3 if mode == "dark" else header2)
    if "{HEADER_2}" in line:
        line = line.replace(
            "{HEADER_2}", header3 if mode == "dark" else header2)
    if "{NAME}" in line:
        line = line.replace("{NAME}", f'{colorName}-DarkHeader')
    newColorSchemeFileDarkHeader.write(line)

newColorSchemeFileDarkHeader.close()

subprocess.Popen(f'plasma-apply-colorscheme {colorName}'.split(),
                 stdout=subprocess.PIPE).wait()
