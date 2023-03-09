import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
from math import sqrt
import os
from numpy import size

# defines list's indexes
ROW = 0
COLUMN = 1
DEPTH = 2
CHANNEL = 3
# end def

save = True
# title = ''


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
filename = separator + os.path.abspath(__file__).split(separator)[-1]
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
        diff_cube = np.where(golden - faulty)
        temp = [(diff_cube[j][i]) for i in range(len(diff_cube[0])) for j in range(len(diff_cube))]
        diff_cube = [tuple(temp[n:n + len(diff_cube)]) for n in range(0, len(temp), len(diff_cube))]

        # errors
        if (size(diff_cube)/4) > 1:
            singlePoint = False
        rReference = diff_cube[0][ROW]
        cReference = diff_cube[0][COLUMN]
        dReference = diff_cube[0][DEPTH]
        chReference = diff_cube[0][CHANNEL]
        Range = int(size(diff_cube)/4)
        atLeastBullet = False
        for k in range (1,Range):
            # same row conditions
            if diff_cube[k][ROW] != rReference or diff_cube[k][COLUMN] != cReference or diff_cube[k][CHANNEL] != chReference:
                isSameRow = False
            # shatteredGlass conditions
            if diff_cube[k][DEPTH] == dReference:
                atLeastBullet = True
            elif diff_cube[k][ROW] != rReference or diff_cube[k][COLUMN] != cReference:
                shatteredGlass = False
                bulletWake = False
            # bulletWake conditions
            elif diff_cube[k][ROW] == rReference or diff_cube[k][COLUMN] == cReference and diff_cube[k][DEPTH] != dReference:
                bulletWake = False

        # adjusting the right classification
        if bulletWake:
            shatteredGlass = False
        if not atLeastBullet:
            shatteredGlass = False

        # print
        faulty = np.load(file_path)[0,...]
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

        # from the line command 1)Linux 2)Windows
        # 1) tensor_name = argv[2].split('/')[-1].split('.')[0]
        # 2) tensor_name = argv[2].split('.')[0].split("\\")[-1]

        # directly from the directory corrupted_tensors
        if separator == '/':
            tensor_name = file_path.split('/')[-1].split('.')[0]
        else:
            tensor_name = file_path.split('.')[0].split("\\")[-1]
        path2err =  os.path.abspath(__file__).replace(filename, '') + separator + 'error_classes' + separator
        if len(diff_cube) == 1:
            title = path2err + 'single_point' + separator + tensor_name
        elif isSameRow:
            title = path2err + 'same_row' + separator + tensor_name
        elif bulletWake and (len(diff_cube) > 1):
            title = path2err + 'bullet_wake' + separator + tensor_name
        elif shatteredGlass:
            title = path2err + 'shattered_glass' + separator + tensor_name
        else:
            title = path2err + 'undefined_error' + separator + tensor_name

        if save:
            plt.savefig(title)
        else:
            plt.show()
        plt.close()
