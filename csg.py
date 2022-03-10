import subprocess
from utils import lighten, selectColor, setColorScheme, kcolorschemes

prefix = "CSG-"

createDirectoryCommand = f'mkdir -p {kcolorschemes}'
subprocess.Popen(createDirectoryCommand.split(), stdout=subprocess.PIPE)

print("Select a color from screen")

hexColor, rgbTuple, rgbColor, darkRgbColor = selectColor()

colorName = f'{prefix}{hexColor.lstrip("#")}'.upper()
newColorScheme=f'{kcolorschemes}/{colorName}.colors'
newColorSchemeAlt=f'{kcolorschemes}/{colorName}-Alt.colors'

colorScheme = setColorScheme(rgbTuple)

subprocess.Popen(f'cp {colorScheme} {newColorScheme}'.split(), stdout=subprocess.PIPE).wait()
subprocess.Popen(f'cp {colorScheme} {newColorSchemeAlt}'.split(), stdout=subprocess.PIPE).wait()

colorSchemeFile = open(newColorScheme, "r")
colorSchemeLines = colorSchemeFile.readlines()
colorSchemeFile.close()

newColorSchemeFile = open(newColorScheme, "w")

for line in colorSchemeLines:
  if "Name" in line:
    continue
  if "BackgroundNormal" in line:
    line = f'BackgroundNormal={rgbColor}\n'
  if "BackgroundAlternate" in line:
    line = f'BackgroundAlternate={rgbColor}\n'
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

for line in colorSchemeAltLines:
  if "[Colors:Header]" in line:
    isInHeader = True
  if "[Colors:Selection]" in line:
    isInHeader = False
  if "Name" in line:
    continue
  if "BackgroundNormal" in line:
    line = f'BackgroundNormal={darkRgbColor if isInHeader else rgbColor}\n'
  if "BackgroundAlternate" in line:
    line = f'BackgroundAlternate={darkRgbColor if isInHeader else rgbColor}\n'
  if "activeBackground" in line:
    line = f'activeBackground={darkRgbColor}\n'
  if "inactiveBackground" in line:
    line = f'inactiveBackground={darkRgbColor}\n'
  if "[General]" in line:
    line = f'[General]\nName={colorName}-Alt\n'
  newColorSchemeFileAlt.write(line)

newColorSchemeFileAlt.close()
