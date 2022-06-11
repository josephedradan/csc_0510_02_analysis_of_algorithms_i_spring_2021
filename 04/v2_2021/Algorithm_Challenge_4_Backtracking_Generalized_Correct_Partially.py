"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 4/24/2021

Purpose:
    Generalized, technically correct solution for Algorithm for SFSU CSC 510 Algorithm Challenge 4: Backtracking.
    This algorithm does not have condition 5.

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
from typing import List, Union, Set, Tuple, FrozenSet, Sequence, Iterable


# @callgraph(use_list_index_args=[6], display_callable_name=False, graph_attrs={"rankdir": "LR"})
def dfs_recursive(list_list_int_matrix: Sequence[Sequence[int]],
                  index_column_i_x_given: Union[int, None] = None,
                  index_row_j_y_given: Union[int, None] = None,
                  set_index_row_j_y_used: Union[Set[int], None] = None,
                  set_index_column_i_x_used: Union[Set[int], None] = None,
                  set_tuple_int_int_used: Union[Set[Tuple[int, int]], None] = None,
                  list_tuple_int_int_solution_partition: Union[List[Tuple[int, int]], None] = None,
                  set_tuple_tuple_int_int_solution_complete: Union[Set[Tuple[Tuple[int, int]]], None] = None,
                  set_frozenset_tuple_tuple_int_int_solutions_complete: Union[Set[FrozenSet[Tuple[Tuple[int, int]]]],
                                                                              None] = None
                  ):
    """
    Recursive call to find the solutions that satisfy thee first 4 of the 5 conditions given.

    :param list_list_int_matrix: Matrix
    :param index_column_i_x_given: Starting x index (Column)
    :param index_row_j_y_given: Starting y index (Row)
    :param set_tuple_int_int_used: Set of tuples that have already been traversed
    :param set_index_row_j_y_used: Set that contains all traversed rows (index y)
    :param set_index_column_i_x_used: Set that contains all traversed columns (index x)
    :param list_tuple_int_int_solution_partition: List of tuples where each tuple contains coordinates
    (collection of indices) in the matrix/matrix.
    :param set_tuple_tuple_int_int_solution_complete: Set of tuple of tuples where the inner most tuple is a
    coordinate in the matrix and the outer most tuple is a collection of those inner tuples. The set contains a
    collection of those outer tuples, a complete collection of the outer tuples are partitions that don't reuse
    the same inner tuples but satisfy the conditions for this algorithm. Basically, it uses the remaining inner tuples
    to make another solutions based on the existing already traversed matrix.
    :param set_frozenset_tuple_tuple_int_int_solutions_complete: Set of frozensets where the frozensets are
    set_tuple_tuple_int_int_solution_complete, basically a set of complete solutions.

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
    for index_row_j_y, row in enumerate(list_list_int_matrix):

        """
        Condition 1. All the indexes i and j for that sum of P_k are unique
        
        Condition 1 is partially satisfied by eliminating entire
        rows from being used to prevent duplicates.
        """
        if index_row_j_y in set_index_row_j_y_used:
            continue

        # Loop over columns
        for index_column_i_x, element_x_y in enumerate(row):

            collection_index = (index_column_i_x, index_row_j_y)

            """
            Condition 1. All the indexes i and j for that sum of P_k are unique
            
            Condition 1 is completely satisfied by eliminating entire 
            columns from being used to prevent duplicates.
            """
            if index_column_i_x in set_index_column_i_x_used:
                continue

            """
            Special Condition 1. Check if collection of indices x, y are already used
            
            This is used for the recursive call for partitions to create a complete set_frozenset_solutions.
            This can partially satisfy condition 1 only by the collection of indices x, y and not an 
            entire row or column which condition 1 is based on.
            """
            if collection_index in set_tuple_int_int_used:
                continue

            """
            Condition 3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1
            
            Condition 3 is completely satisfied by swapping the recursive call's index_row_j_y and index_column_i_x
            arguments. This is to state that the index of the current row here will be the column for the following
            recursive call. Now compare index_column_i_x to index_column_i_x_given and only allow code to execute if
            the indices are the same.
            """
            if index_column_i_x_given is not None and index_column_i_x != index_column_i_x_given:
                continue

            """
            Condition 2. The integer in M(i, j) is not zero.
            
            Condition 2 is completely satisfied by checking if the value at the position is 0.
            """
            if element_x_y == 0:
                continue

            """
            Condition 4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k
            
            Condition 4 is partially satisfied because of Index i == 0 for M(i, j)_1
            If set_index_column_i_x_used is empty and index_column_i_x is not 0 then continue, then only 
            index_column_i_x == 0 can pass.
            """
            if len(set_index_column_i_x_used) == 0 and index_column_i_x != 0:
                continue

            """
            Condition 4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k.
            
            Condition 4 is completely satisfied because of the previous line and Index j == 0 for M(i, j)_m
            If set_index_row_j_y_used full-1 and index_row_j_y is not 0 then continue, 
            then only index_row_j_y == 0 can pass.
            """
            if len(set_index_row_j_y_used) == len(list_list_int_matrix) - 1 and index_row_j_y != 0:
                continue

            # If the size of Solution Partition is not yet complete
            if len(set_index_column_i_x_used) <= len(list_list_int_matrix):

                # Default initialization
                tuple_tuple_int_int_partition = None

                # Add indices to corresponding sets and collection of indices to list_tuple_int_int_solution_partition
                set_index_row_j_y_used.add(index_row_j_y)
                set_index_column_i_x_used.add(index_column_i_x)
                list_tuple_int_int_solution_partition.append(collection_index)

                """
                Used for Special Condition 1 to indicate that the collection of indices x, y is already used 
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
                    set_frozenset_tuple_tuple_int_int_solutions_complete.
                    """

                    dfs_recursive(list_list_int_matrix,
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
                if len(set_index_row_j_y_used) == len(list_list_int_matrix):
                    frozenset_tuple_tuple_int_int_solution = frozenset(set_tuple_tuple_int_int_solution_complete)
                    set_frozenset_tuple_tuple_int_int_solutions_complete.add(frozenset_tuple_tuple_int_int_solution)

                # If you haven't traversed every row, then you must recursive call
                else:
                    """
                    Recursive call (DFS) to find next collection of indices
                    
                    Note: 
                        index_row_j_y is the second argument and index_column_i_x is the third argument,
                        this is to support Condition 3.
                    """
                    dfs_recursive(list_list_int_matrix,
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
                Removal of collection of indices x, y from set_tuple_int_int_used for backtracking.
                """
                set_tuple_int_int_used.remove(collection_index)

                """
                Remove indices from corresponding sets and collection of indices from 
                list_tuple_int_int_solution_partition.
                """
                list_tuple_int_int_solution_partition.pop()
                set_index_column_i_x_used.remove(index_column_i_x)
                set_index_row_j_y_used.remove(index_row_j_y)

    return set_frozenset_tuple_tuple_int_int_solutions_complete


def get_values_from_collection_of_indices(matrix: Sequence[Sequence[int]], collection: Sequence[Sequence[int]]):
    """
    Given the matrix and a sequence of sequences (collection) containing ints, create a list of ints containing the
    values based on the inner sequence of ints, then return this list of ints. This assumes that the given order of
    the matrix is in form y, x and you give a collection in x, y form.

    :param matrix:
    :param collection:
    :return:
    """
    # Note that the matrix is in row then column format which is why you use y (i[1]) then x (i[0]).
    list_values = [matrix[i[1]][i[0]] for i in collection]
    return list_values


def print_algorithm_challenge_4_solution(matrix: Sequence[Sequence[int]],
                                         set_frozenset_solutions: Set[FrozenSet[Tuple[Tuple[int, int]]]]):
    """
    Given a matrix and a set of frozenset of solutions, do a formal print of the frozenset of solutions.

    :param matrix:
    :param set_frozenset_solutions:
    :return:
    """

    print("Solutions Complete:")
    for index, solution_complete in enumerate(set_frozenset_solutions):
        print("{}{}".format(" " * 5, "Solution Complete {}".format(index + 1)))
        print_algorithm_challenge_4_solution_inner(matrix, solution_complete)
        print()


def print_algorithm_challenge_4_solution_inner(matrix: Sequence[Sequence[int]],
                                               solutions: Iterable[Tuple[Tuple[int, int]]]):
    """
    Given a matrix and a set of solutions, do a formal print of the solution.

    :param matrix:
    :param solutions:
    :return:
    """
    for solution in solutions:
        list_value = get_values_from_collection_of_indices(matrix, solution)

        # Print Style 1
        # str_collection = "".join(["{:<10}".format(str(i)) for i in solution])
        # str_value = "".join(["{:<10}".format("{:>4}".format(i)) for i in list_value])
        #
        # print(str_collection)
        # print("{:<{}}Sum:{}".format(str_value, len(str_value) + 10, sum(list_value)))

        # Print Style 2
        # str_full = "{}{}".format(
        #     " " * 10,
        #     "".join(["{:<10}".format("{}={}".format(a, b)) for a, b in zip(solution, list_value)]) +
        #     "Sum:{}".format(sum(list_value)))
        # print(str_full)

        # Print Style 3
        str_full = "{}{}{}{}".format(
            " " * 10,
            "".join(["{:<7}".format("{}".format(a)) for a in solution]) + " " * 5,
            " + ".join(["{:<7}".format("M[{}][{}]".format(c[1], c[0])) for c in solution]) + " " * 5,
            " + ".join(["{:<1}".format(b) for b in list_value]) + " = {}".format(sum(list_value)) + " " * 5,
        )
        print(str_full)


def example_1():
    """
    Using the first matrix given in the algorithm challenge.
    :return:
    """
    list_given = [[0, 3, 6, 0],
                  [3, 0, 2, 5],
                  [6, 2, 0, 1],
                  [0, 5, 1, 0]]

    print("Matrix 1:")
    print(numpy.array(list_given))
    print()

    set_solutions = dfs_recursive(list_given)
    print_algorithm_challenge_4_solution(list_given, set_solutions)


def example_2():
    """
    Using the second matrix given in the algorithm challenge.
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

    set_solutions = dfs_recursive(list_given)
    print_algorithm_challenge_4_solution(list_given, set_solutions)


def main():
    example_1()
    print("\n" + "#" * 100 + "\n")
    example_2()

    # create_callgraph()


if __name__ == '__main__':
    main()
