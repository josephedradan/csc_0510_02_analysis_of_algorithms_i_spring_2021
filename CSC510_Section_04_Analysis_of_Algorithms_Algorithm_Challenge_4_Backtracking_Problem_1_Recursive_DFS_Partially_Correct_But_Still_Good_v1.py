"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 11/16/2020

Purpose:
    Solve sum of values from each rows of a matrix to equal a target value with recursive calls

Details:

Description:

Notes:

IMPORTANT NOTES:
    This is not the correct solution, because it does not hit the criteria of the question.
    The real solution is close to a Hamiltonian path.

Explanation:

Reference:

"""
from collections import defaultdict

# from josephs_resources.decorators.v1.callgraph_simple import callgraph, create_callgraph
from typing import List, Dict, Tuple


# Recursive call
# @callgraph
def dfs_recursive(list_list_given: List[List[int]], target: int, index_row: int = 0,
                  solution_possible: List[int] = None,
                  list_solution: List[List[int]] = None) -> List[List[int]]:
    """
    Recursive DFS to take 1 value from each row of the matrix and make them equal the target value

    :param list_list_given: Matrix
    :param target: Target value to achieve
    :param index_row: Current row via index in the matrix
    :param solution_possible: A Partial or Full Solution whose sum equals the target value
    :param list_solution: List of Full solutions to equal the target (IT IS NOT UNIQUE)
    :return: List of solutions that equal the target (list_solution)
    """
    # Allows for resets for new calls from the initial call
    if list_solution is None:
        list_solution = []
        solution_possible = []

    # Current row you are working on
    row_current = list_list_given[index_row]

    # Loop through the values of the given row based on index_row
    for value in row_current:

        # New target value
        target -= value

        # Add value from the current row to the list of possible solutions
        solution_possible.append(value)

        # DEBUG PRINTING
        # print("Row: {}".format(row_current))
        # print("Partial: {}".format(list_solution_possible))
        # print("Target: {}".format(target))
        # print("Row Index: {}".format(index_row))
        # print()

        # Found solution is when target == 0
        if target == 0:
            # If solution is found then add it to list of solutions
            list_solution.append(solution_possible.copy())

            # Remove last value from list_solution_possible
            # (Uncommenting the below will stop after the first instance of the solution of a row which is wrong)
            # list_solution_possible.pop(-1)
            # return

        # If not on the last index of matrix, then do a recursive call
        if index_row < len(list_list_given) - 1:
            # Recursive call
            dfs_recursive(list_list_given, target, index_row + 1, solution_possible, list_solution)

        """
        When done after doing stuff with solution_possible.append(value) remove that value from solution_possible and
        return target to its original value before its change in this for loop
        """
        target += solution_possible.pop(-1)

    # Return list_solution
    return list_solution


# IGNORE The below (it's A possible solution using Algorithm X's style of solving)
"""
Index Value
0: 3, 6
1: 5, 3 ,2
2: 6, 2, 1
3: 1, 5, 0

# Value space is not needed 
Value Index 
0: 3
1: 2, 3
2: 1, 2
3: 0, 1
5: 1, 3
6: 0, 2
"""


# NOT USED
def get_dict_index_value_space(list_solution_given: List[List[int]]) -> Dict[int, list]:
    """
    Given a list of solutions, convert a solution to (Key) index (Value) value space

    :param list_solution_given: the result of dfs_recursive() call (list_solution)
    :return: dict where the Key is the index of the value of a solution and Value is a list of those values
    """

    # Default dict because why not
    dict_temp = defaultdict(list)

    # For solution in list_solution_given
    for solution in list_solution_given:

        # Enumerate through the solution
        for index, value in enumerate(solution):
            dict_temp[index].append(value)

    # Return the dict
    return dict_temp


def dfs_recursive_algorithm_x_cover_set_style_solutions_partitioned_solver(
        list_solution_given: List[List[int]],
        list_solution_possible: List[List[int]] = None,
        list_list_solution: List[List[List[int]]] = None):
    """
    Recursive DFS call to find all Partitioned Solutions of the given list of all solutions.

    Basically, you give the list of all the solutions, then find a combination of those solutions where the values in
    each solution in the combination DO NOT USE the same VALUES in the same INDICES of each other.

    :param list_solution_given: list_solution_given: the result of dfs_recursive call (list_solution)
    :param list_solution_possible: a combination of solutions from list_solution_given (solution partitioned)
    :param list_list_solution: list of (solution partitioned) where each solution is a list of the partitioned solutions
    from list_solution_given.
    :return: list of (solution partitioned) where each solution is a list of the partitioned solutions from
    list_solution_given.
    """

    """
    Copy the list so you don't modify the original since your going to constantly modify this variable many times.
    It is possible to do a delete and restore via dictionary rather than copying the entire matrix
    """
    list_solution_given = list_solution_given.copy()

    # DEBUG PRINTING
    # print(list_list_given)
    # print(list_solution_possible)
    # print(list_solution)
    # print()

    # Allows for resets for new calls
    if list_list_solution is None:
        list_list_solution = []
        list_solution_possible = []

    # Select row from list list given
    for row_selected in list_solution_given:

        # Add that row as a possible partition for a solution
        list_solution_possible.append(row_selected)

        """
        New list of list_list_given because the row selected should eliminate lists with duplicate items as row_selected
        """
        list_list_given_new = []

        # Eliminate rows with duplicate items as row_selected
        for list_given in list_solution_given:

            """
            Because you can have different sizes of partitions, you need to be limited by the smallest length list
            """
            length_min = len(row_selected)
            length_list_given = len(list_given)

            if len(list_given) < length_min:
                length_min = length_list_given

            # A Row is valid if they don't have the same items given the index
            valid = True

            # Loop to check the values in the row_selected are the same as the values in th list_given
            for index in range(length_min):

                # If values match, then the given list_given cannot be used
                if row_selected[index] == list_given[index]:
                    valid = False
                    break

            # If list_given is valid then add that list to list_list_given_new
            if valid:
                list_list_given_new.append(list_given)

        # If list_list_given_new is empty then the existing list_solution_possible is a possible solution
        if not list_list_given_new:
            # Add a copy of list_solution_possible to the list of solutions
            list_list_solution.append(list_solution_possible.copy())

            # Because you are still in a loop you still need to check for the other row_selected in list_list_given
            list_solution_possible.pop(-1)

        else:
            """
            Recursive call when the list_list_given_new IS NOT EMPTY to prevent unnecessary calls on an empty 
            list_list_given_new
            """
            dfs_recursive_algorithm_x_cover_set_style_solutions_partitioned_solver(list_list_given_new,
                                                                                   list_solution_possible,
                                                                                   list_list_solution)

        # Reset list_solution_possible when you have a new row_selected
        list_solution_possible = []

    # Return list_list_solution
    return list_list_solution


def find_solutions_partitioned_unique(list_solution_partitioned: List[List[List[int]]]) -> List[List[Tuple[int]]]:
    """
    Given the solutions partitioned find all the unique solutions using frozenset and set because it's clean

    :param list_solution_partitioned: list_solution from
    dfs_recursive_algorithm_x_cover_set_style_solutions_partitioned_solver call
    :return: list_solution but only of the unique solutions
    """
    set_solution = set()

    for solution_partitioned in list_solution_partitioned:
        set_solution.add(frozenset(
            tuple(i) for i in solution_partitioned

        ))
    return [list(i) for i in set_solution]


if __name__ == '__main__':

    # Matrix to solve
    list_given = [[0, 3, 6, 0],
                  [3, 0, 2, 5],
                  [6, 2, 0, 1],
                  [0, 5, 1, 0]]

    # Target sum to hit
    target = 15

    list_solution = dfs_recursive(list_given, target)

    # For print spacing
    try:
        length_of_a_row = len(list_solution[0])
    except IndexError as e:
        print("There are no solutions for the given Matrix")
        length_of_a_row = 1

    print("All possible solutions")
    # Print All possible solutions
    for i in list_solution:
        # print(i, sum(i))
        print(f"\t{str(i):<{length_of_a_row * 3 + 1}} {sum(i)}")
    print()

    list_solution_partitioned = dfs_recursive_algorithm_x_cover_set_style_solutions_partitioned_solver(
        list_solution)

    print("Solutions Partitioned")
    # Print the Solutions Partitioned
    for index, solution in enumerate(list_solution_partitioned):
        print("\tSolution {}".format(index + 1))
        for partition in solution:
            print("\t{}".format(partition))
        print()

    list_solution_partitioned_unique = find_solutions_partitioned_unique(list_solution_partitioned)

    print("Solutions Partitioned (Unique)")
    # Print the Solutions Partitioned (Unique)
    for index, solution in enumerate(list_solution_partitioned_unique):
        print("\tSolution {}".format(index + 1))
        for partition in solution:
            print("\t{}".format(partition))
        print()

    # create_callgraph()
