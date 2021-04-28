"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 4/11/2021

Purpose:
    Solve CSC510 Analysis of Algorithms Algorithm Challenge 3: Dynamic Programming

Details:

Description:

Notes:
    Example
        Given a list of prices (in dollars) P = [9; 8; 5; 3] per len, where the (indexes + 1) of
        those prices represent the number of len, and the maximum profit for selling 3 len of wire.

        From the above data, we know that 1len = $9, 2len = $8, 3len = $5, and 4len = $3 Then, 3len of wire
        can be sold in any of the following ways:

        • 3len = $5
        • 1len + 2len = $9 + $8 = $17
        • 1len + 1len + 1len = $9 + $9 + $9 = $27

        Therefore you will get the maximum profit from 3 len of wire if you sell them in pieces of 1 len.

Question:
    (50 points) Given list of prices P = [p_1; p_2; p_3; ...; p_n] and a random number of len where
    0 < len <= n, create the algorithm to solve the problem using the following two approaches
    (including an educated guess of their time complexities)

    Solve for both Brute force and Dynamic Programming methods

Pseudocode
    dynamic_programming_math(list_price, amount_len_to_sell)

        list_tuple_p_l = get list of tuples containing price and length for price from list_price

        list_tuple_p_l_r = get list of tuples containing price, length, and ratio (length/price) from list_tuple_p_l

        ascending sort list_tuple_p_l_r by tuple's ratio
            if tuples have the same ratio
                 ascending sort tuples with the same ratio by tuple's length
        
        price_max = list_tuple_p_l_r[0]'s price

        length_of_price_max = list_tuple_p_l_r[0]'s length

        amount_length_max_sold = floor(amount_len_to_sell / length_of_price_max)

        amount_length_remainder = amount_len_to_sell - (length_of_price_max * amount_len_max_sold)

        list_tuple_p_l_r_sold = List contains "amount_length_max_sold" copies of list_tuple_p_l_r[0]

        profit_max = price_max * amount_len_max_sold

        while amount_length_remainder is > 0
            for every tuple in list_tuple_p_l_r
                if the tuple's length is <= amount_length_remainder
                    Add tuple to list_tuple_p_l_r_sold
                    amount_length_remainder -= tuple's price
                    profit_max += tuple's price
                    break

        return list_tuple_p_l_r_sold, profit_max


IMPORTANT NOTES:

Explanation:

Reference:

"""

from typing import List, Tuple, Union

FORMAT_PRINT_LIST = "{:<10}{:<10}{:<10}"
FORMAT_PRINT = "Amount of length to sell: {}\nMax Profit: {}\n"


def get_list_tuple_price_len_ratio_sorted(list_tuple_price_len: List[Tuple[int, int]]) -> List[Tuple[int, int, float]]:
    """
    Sort list_price_len_ratio by ratio (len/price) in ascending order and if the ratios are the same then sort by
    len in ascending order. The reason to sort by ratio (len/price) in ascending order is because the lowest ratio
    maximizes profit and the reason to sort by len in ascending order is because you want to sell the least amount of
    length at the highest price so you can sell more length, presumably, at that same price.

    Complexity:
        Standard Time complexity:
            Worst case:
                O(n*log(n))
            Notes:
                Python uses Timsort


    :param list_tuple_price_len: list containing a tuple with price and len in that order
    :return:  list_info List containing tuple in price, len, ratio (len/price) order
    """
    list_info = [(price, len, len / price) for price, len in list_tuple_price_len]

    list_info.sort(key=lambda i: (i[2], i[1]))

    return list_info


def get_list_tuple_price_len(list_price: List[int]) -> List[Tuple[int, int]]:
    """
    Get a list containing a tuple of price and len in that order

    Complexity:
        Standard Time complexity:
            Theta
                Theta(n)

    :param list_price: list containing prices
    :return: list_tuple_len_price
    """
    list_tuple_len_price = []

    for i, price in enumerate(list_price):
        list_tuple_len_price.append((price, i + 1))

    return list_tuple_len_price


def dynamic_programming_math(list_tuple_price: List[int], amount_len_to_sell: int):
    """
    Math method to maximize profit when selling lengths at a given prices

    Complexity:
        Standard Time complexity:
            Worst case:
                O( n + n*log(n) + m*n )

            Notes:
                get_list_price_len +
                get_list_price_len_ratio_sorted() +
                m*n (from this file)

                m is the amount iterations until the remainder == 0
                Excludes print time complexity

        Optimal Time complexity:
            Worst case:
                O( n*log(n) + m*n )

            Notes:
                get_list_price_len_ratio_sorted()
                m*n (from this file)

                m is the amount iterations until the remainder == 0
                This method removes get_list_price_len and uses the index instead

    :param list_tuple_price:
    :param amount_len_to_sell:
    :return:
    """
    """
    List containing tuple of price and len
    Ignore this time complexity of Theta(n) and assume using index for Optimal Time complexity.
    """
    list_tuple_price_len = get_list_tuple_price_len(list_tuple_price)

    # List containing tuple of price, len, ratio (len/price).
    list_tuple_price_len_ratio = get_list_tuple_price_len_ratio_sorted(list_tuple_price_len)

    # Price maximized
    price_max = list_tuple_price_len_ratio[0][0]

    # Length for price maximized
    len_max = list_tuple_price_len_ratio[0][1]

    # Amount of len_max sold
    amount_len_max_sold = amount_len_to_sell // len_max

    # Amount of len remaining to sell
    amount_len_to_sell_remainder = amount_len_to_sell - (len_max * amount_len_max_sold)

    # List containing tuple of price, len, ratio (len/price) to sell length
    list_tuple_price_len_ratio_sell = [list_tuple_price_len_ratio[0]] * amount_len_max_sold

    # Profit max
    profit_max = price_max * amount_len_max_sold

    # Loop to exhaust amount_len_to_sell_remainder to 0
    while amount_len_to_sell_remainder > 0:

        """
        Loop over List containing tuple of price, len, ratio (len/price) 
        This will select the next lowest ratio because it is already sorted in that order
        """
        for info in list_tuple_price_len_ratio:

            # Check if length is <= amount_len_to_sell_remainder
            if info[1] <= amount_len_to_sell_remainder:
                list_tuple_price_len_ratio_sell.append(info)  # Append info
                amount_len_to_sell_remainder -= info[1]  # Subtract length from amount_len_to_sell_remainder
                profit_max += info[0]  # Add to max profit
                break  # Prevent other prices to modify the remainder

    # Printing zone (Ignore time complexity of this as it's unrelated to the algorithm)
    print(FORMAT_PRINT.format(amount_len_to_sell, profit_max))

    print("Lengths to sell:")
    print(FORMAT_PRINT_LIST.format("Price", "Length", "Ratio"))
    for i in list_tuple_price_len_ratio_sell:
        print(FORMAT_PRINT_LIST.format(i[0], i[1], "{:.5f}".format(i[2])))

    return list_tuple_price_len_ratio_sell, profit_max


def get_list_tuple_len_price_max(list_tuple_price_len: List[Tuple[int, int]],
                                 amount_len_to_sell: int = None) -> List[Tuple[int, int, int]]:
    """
    Given the list of tuples containing price and length, create a list of lengths its max profit and
    create a list of tuples of price and it's corresponding length that will lead to max profits.
    This is the body of the dynamic programming solution.

    Notes:
        Cannot do sell order here because it requires the amount length to sell.

    Complexity:
        Standard Time complexity:
            Worst case:
                O( n^2 )

        Standard Space complexity:
            Worst case:
                O( 2n )

    :param amount_len_to_sell: Amount of the length to sell, it will change in this function
    :param list_tuple_price_len:
    :return:
    """

    # List tuple of length and max profit
    list_tuple_len_profit_max = []

    # List tuple of price and length to sell length (The lengths to sell to lead to max profit)
    # list_tuple_price_len_sell = []

    # Current iteration abs price max for a length and the length itself
    # price_max_abs = 0
    # len_price_max_abs = 0

    # Is the length that set len_price_max_abs
    len_price_max_local = 0

    for index_upper_bound, tuple_price_len in enumerate(list_tuple_price_len):

        price_iter_current = tuple_price_len[0]
        len_iter_current = tuple_price_len[1]

        # Current iteration's price max based on the list of tuples containing the length and the max profit 
        price_solution_sub_max = 0

        # Loop over the list containing the tuple of length and max profit for that length
        for index, tuple_len_price_max in enumerate(list_tuple_len_profit_max):

            # Length representing this loop's tuple
            len_inner = tuple_len_price_max[0]

            # Max price representing this loop's tuple
            price_inner = tuple_len_price_max[1]

            # len based on the difference between len_iter_current and len_inner
            len_diff = len_iter_current - len_inner

            # Index representing the length for len_diff
            index_len_diff = len_diff - 1

            # Price based on index_len_diff
            price_len_diff = list_tuple_price_len[index_len_diff][0]

            # Possible max price for len_iter_current
            price_max_solution_sub_possible = price_inner + price_len_diff

            # Check if price_max_solution_sub_possible is > price_solution_sub_max
            if price_max_solution_sub_possible > price_solution_sub_max:
                # Replace max price for sub solution
                price_solution_sub_max = price_max_solution_sub_possible

                # Update price max and len for that price max
                # price_max_abs = price_len_diff
                # len_price_max_abs = len_diff
                len_price_max_local = len_diff

        # Check if the current iteration price is > price_solution_sub_max
        if price_iter_current > price_solution_sub_max:
            # Replace max price for sub solution
            price_solution_sub_max = price_iter_current

            # Update price max and len for that price max
            # price_max_abs = price_iter_current
            # len_price_max_abs = len_iter_current
            len_price_max_local = len_iter_current

        # Add tuple len, profit to list of tuple len, max profit
        list_tuple_len_profit_max.append((len_iter_current, price_solution_sub_max, len_price_max_local))

        # Update remaining length to sell
        # amount_len_to_sell -= len_price_max_local
        # print(amount_len_to_sell)

        """
        If amount_len_to_sell results into 0, then the list of lengths to get to amount_len_to_sell is 
        complete and max profit has been achieved.
        """
        # if amount_len_to_sell >= 0:
        #     # Append tuple price, len to list_tuple_price_len_sell
        #     list_tuple_price_len_sell.append((price_max_abs, len_price_max_abs))
        #     pass

    # return list_tuple_len_profit_max, list_tuple_price_len_sell
    return list_tuple_len_profit_max


def dynamic_programming(list_price: List[int], amount_len_to_sell: int):
    """
    Use the previous max sub solution to solve for the current max sub solution to get the
    max complete solution.

    Notes:
        This is a unique case were the max sub solutions lead to the max complete solution

    Complexity:
        Standard Time complexity:
            Worst case:
                O( n + n^2 )

        Optimal Time complexity:
            Worst case:
                O( n^2 )

            Notes:
                Remove n due to get_list_price_len and instead uses the index

    :param list_price:
    :param amount_len_to_sell:
    :return:
    """
    if amount_len_to_sell < 1:
        print("Cannot sell 0 length")
        exit()

    if amount_len_to_sell > len(list_price):
        print("Does not follow rule: 0 < length <= n")
        exit()

    # List containing tuple of price, len
    list_tuple_price_len = get_list_tuple_price_len(list_price)

    list_tuple_len_profit_max = get_list_tuple_len_price_max(list_tuple_price_len,
                                                             amount_len_to_sell)

    list_tuple_price_len_sell = []

    amount_len_to_sell_temp = amount_len_to_sell

    while amount_len_to_sell_temp > 0:
        length = list_tuple_len_profit_max[amount_len_to_sell_temp - 1][2]
        price = list_price[length - 1]
        list_tuple_price_len_sell.append((price, length))
        amount_len_to_sell_temp -= length

    print("Max Profit Table: Length, Profit")
    print(FORMAT_PRINT_LIST.format("Len Max", "Profit", "Length"))
    for i in list_tuple_len_profit_max:
        print(FORMAT_PRINT_LIST.format(i[0], i[1], i[2]))
    print()

    profit_max = list_tuple_len_profit_max[amount_len_to_sell - 1][1]

    print(FORMAT_PRINT.format(amount_len_to_sell, profit_max))

    print("Lengths to sell:")
    print(FORMAT_PRINT_LIST.format("Price", "Length", ""))
    for i in list_tuple_price_len_sell:
        print(FORMAT_PRINT_LIST.format(i[0], i[1], ""))


def brute_force_dfs(list_price: List[int],
                    amount_len_to_sell: int,
                    sum_temp: Union[int, None] = None,
                    list_length_temp: Union[List[int], None] = None,
                    list_solution: Union[Tuple[List[int], int], None] = None,
                    list_solution_max: Union[Tuple[List[int], int], None] = None):
    """
    DFS to find every possible combination of lengths regardless of the order of lengths

    Complexity:
        Standard Time complexity:
            Worst case:
                O( n^2 + m*n )

            Notes:
                m is the amount of times to copy a solution into list_solution

    :param list_price: list of prices
    :param amount_len_to_sell: Amount of the length to sell
    :param sum_temp: Sum of a solution
    :param list_length_temp: Temp list containing lengths
    :param list_solution: List of solutions
    :param list_solution_max: List that contains 1 solution which is the max solution
    :return: list_solution, list_solution_max
    """
    # Resetter (Allows for multiple uses of this function unrelated to the algorithm)
    if list_solution is None:
        list_solution = []
        sum_temp = 0
        list_length_temp = []
        list_solution_max = []

    # Check if amount_len_to_sell is 0
    if amount_len_to_sell <= 0:

        # Create a solution (Copy of list_length_temp, sum of the prices based on the lengths)
        solution = (list_length_temp.copy(), sum_temp)

        # Append solution to list of solutions
        list_solution.append(solution)

        # Initialize max solution
        if not list_solution_max:
            list_solution_max.append(solution)

        # Replace current max solution with new max solution
        elif solution[1] > list_solution_max[0][1]:
            list_solution_max[0] = solution

        return

    # Loop through list of prices
    for index, price in enumerate(list_price):
        # Calculate length from index
        length = index + 1

        # Add length to list_length_temp
        list_length_temp.append(length)

        # Calculate new amount_len_to_sell_new
        amount_len_to_sell_new = amount_len_to_sell - length

        # Only recursive call when amount_len_to_sell_new >= 0
        if amount_len_to_sell_new >= 0:
            brute_force_dfs(list_price,
                            amount_len_to_sell_new,
                            sum_temp + price,
                            list_length_temp,
                            list_solution,
                            list_solution_max)

        # Pop most recently added length to list_length_temp
        list_length_temp.pop()

    return list_solution, list_solution_max


def handler_brute_force_dfs(list_price: List[int], amount_len_to_sell: int):
    """
    Print handler for the brute_force_dfs

    :param list_price:
    :param amount_len_to_sell:
    :return:
    """
    list_solution, list_solution_max = brute_force_dfs(list_price, amount_len_to_sell)

    print("DFS all possible solutions")
    for i in list_solution:
        print(i)
    print()

    print(FORMAT_PRINT.format(amount_len_to_sell, list_solution_max[0][1]))

    print("lengths to sell:")
    print(FORMAT_PRINT_LIST.format("Price", "Length", ""))
    for length in list_solution_max[0][0]:
        print(FORMAT_PRINT_LIST.format(list_price[length - 1], length, ""))


if __name__ == '__main__':
    list_price = [1, 2, 3, 4, 5, 6, 13, 8, 9, 10, 11, 23, 13]
    # list_price = [9, 8, 5, 3]
    list_price = [9, 19, 5, 3]

    # amount_len_to_sell = len(list_price)
    amount_len_to_sell = 3

    print()
    print(f"List of prices: {list_price}")
    print(f"Amount of length to sell: {amount_len_to_sell}")
    print(f"\n{'-' * 100}\n")

    print("Dynamic Programming Math method:")
    dynamic_programming_math(list_price, amount_len_to_sell)
    print(f"\n{'-' * 100}\n")

    print("Dynamic Programming method:")
    dynamic_programming(list_price, amount_len_to_sell)
    print(f"\n{'-' * 100}\n")

    print("Brute Force DFS method:")
    handler_brute_force_dfs(list_price, amount_len_to_sell)
