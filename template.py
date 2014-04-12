#! /usr/bin/env python
""" A template for Code Jam solutions. Should work with Python 2 and 3."""
from __future__ import print_function, division
try:
    range = xrange
except NameError:
    pass
import collections
import functools
import itertools as it
import numpy as np # See http://www.numpy.org/
import gmpy2 # See https://code.google.com/p/gmpy/
#import networkx as nx # See http://networkx.github.io/

import os
import sys
# MY MODULES - available at https://github.com/lackofcheese/CodeJamLib/
sys.path.append(os.path.join(
    os.environ['GOOGLE_DRIVE'], 'Coding', 'GCJ', 'CodeJamLib'))
import codejam_io

def toks_line(f_in, fun=lambda x: x):
    return [fun(k) for k in f_in.readline().strip().split()]

def process_first(f_in):
    num_cases = int(f_in.readline())
    other_data = None
    return num_cases, other_data

def process_case(f_in, f_out, case_no, other_data=None):
    ans = "FAIL"
    print("Case #{}: {}".format(case_no, ans), file=f_out)

def solve():
    return None

if __name__ == '__main__':
    codejam_io.process_input(process_case, process_first, __file__)
