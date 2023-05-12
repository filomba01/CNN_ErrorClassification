import numpy as np
import os
from numpy import size
import json

# initialize the dictonary that will be used as hashmap
CoordinatesMap = {}
# initialize the map for json file
NErrorMap = {}
CountErrorMap = {}

# defines list's indexes
ROW = 0
COLUMN = 1
CHANNEL = 2

MIN_PERC = 0.05
# end def

# counter of tensors
counter = 0

# errors list
error_classes = ['single_point', 'same_row', 'bullet_wake', 'shattered_glass', 'undefined_error', 'same_column',
                 'skip_x', 'consecutive_errors', 'negligible_error']

# errors to compare list
error_toCompare_list = ["skip_x"]


# functions

def checkConsecutiveErrors(flatDiffs):
    if size(flatDiffs) < 2:
        return False
    deltaX = flatDiffs[1] - flatDiffs[0]
    if deltaX != 1:
        return False
    for i in range(2, size(flatDiffs)):
        if abs(flatDiffs[i] - flatDiffs[i - 1]) != deltaX:
            return False
    return True


def checkSkipX(flatDiffs, occurencyMap):
    if size(flatDiffs) < 2:
        return False
    deltaX = flatDiffs[1] - flatDiffs[0]
    if deltaX <= 1:
        return False
    for i in range(2, size(flatDiffs)):
        if abs(flatDiffs[i] - flatDiffs[i - 1]) != deltaX:
            return False
    if deltaX in occurencyMap:
        occurencyMap[deltaX] += 1
    else:
        occurencyMap[deltaX] = 1
    return True


def writeOverall(path, errorType, tensor_name):
    file = open(path + separator + "tensors_" + errorType + ".txt", "a")
    file.write(tensor_name + "\n")
    file.close()


def codeError(error_type):
    for i in range(0, size(error_classes) - 1):
        if error_classes[i] == error_type:
            return i
    return 4


def createResultDirectories(choosenTensorsF, separator, pathToDirectory):
    if not os.path.exists(pathToDirectory + experimentPath):
        os.mkdir(pathToDirectory + experimentPath + separator)
    if not os.path.exists(pathToDirectory + experimentPath + separator + choosenTestFolder):
        os.mkdir(pathToDirectory + experimentPath + separator + choosenTestFolder + separator)

    pathToDirectories = pathToDirectory + experimentPath + separator + choosenTestFolder + separator

    os.mkdir(pathToDirectories + choosenTensorsF)

    for error in error_classes:
        os.mkdir(pathToDirectories + choosenTensorsF + separator + error)

    return pathToDirectories


def writeSpatialJson(NErrorMap, pathtoFile, experimentName):
    json_string_spatial = json.dumps(NErrorMap)
    title = os.path.abspath(__file__).replace(filename, '') + separator
    print(title)
    print(json_string_spatial)
    file = open(pathtoFile + experimentName + "_spatial.json", "w")
    file.write(json_string_spatial)
    file.close()


def writeCountJson(CountErrorMap, pathtoFile, experimentName):
    for key in CountErrorMap:
        CountErrorMap[key][1] = float(CountErrorMap[key][0] / counter)
    CountErrorMap = dict(sorted(CountErrorMap.items()))
    json_string_count = json.dumps(CountErrorMap)
    file = open(pathtoFile + experimentName + "_count.json", "w")
    file.write(json_string_count)
    file.close()


def createFlatErrorIndexList(ravelGolden, ravelFaulty):
    flattDiffs = np.abs(ravelGolden - ravelFaulty)
    flattDiffs = np.where(flattDiffs > 1e-3)
    flattDiffs = flattDiffs[0].tolist()
    return flattDiffs


def create3DErrorIndexList(golden, faulty):
    diffs = np.abs(golden - faulty)
    diff_cube = np.where(diffs > 1e-3)

    temp = [(diff_cube[j][i]) for i in range(len(diff_cube[0])) for j in range(len(diff_cube))]
    diff_cube = [tuple(temp[n:n + len(diff_cube)]) for n in range(0, len(temp), len(diff_cube))]
    diff_cube = sorted(diff_cube, key=lambda x: x[2])

    return diff_cube


def initializeNerrorMap(NErrorMap, numberOfErrors, error_classes, error_toCompare_list):
    if numberOfErrors not in NErrorMap:
        NErrorMap[numberOfErrors] = {}
        NErrorMap[numberOfErrors]["FF"] = {}
        NErrorMap[numberOfErrors]["PF"] = {}
        for i in range(0, size(error_classes)):
            NErrorMap[numberOfErrors]["FF"][error_classes[i]] = 0
        for i in range(0, size(error_toCompare_list)):
            NErrorMap[numberOfErrors]["PF"][error_toCompare_list[i]] = {}
    return NErrorMap


def initializeCountErrorMap(CountErrorMap, numberOfErrors):
    if numberOfErrors not in CountErrorMap:
        CountErrorMap[numberOfErrors] = [0, 0]
    return CountErrorMap


def generateKeyMap(diff_cube, k):
    key = ''.join(str(diff_cube[k][x]) + ',' for x in range(0, len(diff_cube[k]) - 1))
    key = key.rstrip(key[-1])

    return key


def initialiazeCoordinateMap(CoordinatesMap, numberOfErrors, diff_cube):
    CoordinatesMap.clear()
    for k in range(0, numberOfErrors):
        key = generateKeyMap(diff_cube, k)
        CoordinatesMap[key] = 0
    return CoordinatesMap


def extractPercentage(NErrorMap):
    keysToDelete = []

    for i in NErrorMap:

        total4Row = 0
        for j in NErrorMap[i]["FF"]:
            total4Row += NErrorMap[i]["FF"][j]

        for j in NErrorMap[i]["FF"]:
            NErrorMap[i]["FF"][j] = NErrorMap[i]["FF"][j] / total4Row

        # if not empty map...
        if bool(NErrorMap[i]["PF"]["skip_x"]):
            # skip_x PF writing
            total4Row = 0
            for j in NErrorMap[i]["PF"]["skip_x"]:
                if j != "MAX" and j != "RANDOM":
                    total4Row += NErrorMap[i]["PF"]["skip_x"][j]

            overallPercNoRandom = 0.0

            # get the maxkey
            maxElem = 0
            for key in NErrorMap[i]["PF"]["skip_x"]:
                if isinstance(key, int):
                    maxElem = key
                    break

            for k in NErrorMap[i]["PF"]["skip_x"]:
                if type(k) == int and int(k) > maxElem:
                    maxElem = int(k)

            NErrorMap[i]["PF"]["skip_x"]["MAX"] = maxElem

            for j in NErrorMap[i]["PF"]["skip_x"]:
                if j != "MAX" and j != "RANDOM":
                    NErrorMap[i]["PF"]["skip_x"][j] = NErrorMap[i]["PF"]["skip_x"][j] / total4Row
                    if int(NErrorMap[i]["PF"]["skip_x"][j]) <= MIN_PERC:
                        keysToDelete.append(j)
                    else:
                        overallPercNoRandom += NErrorMap[i]["PF"]["skip_x"][j]

            NErrorMap[i]["PF"]["skip_x"]["RANDOM"] = 1.0 - overallPercNoRandom

            for j in keysToDelete:
                NErrorMap[i]["PF"]["skip_x"].pop(j)
            keysToDelete.clear()



    return NErrorMap


# MAIN

if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'
experimentPath = input("Insert the folder of the experiment: ")
filename = separator + os.path.abspath(__file__).split(separator)[-1]
directory = os.path.abspath(__file__).replace(filename,
                                              '') + separator + 'tensors_corrupted' + separator + experimentPath

for conv in os.listdir(directory):
    f = os.path.join(directory, conv)
    for tensor in os.listdir(f):
        if not tensor.endswith(".npy") and not tensor.endswith(".md") and not tensor.endswith(".json"):
            print(tensor)
            path = os.path.abspath(__file__).replace(filename, '') + separator + 'tensors_corrupted'
            path = path + separator + experimentPath
            choosenTestFolder = conv
            choosenTensorsF = tensor
            path = path + separator + choosenTestFolder
            golden = np.load(path + separator + 'output_1.npy')[0, ...]

            # print(golden)
            os.chdir(path + separator + choosenTensorsF + separator)

            print(golden.shape)

            # flattered golden
            ravelGolden = np.ravel(golden)

            toInvert = False
            if golden.shape[0] != golden.shape[1]:
                toInvert = True
                golden = np.transpose(golden, (1, 2, 0))
                # golden = np.reshape(golden_transposed, (golden.shape[2], golden.shape[1], golden.shape[0]))

            print(golden.shape)

            pathToDirectory = os.path.abspath(__file__).replace(filename, '') + separator + 'error_classes' + separator
            pathToDirectories = createResultDirectories(choosenTensorsF, separator, pathToDirectory)

            # iterate over all the faulties
            for file in os.listdir():
                if file.endswith(".npy"):
                    counter += 1
                    file_path = path + separator + choosenTensorsF + separator + file
                    faulty = np.load(file_path)[0, ...]

                    # flattered version of the faulty
                    ravelFaulty = np.ravel(faulty)

                    print(faulty.shape)
                    if toInvert:
                        faulty = np.transpose(faulty, (1, 2, 0))
                        print(faulty.shape)

                    # variables for classification
                    singlePoint = True
                    isSameRow = True
                    bulletWake = True
                    shatteredGlass = True
                    sameColumn = True
                    NegligibleError = False

                    # diff cube generation

                    flattDiffs = createFlatErrorIndexList(ravelGolden, ravelFaulty)
                    diff_cube = create3DErrorIndexList(golden, faulty)

                    # gets the number of errors
                    numberOfErrors = size(flattDiffs)

                    if numberOfErrors == 0:
                        NegligibleError = True

                    # initialize the Coordinate map
                    CoordinatesMap = initialiazeCoordinateMap(CoordinatesMap, numberOfErrors, diff_cube)

                    print("\n" + file)
                    print("initialized coordinates: ")
                    print(CoordinatesMap)

                    print("flat array: ")
                    print(size(flattDiffs))
                    print(flattDiffs)

                    print("3d array:")
                    print(size(diff_cube))
                    print(diff_cube)

                    # initialise NError map
                    NErrorMap = initializeNerrorMap(NErrorMap, numberOfErrors, error_classes, error_toCompare_list)
                    CountErrorMap = initializeCountErrorMap(CountErrorMap, numberOfErrors)

                    # errors
                    if numberOfErrors > 1 and not NegligibleError:

                        singlePoint = False
                        rReference = diff_cube[0][ROW]
                        cReference = diff_cube[0][COLUMN]
                        channelRef = diff_cube[0][CHANNEL]
                        nChannel = 1
                        actualChannel = channelRef
                        atLeastBullet = False
                        for k in range(0, numberOfErrors):

                            # super pattern

                            # handle key creation, without assign the channel
                            key = generateKeyMap(diff_cube, k)
                            CoordinatesMap[key] += 1

                            #  common conditions
                            if diff_cube[k][ROW] != rReference:
                                shatteredGlass = False
                                bulletWake = False
                                isSameRow = False

                            if diff_cube[k][COLUMN] != cReference:
                                sameColumn = False

                            if diff_cube[k][CHANNEL] != channelRef:
                                isSameRow = False
                                sameColumn = False

                            # count channels
                            if diff_cube[k][CHANNEL] != actualChannel:
                                actualChannel = diff_cube[k][CHANNEL]
                                nChannel += 1

                        # end for
                        print("final coordinates count: ")
                        print(CoordinatesMap)
                        print("number of channels")
                        print(nChannel)

                        print(diff_cube)
                        if shatteredGlass:
                            for key in CoordinatesMap:
                                if CoordinatesMap[key] == nChannel:
                                    atLeastBullet = True

                                if CoordinatesMap[key] > 1 and CoordinatesMap[key] < nChannel:
                                    bulletWake = False

                            # adjusting the right classification
                            if not atLeastBullet:
                                shatteredGlass = False
                                bulletWake = False

                        if bulletWake:
                            shatteredGlass = False

                    # skip x
                    if bulletWake or sameColumn or isSameRow or shatteredGlass:
                        skipX = False
                        consecutiveErrors = False
                    else:
                        skipX = checkSkipX(flattDiffs, NErrorMap[numberOfErrors]["PF"]["skip_x"])
                        consecutiveErrors = checkConsecutiveErrors(flattDiffs)

                    # from the line command 1)Linux 2)Windows
                    # 1) tensor_name = argv[2].split('/')[-1].split('.')[0]
                    # 2) tensor_name = argv[2].split('.')[0].split("\\")[-1]

                    # directly from the directory corrupted_tensors
                    if separator == '/':
                        tensor_name = file_path.split('/')[-1].split('.')[0]
                    else:
                        tensor_name = file_path.split('.')[0].split("\\")[-1]
                    path2err = pathToDirectories + separator + choosenTensorsF + separator

                    if NegligibleError:
                        errorType = 'negligible_error'
                    elif len(diff_cube) == 1:
                        errorType = 'single_point'
                    elif isSameRow:
                        errorType = 'same_row'
                    elif bulletWake and (len(diff_cube) > 1):
                        errorType = 'bullet_wake'
                    elif shatteredGlass:
                        errorType = 'shattered_glass'
                    elif sameColumn:
                        errorType = 'same_column'
                    elif skipX:
                        errorType = 'skip_x'
                    elif consecutiveErrors:
                        errorType = 'consecutive_errors'
                    else:
                        errorType = 'undefined_error'

                    numberError = errorType
                    NErrorMap[numberOfErrors]["FF"][numberError] += 1
                    CountErrorMap[numberOfErrors][0] += 1

                    title = path2err + errorType + separator
                    writeOverall(pathToDirectory + experimentPath, errorType, tensor_name)

                    # print(tensor_name + ': '+errorType)
                    file = open(title + "tensors_" + errorType + ".txt", "a")
                    file.write(tensor_name + "\n")
                    file.close()
            print("Tensors counted: ", counter)
            NErrorMap = extractPercentage(NErrorMap)
            print(NErrorMap)
NErrorMap = dict(sorted(NErrorMap.items()))

filename = separator + os.path.abspath(__file__).split(separator)[-1]
pathtoStatistics = os.path.abspath(__file__).replace(filename, '') + separator + "statistics" + separator

writeSpatialJson(NErrorMap, pathtoStatistics, experimentPath)
writeCountJson(CountErrorMap, pathtoStatistics, experimentPath)
