"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/19/2021

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""
import math


def algorithm_challenge_01_optimized_v1(string, n):
    amount = (n * (math.floor(math.log(n, 2)) + 1)) - 2 ** (math.floor(math.log(n, 2)) + 1) + math.floor(math.log(n, 2)) + 1 + 1
    print(amount)  # Ignore me
    for i in range(amount):
        print(string)


if __name__ == '__main__':
    algorithm_challenge_01_optimized_v1("hello CSC510-01 class”", 5)
    print()
    algorithm_challenge_01_optimized_v1("hello CSC510-01 class”", 8)
