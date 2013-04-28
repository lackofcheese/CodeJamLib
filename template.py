""" A template for Code Jam solutions. Should work with Python 2 and 3."""
from __future__ import print_function, division
try: 
    range = xrange
except NameError:
    pass
import os
import sys

import collections
import functools
import itertools as it
import numpy as np # See http://www.numpy.org/
import gmpy2 # See https://code.google.com/p/gmpy/
#import networkx as nx # See http://networkx.github.io/

# MY MODULES - available at 
sys.path.append(os.path.join(
    os.environ['GOOGLE_DRIVE'], 'Coding', 'GCJ', 'CodeJamLib'))
import proc

def toks_line(f, fun=lambda x: x):
    return [fun(k) for k in f.readline().strip().split()]

def process_first(f):
    num_cases = int(f.readline())
    other_data = None
    return num_cases, other_data

def process_case(f, f_out, case_no, other_data):
    ans = "FAIL"
    print("Case #{}: {}".format(case_no, ans), file=f_out)

def solve():
    return None

if __name__ == '__main__':
    proc.process_input(process_case, process_first)
