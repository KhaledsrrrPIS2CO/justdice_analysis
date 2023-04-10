import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import seaborn as sns


def load_data(file_path):
    return pd.read_csv(file_path)


def calculate_total_average_max_and_min_payouts(payouts):
    total_payouts = payouts["value_usd"].sum()
    average_payout_per_install = payouts["value_usd"].mean()
    max_payout = payouts["value_usd"].max()
    min_payout = payouts["value_usd"].min()
    return total_payouts, average_payout_per_install, max_payout, min_payout


def calculate_daily_payouts(payouts):
    return payouts.groupby("event_date")["value_usd"].sum().reset_index()


def merge_installs_and_payouts(installs, payouts):
    return pd.merge(installs, payouts, on="install_id", how="inner")


def calculate_average_payouts_per_group(merged_data, group_column):
    return merged_data.groupby(group_column)["value_usd"].mean().reset_index()


def plot_daily_payouts(daily_payouts):
    sns.set(style="whitegrid")
    plt.figure(figsize=(15, 6))
    sns.lineplot(data=daily_payouts, x="event_date", y="value_usd")
    plt.title("Daily Payouts")
    plt.xlabel("Event Date")
    plt.ylabel("Payouts (USD)")
    plt.show()


def get_temporal_scope(dataframe, date_column):
    min_date = dataframe[date_column].min()
    max_date = dataframe[date_column].max()
    return min_date, max_date


def count_install_ids(dataframe, column):
    unique_install_ids = dataframe[column].nunique()
    total_install_ids = dataframe[column].count()
    return unique_install_ids, total_install_ids


def plot_moving_average(daily_payouts, window_size):
    daily_payouts["moving_average"] = daily_payouts["value_usd"].rolling(window=window_size).mean()

    plt.figure(figsize=(15, 6))
    sns.lineplot(data=daily_payouts, x="event_date", y="value_usd", label="Daily Payouts")
    sns.lineplot(data=daily_payouts, x="event_date", y="moving_average", label=f"{window_size}-Day Moving Average")
    plt.title("Daily Payouts with Moving Average")
    plt.xlabel("Event Date")
    plt.ylabel("Payouts (USD)")
    plt.legend()
    plt.savefig("Time_series_plot_for_payouts_over_time_with_Moving_Average.png")
    plt.show()


def plot_install_payout_deciles(dataframe, column):
    # Calculate the deciles of the payouts column
    deciles = dataframe[column].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]).tolist()

    # Group the dataframe by install ID and calculate the total payout for each install ID
    payouts_by_install = dataframe.groupby("install_id")[column].sum().reset_index()

    # Categorize the payouts by decile
    payouts_by_install["decile"] = pd.cut(payouts_by_install[column], bins=[-np.inf] + deciles + [np.inf],
                                          labels=["<10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-70%",
                                                  "70-80%", "80-90%", ">90%"])

    # Calculate the number of installs in each decile
    install_counts = payouts_by_install["decile"].value_counts().sort_index()

    # Plot the bar graph
    plt.figure(figsize=(10, 6))
    sns.barplot(x=install_counts.index, y=install_counts.values)
    plt.title("Install ID Payout Contribution by Deciles")
    plt.xlabel("Decile")
    plt.ylabel("Number of Installs")
    plt.show()


def plot_install_payout_deciles(dataframe, column):
    # Calculate the deciles of the payouts column
    deciles = dataframe[column].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]).tolist()

    # Group the dataframe by install ID and calculate the total payout for each install ID
    payouts_by_install = dataframe.groupby("install_id")[column].sum().reset_index()

    # Categorize the payouts by decile
    payouts_by_install["decile"] = pd.cut(payouts_by_install[column], bins=[-np.inf] + deciles + [np.inf], labels=["<10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-70%", "70-80%", "80-90%", ">90%"])

    # Calculate the USD value of payouts in each decile
    payouts_by_decile = payouts_by_install.groupby("decile")[column].sum().reset_index()

    # Plot the bar graph
    plt.figure(figsize=(10, 6))
    sns.barplot(x="decile", y=column, data=payouts_by_decile)
    plt.title("Install ID Payout Contribution by Deciles")
    plt.xlabel("Decile")
    plt.ylabel("Payouts (USD)")
    plt.show()



def main(payouts_file_path, installs_file_path):
    payouts = load_data(payouts_file_path)
    installs = load_data(installs_file_path)

    total_payouts, average_payout_per_install, max_payout, min_payout = calculate_total_average_max_and_min_payouts(
        payouts)
    print(f"\nTotal Payouts (USD): {total_payouts}\nAverage Payout per Install: {average_payout_per_install}"
          f"\nMaximum Payout: {max_payout}\nMinimum Payout: {min_payout}")

    daily_payouts = calculate_daily_payouts(payouts)
    plot_daily_payouts(daily_payouts)

    merged_data = merge_installs_and_payouts(installs, payouts)

    average_payout_per_country = calculate_average_payouts_per_group(merged_data, "country_id")
    print(f"\nAverage Payout per Country:\n{average_payout_per_country}")

    average_payout_per_app = calculate_average_payouts_per_group(merged_data, "app_id")
    print(f"\nAverage Payout per App:\n{average_payout_per_app}")

    average_payout_per_network = calculate_average_payouts_per_group(merged_data, "network_id")
    print(f"\nAverage Payout per Network:\n{average_payout_per_network}")

    start_date, end_date = get_temporal_scope(payouts, "event_date")
    print(f"\nTemporal scope of payouts_converted.csv: {start_date} - {end_date}")

    unique_install_ids, total_install_ids = count_install_ids(installs, "install_id")
    print(f"\nUnique Install IDs: {unique_install_ids}\nTotal Install IDs: {total_install_ids}")

    daily_payouts = calculate_daily_payouts(payouts)
    plot_moving_average(daily_payouts, window_size=7)

    plot_install_payout_deciles(payouts, "value_usd")


if __name__ == "__main__":
    payouts_file_path = "/Users/khaled/Downloads/data/payouts_converted.csv"
    installs_file_path = "/Users/khaled/Downloads/data/installs.csv"
    main(payouts_file_path, installs_file_path)
