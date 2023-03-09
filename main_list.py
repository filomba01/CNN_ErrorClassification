import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
from math import sqrt
import os

# defines the row index
CHANNEL = 3
ROW = 0
COLUMN = 1
DEPTH = 2
# end def

###
save = False
title = ''


###

def split_two(num):
    if is_square(num):
        return int(sqrt(num)), int(sqrt(num))

    radix = int(sqrt(num))

    while num % radix != 0:
        radix -= 1

    return radix, num // radix


def is_square(apositiveint):
    x = apositiveint // 2
    seen = set([x])
    while x * x != apositiveint:
        x = (x + (apositiveint // x)) // 2
        if x in seen: return False
        seen.add(x)
    return True


golden = np.load(argv[1])[0, ...]
if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'
filename = separator+os.path.abspath(__file__).split(separator)[-1]
os.path.abspath(__file__).replace(filename, '')
path = os.path.abspath(__file__).replace(filename, '') + separator + 'tensors_corrupted'
os.chdir(path)
for file in os.listdir():
    if file.endswith(".npy"):
        file_path = path + separator + file
        faulty = np.load(file_path)

        # variables for classification
        singlePoint = True
        isSameRow = True
        bulletWake = True
        shatteredGlass = True

        # diff cube generation

        a = np.abs(golden - faulty)
        diff_cube = np.where(golden - faulty)
        temp = [(diff_cube[j][i]) for i in range(len(diff_cube[0])) for j in range(len(diff_cube))]
        diff_cube = [tuple(temp[n:n + len(diff_cube)]) for n in range(0, len(temp), len(diff_cube))]

        # print
        if save:
            channels = golden.shape[2]
            x, y = split_two(channels)
            fig, axs = plt.subplots(x, y)
            for j in range(y):
                for i in range(x):
                    diff = np.abs(golden[:, :, i + j * x] - faulty[:, :, i + j * x])
                    diff = np.where(diff < 1e-3, 0, 1)
                    axs[i, j].imshow(diff, cmap='hot', interpolation='nearest')
                    axs[i, j].set_yticks([])
                    axs[i, j].set_xticks([])
                    axs[i, j].set_yticklabels([])
                    axs[i, j].set_xticklabels([])
                    axs[i, j].set_title(f'Channel {i + j * x}', fontsize=8)
            # end print

        print(diff_cube)
        print(len(diff_cube))

        # single point
        if len(diff_cube) > 1:
            firstChannel = -1
            singlePoint = False
            for k in range(0, len(diff_cube)):
                # gets the channel that contains the first error
                if firstChannel == -1:
                    firstChannel = diff_cube[k][CHANNEL]
                    rReference = diff_cube[k][ROW]
                    cReference = diff_cube[k][COLUMN]
                    dReference = diff_cube[k][DEPTH]
                else:
                    # same row conditions
                    if diff_cube[k][ROW] != rReference or diff_cube[k][COLUMN] != cReference or diff_cube[k][CHANNEL] != firstChannel:
                        sameRow = False
                    elif diff_cube[k][ROW] != rReference or diff_cube[k][COLUMN] != cReference:
                        shatteredGlass = False
                    elif diff_cube[k][ROW] != rReference or diff_cube[k][COLUMN] != cReference or diff_cube[k][DEPTH] != dReference:
                        bulletWake = False

                    if sameRow:
                        shatteredGlass = False
                        bulletWake = False
                    elif shatteredGlass:
                        bulletWake = False

        # from the line command 1)Linux 2)Windows
        # 1) tensor_name = argv[2].split('/')[-1].split('.')[0]
        # 2) tensor_name = argv[2].split('.')[0].split("\\")[-1]

        # directly from the directory corrupted_tensors
        if separator == '/':
            tensor_name = file_path.split('/')[-1].split('.')[0]
        else:
            tensor_name = file_path.split('.')[0].split("\\")[-1]
        path2err = os.path.abspath(__file__).replace(filename, '') + 'error_classes' + separator
        # saves results
        if singlePoint:
            title = path2err + 'single_point' + separator + tensor_name
        elif sameRow:
            title = path2err + 'same_row' + separator + tensor_name
        elif bulletWake:
            title = path2err + 'bullet_wake' + separator + tensor_name
        elif shatteredGlass:
            title = path2err + 'shattered_glass' + separator + tensor_name
        else:
            title = path2err + 'undefined_error' + separator + tensor_name

        if save:
            plt.savefig(title)
            plt.close()
        else:
            print(title)
        #plt.close()
