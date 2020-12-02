"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 11/18/2020

Purpose:
    Solve sum of values from each rows of a matrix to equal a target value with recursive calls under certain
    conditions.

Details:

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
    Conditions 1 partially, 2, 3, 4 are satisfied

        Condition 1 is partially met because the condition is ONLY SATISFIED when the Recursive call is called again
        Condition 5 is NOT MET because we don't have a target we have MIN or MAX

        Conclusion:
            Make a new file because Condition 5 and 1 need to be satisfied properly.

Explanation:

Reference:

"""

# from josephs_resources.decorators.v1.callgraph_simple import callgraph, create_callgraph
from typing import List


# Recursive call
# @callgraph
def dfs_recursive(list_list_given: List[List[int]], target: int, index_row: int = 0,
                  solution_possible: List[int] = None,
                  list_solution: List[List[int]] = None) -> List[List[int]]:
    """
    Solve sum of values from each rows of a matrix to equal a target value with recursive calls under certain
    conditions.

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
    for index_col, value in enumerate(row_current):

        """
        2. The integer in M(i, j) is not zero
        
        Condition 2 is satisfied by checking if the value at the given row_current and index_col is 0. Note that the
        value at this position could have been initially 0 OR it is set to zero by the following code after the code
        modifying target.
        """
        if value == 0:
            continue

        # New target value
        target -= value

        """
        1. All the indexes i and j for that sum of P_k are unique
        2. The integer in M(i, j) is not zero

        Condition 1 is Partially satisfied by setting position (i, j) in Matrix to 0 which will prevent duplicate
        positions (i, j) from passing due to Condition 2 preventing values of 0 to pass. However, the values are
        changed in the matrix, this does not mean you are prevented from revisiting this row again for the current
        solution_possible which is why Condition 1 is not Completely satisfied.  
        """
        list_list_given[index_row][index_col] = 0

        # Add the value from the current row to the list of possible solutions
        solution_possible.append(value)

        # DEBUG PRINTING
        # print("Row: {}".format(row_current))
        # print("Partial: {}".format(list_solution_possible))
        # print("Target: {}".format(target))
        # print("Row Index: {}".format(index_row))
        # print()

        """
        VERY IMPORTANT NOTE:
            THE TEACHER DOES NOT GIVE A TARGET SO THE BELOW IS WRONG BECAUSE YOU KNEW THE TARGET FROM THE BEGINNING
            AND SOME LUCK FROM Condition 1 GOT YOU THE SOLUTIONS.
            
        NOTE: 
            REMOVING THE CONDITION if target == 0: WILL GET CLOSER TO THE ACTUAL ANSWER THAT THE TEACHER WANTS
            BUT STILL Condition 1 IS STILL WRONG BECAUSE INDICES ARE NOT UNIQUE
            
        """
        # Found solution is when target == 0
        if target == 0:

            """
            4. Index i in M(i, j)_1 and index j in M(i, j)_m must be zero for all the solutions P_k
            
            Condition 4 is now Completely satisfied by the below condition by checking if the length of 
            solution_possible equals the length of list_list_given 
            (This means we have used EVERY row in list_list_given) 
            and the last column index's value in solution_possible is 0 AKA index j is 0.  
            """
            if len(solution_possible) == len(list_list_given) and index_col == 0:
                # If solution is found then add it to list of solutions
                list_solution.append(solution_possible.copy())

        # Recursive call ONLY WHEN solution_possible HAS A LOWER SIZE compared to list_list_given
        if len(solution_possible) < len(list_list_given):
            """
            3. Index j in M(i, j)_x must be the same as index i in M(i, j)_x+1
            
            Condition 3 is satisfied by the 3rd argument in recursive function call by making the column index the 
            value of the row index parameter in the recursive call.
            """
            dfs_recursive(list_list_given, target, index_col, solution_possible, list_solution)

        """
        When done after doing stuff with solution_possible because of solution_possible.append(value) 
        remove that value from solution_possible and return the matrix's position's value to what it was before
            list_list_given[index_row][index_col] = value_from_solution_possible_last_added.
        and restore target to it's original value before being changed by this loop
            target += value_from_solution_possible_last_added
        """
        # Value of the popped from solution_possible
        value_from_solution_possible_last_added = solution_possible.pop(-1)

        # Restore target to its original value before its change in this for loop
        target += value_from_solution_possible_last_added

        # Restore the value in the Matrix from 0 to it's original value
        list_list_given[index_row][index_col] = value_from_solution_possible_last_added

    # Return list_solution
    return list_solution


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
    length_of_a_row = len(list_solution[0])

    print("All possible solutions")
    # Print All possible solutions
    for i in list_solution:
        # print(i, sum(i))
        print(f"\t{str(i):<{length_of_a_row * 3 + 1}} {sum(i)}")
    print()

    # create_callgraph()
