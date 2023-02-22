import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
from math import sqrt

###
save = False
title = ''
###

def split_two(num):
	if is_square(num):
		return int(sqrt(num)), int(sqrt(num))

	radix = int(sqrt(num))

	while num%radix != 0:
		radix -= 1

	return radix, num//radix


def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True


golden = np.load(argv[1])[0,...]
faulty = np.load(argv[2])[0,...]

channels = golden.shape[2]
x, y = split_two(channels)


fig, axs = plt.subplots(x, y)

for j in range(y):
	for i in range(x):

		diff = np.abs(golden[:,:,i + j*x] - faulty[:,:,i + j*x])

		diff = np.where(diff < 1e-3, 0, 1)

		axs[i, j].imshow(diff, cmap='hot', interpolation='nearest')
		axs[i, j].set_yticks([])
		axs[i, j].set_xticks([])
		axs[i, j].set_yticklabels([])
		axs[i, j].set_xticklabels([])
		axs[i, j].set_title(f'Channel {i + j*x}', fontsize=8)

if save:
	plt.savefig(title)
else:
	plt.show()