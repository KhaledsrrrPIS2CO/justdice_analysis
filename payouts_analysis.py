import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns


def load_data(file_path):
    return pd.read_csv(file_path)


def convert_unix_time_to_datetime(file_path):
    # Read the CSV file into a dataframe
    df = pd.read_csv(file_path)

    # Convert the Unix timestamps to Datetime objects
    for col in df.columns:
        if "event_date" in col:
            df[col] = pd.to_datetime(df[col]).dt.date

    return df


def calculate_total_average_max_and_min_payouts(payouts):
    total_payouts = payouts["value_usd"].sum()
    average_payout_per_install = payouts["value_usd"].mean()
    max_payout = payouts["value_usd"].max()
    min_payout = payouts["value_usd"].min()
    return total_payouts, average_payout_per_install, max_payout, min_payout


def calculate_daily_payouts(payouts):
    return payouts.groupby("event_date")["value_usd"].sum().reset_index()


def calculate_average_payouts_per_group(merged_data, group_column):
    return merged_data.groupby(group_column)["value_usd"].mean().reset_index()


def get_temporal_scope(dataframe, date_column):
    min_date = dataframe[date_column].min()
    max_date = dataframe[date_column].max()
    return min_date, max_date


def count_install_ids(dataframe, column):
    unique_install_ids = dataframe[column].nunique()
    total_install_ids = dataframe[column].count()
    return unique_install_ids, total_install_ids


def calculate_central_tendency(dataframe, column):
    mean = dataframe[column].mean()
    median = dataframe[column].median()
    mode = dataframe[column].mode().values.tolist()[0]
    return mean, median, mode


def get_payouts_info(dataframe):
    shape = dataframe.shape
    num_all_install_ids = dataframe["install_id"].count()
    num_unique_install_ids = dataframe["install_id"].nunique()
    return shape, num_all_install_ids, num_unique_install_ids


def read_and_explore(file_path):
    payouts = file_path
    print("\nExplore payouts DF:", payouts, "\n")
    return payouts


def plot_calculate_time_series(daily_payouts, window_size):
    daily_payouts["moving_average"] = daily_payouts["value_usd"].rolling(window=window_size).mean()

    plt.figure(figsize=(15, 6))
    sns.lineplot(data=daily_payouts, x="event_date", y="value_usd", label="Daily Payouts")
    sns.lineplot(data=daily_payouts, x="event_date", y="moving_average", label=f"{window_size}-Day Moving Average")
    plt.title("Daily Payouts over time with Moving Average")
    plt.tight_layout()
    plt.xlabel("Event Date")
    plt.ylabel("Payouts (USD)")

    # Update the x-axis to display month names
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)  # Optional: Rotate the x-axis labels for better readability
    plt.tight_layout()
    plt.savefig('PTime_series_plot_for_payouts_over_time_with_Moving_Average.png', dpi=300, bbox_inches='tight')
    plt.show()


def calculate_plot_payouts_by_decile_percentage(dataframe):
    # Calculate the payouts for each install ID
    payouts_by_id = dataframe.groupby("install_id")["value_usd"].sum().reset_index()

    # Divide the install IDs into deciles based on their payouts
    payouts_by_id["decile"] = pd.qcut(payouts_by_id["value_usd"], 10, labels=False)

    # Calculate the total payouts for each decile
    decile_payouts = payouts_by_id.groupby("decile")["value_usd"].sum().reset_index()

    # Calculate the payout contribution for each decile
    total_payouts = decile_payouts["value_usd"].sum()
    decile_payouts["payout_contribution"] = decile_payouts["value_usd"] / total_payouts * 100

    # Reorder the deciles by payout contribution and reset the index
    decile_payouts = decile_payouts.sort_values("payout_contribution", ascending=False).reset_index(drop=True)

    # Generate a bar graph of the payout contribution for each decile
    x_labels = ["Decile 1", "Decile 2", "Decile 3", "Decile 4", "Decile 5",
                "Decile 6", "Decile 7", "Decile 8", "Decile 9", "Decile 10"]
    ax = plt.gca()
    ax.bar(x_labels, decile_payouts["payout_contribution"], color="blue")
    plt.title("Payouts by Decile (%)")
    plt.ylabel("Percentage of total payouts")
    plt.xticks(rotation=45)

    # Add the percentage values on top of each bar
    for i, val in enumerate(decile_payouts["payout_contribution"]):
        ax.text(i, val + 1, f"{val:.1f}%", ha="center")
    plt.tight_layout()
    plt.savefig('Payouts by Decile percentage', dpi=300, bbox_inches='tight')
    plt.show()

    return decile_payouts[["decile", "payout_contribution", "value_usd"]]


def calculate_plot_payouts_by_decile_usd(dataframe):
    # Calculate the payouts for each install ID
    payouts_by_id = dataframe.groupby("install_id")["value_usd"].sum().reset_index()

    # Divide the install IDs into deciles based on their payouts
    payouts_by_id["decile"] = pd.qcut(payouts_by_id["value_usd"], 10, labels=False)

    # Calculate the total payouts for each decile
    decile_payouts = payouts_by_id.groupby("decile")["value_usd"].sum().reset_index()

    # Reorder the deciles and reset the index
    decile_payouts = decile_payouts.sort_values("value_usd", ascending=False).reset_index(drop=True)

    # Generate a bar graph of the payouts for each decile
    x_labels = ["Decile 1", "Decile 2", "Decile 3", "Decile 4", "Decile 5",
                "Decile 6", "Decile 7", "Decile 8", "Decile 9", "Decile 10"]
    plt.bar(x_labels, decile_payouts["value_usd"], color="blue")
    plt.title("Payouts by Decile (USD)")
    plt.ylabel("Payouts (USD)")
    plt.xticks(rotation=45)

    # Add USD value on top of each bar
    for i, value in enumerate(decile_payouts["value_usd"]):
        plt.text(i, value, f"${value:.0f}", ha='center')
    plt.tight_layout()
    plt.show()
    plt.savefig('Payouts by Decile usd', dpi=300, bbox_inches='tight')

    return decile_payouts[["decile", "value_usd"]]


def plot_and_calculate_biggest_decile_to_ten_deciles_usd(dataframe):
    # Calculate the payouts for each install ID
    payouts_by_id = dataframe.groupby("install_id")["value_usd"].sum().reset_index()

    # Divide the install IDs into 10 deciles based on their payouts
    payouts_by_id["decile"] = pd.qcut(payouts_by_id["value_usd"], 10, labels=False)

    # Calculate the total payouts for the top decile
    top_decile_payouts = payouts_by_id[payouts_by_id["decile"] == 9]["value_usd"].sum()

    # Divide the top decile into 10 smaller deciles
    top_decile = payouts_by_id[payouts_by_id["decile"] == 9].sort_values("value_usd", ascending=False)
    top_decile["sub_decile"] = pd.qcut(top_decile["value_usd"], 10, labels=False)

    # Calculate the total payouts for each sub-decile
    sub_decile_payouts = top_decile.groupby("sub_decile")["value_usd"].sum().reset_index()

    # Sort the sub-deciles in descending order of value
    sub_decile_payouts = sub_decile_payouts.sort_values("value_usd", ascending=False)

    # Generate a bar graph of the payouts for each sub-decile
    x_labels = [f" Decile {i + 1}" for i in range(10)]
    plt.bar(x_labels, sub_decile_payouts["value_usd"], color="blue")

    # Add labels for sub-decile payouts
    for i, value in enumerate(sub_decile_payouts["value_usd"]):
        plt.text(i, value, f"${value:.0f}", ha='center', va='bottom')

    plt.title("Payouts by Decile of top 10% of payouts (USD)")
    plt.xlabel("")
    plt.ylabel("Payouts (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.savefig('Payouts by Decile of top 10 of payouts (USD).png', dpi=300, bbox_inches='tight')

    return sub_decile_payouts[["sub_decile", "value_usd"]]


def plot_and_calculate_biggest_decile_to_ten_deciles_percent(dataframe):
    total_payouts = dataframe["value_usd"].sum()
    # Calculate the payouts for each install ID
    payouts_by_id = dataframe.groupby("install_id")["value_usd"].sum().reset_index()

    # Divide the install IDs into 10 deciles based on their payouts
    payouts_by_id["decile"] = pd.qcut(payouts_by_id["value_usd"], 10, labels=False)

    # Calculate the total payouts for the top decile
    top_decile_payouts = payouts_by_id[payouts_by_id["decile"] == 9]["value_usd"].sum()

    # Divide the top decile into 10 smaller deciles
    top_decile = payouts_by_id[payouts_by_id["decile"] == 9].sort_values("value_usd", ascending=False)
    top_decile["sub_decile"] = pd.qcut(top_decile["value_usd"], 10, labels=False)

    # Calculate the total payouts for each sub-decile
    sub_decile_payouts = top_decile.groupby("sub_decile")["value_usd"].sum().reset_index()

    # Sort the sub-deciles in descending order of value
    sub_decile_payouts = sub_decile_payouts.sort_values("value_usd", ascending=False)

    # Calculate the percentage of payouts for each sub-decile
    sub_decile_payouts["payout_percentage"] = sub_decile_payouts["value_usd"] / total_payouts * 100

    # Generate a bar graph of the payouts for each sub-decile
    x_labels = [f" Decile {i + 1}" for i in range(10)]
    plt.bar(x_labels, sub_decile_payouts["payout_percentage"], color="blue")

    # Add labels for sub-decile payouts
    for i, value in enumerate(sub_decile_payouts["payout_percentage"]):
        plt.text(i, value, f"{value:.1f}%", ha='center', va='bottom')

    plt.title("Payouts by Decile of top 10% of payouts (USD)")
    plt.xlabel("")
    plt.ylabel("Percentage of Payouts (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.savefig('Payouts by Decile of top 10 of payouts (percent).png', dpi=300, bbox_inches='tight')

    return sub_decile_payouts[["sub_decile", "value_usd", "payout_percentage"]]


def pareto_distribution(dataframe):
    # Calculate the total payouts for each install ID
    payouts_by_id = dataframe.groupby("install_id")["value_usd"].sum().reset_index()

    # Calculate the cumulative percentage of total payouts
    payouts_by_id = payouts_by_id.sort_values("value_usd", ascending=False).reset_index(drop=True)
    payouts_by_id["cumulative_percentage"] = payouts_by_id["value_usd"].cumsum() / payouts_by_id[
        "value_usd"].sum() * 100

    # Plot the Pareto distribution
    percentiles = np.linspace(0, 100, len(payouts_by_id))
    selected_percentiles = np.arange(0, 101, 5)
    selected_cumulative_percentage = np.interp(selected_percentiles, percentiles,
                                               payouts_by_id["cumulative_percentage"])
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(selected_percentiles, selected_cumulative_percentage, marker='o')
    ax.set_xlabel('Percentile of install_id')
    ax.set_ylabel('Cumulative Percentage of Total Payouts')
    ax.set_title('Pareto Distribution of Total Payouts by install_id')
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    plt.grid()
    plt.savefig('PPareto Distribution of Total Payouts by install_id.png', dpi=300, bbox_inches='tight')
    plt.show()

    return payouts_by_id[["install_id", "value_usd", "cumulative_percentage"]]


def payouts_main(payouts_file_path):
    payouts_df = load_data(payouts_file_path)

    start_date, end_date = get_temporal_scope(payouts_df, "event_date")
    print(f"\nTemporal scope of payouts_converted.csv: {start_date} - {end_date}")

    total_payouts, average_payout_per_install, max_payout, min_payout = calculate_total_average_max_and_min_payouts(
        payouts_df)
    print(f"\nTotal Payouts (USD): {total_payouts}\nAverage Payout per Install: {average_payout_per_install}"
          f"\nMaximum Payout: {max_payout}\nMinimum Payout: {min_payout}")

    # Read and explore the data
    read_and_explore(payouts_df)

    payouts_df = convert_unix_time_to_datetime(payouts_file_path)

    shape, num_all_install_ids, num_unique_install_ids = get_payouts_info(payouts_df)
    print(f"Shape of Data: {shape}\nNumber of All Install IDs: {num_all_install_ids}"
          f"\nNumber of Unique Install IDs: {num_unique_install_ids}\n")

    unique_install_ids, total_install_ids = count_install_ids(payouts_df, "install_id")
    print(f"\nUnique Install IDs: {unique_install_ids}\nTotal Install IDs: {total_install_ids}")

    mean, median, mode = calculate_central_tendency(payouts_df, "value_usd")
    print(f"Mean: {mean}\nMedian: {median}\nMode: {mode}")

    daily_payouts = calculate_daily_payouts(payouts_df)
    plot_calculate_time_series(daily_payouts, window_size=30)

    calculate_plot_payouts_by_decile_percentage(payouts_df)
    calculate_plot_payouts_by_decile_usd(payouts_df)
    plot_and_calculate_biggest_decile_to_ten_deciles_usd(payouts_df)
    plot_and_calculate_biggest_decile_to_ten_deciles_percent(payouts_df)
    pareto_distribution(payouts_df)


if __name__ == "__main__":
    payouts_file_path = "data/payouts_converted.csv"
    payouts_main(payouts_file_path)
