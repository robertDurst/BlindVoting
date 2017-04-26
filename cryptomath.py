# Cryptomath Module

import random

def gcd(a, b):
    # Returns the GCD of positive integers a and b using the Euclidean Algorithm.
    x, y = a, b
    while y != 0:
        r = x % y
        x = y
        y = r
    return x

def extendedGCD(a,b):
    # Returns integers u, v such that au + bv = gcd(a,b).
    x, y = a, b
    u1, v1 = 1, 0
    u2, v2 = 0, 1
    while y != 0:
        r = x % y
        q = (x - r) // y
        u, v = u1 - q*u2, v1 - q*v2
        x = y
        y = r
        u1, v1 = u2, v2
        u2, v2 = u, v
    return (u1, v1)

def findModInverse(a, m):
    # Returns the inverse of a modulo m, if it exists.
    if gcd(a,m) != 1:
        return None
    u, v = extendedGCD(a,m)
    return u % m

def RabinMiller(n):
    # Applies the probabilistic Rabin-Miller test for primality.
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while(d % 2 == 0):
        s += 1
        d = d // 2
    # At this point n - 1 = 2^s*d with d odd.
    # Try fifty times to prove that n is composite.
    for i in range(50):
        a = random.randint(2, n - 1)
        if gcd(a, n) != 1:
            return False
        b = pow(a, d, n)
        if b == 1 or b == n - 1:
            continue
        isWitness = True
        r = 1
        while(r < s and isWitness):
            b = pow(b, 2, n)
            if b == n - 1:
                isWitness = False
            r += 1
        if isWitness:
            return False
    return True
            

def isPrime(n):
    # Determines whether a positive integer n is composite or probably prime.
    if n < 2:
        return False
    smallPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                   59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                   127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
                   191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251,
                   257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                   331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
                   401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                   467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557,
                   563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619,
                   631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                   709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
                   797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
                   877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953,
                   967, 971, 977, 983, 991, 997]
    # See if n is a small prime.
    if n in smallPrimes:
        return True
    # See if n is divisible by a small prime.
    for p in smallPrimes:
        if n % p == 0:
            return False
    # Apply Fermat test for compositeness.
    for base in [2,3,5,7,11]:
        if pow(base, n - 1, n) != 1:
            return False
    # Apply Rabin-Miller test.
    return RabinMiller(n)


def findPrime(bits=1024, tries=10000):
    # Find a prime with the given number of bits.
    x = 2**(bits - 1)
    y = 2*x
    for i in range(tries):
        n = random.randint(x, y)
        if n % 2 == 0:
            n += 1
        if isPrime(n):
            return n
    return None
    
def base_b_digits(x, b):
    # Builds a list of the base-b digits of x.
    digits = []
    n = x
    while(n > 0):
        r = n % b
        digits.append(r)
        n = (n - r) // b
    return digits

def isSquare(a, p):
    # Determines whether a is a square modulo p.
    # Assumes that p is an odd prime and a is coprime to p.
    return pow(a, (p - 1) // 2, p) == 1

def modularSqrt(a, p):
    # Returns a square root of a modulo p, if one exists.
    # Assumes that p is a prime congruent to 3 mod 4.
    if isSquare(a, p):
        return pow(a, (p + 1) // 4, p)
    return None

def ellipticCurveAddition(curve, p, points):
    # Adds the points on the given curve over the field F_p.
    # The curve y^2 = x^3 + ax + b is specified by the list [a,b].
    # Individual points are specified as a list [x,y] or as the string 'O'.
    a, b = curve
    P, Q = points
    if P == 'O':
        return Q
    if Q == 'O':
        return P
    x1, y1 = P
    x2, y2 = Q
    if (x1 - x2) % p == 0 and (y1 + y2) % p == 0:
        return 'O'
    if P == Q:
        scalarNum = (3*x1**2 + a) % p
        scalarDen = 2*y1 % p
    else:
        scalarNum = (y2 - y1) % p
        scalarDen = (x2 - x1) % p
    scalar = (scalarNum*findModInverse(scalarDen, p)) % p
    x3 = (scalar**2 - x1 - x2) % p
    y3 = (scalar*(x1 - x3) - y1) % p
    return [x3,y3]

    
def ellipticCurveMultiplication(curve, p, P, n):
    # Returns n*P, where n is a positive integer and P is a point on the curve.
    bits = base_b_digits(n, 2)
    Q = P
    P_multiples = [P]
    for i in range(len(bits) - 1):
        Q = ellipticCurveAddition(curve, p, [Q, Q])
        P_multiples.append(Q)
    R = 'O'
    for i in range(len(bits)):
        if bits[i] == 1:
            R = ellipticCurveAddition(curve, p, [R, P_multiples[i]])
    return R

    
    