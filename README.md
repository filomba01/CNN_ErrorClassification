infomal readme
# CNN Error Classificator for CLASSES
The aim of this project is to automatize error patterns classifications based on the descriptions made in "Fast and Accurate Error Simulation for CNNs against Soft Errors" in order to implement it in CLASSES.
The creators are Matteo Bettiati and Filippo Balzarini from Politecnico of Milano.

### About the Project
The project offers two approaches to the problem.

### main
The first approach was to divide the golden matrix in channels.
For each channel the program recognise automatically errors and dives them in different directories.
At the moment known errors are:
-Single point errors:
    after exploring all channels, the counter of error has counted just one
-Same row:
    after have found the first error, is checked if all other eventual errors are located in the same row
    (there must be one row of error in the entire corrupted tensor)
-Bullet wake:
    all the eventual errors in the corrupted tensors are located in the same coordinates for each channel
-Shattered glass:
    all the eventual errors in the corrupted tensors are located in the same coordinates for each channel,
    but on the same row of the error are accepted other errors.