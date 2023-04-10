import pandas as pd


def read_csv_files():
    adspend = pd.read_csv('adspend.csv')
    installs = pd.read_csv('installs.csv')
    payouts = pd.read_csv('payouts.csv')
    revenue = pd.read_csv('revenue.csv')
    return adspend, installs, payouts, revenue


def merge_datasets(adspend, installs, payouts, revenue):
    merged_data = pd.merge(installs, adspend, on=['event_date', 'country_id', 'network_id'], how='left')
    merged_data = pd.merge(merged_data, payouts, on=['install_id', 'event_date'], how='left', suffixes=('', '_payouts'))
    merged_data = pd.merge(merged_data, revenue, on=['install_id', 'event_date'], how='left', suffixes=('', '_revenue'))
    return merged_data


def clean_and_sort_data(merged_data):
    merged_data.sort_values(by='event_date', inplace=True)
    merged_data.rename(
        columns={'value_usd': 'ad_spend_usd', 'value_usd_payouts': 'payout_usd', 'value_usd_revenue': 'revenue_usd'},
        inplace=True)
    return merged_data


def main():
    adspend, installs, payouts, revenue = read_csv_files()
    merged_data = merge_datasets(adspend, installs, payouts, revenue)
    cleaned_data = clean_and_sort_data(merged_data)
    print(cleaned_data.head())


if __name__ == '__main__':
    main()
