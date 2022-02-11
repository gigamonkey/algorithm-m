#!/usr/bin/env python

from dataclasses import dataclass

@dataclass
class Float:
    "Represent a floating point number."
    significand: int
    exponent: int


upper = 2 ** 53
lower = 2 ** 52


# Based on algorithm M from "How to Read Floating Point Numbers
# Accurately" by William D Clinger but hardwired to translate from
# base 10 to base 2 with a 53 bit significand, a la IEEE double
# precision. This is straightforward and correct but not very
# efficient as it relies on a lot of arbitrary precision integer math.
# Clinger's paper is about how to go from this to something much more
# efficient.

def algorithm_m(f, e):
    """
    Find the nearest double precision float to the value specified by
    f * 10^e where f and e are integers. For instance 1.05 would be
    f=105, e=-2.
    """

    # Find u, v, and k, such that f * 10^e = u/v * 2^k and u/v is in
    # the range [lower, upper). Start by setting u, v, and k such that
    # the equation is trivially satisfied with k = 0 and then adjust u
    # or v until u // v is in the correct range, adjusting k to
    # maintain the equality. When done, create a float coresponding to
    # the three values.

    if e < 0:
        u = f
        v = 10 ** -e
    else:
        u = f * 10 ** e
        v = 1

    k = 0

    while True:

        q = u // v

        if q < lower:
            u *= 2
            k -= 1
        elif q >= upper:
            v *= 2
            k += 1
        else:
            return ratio_to_float(u, v, k)


def ratio_to_float(u, v, k):
    """
    Make the float that is closest to the value u/v * 2^k, rounding to
    even.
    """

    # Since v is the denominator of our fraction rounding is based on
    # r/v but we want to keep all our calculations in terms of just
    # integers so we use these identities:

    # r/v < 1/2 ≡ r < v/2 ≡ r * 2 < v
    # r/v > 1/2 ≡ r > v/2 ≡ r * 2 > v

    q = u // v
    r2 = (u % v) * 2
    z = Float(q, k)

    if r2 < v:
        # Round down
        return z
    elif r2 > v:
        # Round up
        return nextfloat(z)
    else:
        # Round to even.
        return z if q % 2 == 0 else nextfloat(z)


def nextfloat(z):
    """
    Compute the next float, i.e. the one with a significand one
    greater than the current. The only trick is when the the
    significand is already the largest possible we need to wrap around
    to the smallest possible and increment the exponent.
    """

    plus_one = z.significand + 1

    if plus_one == upper:
        return Float(lower, z.exponent + 1)
    else:
        return Float(plus_one, z.exponent)


def to_bits(n):
    "Translate an integer to a string showing it as a 53-bit number."
    return f"{n:0>53b}"



# The (FP)^3 algorithm from "How to Print Floating-Point Numbers
# Accurately" by Guy L. Steel Jr and Jon L White.

def fp_3(f):

    """
    Given a floating point fraction f, 0 <= f < 1, turn it into the
    shortest representation as decimal digits that will read back to
    the same fraction.
    """

    digits = ""

    k = 0
    R = f
    M = Fraction(1, 2 ** 53) / 2

    while True:
        k += 1
        U = R // 10
        R = (R * 10) % 1
        M *= 10
        if not (R >= M and R <= 1 - M):
            break
        digits += str(U)

    if R <= 1/2:
        digits += str(U)
    else:
        digits += str(U + 1)

    return digits, k



if __name__ == "__main__":

    print(algorithm_m(5, -2))
