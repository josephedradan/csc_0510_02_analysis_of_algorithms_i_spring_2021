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

eqn_log = lambda x: math.log(math.factorial(x), 2)
counter = 0

while True:
    if (x := eqn_log(counter)) > counter:
        print(True)
        print(f"eqn_log: {x} n:{counter}")
        break

    counter += 1
