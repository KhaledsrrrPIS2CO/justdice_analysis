import pandas as pd
import matplotlib.pyplot as plt

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
    # Read the revenue.csv file
    revenue = pd.read_csv(file_path)
    print("Explore revenue pd:", revenue)
    print("______________________")

    # Clean and preprocess the data
    revenue['event_date'] = pd.to_datetime(revenue['event_date'])

    # Perform exploratory data analysis
    # Calculate total revenue
    total_revenue = revenue['value_usd'].sum()
    print(f"Total Revenue (USD):\n{total_revenue:.2f}")
    print("______________________")

    # Calculate revenue statistics
    revenue_summary = revenue['value_usd'].describe()
    print("Revenue central tendency:\n", revenue_summary)
    print("______________________")

    # Aggregate revenue over time
    revenue_by_date = revenue.groupby('event_date')['value_usd'].sum()
    print("Revenue by Date:\n", revenue_by_date)
    print("______________________")

    # Aggregate revenue by install_id
    revenue_by_install_id = revenue.groupby('install_id')['value_usd'].sum().sort_values(ascending=False)
    print("Revenue by install_id:\n", revenue_by_install_id)
    print("______________________")

    # Find the duplicate install_ids
    duplicate_install_ids = revenue[revenue['install_id'].duplicated()]
    # Print the duplicate install_ids
    print("Duplicate install_ids:\n", duplicate_install_ids)
    print("______________________")

    # Count the occurrences of each install_id
    install_id_counts = revenue['install_id'].value_counts()
    # Get the most repeated install_id and its count
    most_repeated_install_id = install_id_counts.idxmax()
    least_repeated_install_id = install_id_counts.idxmin()
    most_repeated_count = install_id_counts.max()
    least_repeated_count = install_id_counts.min()
    # Print the most repeated install_id and its count
    print(f"The most repeated install_id: {most_repeated_install_id} with {most_repeated_count} occurrences.")
    print(f"The least repeated install_id: {least_repeated_install_id} with {least_repeated_count} occurrences.")

    # Create visualizations
    # Time series plot for revenue over time
    plt.figure(figsize=(12, 6))
    revenue_by_date.plot(kind="line")
    plt.title("Revenue Distribution Over Time")
    plt.xlabel("Date")
    plt.ylabel("Revenue (USD)")
    plt.tight_layout()
    plt.savefig('Time: Time series plot for Revenue over time.png', dpi=300, bbox_inches='tight')
    plt.show()


# Call the function with the file path as an argument
revenue_path = '//Users/khaled/Downloads/data/revenue_converted.csv'
analyze_revenue(revenue_path)

exit()
