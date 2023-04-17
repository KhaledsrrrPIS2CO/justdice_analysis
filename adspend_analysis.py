import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
from scipy.stats import pareto


def get_adspend_temporal_scope(csv_file):
    """
    Returns:
        dict: A dictionary containing information about the temporal scope of the Adspend data.
    """
    df = pd.read_csv(csv_file)
    date_col = [col for col in df.columns if 'date' in col.lower()][0]
    first_date = pd.to_datetime(df[date_col]).min()
    last_date = pd.to_datetime(df[date_col]).max()
    temporal_scope = (last_date - first_date).days + 1
    temporal_scope_info = {'filename': csv_file, 'first_date': first_date, 'last_date': last_date,
                           'temporal_scope': temporal_scope}
    print(f"File Path: {temporal_scope_info['filename']}")
    print(f"First Date: {temporal_scope_info['first_date']}")
    print(f"Last Date: {temporal_scope_info['last_date']}")
    print(f"Temporal Scope: {temporal_scope_info['temporal_scope']} days")
    print(f"Temporal Scope: {temporal_scope_info['temporal_scope']} days")
    print("______________________")
    return temporal_scope_info


def plot_adspend_by_country(adspend_by_country, total_adspend):
    # Calculate the cumulative percentage of total ad spend by country
    sorted_adspend = adspend_by_country.sort_values(ascending=False).reset_index(drop=True)
    cumulative_percentage = sorted_adspend.cumsum() / total_adspend * 100

    # Plot the Pareto distribution
    percentiles = np.linspace(0, 100, len(sorted_adspend) + 1)
    selected_percentiles = np.arange(0, 101, 5)
    selected_cumulative_percentage = np.interp(selected_percentiles, percentiles,
                                               np.insert(cumulative_percentage.values, 0, 0))
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(selected_percentiles, selected_cumulative_percentage, marker='o')
    ax.set_xlabel('Percentile of Country')
    ax.set_ylabel('Cumulative Percentage of Total Ad Spend')
    ax.set_title('Pareto Distribution of Ad Spend by Country')
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    plt.grid()
    plt.tight_layout()
    plt.savefig('Country_Ad_Spend_Pareto_Distribution.png', dpi=300, bbox_inches='tight')
    plt.show()


def read_and_preprocess_data(file_path):
    # Read and preprocess data
    adspend = pd.read_csv(file_path)
    adspend['event_date'] = pd.to_datetime(adspend['event_date'])
    return adspend


def analyze_adspend_data(adspend):
    # Perform exploratory data analysis:
    adspend_by_country = adspend.groupby('country_id')['value_usd'].sum().sort_values(ascending=False)
    adspend_by_network = adspend.groupby('network_id')['value_usd'].sum().sort_values(ascending=False)
    adspend_by_client = adspend.groupby('client_id')['value_usd'].sum().sort_values(ascending=False)
    adspend_by_date = adspend.groupby('event_date')['value_usd'].sum()
    return adspend_by_country, adspend_by_network, adspend_by_client, adspend_by_date


def print_preview_data(adspend, adspend_by_country, adspend_by_network, adspend_by_client, adspend_by_date):
    # Print preview data
    print("______________________")
    print("adspend type:", type(adspend), "\nContent preview:\n", adspend,
          "\nTotal ad spend (USD):", adspend['value_usd'].sum())
    print("______________________")
    print("adspend_by_date type:", type(adspend_by_date), "\nContent preview:\n", adspend_by_date)
    print("______________________")
    print("adspend_by_client type:", type(adspend_by_client), "\nContent preview:\n", adspend_by_client,
          "\nShape:\n", adspend_by_client.shape)
    print("______________________")
    print("adspend_by_network type:", type(adspend_by_network), "\nContent preview:\n", adspend_by_network)
    print("______________________")
    print("adspend_by_country type:", type(adspend_by_country), "\nContent preview:\n", adspend_by_country)


def plot_adspend_by_country_log(adspend_by_country, total_adspend):
    # Log-scale vertical bar chart for Ad Spend by Country
    plt.figure(figsize=(8, 6))
    barplot = sns.barplot(x=adspend_by_country.index, y=adspend_by_country.values, log=True)
    plt.title('Log-Scale Ad Spend by Country')
    plt.xlabel('Country ID')
    plt.ylabel('Ad Spend (USD)')
    plt.yscale('log')
    # Set y-axis ticks to USD values
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '${:,.0f}'.format(y)))
    # Calculate the percentage of total ad spend for each country
    percentage_adspend_by_country = (adspend_by_country / total_adspend) * 100
    # Add percentages on top of each bar
    for p, perc in zip(barplot.patches, percentage_adspend_by_country.values):
        barplot.annotate('{:.1f}%'.format(perc),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='baseline',
                         fontsize=10, color='black',
                         xytext=(0, 5),
                         textcoords='offset points')
    plt.tight_layout()
    plt.savefig('Country: Log-Scale Vertical Bar chart for Ad Spend by Country (USD).png', dpi=300,
                bbox_inches='tight')
    plt.show()


def plot_adspend_by_country(adspend_by_country, total_adspend):
    # Normal scale vertical bar chart for Ad Spend by Country
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=adspend_by_country.index, y=adspend_by_country.values)
    # Add dollar values on top of each bar
    for i, v in enumerate(adspend_by_country.values):
        ax.text(i, v + 100, '${:,.0f}'.format(v), ha='center', fontsize=10)
    plt.title('Ad Spend by Country')
    plt.xlabel('Country ID')
    plt.ylabel('Ad Spend (USD)')
    plt.savefig('Country: Normal-Scale Vertical Bar chart for Ad Spend by Country.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_adspend_over_time(adspend_by_date):
    # Calculate 30-day rolling adspend
    rolling_adspend = adspend_by_date.rolling(window=30).mean()
    # Time series plot for Ad Spend over time
    plt.figure(figsize=(12, 6))
    adspend_by_date.plot(kind="line")
    rolling_adspend.plot(kind="line", color="red", label="30-day Moving Average")
    plt.title("Ad Spend Distribution Over Time")
    plt.xlabel("Date")
    plt.ylabel("Ad Spend (USD)")
    plt.tight_layout()
    plt.savefig('Time: Time series plot for Ad Spend over time.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_adspend_by_network(adspend_by_network, total_adspend):
    # Bar chart for Ad Spend by Ad Network
    plt.figure(figsize=(12, 6))
    barplot = sns.barplot(x=adspend_by_network.index, y=adspend_by_network.values)
    plt.title('Ad Spend by Ad Network')
    plt.xlabel('Network ID')
    plt.ylabel('Ad Spend (USD)')
    # Add percentages on top of each bar
    for p in barplot.patches:
        percentage = 100 * p.get_height() / total_adspend
        barplot.annotate('{:.1f}%'.format(percentage),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='baseline',
                         fontsize=10, color='black',
                         xytext=(0, 5),
                         textcoords='offset points')
    plt.tight_layout()
    plt.savefig('Network: Bar chart for Ad Spend by Ad Network.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_adspend_by_client(adspend_by_client, total_adspend):
    # Bar chart of the ad spend by client
    plt.figure(figsize=(12, 6))
    barplot = sns.barplot(x=adspend_by_client.index, y=adspend_by_client.values)
    plt.title('Ad Spend by Client')
    plt.xlabel('Client ID')
    plt.ylabel('Ad Spend (USD)')
    plt.xticks(rotation=45)  # Optional: Rotate the x-axis labels for better readability
    # Add the percentage of total ad spend on top of each bar
    for p in barplot.patches:
        height = p.get_height()
        percentage = (height / total_adspend) * 100
        barplot.annotate('{:.1f}%'.format(percentage),
                         (p.get_x() + p.get_width() / 2., height),
                         ha='center', va='baseline',
                         fontsize=10, color='black',
                         xytext=(0, 5),
                         textcoords='offset points')
    plt.tight_layout()
    plt.savefig('Client: Bar chart of the ad spend by client.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_pareto_distribution_adspend_by_client(adspend_by_client):
    # Calculate the cumulative percentage of total ad spend
    sorted_adspend = adspend_by_client.sort_values(ascending=False).reset_index(drop=True)
    cumulative_percentage = sorted_adspend.cumsum() / sorted_adspend.sum() * 100

    # Plot the Pareto distribution
    percentiles = np.linspace(0, 100, len(sorted_adspend) + 1)
    selected_percentiles = np.arange(0, 101, 5)
    selected_cumulative_percentage = np.interp(selected_percentiles, percentiles,
                                               np.insert(cumulative_percentage.values, 0, 0))
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(selected_percentiles, selected_cumulative_percentage, marker='o')
    ax.set_xlabel('Percentile of Client')
    ax.set_ylabel('Cumulative Percentage of Total Ad Spend')
    ax.set_title('Pareto Distribution of Ad Spend by Client')
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    plt.grid()
    plt.tight_layout()
    plt.savefig('Client_Ad_Spend_Pareto_Distribution.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_adspend_percentage_pareto(adspend_by_client):
    # Calculate the percentage of ad spend for each client & print client_id with % of adspend total
    adspend_percentage = adspend_by_client / adspend_by_client.sum() * 100
    print("The percentage of ad spend for each client: ", adspend_percentage)

    # Fit Pareto distribution
    b, loc, scale = pareto.fit(adspend_percentage.values)
    # Create histogram
    plt.figure(figsize=(12, 6))
    n, bins, patches = plt.hist(adspend_percentage.values, bins=100, density=False, alpha=0.6, color='b',
                                label='Ad Spend Percentage Histogram')
    # Plot the fitted Pareto distribution
    x = np.linspace(min(adspend_percentage.values), max(adspend_percentage.values), 100)
    y = pareto.pdf(x, b, loc=loc, scale=scale) * n.sum() * (bins[1] - bins[0])
    plt.plot(x, y, label='Fitted Pareto', linestyle='--', color='r')
    plt.title("Concentration of Ad Spend Among Clients: A Pareto Distribution")
    plt.xlabel("Ad Spend Percentage (%)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig('Client: Pareto distribution of Ad Spend Percentage by Client.png', dpi=300, bbox_inches='tight')
    plt.show()


def adspend_main(file_path):
    get_adspend_temporal_scope(adspend_path)
    adspend = read_and_preprocess_data(file_path)
    adspend_by_country, adspend_by_network, adspend_by_client, adspend_by_date = analyze_adspend_data(adspend)
    print_preview_data(adspend, adspend_by_country, adspend_by_network, adspend_by_client, adspend_by_date)
    total_adspend = adspend_by_country.sum()
    plot_adspend_by_country(adspend_by_country, total_adspend)
    plot_adspend_over_time(adspend_by_date)
    plot_adspend_by_network(adspend_by_network, total_adspend)
    plot_adspend_by_client(adspend_by_client, total_adspend)
    plot_adspend_by_country_log(adspend_by_country, total_adspend)
    plot_adspend_percentage_pareto(adspend_by_client)
    plot_pareto_distribution_adspend_by_client(adspend_by_client)


# Call the analyze_adspend function with the file_path
adspend_path = "data/adspend_converted.csv"
adspend_main(adspend_path)
