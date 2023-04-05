import numpy as np
import os
from numpy import size

# initialize the dictonary that will be used as hashmap
CoordinatesMap = {}

# defines list's indexes
ROW = 0
COLUMN = 1
CHANNEL = 2
# end def

# counter of tensors
counter = 0

# for per iterare nella cartella experimant name
if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'
experimentPath = input("Insert the folder of the experiment: ")
filename = separator + os.path.abspath(__file__).split(separator)[-1]
os.path.abspath(__file__).replace(filename, '')
directory = os.path.abspath(__file__).replace(filename, '') + separator + 'tensors_corrupted' + separator + experimentPath
for conv in os.listdir(directory):
    f = os.path.join(directory, conv)
    for tensor in os.listdir(f):
        if not tensor.endswith(".npy") and not tensor.endswith(".md"):
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
            toInvert = False
            if golden.shape[0] != golden.shape[1]:
                toInvert = True
                golden = np.reshape(golden, (golden.shape[2], golden.shape[1], golden.shape[0]))

            print(golden.shape)

            pathToDirectory = os.path.abspath(__file__).replace(filename, '') + separator + 'error_classes' + separator
            if not os.path.exists(pathToDirectory + experimentPath):
                os.mkdir(pathToDirectory + experimentPath + separator)
            if not os.path.exists(pathToDirectory + experimentPath + separator + choosenTestFolder):
                os.mkdir(pathToDirectory + experimentPath + separator + choosenTestFolder + separator)
            pathToDirectories = pathToDirectory + experimentPath + separator + choosenTestFolder + separator
            os.mkdir(pathToDirectories + choosenTensorsF)
            os.mkdir(pathToDirectories + choosenTensorsF + separator + 'single_point')
            os.mkdir(pathToDirectories + choosenTensorsF + separator + 'same_row')
            os.mkdir(pathToDirectories + choosenTensorsF + separator + 'bullet_wake')
            os.mkdir(pathToDirectories + choosenTensorsF + separator + 'shattered_glass')
            os.mkdir(pathToDirectories + choosenTensorsF + separator + 'undefined_error')

            for file in os.listdir():
                if file.endswith(".npy"):
                    counter += 1
                    file_path = path + separator + choosenTensorsF + separator + file
                    # print(file_path)
                    faulty = np.load(file_path)[0, ...]
                    print(faulty.shape)
                    if toInvert:
                        faulty = np.reshape(faulty, (faulty.shape[2], faulty.shape[1], faulty.shape[0]))
                        print(faulty.shape)

                    # variables for classification
                    singlePoint = True
                    isSameRow = True
                    bulletWake = True
                    shatteredGlass = True

                    # diff cube generation
                    diffs = np.abs(golden - faulty)
                    diff_cube = np.where(diffs > 1e-3)
                    temp = [(diff_cube[j][i]) for i in range(len(diff_cube[0])) for j in range(len(diff_cube))]
                    diff_cube = [tuple(temp[n:n + len(diff_cube)]) for n in range(0, len(temp), len(diff_cube))]

                    diff_cube = sorted(diff_cube, key=lambda x: x[2])
                    Range = int(size(diff_cube) / 3)

                    CoordinatesMap.clear()
                    # initialize the map
                    for k in range(0, Range):
                        key = ''.join(str(diff_cube[k][x]) + ',' for x in range(0, len(diff_cube[k]) - 1))
                        key = key.rstrip(key[-1])
                        CoordinatesMap[key] = 0

                    print("initialized coordinates: ")
                    print(CoordinatesMap)
                    # errors
                    if (size(diff_cube) / 4) > 1:
                        singlePoint = False
                        rReference = diff_cube[0][ROW]
                        cReference = diff_cube[0][COLUMN]
                        channelRef = diff_cube[0][CHANNEL]
                        nChannel = 1
                        actualChannel = channelRef
                        atLeastBullet = False
                        for k in range(0, Range):

                            # super pattern

                            # handle key creation, without assign the channel
                            key = ''.join(str(diff_cube[k][x]) + ',' for x in range(0, len(diff_cube[k]) - 1))
                            key = key.rstrip(key[-1])
                            CoordinatesMap[key] += 1

                            #  common conditions
                            if diff_cube[k][ROW] != rReference or diff_cube[k][COLUMN] != cReference:
                                isSameRow = False
                                shatteredGlass = False
                                bulletWake = False

                            if diff_cube[k][CHANNEL] != channelRef:
                                isSameRow = False

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

                    # from the line command 1)Linux 2)Windows
                    # 1) tensor_name = argv[2].split('/')[-1].split('.')[0]
                    # 2) tensor_name = argv[2].split('.')[0].split("\\")[-1]

                    # directly from the directory corrupted_tensors
                    if separator == '/':
                        tensor_name = file_path.split('/')[-1].split('.')[0]
                    else:
                        tensor_name = file_path.split('.')[0].split("\\")[-1]
                    path2err = pathToDirectories + separator + choosenTensorsF + separator
                    if len(diff_cube) == 1:
                        errorType = 'single_point'
                        title = path2err + 'single_point' + separator
                    elif isSameRow:
                        errorType = 'same_row'
                        title = path2err + 'same_row' + separator
                    elif bulletWake and (len(diff_cube) > 1):
                        errorType = 'bullet_wake'
                        title = path2err + 'bullet_wake' + separator
                    elif shatteredGlass:
                        errorType = 'shattered_glass'
                        title = path2err + 'shattered_glass' + separator
                    else:
                        errorType = 'undefined_error'
                        title = path2err + 'undefined_error' + separator

                    # print(tensor_name + ': '+errorType)
                    file = open(title + "tensors_" + errorType + ".txt", "a")
                    file.write(tensor_name + "\n")

            print("Tensors counted: ", counter)