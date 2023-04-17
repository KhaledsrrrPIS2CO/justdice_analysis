from adspend_analysis import *

def analyze_adspend(file_path):
    get_adspend_temporal_scope(adspend_path)
    adspend = read_and_preprocess_data(file_path)
    adspend_by_country, adspend_by_network, adspend_by_client, adspend_by_date = analyze_adspend_data(adspend)
    print_preview_data(adspend, adspend_by_country, adspend_by_network, adspend_by_client, adspend_by_date)
    total_adspend = adspend_by_country.sum()
    plot_adspend_by_country(adspend_by_country, total_adspend)
    plot_adspend_over_time(adspend_by_date)
    plot_adspend_by_network(adspend_by_network, total_adspend)
    plot_adspend_by_client(adspend_by_client, total_adspend)
    plot_pareto_distribution_adspend_by_client(adspend_by_client)
    plot_adspend_by_country_log(adspend_by_country, total_adspend)
    plot_adspend_percentage_pareto(adspend_by_client)


# Call the analyze_adspend function with the file_path
adspend_path = '/Users/khaled/Downloads/data/adspend_converted.csv'
analyze_adspend(adspend_path)

print("_____")