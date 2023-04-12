import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=["event_date"])


def get_temporal_scope(dataframe, date_column):
    min_date = dataframe[date_column].min()
    max_date = dataframe[date_column].max()
    print(f"\nTemporal scope of installs.csv: {min_date} - {max_date}")
    return min_date, max_date


def count_install_ids(dataframe, column):
    unique_install_ids = dataframe[column].nunique()
    total_install_ids = dataframe[column].count()
    print(f"\nUnique Install IDs: {unique_install_ids}\nTotal Install IDs: {total_install_ids}\n")
    return unique_install_ids, total_install_ids


def read_and_explore(dataframe):
    installs_explore = dataframe
    print("\nExplore installs DF:", installs_explore, "\n")
    return installs_explore


def count_unique_values(dataframe):
    columns = ["country_id", "network_id", "app_id", "device_os_version"]
    unique_counts = {}
    for column in columns:
        unique_values = dataframe[column].unique()
        print(f"Number of unique {column}s:", len(unique_values))
        print(f"List of unique {column}s:", unique_values)
        print()


def plot_installs_over_time_and_moving_average(dataframe, date_column, window=30, figsize=(10, 6)):
    # Aggregate installs by date
    installs_by_date = dataframe.groupby(date_column).size()

    # Calculate the 30-day moving average
    moving_average = installs_by_date.rolling(window=window).mean()

    # Create a time series plot with installs and moving average
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(installs_by_date.index, installs_by_date, label='Installs')
    ax.plot(moving_average.index, moving_average, label=f'{window}-Day Moving Average', linestyle='--')

    # Customize the plot appearance
    ax.set_title('Installs Over Time and Moving Average')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Installs')
    ax.legend()
    ax.grid()

    # Format the x-axis to display months as text
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    # Rotate x-axis labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Show the plot
    plt.tight_layout()
    plt.show()


def plot_installs_by_country(dataframe):
    installs_by_country = dataframe.groupby("country_id")["install_id"].count().sort_values(ascending=False)
    total_installs = installs_by_country.sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = installs_by_country.plot(kind="bar", ax=ax)

    ax.set_title("Distribution of Install IDs by Country")
    ax.set_xlabel("Country ID")
    ax.set_ylabel("Number of Install IDs")

    for bar in bars.containers[0]:
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        label = f"{y:.0f}, {y / total_installs * 100:.1f}%"
        ax.text(x, y + 5, label, ha="center", va="bottom", fontsize=9, rotation=0,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_installs_by_network(dataframe):
    installs_by_network = dataframe.groupby("network_id")["install_id"].count().sort_values(ascending=False)
    total_installs = installs_by_network.sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = installs_by_network.plot(kind="bar", ax=ax)

    ax.set_title("Distribution of Install IDs by Network")
    ax.set_xlabel("Network ID")
    ax.set_ylabel("Number of Install IDs")

    for bar in bars.containers[0]:
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        label = f"{y:.0f}, {y / total_installs * 100:.1f}%"
        ax.text(x, y + 5, label, ha="center", va="bottom", fontsize=9, rotation=0,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_installs_by_app(dataframe):
    installs_by_app = dataframe.groupby("app_id")["install_id"].count().sort_values(ascending=False)
    total_installs = installs_by_app.sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = installs_by_app.plot(kind="bar", ax=ax)

    ax.set_title("Distribution of Install IDs by App")
    ax.set_xlabel("App ID")
    ax.set_ylabel("Number of Install IDs")

    for bar in bars.containers[0]:
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        label = f"{y:.0f}, {y / total_installs * 100:.1f}%"
        ax.text(x, y + 5, label, ha="center", va="bottom", fontsize=9, rotation=0,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_installs_by_os(dataframe):
    installs_by_os = dataframe.groupby("device_os_version")["install_id"].count().sort_values(ascending=False)
    total_installs = installs_by_os.sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = installs_by_os.plot(kind="bar", ax=ax)

    ax.set_title("Distribution of Install IDs by Device OS Version")
    ax.set_xlabel("Device OS Version")
    ax.set_ylabel("Number of Install IDs")

    for bar in bars.containers[0]:
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        label = f"{y:.0f}, {y / total_installs * 100:.1f}%"
        ax.text(x, y + 5, label, ha="center", va="bottom", fontsize=9, rotation=0,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main(file_path):
    installs_df = load_data(file_path)

    get_temporal_scope(installs_df, "event_date")

    # Read and explore the data
    read_and_explore(installs_df)

    count_install_ids(installs_df, "install_id")

    count_unique_values(installs_df)

    plot_installs_over_time_and_moving_average(installs_df, 'event_date')

    plot_installs_by_country(installs_df)

    plot_installs_by_network(installs_df)

    plot_installs_by_app(installs_df)

    plot_installs_by_os(installs_df)


if __name__ == "__main__":
    installs_file_path = "/Users/khaled/Downloads/data/installs.csv"
    main(installs_file_path)
