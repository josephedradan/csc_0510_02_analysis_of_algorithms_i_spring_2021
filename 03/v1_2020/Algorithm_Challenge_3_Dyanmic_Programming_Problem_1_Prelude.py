"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 11/2/2020

Purpose:
    Prelude to the solution for
    CSC510_Section_04_Analysis_of_Algorithms_Algorithm_Challenge_2_Dividing_and_Conquering_Problem_1

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""
import itertools

x = [1, 2, 3]
z = list(itertools.product(*[x for i in range(len(x))]))  # [[1, 2, 3], [1, 2, 3], [1, 2, 3]]


# def sum(x):
#     return reduce(lambda i, y: i + y, x)


def fuck(x):
    value = 0
    temp = []
    for i in x:
        value = value + i
        if value > 3:
            break
        temp.append(i)
    return temp


if __name__ == '__main__':
    print(z)
    print()
    for i in z:
        result = fuck(i)
        if sum(result) == 3:
            print(result)
