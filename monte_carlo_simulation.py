import numpy as np
import random
import matplotlib.pyplot as plt
import time


def initialize_parameters():
    """
    Initializes the parameters used in the Monte Carlo simulation.

    Returns:
    initial_equity (float): the starting equity for each simulation
    loss_pct (float): the percentage loss incurred on a losing trade
    win_pct (float): the percentage gain earned on a winning trade
    win_rate (float): the probability of a trade being a winning trade
    number_of_trades (int): the number of trades in each simulation
    number_of_paths (int): the number of simulations to run
    sudden_error_interval_lower (int): the lower limit for the number of trades between sudden error events
    sudden_error_interval_upper (int): the upper limit for the number of trades between sudden error events
    sudden_error_upper (float): the upper limit for the percentage loss incurred on a sudden error event
    sudden_error_lower (float): the lower limit for the percentage loss incurred on a sudden error event
    sudden_convex_interval_lower (int): the lower limit for the number of trades between sudden convex profit events
    sudden_convex_interval_upper (int): the upper limit for the number of trades between sudden convex profit events
    convex_payoff_upper (float): the upper limit for the percentage gain earned on a sudden convex profit event
    convex_payoff_lower (float): the lower limit for the percentage gain earned on a sudden convex profit


    """
    initial_equity = 254075 + 62320
    loss_pct = 0.01
    win_pct = 0.0122
    win_rate = 0.3726
    number_of_trades = 400
    number_of_paths = 50

    # error parameters
    sudden_error_interval_lower = 40
    sudden_error_interval_upper = 80
    sudden_error_upper = 0.01
    sudden_error_lower = 0.01

    #  convex parameters
    sudden_convex_interval_lower = 80
    sudden_convex_interval_upper = 160
    convex_payoff_upper = 0.3
    convex_payoff_lower = 0.2

    print(f"Stats\nrrr: ", win_pct * 100, " to ", loss_pct * 100, "\nwin rate: ", win_rate, "%", "\nTrades num:",
          number_of_trades, "\nPaths/traders num: ", number_of_paths, "\n"f'Sudden error % (random range) from'
                                                                      f' {sudden_error_lower * 100}'  f' to {sudden_error_upper * 100}\nSudden convex profit % (random range) from'
                                                                      f' {convex_payoff_lower * 100} to {convex_payoff_upper * 100}\n')

    return initial_equity, loss_pct, win_pct, win_rate, number_of_trades, number_of_paths, \
        sudden_error_interval_lower, sudden_error_interval_upper, sudden_error_upper, sudden_error_lower, \
        sudden_convex_interval_lower, sudden_convex_interval_upper, convex_payoff_upper, convex_payoff_lower


def simulate_equity_curve(initial_equity, loss_pct, win_pct, win_rate, n_simulations,
                          sudden_error_interval_lower, sudden_error_interval_upper,
                          sudden_error_upper, sudden_error_lower,
                          sudden_convex_interval_lower, sudden_convex_interval_upper,
                          convex_payoff_upper, convex_payoff_lower):
    """
    Simulates the equity curve of a trading strategy with random sudden errors and convex profits.

    Args:
        All initialize parameters


    Returns:
        equity_array (numpy.ndarray): Array of equity values after each simulated trade.
    """
    equity_array = np.zeros(n_simulations)
    equity_array[0] = initial_equity
    equity_counter = initial_equity
    commissions_or_costs = -4

    sudden_error_interval = random.randint(sudden_error_interval_lower, sudden_error_interval_upper)
    sudden_convex_interval = random.randint(sudden_convex_interval_lower, sudden_convex_interval_upper)

    #  Loop through the number of trades to be simulated
    for i in range(1, n_simulations):
        # n: the number of Bernoulli trials
        # p: the probability of success in each trial
        win = np.random.binomial(1, win_rate, 1)

        if win:
            # Calculate the daily return for a successful trade
            daily_return = equity_counter * win_pct
        else:
            # Calculate the daily return for an unsuccessful trade
            daily_return = -equity_counter * loss_pct

        # Add the daily return and commissions/costs to the equity counter
        equity_counter += daily_return
        equity_counter += commissions_or_costs
        equity_array[i] = equity_counter

        # Introduce a random convex payoff with a random frequency
        if i % sudden_convex_interval == 0:
            # Generate a random convex payoff rate between random convex_payoff_lower, convex_payoff_upper
            convex_payoff_pct = np.random.uniform(convex_payoff_lower, convex_payoff_upper)
            convex_payoff_amount = equity_counter * convex_payoff_pct
            equity_counter += convex_payoff_amount

        # Introduce the sudden loss of a random percentage between random sudden_error_upper, sudden_error_lower
        if i % sudden_error_interval == 0:
            # Generate a random percentage loss between sudden_error_upper, sudden_error_lower
            sudden_loss_pct = np.random.uniform(sudden_error_upper, sudden_error_lower)
            sudden_loss = -equity_counter * sudden_loss_pct
            equity_counter += sudden_loss

        if equity_counter <= 0:
            break

    return equity_array


def run_simulations(initial_equity, loss_pct, win_pct, win_rate, number_of_trades, number_of_paths,
                    sudden_error_interval_lower, sudden_error_interval_upper,
                    sudden_error_upper, sudden_error_lower,
                    sudden_convex_interval_lower, sudden_convex_interval_upper,
                    convex_payoff_upper, convex_payoff_lower):
    # This function takes several parameters to simulate multiple equity curves for a given set of trading parameters.
    # It returns a list of equity curves of length number_of_trades for each path.

    all_paths_results = []

    for i in range(number_of_paths):
        result = simulate_equity_curve(initial_equity, loss_pct, win_pct, win_rate, number_of_trades,
                                       sudden_error_interval_lower, sudden_error_interval_upper,
                                       sudden_error_upper, sudden_error_lower,
                                       sudden_convex_interval_lower, sudden_convex_interval_upper,
                                       convex_payoff_upper, convex_payoff_lower)
        all_paths_results.append(result)

    return all_paths_results


def calculate_stats(all_paths_results, initial_equity, loss_pct, win_pct, win_rate, number_of_trades,
                    number_of_paths):
    # This function calculates statistics on multiple simulations results, including minimum, maximum,
    # and average equity, percentage above/below average equity, percentage of simulations that double
    # the initial equity, and the standard deviation of equity variation from the average.

    min_equity = np.min([result[-1] for result in all_paths_results])
    max_equity = np.max([result[-1] for result in all_paths_results])
    avg_equity = np.average([result[-1] for result in all_paths_results])

    n_above_avg = np.count_nonzero([result[-1] > avg_equity for result in all_paths_results])
    p_above_avg = round(n_above_avg / number_of_paths * 100, 2)
    p_below_avg = 100 - p_above_avg

    n_doubled = 0
    for result in all_paths_results:
        final_equity = result[-1]
        if final_equity >= 2 * initial_equity:
            n_doubled += 1
    p_doubled = round((n_doubled / number_of_paths) * 100, 2)

    variation_from_avg = [result[-1] - avg_equity for result in all_paths_results]
    std_dev = np.std(variation_from_avg)
    std_dev_round = round(std_dev, 2)

    return min_equity, max_equity, avg_equity, p_above_avg, p_below_avg, p_doubled, std_dev_round


def plot_equity_curves(all_paths_results, min_equity, max_equity, avg_equity, number_of_trades, number_of_paths):
    # This function plots the equity curves for multiple simulations and adds markers for the minimum, maximum,
    # and average equity. It also displays the values of the minimum, maximum, and average equity.

    plt.figure(figsize=(12, 8))
    for i in range(number_of_paths):
        plt.plot(all_paths_results[i], color=plt.cm.cool(i / number_of_paths), label="")

    plt.plot([0, number_of_trades - 1], [max_equity, max_equity], color='green', label="max")
    plt.plot([0, number_of_trades - 1], [avg_equity, avg_equity], color='blue', label="avg")
    plt.plot([0, number_of_trades - 1], [min_equity, min_equity], color='red', label="min")

    plt.text(0, min_equity, f'${min_equity:.0f}', fontsize="13")
    plt.text(0, max_equity, f'${max_equity:.0f}', fontsize="13")
    plt.text(0, avg_equity, f'${avg_equity:.0f}', fontsize="13")

    plt.title("JustDice Monte Carlo Simulation")
    plt.ylabel("$$$")
    plt.xlabel("Num of simulations")
    plt.savefig('Monte Carlo Simu paths.png', dpi=600, bbox_inches='tight')
    plt.show()


def plot_histogram(all_paths_results, number_of_paths):
    end_results = [result[-1] for result in all_paths_results]

    plt.figure(figsize=(12, 8))
    plt.hist(end_results, bins=150)
    plt.xlabel("$$$")
    plt.ylabel("Number of companies/traders")
    plt.title("Histogram of End Results")
    plt.savefig('Monte Carlo Simu Histogram of End Results.png', dpi=300, bbox_inches='tight')
    plt.show()


def calc_min_max_avg_equity(all_paths_results):
    min_equity = np.min([result[-1] for result in all_paths_results])
    max_equity = np.max([result[-1] for result in all_paths_results])
    avg_equity = np.average([result[-1] for result in all_paths_results])

    return round(min_equity, 2), round(avg_equity, 2), round(max_equity, 2)


def calc_probabilities(all_paths_results, avg_equity, n_paths):
    # thsi function calculates the probabilities of being above below average
    n_above_avg = np.count_nonzero([result[-1] > avg_equity for result in all_paths_results])
    p_above_avg = round(n_above_avg / n_paths * 100, 2)
    p_below_avg = 100 - p_above_avg

    return p_above_avg, p_below_avg


def calc_probability_doubling(all_paths_results, initial_equity, n_paths):
    # this function calculates the probability of doubling the initial equity

    n_doubled = 0
    for result in all_paths_results:
        final_equity = result[-1]
        if final_equity >= 2 * initial_equity:
            n_doubled += 1
    p_doubled = round((n_doubled / n_paths) * 100, 2)

    return p_doubled


def calc_std_dev_from_avg(all_paths_results, avg_equity):
    variation_from_avg = [result[-1] - avg_equity for result in all_paths_results]
    std_dev = np.std(variation_from_avg)
    std_dev_round = round(std_dev, 2)

    return std_dev_round


def monte_carlo_main():
    start_time = time.time()

    initial_equity, loss_pct, win_pct, win_rate, number_of_trades, number_of_paths, \
        sudden_error_interval_lower, sudden_error_interval_upper, sudden_error_upper, sudden_error_lower, \
        sudden_convex_interval_lower, sudden_convex_interval_upper, convex_payoff_upper, convex_payoff_lower \
        = initialize_parameters()

    all_paths_results = run_simulations(initial_equity, loss_pct, win_pct, win_rate, number_of_trades,
                                        number_of_paths, sudden_error_interval_lower, sudden_error_interval_upper,
                                        sudden_error_upper, sudden_error_lower, sudden_convex_interval_lower,
                                        sudden_convex_interval_upper, convex_payoff_upper, convex_payoff_lower)

    min_equity, max_equity, avg_equity, p_above_avg, p_below_avg, p_doubled, std_dev_round \
        = calculate_stats(all_paths_results, initial_equity, loss_pct, win_pct, win_rate, number_of_trades,
                          number_of_paths)

    plot_equity_curves(all_paths_results, min_equity, max_equity, avg_equity, number_of_trades, number_of_paths)

    plot_histogram(all_paths_results, number_of_paths)

    min_equity, avg_equity, max_equity = calc_min_max_avg_equity(all_paths_results)
    print("Min equity:", min_equity, "\nAvg equity:", avg_equity, "\nMax equity:", max_equity)

    p_above_avg, p_below_avg = calc_probabilities(all_paths_results, avg_equity, number_of_paths)
    print("\nProbability of above avg equity:", p_above_avg, "%")
    print("Probability of below avg equity:", p_below_avg, "%")

    p_doubled = calc_probability_doubling(all_paths_results, initial_equity, number_of_paths)
    print("Probability of doubling initial equity:", p_doubled, "%")

    elapsed_time = time.time() - start_time
    rounded_time = round(elapsed_time / 60, 2)
    print("Computation time: ", rounded_time, "minutes")

    std_dev_round = calc_std_dev_from_avg(all_paths_results, avg_equity)
    print("σ: One standard deviation of variation from average equity:", std_dev_round)


if __name__ == "__main__":
    monte_carlo_main()

