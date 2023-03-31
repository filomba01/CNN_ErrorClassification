import numpy as np
import os

if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'
filename = separator + os.path.abspath(__file__).split(separator)[-1]
os.path.abspath(__file__).replace(filename, '')
path = os.path.abspath(__file__).replace(filename, '') + separator + 'tensors_corrupted'
experimentPath = input("Insert the folder of the experiment: ")
path = path + separator + experimentPath
choosenTestFolder = input("Insert the name of experiment: ")
choosenTensorsF = input("Insert the type of injection: ")
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
    os.mkdir(pathToDirectory + experimentPath + separator + choosenTestFolder)
pathToDirectory = pathToDirectory + experimentPath + separator + choosenTestFolder + separator
os.mkdir(pathToDirectory + choosenTensorsF)
os.mkdir(pathToDirectory + choosenTensorsF + separator + 'single_point')
os.mkdir(pathToDirectory + choosenTensorsF + separator + 'same_row')
os.mkdir(pathToDirectory + choosenTensorsF + separator + 'bullet_wake')
os.mkdir(pathToDirectory + choosenTensorsF + separator + 'shattered_glass')
os.mkdir(pathToDirectory + choosenTensorsF + separator + 'undefined_error')