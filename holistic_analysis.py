import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def calculate_user_acquisition_cost(adspend_csv, installs_csv):
    # Read the CSV files
    adspend_df = pd.read_csv(adspend_csv)
    installs_df = pd.read_csv(installs_csv)

    # Calculate the total ad spend
    total_ad_spend = adspend_df['value_usd'].sum()

    # Calculate the total number of installs
    total_installs = installs_df['install_id'].nunique()

    # Calculate the User Acquisition Cost
    user_acquisition_cost = total_ad_spend / total_installs

    return user_acquisition_cost


def calculate_average_revenue_per_user(installs_csv, revenue_csv):
    # Read the CSV files into DataFrames
    installs_df = pd.read_csv(installs_csv)
    revenue_df = pd.read_csv(revenue_csv)

    # Merge the installs and revenue DataFrames on the 'install_id' column
    merged_df = pd.merge(installs_df, revenue_df, on='install_id')

    # Calculate the total revenue and the number of unique users
    total_revenue = merged_df['value_usd'].sum()
    unique_users = merged_df['install_id'].nunique()

    # Calculate the ARPU
    average_revenue_per_user = total_revenue / unique_users

    return average_revenue_per_user


def calculate_average_payout_per_user(installs_csv, payouts_csv):
    # Read the CSV files into DataFrames
    installs_df = pd.read_csv(installs_csv)
    payouts_df = pd.read_csv(payouts_csv)

    # Merge the installs and payouts DataFrames on the 'install_id' column
    merged_df = pd.merge(installs_df, payouts_df, on='install_id')

    # Calculate the total payout amount and the number of unique users
    total_payout = merged_df['value_usd'].sum()
    unique_users = merged_df['install_id'].nunique()

    # Calculate the APPU
    appu = total_payout / unique_users

    return appu


# this is nonsense  I got the formula form Hubspot
# def calculate_marketing_roi(adspend_csv, installs_csv, revenue_csv, conversion_pct):
#     adspend = pd.read_csv(adspend_csv)
#     installs = pd.read_csv(installs_csv)
#     revenue = pd.read_csv(revenue_csv)
#
#     leads_num = len(installs)
#
#     installs_with_revenue = installs.merge(revenue, on='install_id', suffixes=('', '_revenue'))
#
#     # Filter installs with revenue greater than 0 USD
#     installs_with_revenue = installs_with_revenue[installs_with_revenue['value_usd'] > 0]
#
#     lead_to_customer_rate = conversion_pct
#
#     average_sales_price = revenue['value_usd'].mean()
#
#     total_ad_spend = adspend['value_usd'].sum()
#
#     marketing_roi = (((leads_num * lead_to_customer_rate * average_sales_price) - total_ad_spend) / total_ad_spend) * 100
#
#     return marketing_roi


def conversion_rate(installs_csv, revenue_csv):
    """
    Calculate the conversion rate based on installs and revenue, considering only installs with revenue greater than zero.

    Args:
    installs_csv (str): The path to the CSV file containing installs data.
    revenue_csv (str): The path to the CSV file containing revenue data.

    Returns:
    float: The conversion rate as a percentage.
    """

    installs = pd.read_csv(installs_csv).drop_duplicates(subset='install_id', keep='first')
    revenue = pd.read_csv(revenue_csv).drop_duplicates(subset='install_id', keep='first')

    total_leads = len(installs)
    installs_with_revenue = installs.merge(revenue[revenue['value_usd'] > 0], on='install_id',
                                           suffixes=('', '_revenue'))
    total_conversions = len(installs_with_revenue)

    conversion_pct = (total_conversions / total_leads) * 100

    return conversion_pct


def calculate_gross_profit_margin(revenue_csv, adspend_csv, payouts_csv):
    # Read the CSV files into DataFrames
    revenue_df = pd.read_csv(revenue_csv)
    adspend_df = pd.read_csv(adspend_csv)
    payouts_df = pd.read_csv(payouts_csv)

    # Calculate the total revenue
    total_revenue = revenue_df['value_usd'].sum()

    # Calculate the total ad spend
    total_ad_spend = adspend_df['value_usd'].sum()

    # Calculate the total payout amount
    total_payout = payouts_df['value_usd'].sum()

    # Calculate the profit margin
    profit_margin = (total_revenue - total_ad_spend - total_payout) / total_revenue

    return profit_margin


def plot_time_series(installs_path, revenue_path, adspend_path, payouts_path):
    # Read CSV files
    installs_df = pd.read_csv(installs_path, parse_dates=['event_date'])
    revenue_df = pd.read_csv(revenue_path, parse_dates=['event_date'])
    adspend_df = pd.read_csv(adspend_path, parse_dates=['event_date'])
    payouts_df = pd.read_csv(payouts_path, parse_dates=['event_date'])

    # Calculate total value per month
    # For installs, create a 'month' column, group by month, and count the number of installs per month
    installs_df['month'] = installs_df['event_date'].dt.to_period('M')
    installs_monthly = installs_df.groupby('month').size()

    # For revenue, create a 'month' column, group by month, and sum the value_usd per month
    revenue_df['month'] = revenue_df['event_date'].dt.to_period('M')
    revenue_monthly = revenue_df.groupby('month')['value_usd'].sum()

    # For adspend, create a 'month' column, group by month, and sum the value_usd per month
    adspend_df['month'] = adspend_df['event_date'].dt.to_period('M')
    adspend_monthly = adspend_df.groupby('month')['value_usd'].sum()

    # For payouts, create a 'month' column, group by month, and sum the value_usd per month
    payouts_df['month'] = payouts_df['event_date'].dt.to_period('M')
    payouts_monthly = payouts_df.groupby('month')['value_usd'].sum()

    # Calculate percentage change
    installs_pct = installs_monthly.pct_change()
    revenue_pct = revenue_monthly.pct_change()
    adspend_pct = adspend_monthly.pct_change()
    payouts_pct = payouts_monthly.pct_change()

    # Convert Period objects to Timestamp objects
    installs_pct.index = installs_pct.index.to_timestamp()
    revenue_pct.index = revenue_pct.index.to_timestamp()
    adspend_pct.index = adspend_pct.index.to_timestamp()
    payouts_pct.index = payouts_pct.index.to_timestamp()

    # Plot time series
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    plt.plot(installs_pct, label="Installs", marker='o', linestyle='--')
    plt.plot(revenue_pct, label="Revenue", marker='o', color='green')
    plt.plot(adspend_pct, label="Adspend", marker='o', color='red')
    plt.plot(payouts_pct, label="Payouts", marker='o', linestyle='dotted')
    plt.xlabel("")
    plt.ylabel("Percentage Change")
    plt.title("Holistic Time Series Analysis")

    # Change x-axis labels to show month name and year in text
    plt.xticks(revenue_pct.index, revenue_pct.index.strftime('%b %Y'), rotation=45, ha='right')

    plt.legend()
    plt.tight_layout()
    plt.savefig('Holistic Time Series.png', dpi=600, bbox_inches='tight')
    plt.show()


def calculate_risk_to_reward(user_acquisition_cost, average_revenue_per_user, average_payout_per_user):
    # Calculate Install ID cost
    install_id_cost = average_payout_per_user + user_acquisition_cost

    # Calculate Risk-to-Reward ratio
    risk_to_reward = average_revenue_per_user / install_id_cost

    return risk_to_reward


def holistic_main():
    # Set the paths to the CSV files
    installs_path = "data/installs.csv"
    revenue_path = "data/revenue_converted.csv"
    adspend_path = "data/adspend_converted.csv"
    payouts_path = "data/payouts_converted.csv"

    # Calculate the ARPU
    average_revenue_per_user = calculate_average_revenue_per_user(installs_path, revenue_path)
    print('Average Revenue per User (ARPU): $', round(average_revenue_per_user, 2))

    # Calculate the UAC
    user_acquisition_cost = calculate_user_acquisition_cost(adspend_path, installs_path)
    print('User Acquisition Cost (UAC/CPL): $', round(user_acquisition_cost, 2))

    # Calculate the APPU
    average_payout_per_user = calculate_average_payout_per_user(installs_path, payouts_path)
    print('Average Payout per User (APPU): $', round(average_payout_per_user, 2))

    conversion_rate_pct = conversion_rate(installs_path, revenue_path)
    print(f"Conversion Rate: {round(conversion_rate_pct, 2)}%")

    # # Call the function calculate_marketing_roi
    # roi = calculate_marketing_roi(adspend_path, installs_path, revenue_path, conversion_rate_pct)
    # print(f"Marketing ROI: {roi:.2f}%")

    # Calculate the profit margin
    profit_margin = calculate_gross_profit_margin(revenue_path, adspend_path, payouts_path)
    print('Gross Profit Margin:', round(profit_margin, 2) * 100, "%")

    # Plot plot_time_series
    plot_time_series(installs_path, revenue_path, adspend_path, payouts_path)

    risk_to_reward = calculate_risk_to_reward(user_acquisition_cost, average_revenue_per_user, average_payout_per_user)
    print(f"Risk-to-Reward ratio: {risk_to_reward:.2f}:1")


if __name__ == '__main__':
    holistic_main()
