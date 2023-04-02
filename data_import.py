import csv
import os


def check_data_types(file_path):
    data_types = {}

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)

        for header in headers:
            data_types[header] = {'int': 0, 'float': 0, 'string': 0, 'empty': 0}

        for row in reader:
            for i, val in enumerate(row):
                if val == '':
                    data_type = 'empty'
                else:
                    try:
                        int(val)
                        data_type = 'int'
                    except ValueError:
                        try:
                            float(val)
                            data_type = 'float'
                        except ValueError:
                            data_type = 'string'

                data_types[headers[i]][data_type] += 1

    return data_types


if __name__ == '__main__':
    directory = '/Users/khaled/Downloads/data'
    file_name = 'adspend.csv'
    file_path = os.path.join(directory, file_name)

    data_types = check_data_types(file_path)
    print(data_types)
