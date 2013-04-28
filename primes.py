""" Includes some handy tools for working with prime numbers. """
import sys
import os
import numpy as np
import itertools as it

class Primes32(object):
    """ A class that acts like a list of 32-bit primes. 
    
    This class is written as a dynamically expanding infinite list and hence
    can be modified to generate larger lists of primes, but the memory
    requirements would be a problem.

    Also, the class automatically saves the data to the hard drive and
    will attempt to reload the data before recalculating it on future
    executions. This saves time on computation, but the file is ~1GB.

    The algorithm used is an incremental Sieve of Erastothenes.
    """
    GF = 1.2 # Growth factor.
    MAX_DELTA = 10**8 # The maximum amount by which to grow the list.
    MAX_END = 2**32+1 # The endpoint (non-inclusive) for primality testing.
    MAX_NP = 203280221 # The number of 32-bit primes.

    def __init__(self,
            primes_path=os.path.join(os.path.expanduser('~'),
                'Files', 'gcj-data', 'p32.npy'),
            init_max=MAX_END,
            capacity=MAX_NP
            ):
        """ Initializes the list, either by generating an initial list up to
        the given max_, or by loading the file from the given path, if it is
        found and is valid.
        """
        if primes_path is not None:
            dirname = os.path.dirname(primes_path)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            try:
                self.data = np.load(primes_path)
                self._np = len(self.data)
                self._end = self.data[-1]+2
                return
            except IOError:
                pass
        self.capacity = capacity
        self.data = np.zeros(self.capacity, dtype=np.uint32)
        self.data[0] = 2 # Must contain 2 as we sieve only odd primes
        self._np = 1
        self._end = 3
        try:
            print("Calculating")
            self._extend(init_max)
            if primes_path is not None:
                print("Saving to file")
                np.save(primes_path, self.data)
        except MemoryError as e:
            if primes_path is not None:
                os.remove(primes_path)
            raise e

    def __len__(self):
        """ Returns the number of primes currently in the list. """
        return self._np
            
    def __iter__(self):
        """ Returns an iterator through all primes.
        
        Currently stops after 32 bits, but could be changed to an infinite
        iterator.
        """
        i = 0
        while True:
            for v in self.data[i:self._np]:
                yield int(v)
            i = self._np
            try:
                self._extend()
            except IndexError:
                raise StopIteration

    def __getitem__(self, indices):
        """ Returns the i-th prime, or for a slice/sequence input returns
        a sequence of primes with the given indices.

        Currently has an IndexError for primes past 32 bits.
        """
        if isinstance(indices, slice):
            np = indices.stop
        else:
            try:
                indices = list(indices)
                np = max(indices)+1
            except Exception:
                np = indices+1
        if np >= self._np:            
            self._lengthen(np)
        result = self.data[indices]
        return result.astype(object)

    def __contains__(self, n):
        """ Returns whether the given number is in the list of primes.

        This is done via binary search, and hence is an
        efficient way to test if a number is prime.
        """
        if n > self._end:
            self._extend(n+1)
        idx = self._insert_pos(n)
        return idx < self._np and n == self.data[idx]

    def ip(self, n):
        """ Returns the index that the given number would have in the list.

        If it is a prime, this is precisely the rank of that prime in the 
        sequence of primes.
        """
        if n > self._end:
            self._extend(n+1)
        return self._insert_pos(n)

    def _insert_pos(self, n):
        """ Inner method for returing the insert-position; does not
        auto-expand the list.
        """
        if n <= 2:
            return 0
        lo = 0
        hi = self._np
        while hi - lo > 1:
            mid = (lo+hi)//2
            val = self.data[mid]
            if val == n:
                return mid
            elif val < n:
                lo = mid
            else:
                hi = mid
        return hi

    def between(self, start, stop):
        """ Returns all the primes from start to stop.

        Note that start is inclusive, and stop is exclusive.
        """
        if stop > self._end:
            self._extend(stop)
        return self.data[self._insert_pos(start):
                            self._insert_pos(stop)]

    def _extend(self, limit=None):
        """ Extends the list of primes up to the given limit.

        If no limit is given, the list will grow by an exponential
        factor, but at most by a constant amount to avoid memory troubles.
        """
        if limit is not None and limit <= self._end:
            return
        if limit is None:
            limit = 0
        if limit > self.MAX_END or self._end == self.MAX_END:
            raise IndexError('Cannot handle >32-bit primes')
        limit = max(limit, min(self._end+self.MAX_DELTA,
                               int(self.GF*self._end)+1,
                               self.MAX_END))
        while self._end < limit:
            start = self._end
            stop = min(limit, start+self.MAX_DELTA, self.MAX_END)
            stop += 1 - stop%2
            length = (stop - start)//2
            is_prime = np.ones(length, dtype=bool)
            for p in it.chain(self.data[1:self._np],
                              it.islice(it.count(start, 2), length)):
                p = int(p)
                if p*p >= stop:
                    break
                if p >= start and not is_prime[(p-start)//2]:
                    continue
                first = max(((start+p-1) // (2*p) * 2 + 1), p) * p
                is_prime[(first-start)//2::p] = False
            new_primes = 2*is_prime.nonzero()[0] + start
            new_np = self._np + len(new_primes)
            self.data[self._np:new_np] = new_primes
            self._np = new_np
            self._end = stop
            
    def _lengthen(self, np=0):
        """ Lengthens the list up to the i-th prime. """
        if np > self.capacity:
            raise IndexError('Cannot handle >32-bit primes')           
        while self._np < np:
            self._extend()

def factors(n, pfs=None):
    """ Returns a full list of all factors of the given number. """
    if pfs is None:
        pfs = pf(n)
    factors = [fp[0][0] for fp in factor_pairs(n, pfs, True)]
    factors.sort()
    return factors

def factor_pairs(n, pfs=None, ordered=False):
    """ Returns a list of factor-pairs for the given number.
    
    The factor pairs include both the numbers and their respective
    base-exponent pairs, in terms of the prime factors of the given number.
    """
    if n == 0:
        return
    elif n == 1:
        yield ((1, ()), (1, ()))
        return
    if pfs is None:
        pfs = pf(n)
    pfa = [[p, 0] for (p, mp) in pfs]
    pfb = [list(tp) for tp in pfs]
    values = [1] * len(pfs)
    a, b = 1, n
    while True:
        if ordered or a <= b:
            yield ((a, tuple(tuple(s) for s in pfa)),
                   (b, tuple(tuple(s) for s in pfb))) 
        for i, (p, mp) in enumerate(pfs):
            if pfb[i][1] > 0:
                pfb[i][1] -= 1
                pfa[i][1] += 1
                values[i] *= p
                a *= p
                b //= p
                break
            elif i == len(pfs)-1:
                return
            else:
                pfb[i][1] = mp
                pfa[i][1] = 0
                a //= values[i]
                b *= values[i]
                values[i] = 1

def pf(n, tests=None):
    """ Calculates the prime factorization of the given number,
    as a list of base-exponent pairs, in ascending order.
    """
    if tests is None:
        tests = it.chain(p32, it.count(p32[-1]+2, 2))
    if n <= 1:
        return []
    factors = []
    power_of_2 = (n&-n).bit_length() - 1
    if power_of_2 > 0:
        factors.append((2, power_of_2))
    n >>= power_of_2
    for p in tests:
        if p * p > n:
            break
        count = 0
        while n%p == 0:
            n //= p
            count += 1
        if count:
            factors.append((p, count))
    if n > 1:
        factors.append((n, 1))
    return factors

p32 = Primes32()
