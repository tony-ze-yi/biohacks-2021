import os
import sys
import time
import argparse

import numpy as np

def similar(str1, str2):
    m = len(str1)
    n = len(str2)

    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
    return dp[m][n]

def run_for_timing(stringA, stringB) -> float:

    with open(stringA, "r") as file:
        string1 = file.read().replace("\n", "")

    with open(stringB, "r") as file:
        string2 = file.read().replace("\n", "")
    str_arr1 = np.array(list(string1))
    str_arr2 = np.array(list(string2))

    start = time.time()
    res = similar(str_arr1, str_arr2)
    end = time.time()
    return end - start

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "string1", type=str, help="path to first text file containing string"
    )
    parser.add_argument(
        "string2", type=str, help="path to first text file containing string"
    )

    args = parser.parse_args()

    with open(args.string1, "r") as file:
        string1 = file.read().replace("\n", "")

    with open(args.string2, "r") as file:
        string2 = file.read().replace("\n", "")

    str_arr1 = np.array(list(string1))
    str_arr2 = np.array(list(string2))

    start = time.time()
    res = similar(str_arr1, str_arr2)
    end = time.time()
    print(res)
    print("Time: {}".format(end - start))

if __name__ == '__main__':
    main()