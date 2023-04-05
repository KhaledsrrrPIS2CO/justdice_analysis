import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

adspend_path = '/Users/khaled/Downloads/data/adspend_converted.csv'


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


temporal_scope_results = get_temporal_scope(adspend_path)

print(f"File Path: {temporal_scope_results['filename']}")
print(f"First Date: {temporal_scope_results['first_date']}")
print(f"Last Date: {temporal_scope_results['last_date']}")
print(f"Temporal Scope: {temporal_scope_results['temporal_scope']} days")


def analyze_adspend(file_path):
    """
    This function reads a CSV file containing ad spend data, performs exploratory data analysis,
    and creates visualizations to display ad spend by country, ad network, client, and over time.

    Args:
        file_path (str): The file path of the adspend.csv file.
    """
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

    # Visualize Ad Spend by Country
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

    # Create a histogram and KDE plot
    plt.figure(figsize=(12, 6))
    sns.histplot(client_adspend, kde=True, bins=10)
    plt.title("Ad Spend Distribution by Client")
    plt.xlabel("Ad Spend (USD)")
    plt.ylabel("Frequency")
    plt.show()

    # Apply log transformation
    log_adspend_by_client = np.log1p(client_adspend)
    # Create a histogram and KDE plot
    plt.figure(figsize=(12, 6))
    sns.histplot(log_adspend_by_client, kde=True, bins=10)
    plt.title("Log-transformed Ad Spend Distribution by Client")
    plt.xlabel("Log Ad Spend (USD)")
    plt.ylabel("Frequency")
    plt.show()
    # Box plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=client_adspend)
    plt.title("Ad Spend Distribution by Client - Box Plot")
    plt.xlabel("Ad Spend (USD)")
    plt.show()

    # Violin plot
    plt.figure(figsize=(12, 6))
    sns.violinplot(x=client_adspend)
    plt.title("Ad Spend Distribution by Client - Violin Plot")
    plt.xlabel("Ad Spend (USD)")
    plt.show()

    # Create a time series plot
    plt.figure(figsize=(12, 6))
    date_adspend.plot(kind="line")
    plt.title("Ad Spend Distribution Over Time")
    plt.xlabel("Date")
    plt.ylabel("Ad Spend (USD)")
    plt.show()


# Call the function with the file path as an argument
analyze_adspend(adspend_path)

exit()
