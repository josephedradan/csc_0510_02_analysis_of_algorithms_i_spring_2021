"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 11/2/2020

Purpose:
    Prelude to
    CSC510_Section_04_Analysis_of_Algorithms_Algorithm_Challenge_4_Backtracking_Problem_1_Recursive_DFS_Correct
    
Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""
list_temp = [9, 8, 5, 3]

# dict_length_cost = {index + 1: value for index, value in enumerate(list_temp)}

dict_length_list_indices = {}


def solver(list_temp, target, list_temp_solution=[], solution_dict=None):
    print()
    print(f"Target {target}")
    if solution_dict is None:
        solution_dict = {}

    # list_temp_new = list_temp.copy()
    list_temp_new = list_temp[:target]
    print(list_temp_new)

    # if target == 1:
    #     return

    for i in range(target):

        cost = list_temp_new[i]

        # if solution_dict.get(target) is None:
        #     solution_dict[target] = []
        #     solution_dict[target].append(i + 1)

        print(f"index: {i}")
        target_new = target - 1

        list_temp_solution.append(i)

        print("list_temp_solution (index)", list_temp_solution)

        if target_new == 0:
            list_temp_solution.clear()
            print("-" * 100)
        if target_new <= 0:
            return

        solver(list_temp_new, target_new, list_temp_solution, solution_dict)


if __name__ == '__main__':
    solver(list_temp, 3)
