import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_temporal_scope(csv_file):
    """
    Returns:
        A dictionary with keys 'filename', 'first_date', 'last_date', and 'temporal_scope' representing the filename,
        first and last dates in the CSV file, and the number of days between them (inclusive). to better understand the
        data
    """
    df = pd.read_csv(csv_file)
    date_col = [col for col in df.columns if 'date' in col.lower()][0]
    first_date = pd.to_datetime(df[date_col]).min()
    last_date = pd.to_datetime(df[date_col]).max()
    temporal_scope = (last_date - first_date).days + 1
    return {'filename': csv_file, 'first_date': first_date, 'last_date': last_date, 'temporal_scope': temporal_scope}


csv_file = '/Users/khaled/Downloads/data/adspend_converted.csv'
results = get_temporal_scope(csv_file)
print(results)


def analyze_adspend(file_path):
    # Read the CSV file
    adspend = pd.read_csv(file_path)

    # Clean the data
    adspend['event_date'] = pd.to_datetime(adspend['event_date'])

    # Perform exploratory data analysis
    # Analyze ad spend by country
    country_adspend = adspend.groupby('country_id')['value_usd'].sum().sort_values(ascending=False)
    # Analyze ad spend by ad network
    network_adspend = adspend.groupby('network_id')['value_usd'].sum().sort_values(ascending=False)
    # Analyze ad spend by client
    client_adspend = adspend.groupby('client_id')['value_usd'].sum().sort_values(ascending=False)
    # Analyze ad spend over time
    date_adspend = adspend.groupby('event_date')['value_usd'].sum()

    # Visualize the data
    plt.figure(figsize=(12, 6))
    sns.barplot(x=country_adspend.index, y=country_adspend.values)
    plt.title('Ad Spend by Country')
    plt.xlabel('Country ID')
    plt.ylabel('Ad Spend (USD)')
    plt.show()

    # Analyze ad spend by ad network
    plt.figure(figsize=(12, 6))
    sns.barplot(x=network_adspend.index, y=network_adspend.values)
    plt.title('Ad Spend by Ad Network')
    plt.xlabel('Network ID')
    plt.ylabel('Ad Spend (USD)')
    plt.show()

    # Ad Spend Time Series Plot
    plt.figure(figsize=(12, 6))
    plt.plot(date_adspend.index, date_adspend.values)
    plt.title('Ad Spend Time Series Plot')
    plt.xlabel('Date')
    plt.ylabel('Ad Spend (USD)')
    plt.show()

    # Visualize the ad spend by client
    plt.figure(figsize=(12, 6))
    sns.barplot(x=client_adspend.index, y=client_adspend.values)
    plt.title('Ad Spend by Client')
    plt.xlabel('Client ID')
    plt.ylabel('Ad Spend (USD)')
    plt.xticks(rotation=45)  # Optional: Rotate the x-axis labels for better readability
    plt.show()


# Call the function with the file path as an argument
analyze_adspend('/Users/khaled/Downloads/data/adspend_converted.csv')


exit()





