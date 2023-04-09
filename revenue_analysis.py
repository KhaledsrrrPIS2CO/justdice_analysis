import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

revenue_path = '/Users/khaled/Downloads/data/revenue_converted.csv'


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
    return {'filename': csv_file, 'first_date': first_date, 'last_date': last_date, 'temporal_scope': temporal_scope}


temporal_scope_results = get_revenue_temporal_scope(revenue_path)

# Print  revenue timeline details
print(f"File Path: {temporal_scope_results['filename']}")
print(f"First Date: {temporal_scope_results['first_date']}")
print(f"Last Date: {temporal_scope_results['last_date']}")
print(f"Temporal Scope: {temporal_scope_results['temporal_scope']} days")
print("______________________")


def analyze_revenue(file_path):
    # Read the revenue.csv file & explore print
    revenue = pd.read_csv(file_path)
    print("Explore revenue DF:", revenue, "Shape: ", revenue.shape)
    print("______________________")
    # Calculate the number of unique install_id & print
    unique_install_id_count = revenue['install_id'].nunique()
    print(f"The number of unique install_id: {unique_install_id_count}")
    print("______________________")

    # Clean and preprocess the data
    revenue['event_date'] = pd.to_datetime(revenue['event_date'])

    # Perform exploratory data analysis & explore print
    # Calculate total revenue
    total_revenue = revenue['value_usd'].sum()

    print(f"Total Revenue (USD):\n{total_revenue:.2f}")
    print("______________________")

    # Calculate revenue statistics & explore print
    revenue_summary = revenue['value_usd'].describe()
    print("Revenue central tendency:\n", revenue_summary)
    print("______________________")

    # Aggregate revenue over time & explore print
    revenue_by_date = revenue.groupby('event_date')['value_usd'].sum()
    print("Revenue by Date:\n", revenue_by_date, "Shape: ", revenue_by_date.shape)
    print("______________________")

    # Aggregate revenue by install_id & explore print
    revenue_by_install_id = revenue.groupby('install_id')['value_usd'].sum().sort_values(ascending=False)
    pd.options.display.float_format = '{:.6f}'.format
    print("Revenue by install_id:\n", revenue_by_install_id, "Shape: ", revenue_by_install_id.shape)
    print("______________________")

    cumulative_revenue = revenue_by_install_id.cumsum()
    print("cumulative_revenue:", cumulative_revenue)
    print("______________________")

    top_1_percent = cumulative_revenue[cumulative_revenue >= cumulative_revenue.quantile(0.99)]
    print("top_1_percent", top_1_percent)
    print("______________________")

    total_revenue = cumulative_revenue.iloc[-1]
    cumulative_percentage = (cumulative_revenue / total_revenue) * 100

    # Calculate the decile thresholds
    decile_thresholds = np.linspace(0, 1, 11)
    # Calculate the revenue for each decile
    decile_revenues = []
    for i in range(len(decile_thresholds) - 1):
        lower = int(decile_thresholds[i] * len(revenue_by_install_id))
        upper = int(decile_thresholds[i + 1] * len(revenue_by_install_id))
        decile_revenue = revenue_by_install_id.iloc[lower:upper].sum()
        decile_revenues.append(decile_revenue)

    # Print the revenue for each decile in USD and in % out of the total revenue
    for i, decile_revenue in enumerate(decile_revenues):
        decile_percentage = (decile_revenue / total_revenue) * 100
        print(f"Decile {i + 1}: {decile_revenue:.2f} USD ({decile_percentage:.2f}%)")

    # Find the duplicate install_ids & explore print
    duplicate_install_ids = revenue[revenue['install_id'].duplicated()]
    print("Duplicate install_ids:\n", duplicate_install_ids, "Shape: ", duplicate_install_ids.shape)
    print("______________________")

    # Count the occurrences of each install_id & explore print
    install_id_counts = revenue['install_id'].value_counts()
    most_repeated_install_id = install_id_counts.idxmax()
    least_repeated_install_id = install_id_counts.idxmin()
    most_repeated_count = install_id_counts.max()
    least_repeated_count = install_id_counts.min()
    print(f"The most repeated install_id: {most_repeated_install_id} with {most_repeated_count} occurrences.")
    print(f"The least repeated install_id: {least_repeated_install_id} with {least_repeated_count} occurrences.")
    print("______________________")

    # Calculate 30-day rolling average
    rolling_revenue = revenue_by_date.rolling(window=30).mean()
    # Time series plot for revenue over time & save png
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

    # Bar graph of revenue contribution of each decile
    deciles = [f'Decile {i + 1}' for i in range(len(decile_revenues))]
    decile_percentages = [(decile_revenue / total_revenue) * 100 for decile_revenue in decile_revenues]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(deciles, decile_percentages)
    ax.set_xlabel('Deciles')
    ax.set_ylabel('Percentage of Total Revenue')
    ax.set_title('Revenue Contribution by Decile as percentage')
    for i, v in enumerate(decile_percentages):
        ax.text(i - 0.25, v + 0.25, f"{v:.2f}%", fontsize=9)
    plt.savefig('Revenue Contribution by Decile as percentage.png', dpi=300, bbox_inches='tight')
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(deciles, decile_revenues)
    ax.set_xlabel('Deciles')
    ax.set_ylabel('Revenue (USD)')
    ax.set_title('Revenue Contribution by Decile in USD')
    for i, v in enumerate(decile_revenues):
        ax.text(i - 0.25, v + 1000, f"${v:,.2f}", fontsize=9)
    plt.savefig('Revenue Contribution by Decile in USD.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Pareto Distribution of Total Revenue by install_id
    percentiles = np.linspace(0, 100, len(cumulative_percentage))
    # Select fewer percentiles to plot
    selected_percentiles = np.arange(0, 101, 5)  # Select every 5th percentile
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

    # Get the top 10% install_ids
    top_10_percent_install_ids = revenue_by_install_id.head(int(len(revenue_by_install_id) * 0.1))

    # Calculate the revenue contribution for each install_id in the top 10%
    top_10_percent_revenue = top_10_percent_install_ids.sum()
    top_10_percent_decile_revenues = []
    for i in range(10):
        start = int(len(top_10_percent_install_ids) * i / 10)
        end = int(len(top_10_percent_install_ids) * (i + 1) / 10)
        decile_revenue = top_10_percent_install_ids[start:end].sum()
        top_10_percent_decile_revenues.append(decile_revenue)

    # Calculate the percentage for each decile
    top_10_percent_decile_percentages = [(decile_revenue / total_revenue) * 100 for decile_revenue in
                                         top_10_percent_decile_revenues]

    # Plot the revenue contribution by decile for the top 10% install_ids as percentages of the total revenue
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

    # Bar graph revenue contribution by decile for the top 10% install_ids as $$
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


    ####
    ####
    ####
    ####
    ####


# Call the function with the file path as an argument
revenue_path = '//Users/khaled/Downloads/data/revenue_converted.csv'
analyze_revenue(revenue_path)

exit()
