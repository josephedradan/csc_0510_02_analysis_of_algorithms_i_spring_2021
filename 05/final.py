"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 5/18/2021

Purpose:
    Solve final
Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""
import numpy

from San_Francisco_State_University.csc_0510_02_analysis_of_algorithms_i_spring_2021.algorithm_challenge_5.Algorithm_Challenge_5_Branch_and_Bound import \
    branch_and_bound_bfs_priority_queue, branch_and_bound_node_exit, \
    get_sum_cost_path_complete_given_list_node_path, branch_and_bound_node_entry, branch_and_bound_node_exit_entry


def example1():
    matrix = [[0, 3, 7, 10, 9, 22, 10],
              [14, 0, 15, 22, 3, 16, 20],
              [35, 33, 0, 41, 7, 14, 23],
              [11, 30, 21, 0, 40, 15, 13],
              [12, 5, 17, 1, 0, 3, 27],
              [23, 24, 11, 13, 34, 0, 5],
              [11, 2, 14, 26, 2, 10, 0]]

    print("Consider Exit Only Calculation")
    solutions_exit = branch_and_bound_bfs_priority_queue(matrix,
                                                         function_branch_and_bound=branch_and_bound_node_exit)

    print(f"\n{'=' * 200}\n")

    print("Matrix:")
    print(numpy.array(matrix), end="\n")
    print()

    print("Solution Containers (Exit only) [Read List Left to Right for path]")
    for i in solutions_exit:
        forward, backward = get_sum_cost_path_complete_given_list_node_path(matrix, i.get_exit_list_node_path())
        str_temp = "{:<40} {:<50} {:<50}".format(str(i),
                                                 f"Read List Node Path Forward Sum: {forward}",
                                                 f"Read List Node Path Backward Sum: {backward}")
        print(str_temp)
    print()


def example2():
    matrix = [[0, 3, 7, 10, 9, 22, 10],
              [14, 0, 15, 22, 3, 16, 20],
              [35, 33, 0, 41, 7, 14, 23],
              [11, 30, 21, 0, 40, 15, 13],
              [12, 5, 17, 1, 0, 3, 27],
              [23, 24, 11, 13, 34, 0, 5],
              [11, 2, 14, 26, 2, 10, 0]]

    print("Consider Entry Only Calculation")
    solutions_entry = branch_and_bound_bfs_priority_queue(matrix,
                                                          function_branch_and_bound=branch_and_bound_node_entry)
    print(f"\n{'=' * 200}\n")

    print("Solution Containers (Entry only) [Read List Right to Left for path]")
    for i in solutions_entry:
        forward, backward = get_sum_cost_path_complete_given_list_node_path(matrix, i.get_entry_list_node_path())
        str_temp = "{:<40} {:<50} {:<50}".format(str(i),
                                                 f"Read List Node Path Forward Sum: {forward}",
                                                 f"Read List Node Path Backward Sum: {backward}")
        print(str_temp)
    print()


def example3():
    matrix = [[0, 3, 7, 10, 9, 22, 10],
              [14, 0, 15, 22, 3, 16, 20],
              [35, 33, 0, 41, 7, 14, 23],
              [11, 30, 21, 0, 40, 15, 13],
              [12, 5, 17, 1, 0, 3, 27],
              [23, 24, 11, 13, 34, 0, 5],
              [11, 2, 14, 26, 2, 10, 0]]

    print("Consider Exit and Entry (Exit is Priority?) Calculation")
    solutions_exit_entry = branch_and_bound_bfs_priority_queue(matrix,
                                                               function_branch_and_bound=branch_and_bound_node_exit_entry)
    print(f"\n{'=' * 200}\n")

    print("Matrix:")
    print(numpy.array(matrix), end="\n")
    print()

    print("Solution Containers (Exit and Entry, Exit is Priority?) [Read List Left to Right for path]")
    for i in solutions_exit_entry:
        forward, backward = get_sum_cost_path_complete_given_list_node_path(matrix, i.get_exit_list_node_path())
        str_temp = "{:<40} {:<50} {:<50}".format(str(i),
                                                 f"Read List Node Path Forward Sum: {forward}",
                                                 f"Read List Node Path Backward Sum: {backward}")
        print(str_temp)
    print()


if __name__ == '__main__':
    # example2()

    example3()
