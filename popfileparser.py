import os
import re
import sys

# a recursive function that returns keyvalue pairs in a list
def ParseTree(popfile, index):
    indexnumber = index
    keyvaluepairs = []
    key = ''
    value = ''
    iskey = True
    inquote = False
    insubtree = False
    depth = 0               # used to determine how many layers of brackets we're in after calling the function

    for i in popfile[index:]:
        indexnumber = indexnumber + 1

        # skip these characters
        if i == '{':
            depth += 1
            if depth == 1:
                insubtree = True
                # call this function again when we get to a subtree and pass the list of keyvalues through, index is at the curly bracket
                value = ParseTree(popfile, indexnumber)
                keyvaluepairs.append({key : value})
                key = ''
                value = ''
                # need this to be True
                iskey = True
            continue

        if i == '}':
            depth -= 1
            if depth == 0:
                insubtree = False
                continue
            # index started at the last open curly bracket, exit the function at the first closing curly bracket
            if depth == -1:
                return keyvaluepairs

        # keep quotes
        if i == '"':
            inquote = not inquote

        if insubtree == False:
            if inquote == False:
                if i.isspace() == False:
                    #if the index character is not whitespace, write character to key string, or value if its not a key
                    if iskey == True:
                        key = key + i
                    else:
                        value = value + i

                # if key is being written and we reach a white space, end the key and start value
                if key != '' and i.isspace() == True:
                    iskey = False
                # when we each the end of the value, update dictionary and reset key and value buffers
                if value != '' and i.isspace() == True:
                    iskey = True
                    if value != '{':
                        keyvaluepairs.append({key : value})
                        key = ''
                        value = ''

            #if we're inside a quote, include spaces
            else:
                if iskey == True:
                    key = key + i
                else:
                    value = value + i

    #if you've made it here, the end of the popfile has been reached
    return keyvaluepairs

#can print ParseTree's return in a legible format
def printpop(pop, indentationnumber):
    newindent = 0
    for i in pop:
        key = list(i)[0]
        value = i.get(key)
        print('\t' * indentationnumber, end = '')
        if isinstance(value, list):
            print(key, end = '')
            if key.lower() in KeyValuesLower or key.lower() in CustomAttributesLower:
                print('\t[$SIGSEGV]', end ='\n')
            else:
                print('', end ='\n')
            print('\t' * indentationnumber, end = '{\n')
            indentationnumber += 1
            newindent += 1
            printpop(value, indentationnumber)
            indentationnumber -= 1
            newindent -= 1
            if newindent == 0:
                print('\t' * indentationnumber, end = '}\n')
        else:
            print(key, value, end = '')
            if key.lower() in KeyValuesLower or key.lower() in CustomAttributesLower:
                print('\t[$SIGSEGV]', end ='\n')
            else:
                print('', end ='\n')







# directory/folder path
#
# change path if needed
dir_path = 'C:\\Users\\M\\Desktop\\New folder (2)'

# list to store files
res = []

# Iterate directory
for file_path in os.listdir(dir_path):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(dir_path, file_path)):
        # add filename to list
        res.append(file_path)

for i in range(0, len(res)):
    if res[i].startswith('mvm'):
        popfile = open(os.path.join(dir_path, res[i]),'r').read()







####################################################
#Action, FireWeapon, ChangeAttributes and anything that is a substring of a vanilla KeyValue is not included
KeyValues = set()
table = open(os.path.join(dir_path, 'keyvalues.txt'),'r').readlines()
for i in range(1, len(table)):
    KeyValues.add(table[i].split()[0])
KeyValues = list(KeyValues)
KeyValues.sort()
KeyValuesLower = [x.lower() for x in KeyValues]

CustomAttributes = []
table = open(os.path.join(dir_path, 'attributes.txt'),'r').readlines()
for i in range(1, len(table)):
    CustomAttributes.append('"' + table[i].split('"')[1] + '"')
CustomAttributes.sort()
CustomAttributesLower = [x.lower() for x in CustomAttributes]
####################################################










# #puts a [$SIGSEGV] tag back on non vanilla keyvalues
# def findsigkvs(kvlist, indentationnumber, previouskeyvalue):
#     #


#     # wip


#     #
#     def check(keyvalue, previouskeyvalue):
#         base = ['#base']
#         PopulationManager = ['Templates', 'StartingCurrency', 'RespawnWaveTime', 'EventPopfile', 'FixedRespawnWaveTime', 'AddSentryBusterWhenDamageDealtExceeds', 'AddSentryBusterWhenKillCountExceeds', 'CanBotsAttackWhileInSpawnRoom', 'Advanced', 'Endless']
#         Populator = ['RandomPlacement', 'PeriodicSpawn', 'Mission', 'Wave', 'WaveSpawn']
#         Spawners = ['Mob', 'SentryGun', 'Tank', 'TFBot', 'Squad', 'RandomChoice']

#         RandomPlacement = ['Count', 'MinimumSeparation', 'NavAreaFilter']
#         PeriodicSpawn = ['Where', 'When', 'MinInterval', 'MaxInterval']
#         Mission = ['Where', 'Objective', 'InitialCooldown', 'CooldownTime', 'BeginAtWave', 'RunForThisManyWaves', 'DesiredCount']
#         Wave = ['WaveSpawn', 'Sound', 'Description', 'WaitWhenDone', 'Checkpoint', 'StartWaveOutput', 'DoneOutput', 'InitWaveOutput']
#         Output = ['Target', 'Action']
#         WaveSpawn = ['Template', 'Where', 'TotalCount', 'MaxActive', 'SpawnCount', 'WaitBeforeStarting', 'WaitBetweenSpawns', 'WaitBetweenSpawnsAfterDeath', 'StartWaveWarningSound', 'StartWaveOutput', 'FirstSpawnWarningSound', 'FirstSpawnOutput', 'LastSpawnWarningSound', 'LastSpawnOutput', 'DoneWarningSound', 'DoneOutput', 'TotalCurrency', 'Name', 'WaitForAllSpawned', 'WaitForAllDead', 'Support', 'RandomSpawn']
#         Mob = ['Count']
#         SentryGun = ['Level']
#         TFBot = ['Template', 'Class', 'ClassIcon', 'Health', 'Scale', 'Name', 'TeleportWhere', 'AutoJumpMin', 'AutoJumpMax', 'Skill', 'WeaponRestrictions', 'BehaviorModifiers', 'MaxVisionRange', 'Item', 'Attributes', 'ItemAttributes', 'ItemName', 'CharacterAttributes', 'EventChangeAttributes']
#         EventChangeAttributes = ['Default', 'RevertGateBotsBehavior']
#         Squad = ['FormationSize', 'ShouldPreserveSquad']
#         RandomChoice = ['Spawner']

#         BehaviorModifiers = ['Idle', 'Push', 'Mobber']
#         Attributes = ['RemoveOnDeath', 'Aggressive', 'SuppressFire', 'DisableDodge', 'BecomeSpectatorOnDeath', 'RetainBuildings', 'SpawnWithFullCharge', 'AlwaysCrit', 'IgnoreEnemies', 'HoldFireUntilFullReload', 'AlwaysFireWeapon', 'TeleportToHint', 'MiniBoss', 'UseBossHealthBar', 'IgnoreFlag', 'AutoJump', 'AirChargeOnly', 'VaccinatorBullets', 'VaccinatorBlast', 'VaccinatorFire', 'BulletImmune', 'BlastImmune', 'FireImmune', 'Parachute', 'ProjectileShield']
#         Objective = ['DestroySentries', 'SeekAndDestroy', 'Sniper', 'Spy', 'Engineer']
#         Skill = ['Easy', 'Normal', 'Hard', 'Expert']
#         WeaponRestrictions = ['PrimaryOnly', 'SecondaryOnly', 'MeleeOnly']
#         Where = ['Ahead', 'Behind', 'Anywhere']

#         if keyvalue == 'Templates':
#             return False

#         if keyvalue == 'Where':
#             return False

#         if keyvalue == 'Action':
#             return False

#         if keyvalue == 'Templates':
#             return False

#         if keyvalue == 'Templates':
#             return False

#         if previouskeyvalue == '':
#             return False

#         if previouskeyvalue not in base and keyvalue in PopulationManager:
#             return False

#         if previouskeyvalue in Populator:
#             return False

#         if previouskeyvalue in Spawners:
#             return False

#         return True

#     newindent = 0
#     for i in kvlist:
#         check(list(i)[0], previouskeyvalue)
#         print('\t' * indentationnumber, end = '')
#         if isinstance(i.get(list(i)[0]), list):
#             print(list(i)[0])
#             print('\t' * indentationnumber, end = '{\n')
#             indentationnumber += 1
#             newindent += 1
#             findsigkvs(i.get(list(i)[0]), indentationnumber, list(i)[0])
#             indentationnumber -= 1
#             newindent -= 1
#             if newindent == 0:
#                 print('\t' * indentationnumber, end = '}\n')
#         else:
#             print(list(i)[0], i.get(list(i)[0]), end ='')




for i in range(0, len(res)):
    if res[i].endswith('.pop'):
        popfile = open(os.path.join(dir_path, res[i]),'r').read()

        # Remove comments
        while popfile.find('//') != -1:
            popfile = popfile[:popfile.find('//')] + popfile[popfile.find('\n', popfile.find('//')):]

        # Remove [$SIGSEGV] tags
        popfile = popfile.replace('[$SIGSEGV]', '')

        # Parse file
        population = ParseTree(popfile, 0)

        # Re add [$SIGSEGV] tags, not 100% complete implementation
        sanitized = printpop(population, 0)

        # Save the current stdout so that we can revert sys.stdou after we complete
        # our redirection
        stdout_fileno = sys.stdout

        # Redirect sys.stdout to the file
        sys.stdout = open(os.path.join(dir_path, 'mvm_heatrock_rc6a_adv_brain_taker.pop'), 'w')

        printpop(population, 0)

        # Close the file
        sys.stdout.close()
        # Restore sys.stdout to our old saved file handler
        sys.stdout = stdout_fileno