import csv


def check_data_types(file_path):
    """
    To make sure the data is clean,   this function takes the path of a CSV file as input, reads the file, and analyzes
    the data in it to determine the count of values for each column by their data type: integer, float, string, or empty
    . The function returns a dictionary containing the counts for each column.

    :param file_path: The path of the CSV file to analyze.
    :type file_path: str
    :return: A dictionary containing the counts of values for each column by their data type.
    :rtype: dict
    """
    data_types_count = {}

    with open(file_path, 'r') as file:
        # Use csv.reader to read the CSV file and return an iterator over its rows
        reader = csv.reader(file)

        # Use next() to get the first row of the CSV file, which typically contains the headers
        headers = next(reader)

        # Initialize dictionary to store counts of data types for each header
        for header in headers:
            data_types_count[header] = {'int': 0, 'float': 0, 'string': 0, 'empty': 0}

        # Iterate through each row in the file and count the data types for each value in the row
        for row in reader:
            for column_index, cell_value in enumerate(row):
                if cell_value == '':
                    data_type = 'empty'
                else:
                    try:
                        int(cell_value)
                        data_type = 'int'
                    except ValueError:
                        try:
                            float(cell_value)
                            data_type = 'float'
                        except ValueError:
                            data_type = 'string'

                # Increment count for the data type of the value in the corresponding header
                data_types_count[headers[column_index]][data_type] += 1

    return data_types_count


if __name__ == '__main__':
    adspend_path = f"/Users/khaled/Downloads/data/adspend.csv"
    installs_path = f"/Users/khaled/Downloads/data/installs.csv"
    payouts_path = f"/Users/khaled/Downloads/data/payouts.csv"
    revenue_path = f"/Users/khaled/Downloads/data/revenue.csv"


    # Call the function with the file paths and print the resulting dictionary
    data_types_count_adspend = check_data_types(adspend_path)
    for column, count in data_types_count_adspend.items():
        print(f"{column}, {count}")

    print("\nInstalls: ")
    data_types_count_installs = check_data_types(installs_path)
    for column, count in data_types_count_installs.items():
        print(f"{column}, {count}")

    print("\nPayouts: ")
    data_types_count_payouts = check_data_types(payouts_path)
    for column, count in data_types_count_payouts.items():
        print(f"{column}, {count}")

    print("\nRevenue: ")
    data_types_count_revenue = check_data_types(revenue_path)
    for column, count in data_types_count_revenue.items():
        print(f"{column}, {count}")
