""" Some combinatorics functions. """
from __future__ import division, print_function
import gmpy2

def modulo_combs(m, n, p):
    """ Uses Lucas' theorem to calculate the value of m choose n, modulo p. 
    For this to work p must be a prime - the output is indeterminate for
    non-prime values of p.
    """
    product = 1
    while m > 0:
        m, mi = divmod(m, p)
        n, ni = divmod(n, p)
        product = (product * gmpy2.comb(mi, ni)) % p
        if product == 0:
            return 0
    return product

def visit_subsets(s, ls=None, fun=lambda s: (print(s), False)[1]):
    """ Recursively visit subsets of s, applying fun.
    If fun returns True for any set, its subsets will not be visited,
    unless they were already visited as subsets of an earlier set.
    """
    s = frozenset(s)
    if ls is None:
        ls = list(s)

    if fun(s) or not(s):
        return

    for i in range(len(ls)):
        result = visit_subsets(s-{ls[i]}, ls[i+1:], fun=fun)


def reverse(seq, start, end):
    """ In-place reversal of the subseqence seq[start:end].
    From http://blog.bjrn.se/2008/04/lexicographic-permutations-using.html
    """
    end -= 1
    if end <= start:
        return
    while True:
        seq[start], seq[end] = seq[end], seq[start]
        if start == end or start+1 == end:
            return
        start += 1
        end -= 1

def multiset_permutations_from(seq, key=lambda x: x):
    """ Returns a generator that yields unique permutations of seq that 
    are equal to or greater than seq in lexicographical order, based on
    the ordering key given.

    Note that this behaviour means that the sequence itself is always the
    first item to be yielded.

    This is a classical algorithm; as used in C++ std::next_permutation().
    From http://blog.bjrn.se/2008/04/lexicographic-permutations-using.html
    """
    if not seq:
        raise StopIteration
    try:
        seq[0]
    except TypeError:
        raise TypeError("seq must allow random access.")

    first = 0
    last = len(seq)
    seq = list(seq)

    # Yield a copy of the sequence itself.
    yield seq[:]
    
    if last == 1:
        raise StopIteration

    while True:
        next = last - 1

        while True:
            # Step 1.
            next1 = next
            next -= 1
            
            if key(seq[next]) < key(seq[next1]):
                # Step 2.
                mid = last - 1
                while key(seq[next]) >= key(seq[mid]):
                    mid -= 1
                seq[next], seq[mid] = seq[mid], seq[next]
                
                # Step 3.
                reverse(seq, next1, last)

                # Change to yield references to get rid of
                # (at worst) |seq|! copy operations.
                yield seq[:]
                break
            if next == first:
                raise StopIteration
