import os

import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
from math import sqrt

###
save = True
title = r'C:\Users\matte\PycharmProjects\pythonProject\plots\tensor1'


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


def is_prime(n):
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True


golden = np.load(argv[1])[0, ...]
faulty = np.load(argv[2])[0, ...]

if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'
filename = separator + os.path.abspath(__file__).split(separator)[-1]
os.path.abspath(__file__).replace(filename, '')
path = os.path.abspath(__file__).replace(filename, '') + separator + 'tensors_corrupted'+separator+'experiments'
choosenTestFolder = input("Insert the folder: ")
choosenTensorsF = input("Insert the subfolder: ")
faultyTensorName = input("Insert the tensor to analyze: ")
path = path + separator + choosenTestFolder
golden = np.load(path+ separator +'output_1.npy')[0,...]
faulty = np.load(path+ separator + choosenTensorsF + separator + faultyTensorName)[0,...]

toInvert = False
if golden.shape[0] != golden.shape[1]:
    toInvert = True
    golden = np.reshape(golden, (golden.shape[2], golden.shape[1], golden.shape[0]))
if toInvert:
    faulty = np.reshape(faulty, (faulty.shape[2], faulty.shape[1], faulty.shape[0]))

channels = golden.shape[2]
print(golden.shape[0])

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
        axs[i, j].set_title(f' {i + j * x}', fontsize=4)



if save:
    plt.savefig(title)
else:
    plt.show()
