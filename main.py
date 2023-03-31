from folder_and_path_handler import *
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
        path2err = pathToDirectory + separator + choosenTensorsF + separator
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