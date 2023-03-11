# CNN Error Classificator for CLASSES
The aim of this project is to automatize error patterns classifications based on the descriptions made in "Fast and Accurate Error Simulation for CNNs against Soft Errors" in order to implement it in CLASSES.
Code is written by Matteo Bettiati ([@matteobettiati](https://github.com/matteobettiati)) and Filippo Balzarini ([@filomba01](https://github.com/filomba01)) from [Politecnico di Milano](https://polimi.it).

### About the Project
Analysis starts with the comparison between the curropted tensor matrix and the golden one, the _diff\_cube_ result represent the field of the matrix where an error occured because of the corrupted tensor injection in the CNN, the program is be able to automatically divide different errors into proper error class.

The currently error classes in analysis are:
* **single points error**: here are classified all the corrupted tensors having only one corrupted value
* **same Row error**: a corrupted tensor is classified as same row error if the errors in diff_cube have been found in a single row
* **Bullet wake**: for each channel there is just one error and in the same coordinate
* **shattered glass** : as bullet wake, but errors may be also found in the same row of the error reference.

### Approach
As it can be seen in the code, all the error classes are supposed to be true at the beginning, the approach of this classification is to individuate if exists a single element which does not respect the specific rule of an error class, in order to exclude that class from the possible ones.
This approach make more simple to identify the right classification for each tensor.

