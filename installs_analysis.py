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
    print(f"\nUnique Install IDs: {unique_install_ids}\nTotal Install IDs: {total_install_ids}")
    return unique_install_ids, total_install_ids


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



def read_and_explore(installs_df):
    installs_explore = installs_df
    print("\nExplore installs DF:", installs_explore, "\n")
    return installs_explore

def main(installs_file_path):
    installs_df = load_data(installs_file_path)

    get_temporal_scope(installs_df, "event_date")

    # Read and explore the data
    read_and_explore(installs_df)

    count_install_ids(installs_df, "install_id")

    plot_installs_over_time_and_moving_average(installs_df, 'event_date')


if __name__ == "__main__":
    installs_file_path = "/Users/khaled/Downloads/data/installs.csv"
    main(installs_file_path)
