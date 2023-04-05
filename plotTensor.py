import os

import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
from math import sqrt

###



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

###

if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'

save = True
filename = separator + os.path.abspath(__file__).split(separator)[-1]
title = os.path.abspath(__file__).replace(filename, '') + separator + 'plotted_tensors'


experimentPath = input("Insert the folder of the experiment: ")
filename = separator + os.path.abspath(__file__).split(separator)[-1]
os.path.abspath(__file__).replace(filename, '')
directory = os.path.abspath(__file__).replace(filename,'') + separator + 'tensors_corrupted' + separator + experimentPath
for conv in os.listdir(directory):
    f = directory + separator + conv
    golden = np.load(directory + separator + conv + separator + 'output_1.npy')[0, ...]
    for tensor in os.listdir(f):
        if not tensor.endswith(".npy") and not tensor.endswith(".md"):
            tensdirectory = f + separator + tensor
            for tensor_name in os.listdir(tensdirectory):
                if tensor_name.endswith(".npy"):
                    faulty = np.load(tensdirectory + separator + tensor_name)[0, ...]

                    toInvert = False
                    if golden.shape[0] != golden.shape[1]:
                        toInvert = True
                        golden = np.reshape(golden, (golden.shape[2], golden.shape[1], golden.shape[0]))

                    toInvertFaulty = False
                    if faulty.shape[0] != faulty.shape[1]:
                        toInvertFaulty = True
                        faulty = np.reshape(faulty, (faulty.shape[2], faulty.shape[1], faulty.shape[0]))

                    channels = golden.shape[2]

                    print(golden.shape[0])

                    if is_prime(channels):
                        channels += 2

                    x, y = split_two(channels)

                    fig, axs = plt.subplots(x, y)

                    for j in range(y):
                        for i in range(x):
                            if  i + j * x < golden.shape[2]:
                                diff = np.abs(golden[:, :, i + j * x] - faulty[:, :, i + j * x])
                                diff = np.where(diff < 1e-3, 0, 1)
                                axs[i, j].imshow(diff, cmap='hot', interpolation='nearest')
                                axs[i, j].set_yticks([])
                                axs[i, j].set_xticks([])
                                axs[i, j].set_yticklabels([])
                                axs[i, j].set_xticklabels([])
                                axs[i, j].set_title(f' {i + j * x}', fontsize=4)

                    if save:
                        plt.savefig(title+ separator + tensor_name.split('.')[0])
                    else:
                        plt.show()
                    plt.close()