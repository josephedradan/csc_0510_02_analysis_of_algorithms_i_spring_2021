"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 11/18/2020

Purpose:
    Solve sum of values from each rows of a matrix to equal a target value with recursive calls under certain
    conditions.

Details:
    1 Loop, DFS Recursive using a set for the answer

Description:

Notes:
    Conditions to follow
        Let {P_1, P_2, ..., P_k, ... P_n} be a set of solutions for this problem where P_k = {M(i, j)_1 + M(i, j)_2 +
        M(i, j)_3 + ... + M(i, j)_m-1 + M(i, j)_m} = S is a set of coordinates for integers values in a matrix,
        and S the sum of those integers for that solution P_k. The S sum is valid only if:
            1. All the indexes i and j for that sum of Pk are unique

                Explanation:    i is unique and j is unique regardless

            2. The integer in M(i, j) is not zero

                Explanation:    Value at (i, j) is not 0

            3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1

                Explanation:    Index j of M_sub_x is Index i of M_sub_x+1

            4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions Pk

                Explanation:    Index i of M_sub_1 IS 0 AND Index j of M_sub_m IS 0

            5. A possible solution P_k is only considered an optimal solution if the sum S of all its integers is
               the minimum or the maximum sum S from all the solutions P_k

                Explanation:    A Solution has its sum of values in its list equal to value S and all Solutions must be
                                equal to that value S for that particular list of solutions

    Notice that the left to right diagonal of the matrix are never used because it will bring the following row back
    to the same row which is invalid.

IMPORTANT NOTES:

Explanation:

Reference:

"""
# from joseph_library.decorators._old.callgraph_simple import callgraph, create_callgraph

from typing import FrozenSet, Set, List, Tuple


# Recursive call
# @callgraph
def dfs_recursive(list_list_given: List[List[int]],
                  index_row: int = 0,
                  index_row_final=None,
                  set_indices_traversed: Set = None,
                  index_list_solution_possible: int = 0,
                  list_solution_possible: List[List[int]] = None,
                  solution_possible: List[int] = None,
                  set_frozenset_solution: Set[FrozenSet[Tuple[int]]] = None) -> Set[FrozenSet[Tuple[int]]]:
    """
    Solve sum of values from each rows of a matrix to equal a target value with recursive calls under certain
    conditions.

    :param list_list_given: Matrix
    :param index_row: Current row via index in the matrix
    :param set_indices_traversed: Set containing index_row that we have already traversed
    :param index_list_solution_possible: Keeps track if we added a solution_possible to list_solution_possible
    :param list_solution_possible: List containing solution_possible
    :param solution_possible: List containing values from the matrix
    :param set_frozenset_solution: List of list_solution_possible which are the solutions that meet the conditions listed
    above
    :return: set_frozenset_solution
    """

    # Allows for resets for new calls from the initial call
    if set_frozenset_solution is None:
        index_row_final = index_row
        set_indices_traversed = set()
        list_solution_possible = []
        solution_possible = []
        set_frozenset_solution = set()

    if index_row in set_indices_traversed:
        return set_frozenset_solution

    # Current row you are working on
    row_current = list_list_given[index_row]

    set_indices_traversed.add(index_row)

    # Find min value's index
    index_value_minimum = None
    value_minimum = None
    for index, value in enumerate(row_current):
        if value == 0:
            continue

        if value_minimum is None:
            index_value_minimum = index
            value_minimum = value

        if value < value_minimum:
            index_value_minimum = index
            value_minimum = value

    # Loop through the values of the given row based on index_row
    for index_col, value in enumerate(row_current):

        # DEBUG PRINTING
        # print("Current Row: {}".format(row_current))
        # print("Row Index: {}".format(index_row))
        # print("Set Indices Traversed: {}".format(set_indices_traversed))
        # print("index_list_solution_possible: {}".format(index_list_solution_possible))
        # print("list_solution_possible: {}".format(list_solution_possible))
        # print("solution_possible: {}".format(solution_possible))
        # print("Value: {}".format(value))
        # [print(i) for i in list_list_given]  # Matrix
        # print()

        if value == 0:
            continue

        list_list_given[index_row][index_col] = 0

        # Add the value from the current row to the list of possible solutions
        solution_possible.append(value)

        if len(solution_possible) == len(list_list_given) and index_col == 0:
            # If solution is found then add it to list_solution_possible
            list_solution_possible.append(solution_possible.copy())

        if len(list_solution_possible) > index_list_solution_possible:

            # Assume that the most recently added solution has the same sum
            sum_same = True

            # Check if the sum of the 0th solution is equal to the sum of the most recently added solution
            if len(list_solution_possible) > 1:

                if sum(list_solution_possible[0]) != sum(list_solution_possible[-1]):
                    sum_same = False

            # If sum_same is true then sum(list_solution_possible[0]) == sum(list_solution_possible[-1])
            if sum_same:
                dfs_recursive(list_list_given, 0, set(),
                              index_list_solution_possible + 1,
                              list_solution_possible,
                              [],
                              set_frozenset_solution)

                set_frozenset_solution.add(
                    frozenset(
                        tuple(i) for i in list_solution_possible
                    )
                )

            list_solution_possible.pop(-1)

        if len(solution_possible) < len(list_list_given):
            dfs_recursive(list_list_given, index_col, set_indices_traversed,
                          index_list_solution_possible,
                          list_solution_possible,
                          solution_possible,
                          set_frozenset_solution)

        # Value of the popped from solution_possible
        value_from_solution_possible_last_added = solution_possible.pop(-1)

        # Restore the value in the Matrix from 0 to it's original value
        list_list_given[index_row][index_col] = value_from_solution_possible_last_added

    set_indices_traversed.remove(index_row)

    # Return set_frozenset_solution
    return set_frozenset_solution


if __name__ == '__main__':

    # Matrix to solve
    list_given = [[0, 14, 4, 10, 20],
                  [14, 0, 7, 8, 7],
                  [4, 5, 0, 7, 16],
                  [11, 7, 9, 0, 2],
                  [18, 7, 17, 4, 0]
                  ]

    # list_given = [[0, 1, 2, 3],
    #               [1, 0, 4, 5],
    #               [2, 3, 0, 6],
    #               [4, 5, 6, 0]]

    # list_given = [[0, 7, 1, 0, 0, 8],
    #               [7, 0, 5, 0, 9, 6],
    #               [1, 5, 0, 4, 0, 0],
    #               [0, 0, 4, 0, 2, 0],
    #               [0, 9, 0, 2, 0, 3],
    #               [8, 6, 0, 0, 3, 0]]

    set_frozenset_solution = dfs_recursive(list_given)

    # For print spacing
    try:
        length_of_a_row = len(list_given)
    except IndexError as e:
        print("There are no solutions for the given Matrix")
        length_of_a_row = 1

    print("All Possible Combination of Solutions (Unique)")
    # Print All possible solutions
    for index, solution in enumerate(set_frozenset_solution):
        # print(i, sum(i))
        # print(f"\t{str(i):<{length_of_a_row * 3 + 1}} {sum(i)}")

        print("Solution Combination {}".format(index + 1))
        for solution_partial in solution:
            print(f"\t{str(solution_partial):<{length_of_a_row * 3 + 1}} {sum(solution_partial)}")
        print()

    # create_callgraph()
