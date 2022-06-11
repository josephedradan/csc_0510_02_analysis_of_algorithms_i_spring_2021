"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 11/2/2020

Purpose:
    Given a list of costs where the indices + 1 represents the lengths corresponding to it's costs
    Find the Max Profit given a certain length

Details:

Description:

Notes:
    Faster than Dynamic programming because it uses math tricks rather than memory optimization tricks
    Uses Recursive calls so can it recursion depth (stack overflow)
    Has suboptimal algorithms that can be replaced with faster algorithms at the cost of readability

IMPORTANT NOTES:

Explanation:

Reference:
    Program to find LCM of two numbers
        https://www.geeksforgeeks.org/program-to-find-lcm-of-two-numbers/
"""
import functools

"""
GCD and LCM functions because i'm not writing them...

Python program to find LCM of two numbers
This code is contributed by Danish Raza
"""


# Recursive function to return gcd of a and b
def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


# Function to return LCM of two numbers
def lcm(a, b):
    return (a / gcd(a, b)) * b


def get_profit_max_list(list_cost):
    """
    Get the profit max list

    Notes:
        it's a list where the LOWEST number in the list is PRICE to profit max
        So the INDEX of that number is the length that YOU SHOULD SELL TO PROFIT MAX

    :param list_cost: list of costs
    :return:
    """

    # Indices of list cost
    indices = list(range(len(list_cost)))

    # Least common multiple of list_cost
    least_common_multiple = functools.reduce(lcm, list_cost)

    # List containing amount of times in order for the cost in list_cost to be the LCM
    list_multiple_of_cost_that_fit_in_lcm = [least_common_multiple / i for i in list_cost]

    # List of (indices + 1) * it's corresponding multiple to get to the LCM
    # Lowest value in the list's index + 1 is what you should sell at to max profit
    list_profit_max = [(index + 1) * multiple_of_cost_that_fit_in_lcm for index, multiple_of_cost_that_fit_in_lcm in
                       zip(indices, list_multiple_of_cost_that_fit_in_lcm)]

    print("\tList of the costs:", list_cost)
    print("\tLeast Common Multiple:", least_common_multiple)
    print("\tList of multiples of the cost to equal the LCM:", list_multiple_of_cost_that_fit_in_lcm)
    print("\tList of (indices + 1) * it's corresponding multiple to get to the LCM:", list_profit_max)
    print()
    return list_profit_max


def get_lowest_value_in_list_index(list_given):
    """
    Given a list, return the index of the value in the list that is the lowest value

    :param list_given:
    :return:
    """
    current_lowest_value = list_given[0]
    current_lowest_value_index = 0

    for i, value in enumerate(list_given):
        if value < current_lowest_value:
            current_lowest_value = value
            current_lowest_value_index = i

    return current_lowest_value_index


def calculate_list_of_lengths_you_should_sell_with_amount_of_money_you_would_make(list_cost,
                                                                                  target_amount_of_lengths_to_sell,
                                                                                  list_solution):
    """
    Calculate the amount of lengths you need to sell to maximize profit

    :param list_cost:
    :param target_amount_of_lengths_to_sell:
    :param list_solution:
    :return:
    """
    # List of the profit max (The lowest value in the list is what you should sell at to profit max)
    list_profit_max = get_profit_max_list(list_cost)

    # Index + 1 of the lowest value in List profit max
    index_of_lowest_value_in_list_plus_1 = get_lowest_value_in_list_index(list_profit_max) + 1

    # Length to sell to get the max profit
    length_to_sell_to_get_the_max_profit = index_of_lowest_value_in_list_plus_1

    # Amount of times the length needs to be sold to get max profit
    amount_of_times_length_fits_in_target_value = int(
        target_amount_of_lengths_to_sell / length_to_sell_to_get_the_max_profit)  # Floored

    # The remainder of the amount_of_times_length_fits_in_target_value
    remainder = target_amount_of_lengths_to_sell % length_to_sell_to_get_the_max_profit

    """
    Extend the solution list with a list
        [length_to_sell_to_get_the_max_profit] * the amount of times the length fits in the target lengths to sell
    """
    list_solution.extend([length_to_sell_to_get_the_max_profit] * amount_of_times_length_fits_in_target_value)

    print(f"Index + 1 of the value in the list to profit max: {length_to_sell_to_get_the_max_profit}")
    print(f"Amount of times the length at the profit max index "
          f"can fit in the Target amount of lengths to sell: {amount_of_times_length_fits_in_target_value}")
    print(f"Remainder since the profit max index did not fully "
          f"fit into the Target amount of lengths to sell: {remainder}")
    print(f"List of what lengths to sell to max profit based on the Target amount of lengths to sell: {list_solution}")
    print()

    # Stop function if the target_amount_of_lengths_to_sell is 0
    if remainder == 0:
        return

    # Make a copy of the list because we probably still want list_cost to not change (Can be unnecessary)
    list_cost_new = list_cost.copy()

    # Remove the current index_of_lowest_value_in_list_plus_1 AKA length_to_sell_to_get_the_max_profit
    list_cost_new = list_cost_new[:remainder]

    # Recursive call for (list_cost_new, remainder, list_solution)
    calculate_list_of_lengths_you_should_sell_with_amount_of_money_you_would_make(list_cost_new,
                                                                                  remainder,
                                                                                  list_solution)


if __name__ == '__main__':
    """
    Notice that INDEX 6 has VALUE 13 NOT 7 signifying that it is a relative profit max
    Notice that INDEX 12 has VALUE 23 NOT 12 signifying that it is the absolute profit max
    """
    list_cost = [1, 2, 3, 4, 5, 6, 13, 8, 9, 10, 11, 23, 13]

    # list_cost = [3, 5, 8, 1]
    list_cost = [4, 6, 2, 8]

    # The list of indices + 1 AKA lengths
    list_solutions = []

    target_lengths_to_sell = 14

    calculate_list_of_lengths_you_should_sell_with_amount_of_money_you_would_make(list_cost, target_lengths_to_sell,
                                                                                  list_solutions)

    dict_map_index_with_cost = {index: value for index, value in enumerate(list_cost)}

    # List of the profit
    list_profit = [dict_map_index_with_cost.get(i - 1) for i in list_solutions]

    print("-" * 100)
    print("Amount of lengths to sell (Target): {}".format(target_lengths_to_sell))
    print("List of Costs: {}".format(list_cost))
    print("List of Lengths to sell: {}".format(list_solutions))
    print("List of Profit corresponding to each length: {}".format(list_profit))
    print("Profit for the seller: {}".format(sum(list_profit)))
    print()

    # Graphing section
    import pandas as pd

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    columns = list_cost
    # columns = list(range(max(columns) + 1))
    # columns = [i if i in list_cost else 0 for i in range(max(list_cost))]

    rows = list(range(target_lengths_to_sell + 1))

    pd_df = pd.DataFrame(0, index=rows, columns=columns)

    for col_index, col_val in enumerate(columns):
        for row_index, row_val in enumerate(rows):
            list_solutions = []

            calculate_list_of_lengths_you_should_sell_with_amount_of_money_you_would_make(list_cost[:col_index + 1],
                                                                                          row_val,
                                                                                          list_solutions)

            dict_map_index_with_cost = {index: value for index, value in enumerate(list_cost)}

            # List of the profit
            list_profit = [dict_map_index_with_cost.get(i - 1) for i in list_solutions]

            pd_df.at[row_val, col_val] = sum(list_profit)


    print(pd_df)
    print()
    pd_df_new = pd_df.transpose()

    pd_df_new = pd_df_new.sort_index()

    pd_df_new = pd_df_new.transpose()
    print(pd_df_new)

    # print(columns)
    print("-" * 100)
    print("Amount of lengths to sell (Target): {}".format(target_lengths_to_sell))
    print("List of Costs: {}".format(list_cost))
    print("List of Lengths to sell: {}".format(list_solutions))
    print("List of Profit corresponding to each length: {}".format(list_profit))
    print("Profit for the seller: {}".format(sum(list_profit)))
    print()
