"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 11/18/2020

Purpose:
    Solve sum of values from each rows of a matrix with recursive calls under certain
    conditions.

Details:
    1 Loop, DFS Recursive using a list for the answer

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
from typing import List, Set


# Recursive call
# @callgraph
def dfs_recursive(list_list_given: List[List[int]],
                  index_row: int = 0,
                  index_row_final: int = None,
                  set_indices_traversed: Set = None,
                  index_list_solution_possible: int = 0,
                  list_solution_possible: List[List[int]] = None,
                  solution_possible: List[int] = None,
                  list_list_solution: List[List[List[int]]] = None) -> List[List[List[int]]]:
    """
    Solve sum of values from each rows of a matrix to equal a target value with recursive calls under certain
    conditions.

    :param list_list_given: Matrix
    :param index_row: Current row via index in the matrix
    :param index_row_final: First row via index in the matrix to end at
    :param set_indices_traversed: Set containing index_row that we have already traversed
    :param index_list_solution_possible: Keeps track if we added a solution_possible to list_solution_possible
    :param list_solution_possible: List containing solution_possible
    :param solution_possible: List containing values from the matrix
    :param list_list_solution: List of list_solution_possible which are the solutions that meet the conditions listed
    above
    :return: list_list_solution
    """

    # Allows for resets for new calls from the initial call
    if list_list_solution is None:
        index_row_final = index_row
        set_indices_traversed = set()
        list_solution_possible = []
        solution_possible = []
        list_list_solution = []

    """
    4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k
    
    Condition 4 is Partially satisfied because index_row is initially set to 0 implying that index i is set to 0.
    """

    """
    1. All the indexes i and j for that sum of P_k are unique

    Condition 1 is Partially satisfied for index i by the below condition.
    If the row index is already in the set_indices_traversed, then return because index i NEEDS to be Unique.
    """
    if index_row in set_indices_traversed:
        """
        It is not necessary to return anything because the return at the end of this entire function is the one that
        actually matters. I return list_list_given so pycharm won't complain.
        """
        return list_list_solution

    # Current row you are working on
    row_current = list_list_given[index_row]

    """
    1. All the indexes i and j for that sum of P_k are unique

    Condition 1 is Completely satisfied by adding the row index to the set to prevent revisiting this row making the
    row Unique. Note that THIS revisit is ONLY RELATIVE to the EXISTING solution_possible NOT ANY FOLLOWING 
    solution_possible. Basically, we MIGHT revisit these rows in the future and we CANNOT revisit this row
    for the current solution_possible.

    Note:
        Disabling
            set_indices_traversed.add(index_row)
            set_indices_traversed.remove(index_row)
        Allows you to re use indices.
    """
    set_indices_traversed.add(index_row)

    # Loop through the values of the given row based on index_row
    for index_col, value in enumerate(row_current):

        # DEBUG PRINTING
        # print("Current Row: {}".format(row_current))
        # print("Row Index: {}".format(index_row))
        # print("Set: {}".format(set_indices_traversed))
        # print("index_list_solution_possible: {}".format(index_list_solution_possible))
        # print("list_solution_possible: {}".format(list_solution_possible))
        # print("solution_possible: {}".format(solution_possible))
        # print("Value: {}".format(value))
        # [print(i) for i in list_list_given]  # Matrix
        # print()

        """
        2. The integer in M(i, j) is not zero
        
        Condition 2 is satisfied by checking if the value at the given row_current and index_col is 0. Note that the
        value at this position could have been initially 0 OR it is set to zero by the following code below the code
        for this comment.
        """
        if value == 0:
            continue

        """
        1. All the indexes i and j for that sum of P_k are unique
        2. The integer in M(i, j) is not zero

        Condition 1 is now Completely satisfied again by setting the position's value to 0.
        By Assigning 
            list_list_given[index_row][index_col] = 0
        it will satisfy Condition 1 by disallowing the ability to select this position's value preventing duplicates
        thus index j will be Unique. Also by setting the value at this position to 0, it will also satisfy Condition 2.
        Notice that this CHANGE in position's value is CARRIED OVER to the FOLLOWING solution_possible which will
        prevent DUPLICATE value selection based on indices. Basically, the position's indices are Unique.
        """
        list_list_given[index_row][index_col] = 0

        # Add the value from the current row to the list of possible solutions
        solution_possible.append(value)

        """
        4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k
        
        Condition 4 is now Completely satisfied by the below condition by checking if the length of solution_possible 
        equals the length of list_list_given (This means we have used EVERY row in list_list_given) 
        AND the last column index's value in solution_possible is 0 AKA index j is 0.  
        """
        if len(solution_possible) == len(list_list_given) and index_col == index_row_final:
            # If solution is found then add it to list_solution_possible
            list_solution_possible.append(solution_possible.copy())

        """
        If there is more than 1 solution in list_solution_possible then YOU MIGHT be able to build another solution 
        THAT IS RELATIVE TO WHAT WAS ALREADY USED BY THE EXISTING solutions in list_solution_possible. Basically,
        remember when we assigned
            list_list_given[index_row][index_col] = 0
        this is CARRIED OVER WHEN WE DO a recursive call. Note that if you haven't seen it already, we restore the
        values in the matrix AT THE END of this for loop. 
        """
        if len(list_solution_possible) > index_list_solution_possible:

            """
            5. A possible solution P_k is only considered an optimal solution if the sum S of all its integers is
            the minimum or the maximum sum S from all the solutions P_k
            
            Condition 5 is satisfied here because we check if THE MOST RECENTLY ADDED solution to list_solution_possible
            has its sum EQUAL TO the sum of the 0th solution in list_solution_possible. Note that we add 1 solution
            to list_solution_possible at a time meaning that IT IS NOT POSSIBLE FOR A solution's sum NOT TO BE EQUAL TO
            list_solution_possible[0] to be able to pass and to another recursive call.
            """

            # Assume that the most recently added solution has the same sum
            sum_same = True

            # Check if the sum of the 0th solution is equal to the sum of the most recently added solution
            if len(list_solution_possible) > 1:

                """
                If the most recently added solution does not have the same sum as the 0th solution then change 
                sum_same to False.
                """
                if sum(list_solution_possible[0]) != sum(list_solution_possible[-1]):
                    sum_same = False

            # If sum_same is true then sum(list_solution_possible[0]) == sum(list_solution_possible[-1])
            if sum_same:
                """
                3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1
                
                Condition 3 is satisfied by the 3rd argument in recursive function call by making the column index the 
                value of the row index parameter in the recursive call.
                
                Notes:
                    list_list_given = list_list_given
                        This matrix should be carried over and should have been modified.
                    
                    index_row = 0
                        Remember we need to satisfy Condition 4 by assigning index i to 0.
                        4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions Pk
                    
                    set_indices_traversed = set()
                        We are going to need a new empty set to possibly build a new solution
                        
                    index_list_solution_possible = index_list_solution_possible + 1,
                        We need to increment this index so that we can meet this condition
                            if len(list_solution_possible) > index_list_solution_possible:
                    
                    list_solution_possible = list_solution_possible
                        This list is carried over so we can potentially make list_solution_possible to be a
                        list_solution (this variable does not exist, it's more of an idea) and add that to
                        list_list_solution.
                    
                    solution_possible = []
                        We need a new empty solution_possible to find a new solution_possible. 
                        It complements index_row being reset to 0 and set_indices_traversed being an empty set.
                    
                    list_list_solution = list_list_solution
                        This list is carried over so we can potentially make list_solution_possible to be a
                        list_solution (this variable does not exist, it's more of an idea) and add that to
                        list_list_solution.
                """
                dfs_recursive(list_list_given,
                              0,
                              index_row_final,
                              set(),
                              index_list_solution_possible + 1,
                              list_solution_possible,
                              [],
                              list_list_solution)

                """
                After the recursive call, list_solution_possible is probably a list_solution so we make a copy of it
                and add it to list_list_solution.
                """
                list_list_solution.append(list_solution_possible.copy())

            """
            Since list_solution_possible was probably 1 solution bigger than it was from before the recursive call,
            we need to remove it to check for any following solutions afterwards.
            """
            list_solution_possible.pop(-1)

        """
        Recursive call WHEN solution_possible HAS A LOWER SIZE compared to list_list_given. Basically, this
        recursive call is only called to build solution_possible.
        """
        if len(solution_possible) < len(list_list_given):
            """
            3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1
            
            Condition 3 is satisfied by the 2nd parameter in recursive call by making index_col the value of index_row.
            
            Notes:
                list_list_given = list_list_given
                    This matrix should be carried over and should have been modified.
                
                index_row = index_col
                    Remember we need to satisfy Condition 3 by assigning index i to index j.
                    3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1
                
                set_indices_traversed = set_indices_traversed
                    We use the same set_indices_traversed
                    
                index_list_solution_possible = index_list_solution_possible
                    We use the same index_list_solution_possible
                
                list_solution_possible = list_solution_possible
                    This list is carried over so we can potentially make list_solution_possible to be a
                    list_solution (this variable does not exist, it's more of an idea) and add that to
                    list_list_solution.
                
                solution_possible = solution_possible
                    We use the same solution_possible because we are not done filling it out. Basically
                        len(solution_possible) == len(list_list_given)
                    so we will have a complete solution_possible
                
                list_list_solution = list_list_solution
                    This list is carried over so we can potentially make list_solution_possible to be a
                    list_solution (this variable does not exist, it's more of an idea) and add that to
                    list_list_solution.
            """
            dfs_recursive(list_list_given,
                          index_col,
                          index_row_final,
                          set_indices_traversed,
                          index_list_solution_possible,
                          list_solution_possible,
                          solution_possible,
                          list_list_solution)

        """
        When done after doing stuff with solution_possible because of solution_possible.append(value) 
        remove that value from solution_possible and return the matrix's position's value to what it was before
            list_list_given[index_row][index_col] = value_from_solution_possible_last_added.
        """

        # Value of the popped from solution_possible
        value_from_solution_possible_last_added = solution_possible.pop(-1)

        # Restore the value in the Matrix from 0 to it's original value
        list_list_given[index_row][index_col] = value_from_solution_possible_last_added

    """
    Remember when a index_row added a index_row to set_indices_traversed so index_row would be unique for a particular
    solution_possible, now we need to remove that row so we are allowed to check this row again but in a different
    order.
    
    Note:
        Disabling
            set_indices_traversed.add(index_row)
            set_indices_traversed.remove(index_row)
        Allows you to re use indices.
    """
    set_indices_traversed.remove(index_row)

    # Return list_list_solution
    return list_list_solution


if __name__ == '__main__':

    # Matrix to solve
    list_given = [[0, 3, 6, 0],
                  [3, 0, 2, 5],
                  [6, 2, 0, 1],
                  [0, 5, 1, 0]]

    # list_given = [[0, 1, 2, 3],
    #               [1, 0, 4, 5],
    #               [2, 3, 0, 6],
    #               [4, 5, 6, 0]]

    list_list_solution = dfs_recursive(list_given)

    # For print spacing
    try:
        length_of_a_row = len(list_list_solution[0][0])
    except IndexError as e:
        print("There are no solutions for the given Matrix")
        length_of_a_row = 1

    print("All Possible Combination of Solutions")
    # Print All possible solutions
    for index, solution in enumerate(list_list_solution):
        # print(i, sum(i))
        # print(f"\t{str(i):<{length_of_a_row * 3 + 1}} {sum(i)}")

        print("Solution Combination {}".format(index + 1))
        for solution_partial in solution:
            print(f"\t{str(solution_partial):<{length_of_a_row * 3 + 1}} {sum(solution_partial)}")
        print()

    # create_callgraph()
