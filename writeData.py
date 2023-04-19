import os
import csv

error_classes = ['bullet_wake', 'same_column', 'same_row', 'shattered_glass', 'single_point', 'undefined_error']

def addToErrorMap(nError,type_of_error,error_class,number_corrupted_tensors):
    if type_of_error not in nError:
        nError[type_of_error] = {}
        for err in error_classes:
            nError[type_of_error][err] = 0
        nError[type_of_error][error_class] = number_corrupted_tensors
    else:
        nError[type_of_error][error_class] += number_corrupted_tensors
def writeErrors(writer, nError, experiment):

    percResult = []
    for er_t in nError:
        total_error_number = 0
        row2beWritten = [experiment, er_t]
        for err in error_classes:
            if err in nError[er_t]:
                total_error_number += nError[er_t][err]
                row2beWritten.append(nError[er_t][err])
            else:
                row2beWritten.append(0)

        percResult = ['', '']
        row2beWritten.append(total_error_number)
        for value in row2beWritten:
            if isinstance(value, (int,float)):
                value = int((int(value)/total_error_number)*100)
                percResult.append(str(value) + '%')
        writer.writerow(row2beWritten)
        writer.writerow(percResult)


def create_csv(start_path, exp):
    nError = {}
    nErrorExperiment = {}
    with open(exp + '.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['folder','type_of_injection'] + error_classes)
        # giro le raccolte di esperimenti
        folder_path = os.path.join(start_path)
        # Check if it is a director
        if os.path.isdir(folder_path):
            # giro ogni esperimento
            for experiment in os.listdir(folder_path):
                nErrorExperiment.clear()
                experiment_path = os.path.join(folder_path, experiment)
                # Check if it is a directory
                if os.path.isdir(experiment_path):
                    if os.path.isdir(experiment_path):
                        # giro ogni esperimento
                        for type_of_error in os.listdir(experiment_path):

                            type_of_error_path = os.path.join(experiment_path, type_of_error)
                            if os.path.isdir(type_of_error_path):
                                total_length = 0
                                row2beWritten = [experiment, type_of_error]
                                # Iterate over sub-subfolders
                                for error_class in os.listdir(type_of_error_path):

                                    error_class_path = os.path.join(type_of_error_path, error_class)

                                    file_path = os.path.join(error_class_path, 'tensors_' + error_class + '.txt')

                                    if os.path.isfile(file_path):
                                        with open(file_path, 'r') as file:
                                            number_corrupted_tensors = sum(1 for row in file)
                                        total_length += number_corrupted_tensors

                                        addToErrorMap(nError,type_of_error,error_class,number_corrupted_tensors)
                                        addToErrorMap(nErrorExperiment, type_of_error, error_class,number_corrupted_tensors)

                        writeErrors(writer, nErrorExperiment, experiment)

        writer.writerow('\n')

        writeErrors(writer, nError, 'result')




# for per iterare nella cartella experimant name
if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'
filename = separator + os.path.abspath(__file__).split(separator)[-1]
startpath = os.path.abspath(__file__).replace(filename, '') + separator + 'error_classes'
experiment = input('insert experiments to analyze:')
create_csv(startpath + separator + experiment, experiment)
