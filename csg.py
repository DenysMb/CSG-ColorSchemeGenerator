import subprocess
from utils import lighten, selectColor, setColorScheme, kcolorschemes

prefix = "CSG-"

createDirectoryCommand = f'mkdir -p {kcolorschemes}'
subprocess.Popen(createDirectoryCommand.split(), stdout=subprocess.PIPE)

hexColor, rgbTuple, rgbColor, darkRgbColor, accentRgbColor = selectColor(True)

defaultName = f'{prefix}{hexColor.lstrip("#")}'.upper()

customName = input(
    f"Write a name for the colorscheme or leave it blank to use the default name ({defaultName}): ")

colorName = customName if len(customName.strip()) else defaultName

newColorScheme = f'{kcolorschemes}/{colorName}.colors'
newColorSchemeAlt = f'{kcolorschemes}/{colorName}-Alt.colors'
newColorSchemePlain = f'{kcolorschemes}/{colorName}-Plain.colors'

colorScheme = setColorScheme(rgbTuple)

subprocess.Popen(f'cp {colorScheme} {newColorScheme}'.split(),
                 stdout=subprocess.PIPE).wait()
subprocess.Popen(
    f'cp {colorScheme} {newColorSchemeAlt}'.split(), stdout=subprocess.PIPE).wait()
subprocess.Popen(
    f'cp {colorScheme} {newColorSchemePlain}'.split(), stdout=subprocess.PIPE).wait()

colorSchemeFile = open(newColorScheme, "r")
colorSchemeLines = colorSchemeFile.readlines()
colorSchemeFile.close()

newColorSchemeFile = open(newColorScheme, "w")

isInSelection = False
isInView = False

for line in colorSchemeLines:
    if "[Colors:Selection]" in line:
        isInSelection = True
    if "[Colors:Tooltip]" in line:
        isInSelection = False
    if "[Colors:View]" in line:
        isInView = True
    if "[Colors:Window]" in line:
        isInView = False
    if "Name" in line:
        continue
    if "BackgroundNormal" in line:
        line = f'BackgroundNormal={darkRgbColor if isInView else rgbColor if not isInSelection else accentRgbColor}\n'
    if "BackgroundAlternate" in line:
        line = f'BackgroundAlternate={darkRgbColor if isInView else rgbColor if not isInSelection else accentRgbColor}\n'
    if "DecorationFocus" in line:
        line = f'DecorationFocus={accentRgbColor}\n'
    if "DecorationHover" in line:
        line = f'DecorationHover={accentRgbColor}\n'
    if "activeBackground" in line:
        line = f'activeBackground={rgbColor}\n'
    if "inactiveBackground" in line:
        line = f'inactiveBackground={rgbColor}\n'
    if "[General]" in line:
        line = f'[General]\nName={colorName}\n'
    newColorSchemeFile.write(line)

newColorSchemeFile.close()

colorSchemeFileAlt = open(newColorSchemeAlt, "r")
colorSchemeAltLines = colorSchemeFileAlt.readlines()
colorSchemeFileAlt.close()

newColorSchemeFileAlt = open(newColorSchemeAlt, "w")

isInHeader = False
isInSelection = False
isInView = False

for line in colorSchemeAltLines:
    if "[Colors:Header]" in line:
        isInHeader = True
    if "[Colors:Selection]" in line:
        isInSelection = True
        isInHeader = False
    if "[Colors:Tooltip]" in line:
        isInSelection = False
    if "[Colors:View]" in line:
        isInView = True
    if "[Colors:Window]" in line:
        isInView = False
    if "Name" in line:
        continue
    if "BackgroundNormal" in line:
        line = f'BackgroundNormal={darkRgbColor if isInHeader or isInView else rgbColor if not isInSelection else accentRgbColor}\n'
    if "BackgroundAlternate" in line:
        line = f'BackgroundAlternate={darkRgbColor if isInHeader or isInView else rgbColor if not isInSelection else accentRgbColor}\n'
    if "DecorationFocus" in line:
        line = f'DecorationFocus={accentRgbColor}\n'
    if "DecorationHover" in line:
        line = f'DecorationHover={accentRgbColor}\n'
    if "activeBackground" in line:
        line = f'activeBackground={darkRgbColor}\n'
    if "inactiveBackground" in line:
        line = f'inactiveBackground={darkRgbColor}\n'
    if "[General]" in line:
        line = f'[General]\nName={colorName}-Alt\n'
    newColorSchemeFileAlt.write(line)

newColorSchemeFileAlt.close()

colorSchemeFilePlain = open(newColorSchemePlain, "r")
colorSchemePlainLines = colorSchemeFilePlain.readlines()
colorSchemeFilePlain.close()

newColorSchemeFilePlain = open(newColorSchemePlain, "w")

isInSelection = False

for line in colorSchemeLines:
    if "[Colors:Selection]" in line:
        isInSelection = True
    if "[Colors:Tooltip]" in line:
        isInSelection = False
    if "Name" in line:
        continue
    if "BackgroundNormal" in line:
        line = f'BackgroundNormal={darkRgbColor if isInView else rgbColor if not isInSelection else accentRgbColor}\n'
    if "BackgroundAlternate" in line:
        line = f'BackgroundAlternate={darkRgbColor if isInView else rgbColor if not isInSelection else accentRgbColor}\n'
    if "DecorationFocus" in line:
        line = f'DecorationFocus={accentRgbColor}\n'
    if "DecorationHover" in line:
        line = f'DecorationHover={accentRgbColor}\n'
    if "activeBackground" in line:
        line = f'activeBackground={rgbColor}\n'
    if "inactiveBackground" in line:
        line = f'inactiveBackground={rgbColor}\n'
    if "[General]" in line:
        line = f'[General]\nName={colorName}-Plain\n'
    newColorSchemeFilePlain.write(line)

newColorSchemeFilePlain.close()