import os
import sys
import time

import numpy as np
from numba import jit, njit, prange
from numba import types
from numba.typed import Dict, List
import argparse


def similar(first, second):
    if len(first) < len(second):
        return similar(second, first)

    if len(second) == 0:
        return len(first)

    prev_row = range(len(second) + 1)
    for i, c1 in enumerate(first):
        current_row = [i + 1]
        for j, c2 in enumerate(second):
            insertions = prev_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
    return prev_row[-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "string1", type=str, help="path to first text file containing string"
    )
    parser.add_argument(
        "string2", type=str, help="path to first text file containing string"
    )

    args = parser.parse_args()
    # print(args.string1)
    # print(args.string2)

    with open(args.string1, "r") as file:
        string1 = file.read().replace("\n", "")

    with open(args.string2, "r") as file:
        string2 = file.read().replace("\n", "")

    # print(len(string1))
    str_arr1 = np.array(list(string1))
    str_arr2 = np.array(list(string2))

    # seq
    start = time.time()
    res = similar(str_arr1, str_arr2)
    end = time.time()
    print(res)
    print("Time: {}".format(end - start))

    # parallel
    sigma_seq = {"A": 0, "T": 1, "C": 2, "G": 3}
    sigma = Dict.empty(key_type=types.unicode_type, value_type=types.int64)
    sigma["A"] = 0
    sigma["C"] = 1
    sigma["T"] = 2
    sigma["G"] = 3
    s = ["A", "C", "T", "G"]
    sigma_reverse = List()
    [sigma_reverse.append(a) for a in s]
    u = 4  # A, T, C, G
    m = str_arr1.size
    n = str_arr2.size
    MI = np.zeros((u, n), dtype=int)
    MI_seq = np.zeros((u, n), dtype=int)
    ED = np.zeros((m, n), dtype=int)
    ED_seq = np.zeros((m, n), dtype=int)

    # parallel custom
    start = time.time()
    compute_mi(MI, u, n, sigma_reverse, string2)
    compute_edt(MI, ED, string1, m, n)
    end = time.time()
    print(ED[-1, -1])
    print("Time: {}".format(end - start))

    # seq custom
    start = time.time()
    compute_mi_seq(MI_seq, u, n, sigma_reverse, string2)
    compute_edt_seq(MI_seq, ED_seq, sigma_seq, string1, m, n)
    end = time.time()
    print(ED[-1, -1])
    print("Time: {}".format(end - start))


@njit
def compute_mi(MI, u, n, sigma, str_arr2):
    for i in range(0, u):  # parallelize this
        for j in range(0, n):
            if j == 0 and sigma[i] != str_arr2[j]:
                MI[i, j] = -1
            elif sigma[i] == str_arr2[j]:
                MI[i, j] = j
            else:
                MI[i, j] = MI[i, j - 1]


@njit
def compute_edt(MI, ED, str_arr1, m, n):
    for i in range(0, m):  # str arr1
        for j in range(0, n):  # str arr2, parallelize this
            # mi = MI[sigma[str_arr1[i]], j]
            if str_arr1[i] == "A":
                lmi = MI[0, j]
            elif str_arr1[i] == "C":
                lmi = MI[1, j]
            elif str_arr1[i] == "T":
                lmi = MI[2, j]
            else:
                lmi = MI[3, j]

            if j == 0:
                ED[i, j] = i
            elif i == 0:
                ED[i, j] = j
            elif j == lmi:  # lmi
                ED[i, j] = ED[i - 1, j - 1]
            elif lmi == -1:
                ED[i, j] = min(ED[i - 1, j - 1] + 1, ED[i - 1, j] + 1)
            # elif j < lmi:
            else:
                ED[i, j] = min(
                    ED[i - 1, j - 1] + 1,
                    ED[i - 1, j] + 1,
                    ED[i - 1, lmi - 1] + (j - lmi),
                )
                # else:
                # print("Not supposed to reach here")


def compute_mi_seq(MI, u, n, sigma, str_arr2):
    for i in range(0, u):  # parallelize this
        for j in range(0, n):
            if j == 0 and sigma[i] != str_arr2[j]:
                MI[i, j] = -1
            elif sigma[i] == str_arr2[j]:
                MI[i, j] = j
            else:
                MI[i, j] = MI[i, j - 1]


def compute_edt_seq(MI, ED, sigma, str_arr1, m, n):
    for i in range(0, m):  # str arr1
        for j in range(0, n):  # str arr2, parallelize this
            lmi = MI[sigma[str_arr1[i]], j]
            # if str_arr1[i] == "A":
            #     lmi = MI[0, j]
            # elif str_arr1[i] == "C":
            #     lmi = MI[1, j]
            # elif str_arr1[i] == "T":
            #     lmi = MI[2, j]
            # else:
            #     lmi = MI[3, j]

            if j == 0:
                ED[i, j] = i
            elif i == 0:
                ED[i, j] = j
            elif j == lmi:  # lmi
                ED[i, j] = ED[i - 1, j - 1]
            elif lmi == -1:
                ED[i, j] = min(ED[i - 1, j - 1] + 1, ED[i - 1, j] + 1)
            # elif j < lmi:
            else:
                ED[i, j] = min(
                    ED[i - 1, j - 1] + 1,
                    ED[i - 1, j] + 1,
                    ED[i - 1, lmi - 1] + (j - lmi),
                )


if __name__ == "__main__":
    main()
