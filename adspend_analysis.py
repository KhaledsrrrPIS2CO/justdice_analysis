import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pareto


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
    adspend_by_country = adspend.groupby('country_id')['value_usd'].sum().sort_values(ascending=False)
    # Analyze ad spend by ad network
    adspend_by_network = adspend.groupby('network_id')['value_usd'].sum().sort_values(ascending=False)
    # Analyze ad spend by client
    adspend_by_client = adspend.groupby('client_id')['value_usd'].sum().sort_values(ascending=False)
    # Analyze ad spend over time
    adspend_by_date = adspend.groupby('event_date')['value_usd'].sum()

    print("______________________")
    print("adspend type:", type(adspend), "\nContent preview:\n", adspend)
    print("______________________")
    print("adspend_by_date type:", type(adspend_by_date), "\nContent preview:\n", adspend_by_date)
    print("______________________")
    print("adspend_by_client type:", type(adspend_by_client), "\nContent preview:\n", adspend_by_client)
    print("______________________")
    print("adspend_by_network type:", type(adspend_by_network), "\nContent preview:\n", adspend_by_network)
    print("______________________")
    print("adspend_by_country type:", type(adspend_by_country), "\nContent preview:\n", adspend_by_country)

    # Bar chart for Ad Spend by Country
    plt.figure(figsize=(12, 6))
    sns.barplot(x=adspend_by_country.index, y=adspend_by_country.values)
    plt.title('Ad Spend by Country')
    plt.xlabel('Country ID')
    plt.ylabel('Ad Spend (USD)')
    plt.show()

    # Time series plot for Ad Spend over time
    plt.figure(figsize=(12, 6))
    adspend_by_date.plot(kind="line")
    plt.title("Ad Spend Distribution Over Time")
    plt.xlabel("Date")
    plt.ylabel("Ad Spend (USD)")
    plt.show()

    # Bar chart for Ad Spend by Ad Network
    plt.figure(figsize=(12, 6))
    sns.barplot(x=adspend_by_network.index, y=adspend_by_network.values)
    plt.title('Ad Spend by Ad Network')
    plt.xlabel('Network ID')
    plt.ylabel('Ad Spend (USD)')
    plt.show()

    # Bar chart of the ad spend by client
    plt.figure(figsize=(12, 6))
    sns.barplot(x=adspend_by_client.index, y=adspend_by_client.values)
    plt.title('Ad Spend by Client')
    plt.xlabel('Client ID')
    plt.ylabel('Ad Spend (USD)')
    plt.xticks(rotation=45)  # Optional: Rotate the x-axis labels for better readability
    plt.show()

    # Histogram and power law plot of ad spend by client
    plt.figure(figsize=(12, 6))
    sns.histplot(adspend_by_client, kde=True, bins=500)
    plt.title("Ad Spend Distribution by Client")
    plt.xlabel("Ad Spend (USD)")
    plt.ylabel("Frequency")
    plt.show()

    # Fit Pareto distribution of Ad Spend  by client
    data = adspend_by_client.values
    b, loc, scale = pareto.fit(data)
    # Create histogram
    plt.figure(figsize=(12, 6))
    n, bins, patches = plt.hist(data, bins=200, density=True, alpha=0.6, color='b', label='Ad Spend Histogram')
    # Plot the fitted Pareto distribution
    x = np.linspace(min(data), max(data), 100)
    y = pareto.pdf(x, b, loc=loc, scale=scale)
    plt.plot(x, y, label='Fitted Pareto', linestyle='--', color='r')
    plt.title("Ad Spend Distribution by Client")
    plt.xlabel("Ad Spend (USD)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()


# Call the function with the file path as an argument
analyze_adspend(adspend_path)

exit()
