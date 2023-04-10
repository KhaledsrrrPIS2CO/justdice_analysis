import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_revenue_temporal_scope(csv_file):
    """
    Returns:
        dict: A dictionary containing information about the temporal scope of the revenue data.
    """
    df = pd.read_csv(csv_file)
    date_col = [col for col in df.columns if 'date' in col.lower()][0]
    first_date = pd.to_datetime(df[date_col]).min()
    last_date = pd.to_datetime(df[date_col]).max()
    temporal_scope = (last_date - first_date).days + 1
    temporal_scope_results = {'filename': csv_file, 'first_date': first_date, 'last_date': last_date,
                              'temporal_scope': temporal_scope}
    print(f"File Path: {temporal_scope_results['filename']}")
    print(f"First Date: {temporal_scope_results['first_date']}")
    print(f"Last Date: {temporal_scope_results['last_date']}")
    print(f"Temporal Scope: {temporal_scope_results['temporal_scope']} days")
    print("______________________")
    return temporal_scope_results


def read_and_explore(file_path):
    revenue = pd.read_csv(file_path)
    print("Explore revenue DF:", revenue, "Shape: ", revenue.shape)
    print("______________________")
    return revenue


def unique_install_id_count(revenue):
    count = revenue['install_id'].nunique()
    print(f"The number of unique install_id: {count}")
    print("______________________")
    return count


def preprocess_data(revenue):
    revenue['event_date'] = pd.to_datetime(revenue['event_date'])
    return revenue


def total_revenue(revenue):
    total = revenue['value_usd'].sum()
    print(f"Total Revenue (USD):\n{total:.2f}")
    print("______________________")
    return total


def revenue_summary(revenue):
    summary = revenue['value_usd'].describe()
    print("Revenue central tendency:\n", summary)
    print("______________________")
    return summary


def revenue_by_date(revenue):
    by_date = revenue.groupby('event_date')['value_usd'].sum()
    print("Revenue by Date:\n", by_date, "Shape: ", by_date.shape)
    print("______________________")
    return by_date


def revenue_by_install_id(revenue):
    by_install_id = revenue.groupby('install_id')['value_usd'].sum().sort_values(ascending=False)
    pd.options.display.float_format = '{:.6f}'.format
    print("Revenue by install_id:\n", by_install_id, "Shape: ", by_install_id.shape)
    print("______________________")
    return by_install_id


def cumulative_revenue(revenue_by_install_id):
    cum_revenue = revenue_by_install_id.cumsum()
    print("cumulative_revenue:", cum_revenue)
    print("______________________")
    return cum_revenue


def top_1_percent(cumulative_revenue):
    top_1 = cumulative_revenue[cumulative_revenue >= cumulative_revenue.quantile(0.99)]
    print("top_1_percent", top_1)
    print("______________________")
    return top_1


def decile_revenues(revenue_by_install_id, total_revenue):
    decile_thresholds = np.linspace(0, 1, 11)
    decile_revs = []
    for i in range(len(decile_thresholds) - 1):
        lower = int(decile_thresholds[i] * len(revenue_by_install_id))
        upper = int(decile_thresholds[i + 1] * len(revenue_by_install_id))
        decile_revenue = revenue_by_install_id.iloc[lower:upper].sum()
        decile_revs.append(decile_revenue)
    print_decile_revenues(decile_revs, total_revenue)
    return decile_revs


def print_decile_revenues(decile_revenues, total_revenue):
    for i, decile_revenue in enumerate(decile_revenues):
        decile_percentage = (decile_revenue / total_revenue) * 100
        print(f"Decile {i + 1}: {decile_revenue:.2f} USD ({decile_percentage:.2f}%)")
    print("______________________")


def duplicate_install_ids(revenue):
    duplicates = revenue[revenue['install_id'].duplicated()]
    print("Duplicate install_ids:\n", duplicates, "Shape: ", duplicates.shape)
    print("______________________")
    return duplicates


def install_id_counts(revenue):
    id_counts = revenue['install_id'].value_counts()
    most_repeated_install_id = id_counts.idxmax()
    least_repeated_install_id = id_counts.idxmin()
    most_repeated_count = id_counts.max()
    least_repeated_count = id_counts.min()
    print(f"The most repeated install_id: {most_repeated_install_id} with {most_repeated_count} occurrences.")
    print(f"The least repeated install_id: {least_repeated_install_id} with {least_repeated_count} occurrences.")
    print("______________________")
    return id_counts


def plot_revenue_over_time(revenue_by_date):
    rolling_revenue = revenue_by_date.rolling(window=30).mean()
    plt.figure(figsize=(12, 6))
    revenue_by_date.plot(kind="line")
    rolling_revenue.plot(kind="line", color="red", label="30-day Moving Average")
    plt.title("Revenue Distribution Over Time")
    plt.xlabel("Date")
    plt.ylabel("Revenue (USD)")
    plt.tight_layout()
    plt.legend()
    plt.savefig('Time: Time series plot for Revenue over time with Moving Average.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_decile_revenue_usd(decile_revenues):
    deciles = [f'Decile {i + 1}' for i in range(len(decile_revenues))]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(deciles, decile_revenues)
    ax.set_xlabel('Deciles')
    ax.set_ylabel('Revenue (USD)')
    ax.set_title('Install_id Revenue Contribution by Decile in USD')
    for i, v in enumerate(decile_revenues):
        ax.text(i - 0.25, v + 1000, f"${v:,.2f}", fontsize=9)
    plt.savefig('Install_id Revenue Contribution by Decile in USD.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_decile_revenue_of_total_percentage(decile_revenues, total_revenue):
    deciles = [f'Decile {i + 1}' for i in range(len(decile_revenues))]
    decile_percentages = [(decile_revenue / total_revenue) * 100 for decile_revenue in decile_revenues]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(deciles, decile_percentages)
    ax.set_xlabel('Deciles')
    ax.set_ylabel('Percentage of Total Revenue')
    ax.set_title('Install_id Revenue Contribution by Decile as percentage')
    for i, v in enumerate(decile_percentages):
        ax.text(i - 0.25, v + 0.25, f"{v:.2f}%", fontsize=9)
    plt.savefig('Install_id Revenue Contribution by Decile as percentage.png', dpi=300, bbox_inches='tight')
    plt.show()


def pareto_distribution(cumulative_percentage):
    percentiles = np.linspace(0, 100, len(cumulative_percentage))
    selected_percentiles = np.arange(0, 101, 5)
    selected_cumulative_percentage = np.interp(selected_percentiles, percentiles, cumulative_percentage)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(selected_percentiles, selected_cumulative_percentage, marker='o')
    ax.set_xlabel('Percentile of install_id')
    ax.set_ylabel('Cumulative Percentage of Total Revenue')
    ax.set_title('Pareto Distribution of Total Revenue by install_id')
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    plt.grid()
    plt.savefig('Pareto Distribution of Total Revenue by install_id.png', dpi=300, bbox_inches='tight')
    plt.show()


def top_10_percent_decile_revenues(revenue_by_install_id, total_revenue):
    top_10_percent_install_ids = revenue_by_install_id.head(int(len(revenue_by_install_id) * 0.1))
    top_10_percent_revenue = top_10_percent_install_ids.sum()
    top_10_percent_decile_revenues = []
    for i in range(10):
        start = int(len(top_10_percent_install_ids) * i / 10)
        end = int(len(top_10_percent_install_ids) * (i + 1) / 10)
        decile_revenue = top_10_percent_install_ids[start:end].sum()
        top_10_percent_decile_revenues.append(decile_revenue)
    return top_10_percent_decile_revenues


def plot_top_10_percent_decile_percentages(top_10_percent_decile_revenues, total_revenue):
    top_10_percent_decile_percentages = [(decile_revenue / total_revenue) * 100 for decile_revenue in
                                         top_10_percent_decile_revenues]
    deciles = [f'Decile {i + 1}' for i in range(len(top_10_percent_decile_percentages))]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(deciles, top_10_percent_decile_percentages)
    ax.set_xlabel('Deciles')
    ax.set_ylabel('Percentage of Total Revenue')
    ax.set_title('Revenue Contribution by Decile for Top 10% install_ids as percentage')
    for i, v in enumerate(top_10_percent_decile_percentages):
        ax.text(i - 0.25, v + 0.1, f"{v:.2f}%", fontsize=9)
    plt.savefig('revenue_chart.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_top_10_percent_decile_revenues(top_10_percent_decile_revenues):
    deciles = [f'Decile {i + 1}' for i in range(len(top_10_percent_decile_revenues))]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(deciles, top_10_percent_decile_revenues)
    ax.set_xlabel('Deciles')
    ax.set_ylabel('Revenue (USD)')
    ax.set_title('Revenue Contribution by Decile for Top 10% install_ids in USD')
    for i, v in enumerate(top_10_percent_decile_revenues):
        ax.text(i - 0.25, v + 100, f"${v:,.2f}", fontsize=9)
    plt.savefig('Revenue Contribution by Decile for Top 10% install_ids in USD.png', dpi=300, bbox_inches='tight')
    plt.show()


revenue_path = '/Users/khaled/Downloads/data/revenue_converted.csv'
# analyze_revenue(file_path)

# gGet_revenue_temporal_scope
temporal_scope_results = get_revenue_temporal_scope(revenue_path)

# Read and explore the data
revenue = read_and_explore(revenue_path)

# Get the unique install_id count
unique_count = unique_install_id_count(revenue)

# Preprocess the data
revenue = preprocess_data(revenue)

# Calculate the total revenue
total_rev = total_revenue(revenue)

# Get the revenue summary
summary = revenue_summary(revenue)

# Calculate revenue by date
rev_by_date = revenue_by_date(revenue)

# Calculate revenue by install_id
rev_by_install_id = revenue_by_install_id(revenue)

# Calculate cumulative revenue
cum_revenue = cumulative_revenue(rev_by_install_id)

# Calculate cumulative percentage
cumulative_percentage = (cum_revenue / total_rev) * 100

# Calculate the top 1 percent
top1 = top_1_percent(cum_revenue)

# Calculate decile revenues
decile_revenue = decile_revenues(rev_by_install_id, total_rev)

# Find duplicate install_ids
duplicates = duplicate_install_ids(revenue)

# Calculate install_id counts
id_counts = install_id_counts(revenue)

# Plot revenue over time
plot_revenue_over_time(rev_by_date)

# Plot decile revenue as USD
plot_decile_revenue_usd(decile_revenue)

# Plot decile revenue as percentage
plot_decile_revenue_of_total_percentage(decile_revenue, total_rev)

# Plot the Pareto distribution
pareto_distribution(cumulative_percentage)

# Calculate the top 10% decile revenues
top_10_decile_revenues = top_10_percent_decile_revenues(rev_by_install_id, total_rev)

# Plot the top 10% decile percentages
plot_top_10_percent_decile_percentages(top_10_decile_revenues, total_rev)

# Plot the top 10% decile revenues in USD
plot_top_10_percent_decile_revenues(top_10_decile_revenues)
