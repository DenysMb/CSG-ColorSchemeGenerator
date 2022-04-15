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

hexColor, rgbTuple, accentRgbTuple = selectColor(False)

rgbColor = lighten(rgbTuple, 1)
accentColor = lighten(accentRgbTuple, 1)

newColorScheme=f'{kcolorschemes}/{ruleName}.colors'

colorScheme, mode = setColorScheme(rgbTuple)

subprocess.Popen(f'cp {colorScheme} {newColorScheme}'.split(), stdout=subprocess.PIPE).wait()

colorSchemeFile = open(newColorScheme, "r")
lines = colorSchemeFile.readlines()
colorSchemeFile.close()

newColorSchemeFile = open(newColorScheme, "w")

for line in lines:
  if "{BACKGROUND_1}" in line:
        line = line.replace("{BACKGROUND_1}", rgbColor)
  if "{BACKGROUND_2}" in line:
      line = line.replace("{BACKGROUND_2}", rgbColor)
  if "{BACKGROUND_3}" in line:
      line = line.replace("{BACKGROUND_3}", rgbColor)
  if "{BACKGROUND_4}" in line:
      line = line.replace("{BACKGROUND_4}", rgbColor)
  if "{BACKGROUND_5}" in line:
      line = line.replace("{BACKGROUND_5}", rgbColor)
  if "{BACKGROUND_6}" in line:
      line = line.replace("{BACKGROUND_6}", rgbColor)
  if "{ACCENT_1}" in line:
      line = line.replace("{ACCENT_1}", accentColor)
  if "{ACCENT_2}" in line:
      line = line.replace("{ACCENT_2}", accentColor)
  if "{ACCENT_3}" in line:
      line = line.replace("{ACCENT_3}", accentColor)
  if "{HEADER_1}" in line:
      line = line.replace("{HEADER_1}", rgbColor)
  if "{HEADER_2}" in line:
      line = line.replace("{HEADER_2}", rgbColor)
  if "{NAME}" in line:
      line = line.replace("{NAME}", ruleName)
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
