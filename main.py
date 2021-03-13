import os
import sys

import numpy as np
from numba import jit
import argparse

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

with open(args.string1, 'r') as file:
    string1 = file.read().replace('\n', '')

with open(args.string1, 'r') as file:
    string2 = file.read().replace('\n', '')

print(len(string1))
str_arr1 = np.char.array(string1)

u = 4 # A, T, C, G