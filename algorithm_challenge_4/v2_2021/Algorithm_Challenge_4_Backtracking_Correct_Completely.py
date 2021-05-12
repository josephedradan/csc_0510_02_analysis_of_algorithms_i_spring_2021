"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 4/26/2021

Purpose:
    A solution to SFSU CSC 510's Algorithm Challenge 4

Details:

Description:

Notes:
    Conditions to follow
        Let {P_1, P_2, ..., P_k, ... P_n} be a set of solutions for this problem where P_k = {M(i, j)_1 + M(i, j)_2 +
        M(i, j)_3 + ... + M(i, j)_m-1 + M(i, j)_m} = S is a set of coordinates for integers values in a matrix,
        and S the sum of those integers for that solution P_k. The S sum is valid only if:
            1. All the indexes i and j for that sum of P_k are unique

                Explanation:    i is unique and j is unique regardless

            2. The integer in M(i, j) is not zero

                Explanation:    Value at (i, j) is not 0

            3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1

                Explanation:    Index j of M_sub_x is Index i of M_sub_x+1

            4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k

                Explanation:    Index i of M_sub_1 IS 0 AND Index j of M_sub_m IS 0

            5. A possible solution P_k is only considered an optimal solution if the sum S of all its integers
               is the minimum or the maximum sum S from all the solutions P_k

                Explanation:    A Solution has its sum of values in its list equal to value S and all solutions must be
                                equal to that value S for that particular list of solutions

        Note that i == x == column and j == y == row

    Notice that the left to right diagonal of the matrix are never used because it will bring the following row or
    column back to the same row or column.

    Set and Frozenset notes
        set(((0,1),(0,1)))
            {(1, 2)}

        set(((0,1), (1,0))) ==
        set(((0,1), (1,0)))
            True

        # Order of inner tuples should not matter
        set(((0,1), (1,0))) ==
        set(((1,0), (0,1)))
            True

        set(((0,1), (1,0))) ==
        set(((1,0), (1,0)))
            False

        frozenset(((0,1), (1,0))) ==
        frozenset(((0,1), (1,0)))
            True

        frozenset(((0,1), (1,0))) ==
        frozenset(((1,0), (0,1)))
            True

        # Order of frozensets should not matter
        set((frozenset(((0,1), (1,0))), frozenset(((1,0), (0,1))))) ==
        set((frozenset(((1,0), (0,1))), frozenset(((0,1), (1,0)))))
            True

IMPORTANT NOTES:

Explanation:

Reference:

"""
import numpy
from Algorithm_Challenge_4_Backtracking_Generalized_Correct_Partially import print_algorithm_challenge_4_solution_inner
from josephs_resources.decorators.callgraph_simple import callgraph, create_callgraph
from typing import List, Union, Set, Tuple, Sequence

counter_iterations = 0


@callgraph(use_list_index_args=[5], display_callable_name=False, graph_attrs={"rankdir": "LR"})
def dfs_recursive(list_list_int_matrix: Sequence[Sequence[int]],
                  index_column_i_x_given: Union[int, None] = None,
                  index_row_j_y_given: Union[int, None] = None,
                  set_index_row_j_y_used: Union[Set[int], None] = None,
                  set_index_column_i_x_used: Union[Set[int], None] = None,
                  list_tuple_int_int_solution: Union[List[Tuple[int, int]], None] = None,
                  set_tuple_tuple_int_int_solutions: Union[Set[Tuple[Tuple[int, int]]], None] = None,
                  set_tuple_tuple_int_int_solutions_min: Union[Set[Tuple[Tuple[int, int]]], None] = None,
                  set_tuple_tuple_int_int_solutions_max: Union[Set[Tuple[Tuple[int, int]]], None] = None,
                  list_value_min: Union[List, None] = None,
                  list_value_max: Union[List, None] = None,
                  ):
    """
    Recursive call to find the solutions that satisfy the conditions given.

    :param list_list_int_matrix: Matrix
    :param index_column_i_x_given: Starting x index (Column)
    :param index_row_j_y_given: Starting y index (Row)
    :param set_index_row_j_y_used: Set that contains all traversed rows (index y)
    :param set_index_column_i_x_used: Set that contains all traversed columns (index x)
    :param list_tuple_int_int_solution: List of tuples where each tuple contains coordinates
    (collection of indices) in the matrix/matrix.
    :param set_tuple_tuple_int_int_solutions: Set of tuple of tuples where the inner most tuple is a
    coordinate in the matrix and the outer most tuple is a collection of those inner tuples. The set contains a
    collection of those outer tuples, a complete collection of the outer tuples are all the solutions that the algorithm
    has found.
    :param set_tuple_tuple_int_int_solutions_min: Set containing the solutions where their sum of their collection's
    values are the minimum sum compared to all other sum of other solution's collection's values.
    :param set_tuple_tuple_int_int_solutions_max: Set containing the solutions where their sum of their collection's
    values are the maximum sum compared to all other sum of other solution's collection's values.
    :param list_value_min: Cheap mutable list to pass 1 int that is a min sum to all recursive calls.
    :param list_value_max: Cheap mutable list to pass 1 int that is a max sum to all recursive calls.

    :return:
    """

    # Default argument resetter, not part of algorithm
    if set_tuple_tuple_int_int_solutions is None:
        index_column_i_x_given = 0  # Initial start for condition 4 TODO: Generalized this to start at any column
        set_index_row_j_y_used = set()
        set_index_column_i_x_used = set()
        list_tuple_int_int_solution = []
        set_tuple_tuple_int_int_solutions = set()
        set_tuple_tuple_int_int_solutions_min = set()
        set_tuple_tuple_int_int_solutions_max = set()
        list_value_min = []
        list_value_max = []
    print()
    # Loop over rows
    for index_row_j_y, row in enumerate(list_list_int_matrix):
        global counter_iterations
        counter_iterations += 1
        print(index_column_i_x_given, index_row_j_y)
        """
        Condition 1. All the indexes i and j for that sum of P_k are unique
        
        Condition 1 is partially satisfied by eliminating entire
        rows from being used to prevent duplicates
        """
        if index_row_j_y in set_index_row_j_y_used:
            print("Failed Condition 1 Part 1", list_tuple_int_int_solution)
            continue

        # # Loop over columns
        # for index_column_i_x, element_x_y in enumerate(row):

        # Replacement for the loop variant
        index_column_i_x = index_column_i_x_given
        element_x_y = list_list_int_matrix[index_row_j_y][index_column_i_x]

        collection_index = (index_column_i_x, index_row_j_y)

        """
        Condition 1. All the indexes i and j for that sum of P_k are unique
        
        Condition 1 is completely satisfied by eliminating entire 
        columns from being used to prevent duplicates.
        """
        if index_column_i_x in set_index_column_i_x_used:
            print("Failed Condition 1 Part 2", list_tuple_int_int_solution)
            continue

        """
        Condition 3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1
        
        Condition 3 is completely satisfied by swapping the recursive call's index_row_j_y and index_column_i_x
        arguments. This is to state that the index of the current row here will be the column for the following
        recursive call. Now compare index_column_i_x to index_column_i_x_given and only allow code to execute if
        the indices are the same.
        
        Note:
            This check should be removed, but it exists here because the this entire algorithm is a derivative of
            my custom general solution version of this algorithm in another file which does not necessarily solve 
            the algorithm challenge, but is cooler than this algorithm challenge and uses 2 loops rather than this
            automatic index_column_i_x jump which is determined by the previous call to this function.
        """
        # if index_column_i_x_given is not None and index_column_i_x != index_column_i_x_given:
        # print("Failed Condition 3", list_tuple_int_int_solution)
        #     continue

        """
        Condition 2. The integer in M(i, j) is not zero.
        
        Condition 2 is completely satisfied by checking if the value at the position is 0.
        """
        if element_x_y == 0:
            print("Failed Condition 2", list_tuple_int_int_solution)
            continue

        """
        Condition 4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k
        
        Condition 4 is partially satisfied because of Index i == 0 for M(i, j)_1
        If set_index_column_i_x_used is empty and index_column_i_x is not 0 then continue, then only 
        index_column_i_x == 0 can pass.
        """
        if len(set_index_column_i_x_used) == 0 and index_column_i_x != 0:
            print("Failed Condition 4 Part 1", list_tuple_int_int_solution)
            continue

        """
        Condition 4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k
        
        Condition 4 is completely satisfied because of the previous line and Index j == 0 for M(i, j)_m
        If set_index_row_j_y_used full-1 and index_row_j_y is not 0 then continue, 
        then only index_row_j_y == 0 can pass.
        """
        if len(set_index_row_j_y_used) == len(list_list_int_matrix) - 1 and index_row_j_y != 0:
            print("Failed Condition 4 Part 2", list_tuple_int_int_solution)
            continue

        """
        Condition 4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k
        
        Condition 4 is optimized and will now deny any recursive call with a non solution.
        """
        if len(set_index_row_j_y_used) < len(list_list_int_matrix) - 1 and index_row_j_y == 0:
            print("Failed Condition 4 Part 3", list_tuple_int_int_solution)
            continue

        # If the size of Solution Partition is not yet complete
        if len(set_index_column_i_x_used) <= len(list_list_int_matrix):

            # Add indices to corresponding sets and collection of indices to list_tuple_int_int_solution
            set_index_row_j_y_used.add(index_row_j_y)
            set_index_column_i_x_used.add(index_column_i_x)
            list_tuple_int_int_solution.append(collection_index)

            # Add list_tuple_int_int_solution to set_tuple_tuple_int_int_solutions
            if len(list_tuple_int_int_solution) == len(row):
                tuple_tuple_int_int_partition = tuple(list_tuple_int_int_solution)
                set_tuple_tuple_int_int_solutions.add(tuple_tuple_int_int_partition)

                # print(set_tuple_tuple_int_int_solutions)
                # print(tuple_tuple_int_int_partition)

                """
                Condition 5. A possible solution P_k is only considered an optimal solution if the sum S of 
                all its integers is the minimum or the maximum sum S from all the solutions P_k
                
                Condition 5 is completely satisfied by calculating the sum of tuple_tuple_int_int_partition
                """

                sum_temp = sum([list_list_int_matrix[y][x] for x, y in list_tuple_int_int_solution])

                if not list_value_min:
                    list_value_min.append(sum_temp)
                    set_tuple_tuple_int_int_solutions_min.add(tuple_tuple_int_int_partition)
                elif sum_temp < list_value_min[0]:
                    list_value_min[0] = sum_temp
                    set_tuple_tuple_int_int_solutions_min.clear()
                    set_tuple_tuple_int_int_solutions_min.add(tuple_tuple_int_int_partition)
                elif sum_temp == list_value_min[0]:
                    set_tuple_tuple_int_int_solutions_min.add(tuple_tuple_int_int_partition)

                if not list_value_max:
                    list_value_max.append(sum_temp)
                    set_tuple_tuple_int_int_solutions_max.add(tuple_tuple_int_int_partition)
                elif sum_temp > list_value_max[0]:
                    list_value_max[0] = sum_temp
                    set_tuple_tuple_int_int_solutions_max.clear()
                    set_tuple_tuple_int_int_solutions_max.add(tuple_tuple_int_int_partition)
                elif sum_temp == list_value_max[0]:
                    set_tuple_tuple_int_int_solutions_max.add(tuple_tuple_int_int_partition)

            # If you haven't traversed every row, then you must recursive call
            else:
                """
                Recursive call (DFS) to find next collection of indices
            
                Condition 3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1
                
                Condition 3 is completely satisfied by swapping the recursive call's index_row_j_y and index_column_i_x
                arguments. This is to state that the index of the current row here will be the column for the following
                recursive call.
            
                Note: 
                    index_row_j_y is the second argument and index_column_i_x is the third argument,
                    this is to support Condition 3.
                """
                print("Recursive call")
                dfs_recursive(list_list_int_matrix,
                              index_row_j_y,
                              index_column_i_x,
                              set_index_row_j_y_used,
                              set_index_column_i_x_used,
                              list_tuple_int_int_solution,
                              set_tuple_tuple_int_int_solutions,
                              set_tuple_tuple_int_int_solutions_min,
                              set_tuple_tuple_int_int_solutions_max,
                              list_value_min,
                              list_value_max
                              )
                print("Return from recursive call")
            """
            Remove indices from corresponding sets and collection of indices from 
            list_tuple_int_int_solution.
            """
            list_tuple_int_int_solution.pop()
            set_index_column_i_x_used.remove(index_column_i_x)
            set_index_row_j_y_used.remove(index_row_j_y)

            """
            Condition 4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k
            
            Condition 4 is optimized and will prevent unnecessary iterations after a solution is found
            """
            if len(set_index_row_j_y_used) == len(list_list_int_matrix) - 1 and index_row_j_y == 0:
                return (set_tuple_tuple_int_int_solutions,
                        set_tuple_tuple_int_int_solutions_min,
                        set_tuple_tuple_int_int_solutions_max)

    return (set_tuple_tuple_int_int_solutions,
            set_tuple_tuple_int_int_solutions_min,
            set_tuple_tuple_int_int_solutions_max)


def example_1():
    """
    Using the first matrix given in the algorithm challenge
    :return:
    """
    list_given = [[0, 3, 6, 0],
                  [3, 0, 2, 5],
                  [6, 2, 0, 1],
                  [0, 5, 1, 0]]

    """
    This example uses the most time because most of the paths (because all the conditions must be met) 
    always creates a valid solution.
    
    Notes:
        There are 6 solutions
        Permutations 4 objects, 4 samples = 24
        24/6 = 4
    # """
    # list_given = [[1, 1, 1, 1],
    #               [1, 1, 1, 1],
    #               [1, 1, 1, 1],
    #               [1, 1, 1, 1]]

    print("Matrix 1:")
    print(numpy.array(list_given))
    print()

    _example_helper(list_given)


def example_2():
    """
    Using the second matrix given in the algorithm challenge
    :return:
    """
    list_given = [[0, 7, 1, 0, 0, 8],
                  [7, 0, 5, 0, 9, 6],
                  [1, 5, 0, 4, 0, 0],
                  [0, 0, 4, 0, 2, 0],
                  [0, 9, 0, 2, 0, 3],
                  [8, 6, 0, 0, 3, 0]]

    """
    This example uses the most time because most of the paths (because all the conditions must be met) 
    always creates a valid solution.
    
    Notes:
        There are 120 solutions
        Permutations 6 objects, 6 samples = 720
        720/120 = 6
        
        For 7, there are 720 solutions
        Permutations 7 objects, 7 samples = 5040
        5040/720 = 7
    """
    # list_given = [[1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1]]

    # list_given = [[1, 1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1, 1],
    #               [1, 1, 1, 1, 1, 1, 1]]

    print("Matrix 2:")
    print(numpy.array(list_given))
    print()

    _example_helper(list_given)


def example_any():
    """
    Testing any size matrix
    :return:
    """
    list_given = [[1 for _ in range(5)] for _ in range(5)]
    list_given = [[1 for _ in range(1)] for _ in range(1)]
    list_given = [[1 for _ in range(2)] for _ in range(2)]

    print(list_given)

    print("Matrix 1:")
    print(numpy.array(list_given))
    print()

    _example_helper(list_given)


def _example_helper(matrix: Sequence[Sequence[int]]):
    """
    Helper function to reduce code for printing the examples

    :param matrix:
    :return:
    """
    solutions_all, solutions_min, solutions_max = dfs_recursive(matrix)

    print("Solutions (All)")
    print_algorithm_challenge_4_solution_inner(matrix, solutions_all)
    print()

    print("Solutions (Minimum Sum)")
    print_algorithm_challenge_4_solution_inner(matrix, solutions_min)
    print()

    print("Solutions (Maximum Sum)")
    print_algorithm_challenge_4_solution_inner(matrix, solutions_max)
    print()


def multiple_matrix_sizes_test():
    """
    Testing the amount of solutions for many matrices with the same size
    for rows and columns to find a pattern to find time complexity for the
    write up

    :return:
    """
    from math import perm

    for i in range(1, 10):
        matrix = [[1 for _ in range(i)] for _ in range(i)]

        print("Matrix row/column size:", i)
        print(numpy.array(matrix))
        solutions_all, solutions_min, solutions_max = dfs_recursive(matrix)
        amount_of_solutions_all = len(solutions_all)
        print("Amount of solutions:", amount_of_solutions_all)
        amount_permutations = perm(i)
        print("Amount of permutations ({} objects, {} samples): {}".format(i, i, amount_permutations))
        print("Ratio of permutations to the solutions from the algorithm: {}".format(
            amount_permutations / amount_of_solutions_all))
        print()


def counter_iterations_test():
    """
    Testing worst case

    Notes:
        Do not run any other test other than this to make this work

    :return:
    """
    global counter_iterations
    counter_iterations = 0

    my_approximate_formula = lambda x: (1 / 2) * x * (1 + x) * (math.factorial(x) / x)

    import math
    for i in range(1, 12):
        matrix = [[1 for _ in range(i)] for _ in range(i)]

        solutions_all, solutions_min, solutions_max = dfs_recursive(matrix)

        size = len(matrix[0])

        result = my_approximate_formula(size)

        print("Matrix row/column size:", i)
        print(numpy.array(matrix))
        print("Global counter for iterations (counter_iterations):", counter_iterations)
        print("My formula's calculation for the total amount of iterations for size {}: {}".format(size, result))
        print("Difference (Mine - counter_iterations):", result - counter_iterations)
        print("Percent Error:", (counter_iterations - result) / counter_iterations * 100)
        print()


def testing_one_complete_solution():
    """
    Testing if my formula is right for 1 solution for 2 matrices

    :return:
    """
    import math

    global counter_iterations
    my_approximate_formula = lambda x: (1 / 2) * x * (1 + x) * (math.factorial(x) / x)
    my_approximate_formula_for_1_solution = lambda x: (1 / 2) * x * (1 + x)

    list_given = [[0, 0, 1, 0],
                  [1, 0, 0, 0],
                  [0, 0, 0, 1],
                  [0, 1, 0, 0]]

    # list_given = [[1, 1, 1, 1],
    #               [1, 1, 1, 1],
    #               [1, 1, 1, 1],
    #               [1, 1, 1, 1]]

    solutions_all, solutions_min, solutions_max = dfs_recursive(list_given)

    size = len(list_given[0])
    result = my_approximate_formula(size)
    result_2 = my_approximate_formula_for_1_solution(size)

    print("Matrix 1:")
    print(numpy.array(list_given))
    print()
    print("Global counter for iterations:", counter_iterations)
    # print("My formula's calculation for the total amount of iterations for size {}: {}".format(size, result))
    print("My formula's calculation for the amount of iterations for 1 solution for size {}: {}".format(size, result_2))

    return

    counter_iterations = 0

    list_given_2 = [[0, 0, 0, 0, 0, 8],
                    [0, 0, 0, 0, 9, 0],
                    [1, 0, 0, 0, 0, 0],
                    [0, 0, 4, 0, 0, 0],
                    [0, 0, 0, 2, 0, 0],
                    [0, 6, 0, 0, 0, 0]]

    # list_given_2 = [[1 for _ in range(6)] for _ in range(6)]

    solutions_all, solutions_min, solutions_max = dfs_recursive(list_given_2)

    size = len(list_given_2[0])
    result = my_approximate_formula(size)
    result_2 = my_approximate_formula_for_1_solution(size)

    print("Matrix 2:")
    print(numpy.array(list_given_2))
    print()
    print("Global counter for iterations:", counter_iterations)
    # print("My formula's calculation for the total amount of iterations for size {}: {}".format(size, result))
    print("My formula's calculation for the amount of iterations for 1 solution size {}: {}".format(size, result_2))


def main():
    # example_1()
    # print("\n" + "#" * 100 + "\n")
    # example_2()
    # print("\n" + "#" * 100 + "\n")
    example_any()

    # multiple_matrix_sizes_test()

    # counter_iterations_test()

    # testing_one_complete_solution()

    create_callgraph(type_ouput="png")


if __name__ == '__main__':
    main()
