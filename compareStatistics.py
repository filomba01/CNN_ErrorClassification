import json
import os

# chose the number of tensor to compare
num = int(input("Enter the number of folder to compare: "))

# chose the name of the folders to compare
compareList = []
for i in range(0, num):
    compareList.append(input("Enter folder " + str(i + 1) + ": "))

# chose a probability for each folder
probabilityList = []
for i in range(0, num):
    probabilityList.append(input("probability of " + compareList[i] + ": "))

# path to the files and creation of the original dictionaries
if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'

mapList = []

for i in range(0, num):
    folderName = compareList[i]
    filename = separator + os.path.abspath(__file__).split(separator)[-1]
    os.path.abspath(__file__).replace(filename, '')
    filePath = os.path.abspath(__file__).replace(filename,
                                                 '') + separator + 'statistics' + separator + folderName + "_spatial.json"
    # turn json files back into dictionary
    with open(filePath, 'r') as f:
        data = json.load(f)
    map = {}
    for key1, value1 in data.items():
        map1 = {}
        for key2, value2 in value1.items():
            map2 = {}
            for key3, value3 in value2.items():
                map2[key3] = value3
            map1[key2] = map2
        map[key1] = map1
    mapList.append(map)

# print(mapList)

# comparing the dictionaries
keyList = []
tmpMap = {}

counterMap = 0
# entire dictionary
for i in mapList:
    i_probability = float(probabilityList[counterMap])
    counterMap += 1
    # number of errors
    for j in i.keys():
        # type of errors
        for k in i[j]['FF'].keys():
            tmpMap[k] = [i[j]['FF'][k] * i_probability]
