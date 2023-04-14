import pandas as pd


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


def calculate_return_on_ad_spend(adspend_csv, revenue_csv):
    # Read the CSV files into DataFrames
    adspend_df = pd.read_csv(adspend_csv)
    revenue_df = pd.read_csv(revenue_csv)

    # Calculate the total ad spend and the total revenue
    total_ad_spend = adspend_df['value_usd'].sum()
    total_revenue = revenue_df['value_usd'].sum()

    # Calculate the ROAS
    return_on_ad_spend = total_revenue / total_ad_spend

    return return_on_ad_spend


def calculate_profit_margin(revenue_csv, adspend_csv, payouts_csv):
    # Read the CSV files into DataFrames
    revenue_df = pd.read_csv(revenue_csv)
    adspend_df = pd.read_csv(adspend_csv)
    payouts_df = pd.read_csv(payouts_csv)

    # Calculate the total revenue
    total_revenue = revenue_df['value_usd'].sum()
    print(total_revenue)

    # Calculate the total ad spend
    total_ad_spend = adspend_df['value_usd'].sum()
    print(total_ad_spend)

    # Calculate the total payout amount
    total_payout = payouts_df['value_usd'].sum()
    print(total_payout)

    # Calculate the profit margin
    profit_margin = (total_revenue - total_ad_spend - total_payout) / total_revenue

    return profit_margin


def main():
    # Set the paths to the CSV files
    installs_path = '/Users/khaled/Downloads/data/installs.csv'
    revenue_path = '/Users/khaled/Downloads/data/revenue_converted.csv'
    adspend_path = '/Users/khaled/Downloads/data/adspend_converted.csv'
    payouts_path = "/Users/khaled/Downloads/data/payouts_converted.csv"

    # Calculate the UAC
    user_acquisition_cost = calculate_user_acquisition_cost(adspend_path, installs_path)
    print('User Acquisition Cost (UAC):', round(user_acquisition_cost, 2))

    # Calculate the ARPU
    average_revenue_per_user = calculate_average_revenue_per_user(installs_path, revenue_path)
    print('Average Revenue per User (ARPU):', round(average_revenue_per_user, 2))

    # Calculate the APPU
    average_payout_per_user = calculate_average_payout_per_user(installs_path, payouts_path)
    print('Average Payout per User (APPU):', round(average_payout_per_user, 2))

    # Calculate the ROAS
    return_on_ad_spend = calculate_return_on_ad_spend(adspend_path, revenue_path)
    print('Return on Ad Spend (ROAS):', round(return_on_ad_spend, 2))

    # Calculate the profit margin
    profit_margin = calculate_profit_margin(revenue_path, adspend_path, payouts_path)
    print('Profit Margin:', round(profit_margin, 2) * 100, "%")


if __name__ == '__main__':
    main()
