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

All the errors are compared with a **row referece**, a **column reference** and a **channel reference** choosen from the first error position.

In order to classify errors in bullet wake and shattered glass classification some useful variables have been used, such as:
* CoordinatesMap: is a dictonary used to store the occurency of the error's coordinates. 

* Lastchseen: is a support variable that helps to analise bullet_wake and shattered_glass errors channel through channel.  


The key for the map dictonary is created as below, the result is a 'row,column' index:

    key = ''.join(str(diff_cube[k][x]) + ',' for x in range(1, len(diff_cube[k]) ))
            key = key.rstrip(key[-1])

In order to ensure that an error could be bullet wake or shattered glass is necessary to find a coordinate that occured as many times as the channel with at least one error
    
                if shatteredGlass:
                    for key in CoordinatesMap:
                        if CoordinatesMap[key]== nChannel:
                          atLeastBullet = True

When a channel has been completely analyzed, atLeastBullet flag is checked, if no error in the channel occured in the reference position, it cannot be a shattered glass, neither a bullet wake.
    
            if lastChSeen != diff_cube[k][CHANNEL]:
                lastChSeen = diff_cube[k][CHANNEL]
                if not atLeastBullet:
                    bulletWake = False
                    shatteredGlass = False
                else:
                    atLeastBullet = False


### Review about latest experiments
fp32_wzv
* S1I1 : 1014 undefined_error su 1014
* S1I2 : 1005 undefined_error su 1005
* S1I3 : 937 bullet_wake su 937
* S1I6 : 1852 undefined_error su 1852 
* S1I8 : 1000 bullet_wake su 1000
fp32_wrv
* S1I7 : 1000 bullet_wake su 1000
* 
fp32_ggpr
* S1I10 : 293 bullet su 293
ld_wzv
* S1I9 : 500 bullet_wake su 500