import csv
import re
import pandas as pd
import time


def convert_scientific_notation(file_path):
    # Load CSV into pandas dataframe
    df = pd.read_csv(file_path)

    # Identify columns with scientific notation
    scientific_cols = df.select_dtypes(include=['float', 'int']).columns

    # Define the new file path
    new_file_path = file_path[:-4] + '_converted.csv'

    # Replace scientific notation with decimal representation
    for col in scientific_cols:
        if col == "value_usd":
            df[col] = df[col].apply(lambda x: '{:.10f}'.format(x))
            # Write dataframe to new CSV file
            df.to_csv(new_file_path, index=False)
        else:
            print("Not value_usd column")

    print("Conversion completed.\n")

    return new_file_path

print("Adspend: ")
convert_scientific_notation('/Users/khaled/Downloads/data/adspend.csv')
print("Installs:")
convert_scientific_notation('/Users/khaled/Downloads/data/installs.csv')
print("Payouts:")
convert_scientific_notation('/Users/khaled/Downloads/data/payouts.csv')
print("Revenue:")
convert_scientific_notation('/Users/khaled/Downloads/data/revenue.csv')

print("Files are being exported...\n")
time.sleep(10)  # wait for 10 seconds for csv files to be exported


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
            data_types_count[header] = {'int': 0, 'float': 0, 'string': 0, 'empty': 0, 'scientific': 0}

            # Iterate through each row in the file and count the data types for each value in the row
        for row in reader:
            for column_index, cell_value in enumerate(row):
                if cell_value == '':
                    data_type = 'empty'
                    # Check if the cell_value is a float value or contains scientific notation
                    if re.search(r'[eE][+-]?\d+', cell_value):
                        data_type = 'scientific'
                else:
                    try:
                        int(cell_value)
                        data_type = 'int'
                    except ValueError:
                        try:
                            float(cell_value)
                            data_type = 'float'
                            # Check if the cell_value contains scientific notation
                            if re.search(r'[eE][+-]?\d+', cell_value):
                                data_type = 'scientific'
                        except ValueError:
                            data_type = 'string'

                # Increment count for the data type of the value in the corresponding header
                data_types_count[headers[column_index]][data_type] += 1

    return data_types_count


if __name__ == '__main__':
    adspend_path = f"/Users/khaled/Downloads/data/adspend_converted.csv"
    installs_path = f"/Users/khaled/Downloads/data/installs.csv"
    payouts_path = f"/Users/khaled/Downloads/data/payouts_converted.csv"
    revenue_path = f"/Users/khaled/Downloads/data/revenue_converted.csv"


    # Call the function with the file paths and print the resulting dictionary
    print("Adspend:: ")
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

print("\n-----------------\n")


def explore_csv(file_path):
    """
    Description:
    The "explore_csv" function takes a file path as an argument and performs some basic exploratory analysis on the
    data in the CSV file
    :param file_path:
    """
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Print the first and last few rows of the data
    print("First few rows:")
    print(df.head())
    print("\nLast few rows:")
    print(df.tail())

    # Get information on the data types and number of non-null values in each column
    print("\nData types and non-null values:")
    print(df.info())

    # Get summary statistics for each numeric column in the dataset
    print("\nSummary statistics:")
    print(df.describe())

    # Get the number of rows and columns in the dataset
    print("\nShape of the dataset:")
    print(df.shape)

    # Get a list of all the column names in the dataset
    print("\nColumn names:")
    print(df.columns)

    # Get the number of missing values in each column
    print("\nNumber of missing values:")
    print(df.isnull().sum())


print("\n#Explore Adspend: ")
explore_csv('/Users/khaled/Downloads/data/adspend.csv')
print("\n#Explore Installs:")
explore_csv('/Users/khaled/Downloads/data/installs.csv')
print("\n#Explore Payouts:")
explore_csv('/Users/khaled/Downloads/data/payouts.csv')
print("\n#Explore Revenue:")
explore_csv('/Users/khaled/Downloads/data/revenue.csv')


print("\n---------\nDone, files are ready for analysis.")
