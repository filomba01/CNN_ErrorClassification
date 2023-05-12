import json
import os
from sys import argv

# input sample: programName.py num folder1 folder2... folderN p1 p2... pn

# chose the number of tensor to compare
num = int(argv[1])

# chose the name of the folders to compare
compareList = []
for i in range(2, num + 2):
    compareList.append(argv[i])

# chose a probability for each folder
weightsList = []
for i in range(num + 2, 2 * num + 2):
    weightsList.append(argv[i])

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
    for numberOfError, values in data.items():
        map1 = {}
        for FType, statisticsList in values.items():
            map2 = {}
            for errors, probabilities in statisticsList.items():
                map2[errors] = probabilities
            map1[FType] = map2
        map[numberOfError] = map1
    mapList.append(map)

# comparing the dictionaries
keyList = []
tmpMap = {}

counterMap = 0
# entire dictionary
for i in mapList:
    i_probability = float(weightsList[counterMap])
    counterMap += 1
    # number of errors "0", "2"...
    for j in i.keys():
        if j not in keyList:
            keyList.append(j)
            # type of errors "single_point"...
            for k in i[j]['FF'].keys():
                tmpMap[k] = [i[j]['FF'][k] * i_probability]
print(tmpMap)
