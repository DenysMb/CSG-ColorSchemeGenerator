import subprocess
import re
from utils import lighten, selectColor, setColorScheme, kwinrules, kcolorschemes

prefix = "TKP-"

subprocess.Popen(f'touch {kwinrules}'.split(), stdout=subprocess.PIPE)

createDirectoryCommand = f'mkdir -p {kcolorschemes}'
subprocess.Popen(createDirectoryCommand.split(), stdout=subprocess.PIPE)

print("Select a application")

xpropCommand = "xprop"
xpropList = subprocess.check_output(xpropCommand.split(), universal_newlines=True).strip().split()
xpropTitleIndex = 0

for (index, item) in enumerate(xpropList):
  if item == "WM_CLASS(STRING)":
    xpropTitleIndex = index + 2

name = xpropList[xpropTitleIndex].replace(',', '').replace('"', '')
appName = ''.join(x.capitalize() for x in re.split(r"[^a-zA-Z0-9 \s]", xpropList[xpropTitleIndex]))
ruleName = f'{prefix}{appName}'

print(f'Name: {name}')

hexColor, rgbTuple, rgbColor, darkRgbColor = selectColor(False)

newColorScheme=f'{kcolorschemes}/{ruleName}.colors'

colorScheme = setColorScheme(rgbTuple)

subprocess.Popen(f'cp {colorScheme} {newColorScheme}'.split(), stdout=subprocess.PIPE).wait()

colorSchemeFile = open(newColorScheme, "r")
lines = colorSchemeFile.readlines()
colorSchemeFile.close()

newColorSchemeFile = open(newColorScheme, "w")

for line in lines:
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
    line = f'[General]\nName={ruleName}\n'
  newColorSchemeFile.write(line)

newColorSchemeFile.close()

kwinRulesFile = open(kwinrules, "r")

isInGeneral = False
isAlreadyInKwinrules = False
groupIndex = 0
kgroupnum = 0
kgroupstr = ""

for line in kwinRulesFile:
  if "Description" in line and not isAlreadyInKwinrules:
    groupIndex += 1
    isAlreadyInKwinrules = ruleName in line
  if "[General]" in line:
    isInGeneral = True
  if not isInGeneral:
    continue
  if not len(line.split()):
    continue
  if "count" in line.split()[0]:
    kgroupnum = line.split('=')[1].strip()
  if "rules" in line.split()[0]:
    kgroupstr = line.split('=')[1].strip()

kwinRulesFile.close()

groupIndex = groupIndex + 1 if not isAlreadyInKwinrules else groupIndex

def writeConfig(key, value):
  command = f'kwriteconfig5 --file {kwinrules} --group {groupIndex} --key {key} {value}'
  subprocess.Popen(command.split(), stdout=subprocess.PIPE).wait()

if  not isAlreadyInKwinrules:
  writeConfig("Description", ruleName)
  writeConfig("decocolor", ruleName)
  writeConfig("decocolorrule", 2)
  writeConfig("wmclass", name)
  writeConfig("wmclassmatch", 1)

  newCount = f'kwriteconfig5 --file {kwinrules} --group General --key count {int(kgroupnum) + 1}'
  subprocess.Popen(newCount.split(), stdout=subprocess.PIPE).wait()

  newRulesStr = f'{kgroupstr},{groupIndex}'
  newRules = f'kwriteconfig5 --file {kwinrules} --group General --key rules {newRulesStr if kgroupstr else groupIndex}'
  subprocess.Popen(newRules.split(), stdout=subprocess.PIPE).wait()

  qdbusCommand = f'qdbus-qt5 org.kde.KWin /KWin reconfigure'
  subprocess.Popen(qdbusCommand.split(), stdout=subprocess.PIPE).wait()
else:
  qdbusCommand = f'qdbus-qt5 org.kde.KWin /KWin reconfigure'

  writeConfig("decocolor", "BreezeDark")
  
  subprocess.Popen(qdbusCommand.split(), stdout=subprocess.PIPE).wait()

  subprocess.Popen('sleep 1'.split(), stdout=subprocess.PIPE).wait()
  
  writeConfig("decocolor", ruleName)
  
  subprocess.Popen(qdbusCommand.split(), stdout=subprocess.PIPE).wait()
