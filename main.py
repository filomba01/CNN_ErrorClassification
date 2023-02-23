import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
from math import sqrt

###
save = False
title = 'error_classes/shattered_glass/0'


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


def check_is_same_row(matrix, r, c):
    row2Check = -1
    for i in range(r):
        for j in range(c):
            if diff[i][j] == 1:
                if row2Check == -1:
                    row2Check = i
                elif row2Check != i:
                    return False
    return True


golden = np.load(argv[1])[0, ...]
faulty = np.load(argv[2])[0, ...]

channels = golden.shape[2]
x, y = split_two(channels)

fig, axs = plt.subplots(x, y)
counter = 0
foundBroken = False
### i suppose that can be a same row
isSameRow = True

# saving coordinates for checking eventually bullet wake
coordinates = [0, 0]
selectedSquare = False
bulletWake = False

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

        ## used to evaluate if result is a single point error
        counter += np.count_nonzero(diff == 1)
        ## same row
        if np.count_nonzero(diff == 1) > 0:
            if foundBroken == False:
                foundBroken = True
                isSameRow = check_is_same_row(diff, diff.shape[0], diff.shape[1])
            else:
                isSameRow = False
        # bullet wake
        if np.count_nonzero(diff == 1):
            if not selectedSquare:
                selectedSquare = True
                bulletWake = True
                coordinates = [i, j]
            if ([i, j] != coordinates) and (bulletWake == True):
                bulletWake = False

tensor_name = argv[2].split('/')[-1].split('.')[0]
### if the result contains only one error is a single point!
if counter == 1:
    title = 'error_classes/single_point' + tensor_name
elif isSameRow:
    title = 'error_classes/same_row/' + tensor_name
elif (bulletWake) and (counter > 1):
    title = 'error_classes/bullet_wake/' + tensor_name
else:
    title = 'error_classes/undefined_error/' + tensor_name

if save:
    plt.savefig(title)
else:
    plt.show()
