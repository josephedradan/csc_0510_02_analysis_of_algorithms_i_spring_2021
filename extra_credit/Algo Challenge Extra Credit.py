"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/17/2020

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""

SOMETHING_COUNTER = 0


def doSomething(n):
    global SOMETHING_COUNTER

    n = int(n)
    if n <= 0:
        return

    for i in range(n):
        print("{:>0}".format(i))
        for j in range(n):
            print("{:>10}".format(j))
            for k in range(n):
                print("{:>20}".format(k))

                SOMETHING_COUNTER += 1
                # print("\t\t","something")

    print(50 * "-", "n / 3", 50 * "-")
    doSomething(n / 3)
    print(50 * "-", "n / 3", 50 * "-")
    doSomething(n / 3)
    print(50 * "-", "2 * n / 3", 50 * "-")
    doSomething(2 * n / 3)


if __name__ == '__main__':
    doSomething(10)
    print("Amount of \"something\" called:", SOMETHING_COUNTER)
