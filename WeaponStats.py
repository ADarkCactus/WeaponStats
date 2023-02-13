import json
import re
import PySimpleGUI as sg

# Load PlayerOfflineGear Datablock
with open("GameData_PlayerOfflineGearDataBlock_bin.json") as playerOfflineGearDB:
    playerOfflineGearDict = json.load(playerOfflineGearDB)

# Load GearCategory Datablock
with open("GameData_GearCategoryDataBlock_bin.json") as gearCategoryDB:
    gearCategoryDict = json.load(gearCategoryDB)

# Load Archetype Datablock
with open("GameData_ArchetypeDataBlock_bin.json") as archetypeDB:
    archetypeDict = json.load(archetypeDB)

# Empty weapon map
weaponMap = {}

# Function to generate map
def genWeaponMap():
    """Iterates through datablocks and generates map of {weaponName: archetype}"""
    # Search for possible weapons in PlayerOfflineGearDB
    for weapon in playerOfflineGearDict["Blocks"]:
        components = weapon["GearJSON"]
        if "{\"c\":6" in components:
            global weaponName
            weaponName = weapon["name"]
            # Find gearCategoryID
            gearCategoryResults = re.findall(r"{\"c\":2,\"v\":(\d+)", weapon["GearJSON"])
            gearCategoryID = int(gearCategoryResults[0])
            # Determine FireMode for weapon
            # Auto FireMode
            if "{\"c\":1,\"v\":2}" in components:
                # Find ArchetypeID
                for gearcategory in gearCategoryDict["Blocks"]:
                    if gearCategoryID == gearcategory["persistentID"]:
                        archetypeID = gearcategory["AutoArchetype"]
                        # Print archetype datablock
                        updateArchetype(archetypeID)
            # Semi FireMode
            elif "{\"c\":1,\"v\":0}" in components:
                for gearcategory in gearCategoryDict["Blocks"]:
                    if gearCategoryID == gearcategory["persistentID"]:
                        archetypeID = gearcategory["SemiArchetype"]
                        updateArchetype(archetypeID)
            # Burst FireMode
            elif "{\"c\":1,\"v\":1}" in components:
                for gearcategory in gearCategoryDict["Blocks"]:
                    if gearCategoryID == gearcategory["persistentID"]:
                        archetypeID = gearcategory["BurstArchetype"]
                        updateArchetype(archetypeID)
            # Semi-Burst FireMode
            elif "{\"c\":1,\"v\":3}" in components:
                for gearcategory in gearCategoryDict["Blocks"]:
                    if gearCategoryID == gearcategory["persistentID"]:
                        archetypeID = gearcategory["SemiBurstArchetype"]
                        updateArchetype(archetypeID)
            # Default/Semi FireMode
            else:
                for gearcategory in gearCategoryDict["Blocks"]:
                    if gearCategoryID == gearcategory["persistentID"]:
                        archetypeID = gearcategory["SemiArchetype"]
                        updateArchetype(archetypeID)

def updateArchetype(archetypeID):
    """Takes archetypeid from genWeaponMap() and prints archetype datablock"""
    for archetype in archetypeDict["Blocks"]:
        if archetypeID == archetype["persistentID"]:
            weaponMap.update({weaponName: archetype})

def updateWeaponStats():
    """Function for updating weapon stats displyaed in the PSG window."""
    # Retrieve matching weapon stats
    weaponStats = weaponMap.get(weaponPrompt) 
    # Clear and update data shown
    window['-OUTPUT-'].update("")
    window['-OUTPUT-'].print(json.dumps(weaponStats, indent=4))

# Map weapons in POG to their archetypes.
genWeaponMap()

# List of weapon names to use in PSG
weaponList = list(weaponMap.keys())

# PySimpleGUI settings
sg.theme("Black")
sg.set_options(font="Consolas")

# PySimpleGUI Layout
layout = [
    [sg.Titlebar("WeaponStats",background_color="black",text_color="#fdef14")],
    [sg.Text("SELECT A WEAPON FROM THE LIST",text_color="#ff0d0c")],
    [sg.DropDown(weaponList,default_value=weaponList[0],key='-DD-',background_color="black",text_color="#ff0d0c"), 
    sg.Button("SEARCH",key='-BUTTON-',button_color="#ff0d0c")],
    [sg.Multiline(size=(75,45),key='-OUTPUT-',text_color="#fdef14",background_color="black")]
        ]

# Generates PySimpleGUI window
window = sg.Window('WeaponStats', layout)

# Main Loop
while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-BUTTON-':
        weaponPrompt = values['-DD-']
        updateWeaponStats()

window.close()




            


