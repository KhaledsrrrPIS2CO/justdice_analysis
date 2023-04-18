# main.py

# Import the required functions from their respective modules
from data_check import data_check_main
from adspend_analysis import adspend_main
from holistic_analysis import holistic_main
from installs_analysis import installs_main
from payouts_analysis import payouts_main
from revenue_analysis import revenue_main
from monte_carlo_simulation import monte_carlo_main


def main():
    """
    This function calls the main analysis functions for each of the following:
    - Ad spend
    - Monte carlo simulation
    - Data Check
    - Holistic analysis
    - Installs
    - Payouts
    - Revenue

    It serves as the entry point for the entire analysis pipeline.
    """
    # Call the main data check function for data_check.py
    print("===== Data Check =====")
    data_check_main()
    print("\n")

    # Call the main analysis function for holistic analysis
    print("===== Holistic Analysis =====")
    holistic_main()
    print("\n")

    # Call the main analysis function for revenue
    print("===== Monte Carlo Simulation =====")
    monte_carlo_main()
    print("\n")

    # Call the main analysis function for ad spend
    print("===== Ad Spend Analysis =====")
    adspend_file_path = "data/adspend_converted.csv"
    adspend_main(adspend_file_path)
    print("\n")

    # Call the main analysis function for installs
    print("===== Installs Analysis =====")

    installs_file_path = "data/installs.csv"
    installs_main(installs_file_path)
    print("\n")

    # Call the main analysis function for payouts
    print("===== Payouts Analysis =====")
    payouts_file_path = "data/payouts_converted.csv"
    payouts_main(payouts_file_path)
    print("\n")

    # Call the main analysis function for revenue
    print("===== Revenue Analysis =====")
    revenue_main()
    print("\n")


# Entry point of the script
if __name__ == "__main__":
    # Call the main function to start the analysis pipeline
    main()
