"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 4/24/2021

Purpose:
    Generalized, technically correct solution for Algorithm for CSC510 Algorithm Challenge 4: Backtracking.
    This algorithm does not fully follow condition 5.

Details:

Description:

Notes:
    Conditions to follow
        Let {P_1, P_2, ..., P_k, ... P_n} be a set of solutions for this problem where P_k = {M(i, j)_1 + M(i, j)_2 +
        M(i, j)_3 + ... + M(i, j)_m-1 + M(i, j)_m} = S is a set of coordinates for integers values in a matrix,
        and S the sum of those integers for that set_solutions P_k. The S sum is valid only if:
            1. All the indexes i and j for that sum of Pk are unique

                Explanation:    i is unique and j is unique regardless

            2. The integer in M(i, j) is not zero

                Explanation:    Value at (i, j) is not 0

            3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1

                Explanation:    Index j of M_sub_x is Index i of M_sub_x+1

            4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions Pk

                Explanation:    Index i of M_sub_1 IS 0 AND Index j of M_sub_m IS 0

            5. A possible set_solutions P_k is only considered an optimal set_solutions if the sum S of all its integers
               is the minimum or the maximum sum S from all the solutions P_k

                Explanation:    A Solution has its sum of values in its list equal to value S and all Solutions must be
                                equal to that value S for that particular list of solutions

        Note that i == x == column and j == y == row

    Notice that the left to right diagonal of the matrix are never used because it will bring the following row back
    to the same row which is invalid.

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
from typing import List, Union, Set, Tuple, FrozenSet, Sequence


def dfs_recursive(list_list_int_grid: List[List[int]],
                  index_column_i_x_given: Union[int, None] = None,
                  index_row_j_y_given: Union[int, None] = None,
                  set_index_row_j_y_used: Set[int] = None,
                  set_index_column_i_x_used: Set[int] = None,
                  set_tuple_int_int_used: Set[Tuple[int, int]] = None,
                  list_tuple_int_int_solution_partition: List[Tuple[int, int]] = None,
                  set_tuple_tuple_int_int_solution_complete: Set[Tuple[Tuple[int, int]]] = None,
                  set_frozenset_tuple_tuple_int_int_solutions_complete: Set[FrozenSet[Tuple[Tuple[int, int]]]] = None
                  ):
    """
    Recursive call to find the solutions that satisfy the conditions given.

    :param list_list_int_grid: Matrix
    :param index_column_i_x_given: starting x index (Column)
    :param index_row_j_y_given: starting y index (row)
    :param set_tuple_int_int_used: set of tuples that have already been traversed
    :param set_index_row_j_y_used: set that contains all traversed rows (index y)
    :param set_index_column_i_x_used: set that contains all traversed columns (index x)
    :param list_tuple_int_int_solution_partition: List of tuples where each tuple contains coordinates
    (collection of indices) in the grid/matrix
    :param set_tuple_tuple_int_int_solution_complete: Set of tuple of tuples where the inner most tuple is a
    coordinate in the grid/matrix and the outer most tuple is a collection of those inner tuples. The set contains a
    collection of those outer tuples, a complete collection of the outer tuples are partitions that don't reuse
    the same inner tuples but satisfy the conditions for this algorithm. Basically, it uses the remaining inner tuples
    to make another set_solutions.
    :param set_frozenset_tuple_tuple_int_int_solutions_complete: Set of frozensets where the frozensets are
    set_tuple_tuple_int_int_solution_complete, Basically a set of complete solutions.
    :return:
    """

    # Default argument resetter, not part of algorithm
    if set_frozenset_tuple_tuple_int_int_solutions_complete is None:
        set_index_row_j_y_used = set()
        set_index_column_i_x_used = set()
        set_tuple_int_int_used = set()
        list_tuple_int_int_solution_partition = []
        set_tuple_tuple_int_int_solution_complete = set()
        set_frozenset_tuple_tuple_int_int_solutions_complete = set()

    # Loop over rows
    for index_row_j_y, row in enumerate(list_list_int_grid):

        """
        Condition 1. All the indexes i and j for that sum of Pk are unique
        Condition 1 is partially satisfied through by eliminating entire
        rows from being used to prevent duplicates.
        """
        if index_row_j_y in set_index_row_j_y_used:
            continue

        # Loop over columns
        for index_column_i_x, element_x_y in enumerate(row):

            collection_index = (index_column_i_x, index_row_j_y)

            """
            Condition 1. All the indexes i and j for that sum of Pk are unique
            Condition 1 is completely satisfied by eliminating entire 
            columns from being used to prevent duplicates.
            """
            if index_column_i_x in set_index_column_i_x_used:
                continue

            """
            Special Condition 1.
            Check if collection of indices x, y are already used.
            This is used for the recursive call for partitions of a complete set_solutions.
            This can partially satisfy condition 1 only by the collection of indices x, y and not an 
            entire row or column which condition 1 is based on.
            """
            if collection_index in set_tuple_int_int_used:
                continue

            """
            Condition 3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1
            Condition 3 is completely satisfied by looking at the recursive call's swap of x and y indices as
            arguments.
            Alternative set_solutions is to used a jump based system rather than a loop on row and col values
            """
            if index_column_i_x_given is not None and index_column_i_x != index_column_i_x_given:
                continue

            # if index_row_j_y_given is not None and index_row_j_y != index_row_j_y_given:
            #     continue

            """
            Condition 2. The integer in M(i, j) is not zero
            Condition 2 is completely satisfied by checking if the value at the position is 0
            """
            if element_x_y == 0:
                continue

            """
            Condition 4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions Pk
            Condition 4 is partially satisfied because of Index i == 0 for M(i, j)_1
            If set_index_column_i_x_used is empty and index_column_i_x is not 0 then continue, only 
            index_column_i_x == 0 can pass
            """
            if len(set_index_column_i_x_used) == 0 and index_column_i_x != 0:
                continue

            """
            Condition 4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions Pk
            Condition 4 is completely satisfied because of the previous line and Index j == 0 for M(i, j)_m
            If set_index_row_j_y_used full-1 and index_row_j_y is not 0 then continue, only index_row_j_y == 0 can pass
            """
            if len(set_index_row_j_y_used) == len(list_list_int_grid) - 1 and index_row_j_y != 0:
                continue

            # If the size of Solution Partition is not yet complete
            if len(set_index_column_i_x_used) <= len(list_list_int_grid):

                # Default initialization
                tuple_tuple_int_int_partition = None

                # Add indices to corresponding sets and collection of indices to list_tuple_int_int_solution_partition
                set_index_row_j_y_used.add(index_row_j_y)
                set_index_column_i_x_used.add(index_column_i_x)
                list_tuple_int_int_solution_partition.append(collection_index)

                """
                Used for Special Condition 1 to indicate collection of indices x, y is already used 
                """
                set_tuple_int_int_used.add(collection_index)

                # Add list_tuple_int_int_solution_partition to set_tuple_tuple_int_int_solution_complete
                if len(list_tuple_int_int_solution_partition) == len(row):
                    tuple_tuple_int_int_partition = tuple(list_tuple_int_int_solution_partition)
                    set_tuple_tuple_int_int_solution_complete.add(tuple_tuple_int_int_partition)

                    # print(set_tuple_tuple_int_int_solution_complete)
                    # print(tuple_tuple_int_int_partition)

                    """
                    Special Recursive call (DFS) for finding all partitions for
                    set_tuple_tuple_int_int_solution_complete which will be added to
                    set_frozenset_tuple_tuple_int_int_solutions_complete
                    """

                    dfs_recursive(list_list_int_grid,
                                  None,
                                  None,
                                  set(),
                                  set(),
                                  set_tuple_int_int_used,
                                  list(),
                                  set_tuple_tuple_int_int_solution_complete,
                                  set_frozenset_tuple_tuple_int_int_solutions_complete
                                  )

                # Add set_tuple_tuple_int_int_solution_complete to set_frozenset_tuple_tuple_int_int_solutions_complete
                if len(set_index_row_j_y_used) == len(list_list_int_grid):
                    frozenset_tuple_tuple_int_int_solution = frozenset(set_tuple_tuple_int_int_solution_complete)
                    set_frozenset_tuple_tuple_int_int_solutions_complete.add(frozenset_tuple_tuple_int_int_solution)

                # If you haven't traversed every row, then you must recursive call
                else:
                    """
                    Recursive call (DFS) to find next collection of indices 
                    
                    Note: 
                        index_row_j_y is the second argument and index_column_i_x is the third argument,
                        this is to support Condition 3
                    """
                    dfs_recursive(list_list_int_grid,
                                  index_row_j_y,
                                  index_column_i_x,
                                  set_index_row_j_y_used,
                                  set_index_column_i_x_used,
                                  set_tuple_int_int_used,
                                  list_tuple_int_int_solution_partition,
                                  set_tuple_tuple_int_int_solution_complete,
                                  set_frozenset_tuple_tuple_int_int_solutions_complete
                                  )

                """
                If you add to set_tuple_tuple_int_int_solution_complete, then you must remove from it for backtracking.
                If you do not have this line then set_tuple_tuple_int_int_solution_complete will carry over and use
                set_tuple_tuple_int_int_solution_complete for every tuple_tuple_int_int_partition added to it.
                """
                if len(list_tuple_int_int_solution_partition) == len(row):
                    set_tuple_tuple_int_int_solution_complete.remove(tuple_tuple_int_int_partition)

                """
                Removal of collection of indices x, y from set_tuple_int_int_used for backtracking
                """
                set_tuple_int_int_used.remove(collection_index)

                """
                Remove indices to corresponding sets and collection of indices to list_tuple_int_int_solution_partition
                """
                list_tuple_int_int_solution_partition.remove(collection_index)
                set_index_column_i_x_used.remove(index_column_i_x)
                set_index_row_j_y_used.remove(index_row_j_y)

    return set_frozenset_tuple_tuple_int_int_solutions_complete


def get_values_from_collection_of_indices(grid: Sequence[Sequence[int]], collection: Sequence[Sequence[int]]):
    """
    Given the grid and a sequence of sequences containing ints, create a list of ints containing the values
    based on the inner sequence of int. Then return this list of ints.

    :param grid:
    :param collection:
    :return:
    """
    # Note that the grid is in row then column format which is why you use y (i[1]) then x (i[0]).
    list_values = [grid[i[1]][i[0]] for i in collection]
    return list_values


def print_algo_challenge_4_solution(grid: Sequence[Sequence[int]],
                                    set_solutions: Set[FrozenSet[Tuple[Tuple[int, int]]]]):
    print("Solutions Complete:")
    for index, solution_complete in enumerate(set_solutions):
        print("{}{}".format(" " * 5, "Solution Complete {}".format(index + 1)))
        for solution_partial in solution_complete:
            list_value = get_values_from_collection_of_indices(grid, solution_partial)

            # Print Style 1
            # str_collection = "".join(["{:<10}".format(str(i)) for i in solution_partial])
            # str_value = "".join(["{:<10}".format("{:>4}".format(i)) for i in list_value])
            #
            # print(str_collection)
            # print("{:<{}}Sum:{}".format(str_value, len(str_value) + 10, sum(list_value)))

            # Print Style 2
            # str_full = "{}{}".format(
            #     " " * 10,
            #     "".join(["{:<10}".format("{}={}".format(a, b)) for a, b in zip(solution_partial, list_value)]) +
            #     "Sum:{}".format(sum(list_value)))
            # print(str_full)

            # Print Style 3
            str_full = "{}{}{}{}".format(
                " " * 10,
                "".join(["{:<7}".format("{}".format(a)) for a in solution_partial]) + " " * 5,
                " + ".join(["{:<7}".format("M[{}][{}]".format(c[1], c[0])) for c in solution_partial]) + " " * 5,
                " + ".join(["{:<1}".format(b) for b in list_value]) + " = {}".format(sum(list_value)) + " " * 5,
            )
            print(str_full)

        print()


def example_1():
    """
    Using the first matrix given in the algorithm challenge
    :return:
    """
    list_given = [[0, 3, 6, 0],
                  [3, 0, 2, 8],
                  [6, 2, 0, 1],
                  [0, 5, 1, 0]]

    print("Matrix 1:")
    print(numpy.array(list_given))
    print()
    x = dfs_recursive(list_given)
    print_algo_challenge_4_solution(list_given, x)


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

    print("Matrix 2:")
    print(numpy.array(list_given))
    print()

    x = dfs_recursive(list_given)
    print_algo_challenge_4_solution(list_given, x)


def main():
    example_1()
    print("\n" + "#" * 100 + "\n")
    example_2()


if __name__ == '__main__':
    main()
