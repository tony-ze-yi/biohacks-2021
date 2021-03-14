import os
import sys
import time
import argparse

import numpy as np

def similar(first, second):
    if len(first) < len(second):
        return similar(second, first)

    if len(second) == 0:
        return len(first)

    prev_row = range(len(second) + 1)
    for i, c1 in enumerate(first):
        current_row = [i+1]
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
    print(args.string1)
    print(args.string2)

    with open(args.string1, "r") as file:
        string1 = file.read().replace("\n", "")

    with open(args.string2, "r") as file:
        string2 = file.read().replace("\n", "")

    print(len(string1))
    str_arr1 = np.array(list(string1))
    str_arr2 = np.array(list(string2))

    start = time.time()
    res = similar(str_arr1, str_arr2)
    end = time.time()
    print(res)
    print("Time: {}".format(end - start))

