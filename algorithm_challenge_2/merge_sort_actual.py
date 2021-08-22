"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 3/4/2021

Purpose:

Details:

Description:

Notes:
    The Traversal is the the preorder traversal if that helps
        (Root, Left, Right)

IMPORTANT NOTES:

Explanation:

Reference:
    Why Is Merge Sort O(n * log(n))? The Really Really Long Answer.
        Reference:
            https://www.youtube.com/watch?v=alJswNJ4P3U

    geohot / mergesorts
        Reference:
            https://github.com/geohot/mergesorts/blob/master/mergesort.py

"""

from python_code_analyzer.python_code_analyzer import CodeRecorder
from joseph_resources.decorators.callgraph_simple import callgraph, create_callgraph

algorithm_recorder = CodeRecorder()


@algorithm_recorder.decorator_wrapper_callable
@callgraph
def merge_sort(list_given: list) -> list:
    # print()
    # print(list_given)

    """ ----- Split (base cases) ---- """
    # Len == 1 list
    if len(list_given) == 1:
        return list_given

    # Len == 2 List (Mini optimization)
    elif len(list_given) == 2:
        # Sort immediately for 2 items
        if list_given[0] > list_given[1]:
            return [list_given[1], list_given[0]]
        else:
            return list_given

    """ ----- Split call ---- """
    pivot = len(list_given) // 2

    list_left = merge_sort(list_given[:pivot])
    list_right = merge_sort(list_given[pivot:])

    # print("After Splits", list_left, list_right)

    """ ----- 2 Way Merge ---- """

    ignore_counter = 0

    list_new = []
    while True:

        algorithm_recorder.event_iteration_start("i", ignore_counter)
        # If both left and right list still have elements in them
        if len(list_left) > 0 and len(list_right) > 0:
            # If first item from left list <= first item of right list
            if list_left[0] <= list_right[0]:
                """
                Add the left list first element because it's smaller
                Increment left list pivot forward via list slicing
                """
                list_new.append(list_left[0])
                list_left = list_left[1:]
            else:
                """
                Add the right list first element because it's smaller
                Increment right list pivot forward via list slicing
                """
                list_new.append(list_right[0])
                list_right = list_right[1:]

        # If their are items on the left list when right list if empty
        elif len(list_left) > 0:
            # Aad all elements from left list to new list then empty left list
            list_new += list_left
            list_left = []

        # If their are items on the right list when left list if empty
        elif len(list_right) > 0:
            # Aad all elements from right list to new list then empty right list
            list_new += list_right
            list_right = []
        else:
            algorithm_recorder.iteration_scope_end_break()
            break

        ignore_counter += 1
        algorithm_recorder.event_iteration_end()

    print("List new:", list_new)
    return list_new


if __name__ == '__main__':
    # x = [5, 9, 1, 3, 4, 6, 6, 3, 2, 5, 2, 6, 8, 1, 2, 4, 6, 78]
    # x = [3, 5, 9, 2, 6, 1, 6, 7, 23, 3]
    x = [3, 5, 9, 2, 6, 1, 6, 7]
    x = [3, 5, 9, 2, 6, 1, 6, 7, 9]
    x = [3, 5, 9, 2, 6, 1, 6, 7]
    print(merge_sort(x))

    create_callgraph()
    # algorithm_recorder.print()
