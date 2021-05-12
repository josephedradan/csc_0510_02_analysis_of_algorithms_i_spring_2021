"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/4/2021

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""

from pycode_recorder.code_recorder import AlgorithmRecorder

algorithm_recorder = AlgorithmRecorder()


@algorithm_recorder.decorator_wrapper_callable  # Ignore me
def algorithm_challenge_01(string, n):
    count = 0

    i = 1
    while i <= n:
        algorithm_recorder.iteration_scope_start("For loop Outer (i)", i)  # Ignore me
        # print(i)

        j = 1
        while j <= i:
            algorithm_recorder.iteration_scope_start("For loop Inner (j)", j)  # Ignore me
            # print("\t", j)

            print(string)

            j = j * 2

            count += 1
            algorithm_recorder.iteration_scope_end_none()  # Ignore me

        i = i + 1
        algorithm_recorder.iteration_scope_end_none()  # Ignore me

    print(f"Count: {count}")


if __name__ == '__main__':
    # algorithm_challenge_01("hello CSC510-01 class”", 5)
    # print()

    algorithm_challenge_01("hello CSC510-01 class”", 16)
    print()

    # 1 2 3 4 5  6  7  8
    # 1 3 5 8 11 14 17 21

    algorithm_recorder.print()
