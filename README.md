# CNN Error Classificator for CLASSES
The aim of this project is to automatize error patterns classifications based on the descriptions made in "Fast and
Accurate Error Simulation for CNNs against Soft Errors" in order to implement it in CLASSES.
Code is written by Matteo Bettiati ([@matteobettiati](https://github.com/matteobettiati)) and Filippo
Balzarini ([@filomba01](https://github.com/filomba01)) from [Politecnico di Milano](https://polimi.it).

## About the project
The repository contains two python scripts:

* main.py (which has two helper script for plots and statistics)
    * plotTensor.py
    * writeData.py
* compareStatistics.py

## main
Analysis starts with the comparison between the corrupted tensor matrix and the golden one, the _diff\_cube_ result
represent the field of the matrix where an error occurred because of the corrupted tensor injection in the CNN, the
program is be able to automatically divide different errors into proper error class.

The currently error classes in analysis are:

* **single_points**: here are classified all the corrupted tensors having only one corrupted value.
* **same_row**: a corrupted tensor is classified as same row error if the errors in diff_cube have been found in a
  single row.
* **bullet_wake**: for each channel there is just one error and in the same coordinate.
* **shattered_glass** : as bullet wake, but errors may be also found in the same row of the error reference.
* **undefined_error** : there is a random pattern of errors that cannot be clustered into a proper class.
* **same_column** : a corrupted tensor is classified as same column error if the errors in diff_cube have been found in
  a single column.
* **skip_x** : all the errors emerge every "x" blocks.
* **consecutive_errors** : the errors emerge consecutively every block "n" times.
* **negligible_error** : error so small as to be negligible.

### approach
As it can be seen in the code, all the error classes are supposed to be true at the beginning, the approach of this
classification is to individuate if exists a single element which does not respect the specific rule of an error class,
in order to exclude that class from the possible ones.
This approach make more simple to identify the right classification for each tensor.

All the errors are compared with a **row reference**, a **column reference** and a **channel reference** chosen from the
first error position.

In order to classify errors in bullet wake and shattered glass classification some useful variables have been used, such
as:

* CoordinatesMap: is a dictionary used to store the occurrence of the error's coordinates.

The key for the map dictionary is created as below, the result is a 'row,column' index:

    key = ''.join(str(diff_cube[k][x]) + ',' for x in range(1, len(diff_cube[k]) ))
            key = key.rstrip(key[-1])

In order to ensure that an error could be bullet wake or shattered glass is necessary to find a coordinate that occurred
as many times as the channel with at least one error

                if shatteredGlass:
                    for key in CoordinatesMap:
                        if CoordinatesMap[key]== nChannel:
                          atLeastBullet = True

### results
The result of the classification can be displayed using various approaches:

* plotTensor.py
  with this script you can plot the corrupted tensors in 2-dimensional arrays and see the errors.
* writeData.py
  here is generated a csv file with the percentual of all the errors.

### file json
In main.py are generated two file json:

* _spatial:
  In this file are collected the statistics of the experiment in a specific manner.
  The structure is composed by three nested dictionaries.
  The first dictionary contains as key the occurrences of the errors.
  The second contains as key the type of statistic and as value the respective stats.
  The third contains as key the type of error and as value the percentual of its occurrence.
* _count:
  Contains as key the occurrences of error and as values the effective number of tensors that has "n" errors and the
  probability of it to happen.

## compareStatistics
The purpose of this script is to compare the result of more experiments.
You can enter more than one experiment in the command line, and the weights of probability you want to associate to each
folder.
The script generates a unique file json with all the single statistics of the experiment merged.
