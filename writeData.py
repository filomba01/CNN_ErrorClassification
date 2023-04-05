import os
import csv

def create_csv(start_path):
    nError = {}
    error_classes = ['bullet_wake', 'same_row', 'shattered_glass','single_point','undefined_error']
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerow(['experiment name', 'folder', 'type of error', 'bullet_wake', 'same_row', 'shattered_glass','single_point','undefined_error'])
        # giro le raccolte di esperimenti
        for folder in os.listdir(start_path):
            folder_path = os.path.join(start_path, folder)
            # Check if it is a directorz
            if os.path.isdir(folder_path):
                #giro ogni esperimento
                for experiment in os.listdir(folder_path):
                    experiment_path = os.path.join(folder_path, experiment)
                    # Check if it is a directory
                    if os.path.isdir(experiment_path):
                        if os.path.isdir(experiment_path):
                            # giro ogni esperimento
                            for type_of_error in os.listdir(experiment_path):

                                type_of_error_path = os.path.join(experiment_path, type_of_error)
                                if os.path.isdir(type_of_error_path):
                                    total_length = 0
                                    row2beWritten = [folder, experiment, type_of_error]
                                    # Iterate over sub-subfolders
                                    for error_class in os.listdir(type_of_error_path):
                                        number_corrupted_tensors = 0
                                        error_class_path = os.path.join(type_of_error_path, error_class)
                                        file_path = os.path.join(error_class_path, 'tensors_'+error_class+'.txt')

                                        if os.path.isfile(file_path):
                                            with open(file_path, 'r') as file:
                                                number_corrupted_tensors = sum(1 for row in file)
                                            total_length += number_corrupted_tensors
                                            if type_of_error not in nError:
                                                nError[type_of_error] = {}
                                                nError[type_of_error][error_class] = number_corrupted_tensors
                                            else:
                                                if error_class not in nError[type_of_error]:
                                                    nError[type_of_error][error_class] = number_corrupted_tensors
                                                else:
                                                    nError[type_of_error][error_class] = number_corrupted_tensors + nError[type_of_error][error_class]
                                        row2beWritten.append(number_corrupted_tensors)

                                    row2beWritten.append(total_length)
                                    writer.writerow(row2beWritten)

        writer.writerow('\n')

        for er_t in nError:
            row2beWritten = ['results', '']
            row2beWritten.append(er_t)
            for err in error_classes:
                if err in nError[er_t]:
                    row2beWritten.append(nError[er_t][err])
                else:
                    row2beWritten.append(0)
            writer.writerow(row2beWritten)

        print(nError)

# for per iterare nella cartella experimant name
if len(os.path.abspath(__file__).split('/')) > 1:
    separator = '/'
else:
    separator = '\\'
filename = separator + os.path.abspath(__file__).split(separator)[-1]
startpath = os.path.abspath(__file__).replace(filename, '')+separator+'error_classes'
create_csv(startpath)
