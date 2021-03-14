import time

import numpy as np
from numba import jit, njit, prange
from numba import types
from numba.typed import Dict, List

# constants
with open("sars.txt", 'r') as sars_file:
    sars = sars_file.read().replace('\n', '')

with open("covid19.txt", 'r') as covid_file:
    covid = covid_file.read().replace('\n', '')

@jit
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
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
    return dp[m][n]


def similar_seq(str1, str2):
    m = len(str1)
    n = len(str2)

    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
    return dp[m][n]


@njit(parallel=True)
def compute_mi(MI, u, n, sigma, str_arr2):
    for i in prange(0, u):  # parallelize this
        for j in range(0, n):
            if j == 0 and sigma[i] != str_arr2[j]:
                MI[i, j] = -1
            elif sigma[i] == str_arr2[j]:
                MI[i, j] = j
            else:
                MI[i, j] = MI[i, j - 1]


@njit(parallel=True)
def compute_edt(MI, ED, str_arr1, m, n):
    for i in range(0, m):  # str arr1
        for j in prange(0, n):  # str arr2, parallelize this
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
            # lmi = MI[sigma[str_arr1[i]], j]
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


def regular_alg(string1, string2):
    # seq
    start = time.time()
    res = similar_seq(string1, string2)
    end_seq = time.time()
    print(res)
    print("Time: {}".format(end_seq - start))
    seq_runtime = end_seq - start

    # parallel
    start = time.time()
    res = similar(string1, string2)
    end = time.time()
    print(res)
    print("Time: {}".format(end - start))
    parallel_runtime = end - start
    return parallel_runtime, seq_runtime


def custom_alg(string1, string2):
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
    m = len(string1)
    n = len(string2)
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
    parallel_runtime = end - start

    # seq custom
    start = time.time()
    compute_mi_seq(MI_seq, u, n, sigma_reverse, string2)
    compute_edt_seq(MI_seq, ED_seq, sigma_seq, string1, m, n)
    end_seq = time.time()
    print(ED[-1, -1])
    print("Time: {}".format(end_seq - start))
    seq_runtime = end_seq - start

    return parallel_runtime, seq_runtime


if __name__ == "__main__":
    pass
