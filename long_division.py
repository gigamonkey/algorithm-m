#!/usr/bin/env python

from math import log, floor, frexp

def integer_decode_float(f):
    s, e = frexp(f)
    m = s * 2 ** 53
    assert(int(m) == m)
    return int(s * 2 ** 53), e - 53

def long_division(dividend, divisor):

    """
    Perform long division to get exact (though possibly repeating)
    decimal representation.
    """

    answer = ""

    until_decimal = floor(log(dividend, 10))
    leading_zeros = True

    # For detecting repeating decimals
    seen = []

    first, rest = divmod(dividend, 10 ** until_decimal)
    r = 0

    while True:

        d, r = divmod(r * 10 + first, divisor)

        # print(f"d: {d}; r: {r}, first: {first}, rest: {rest}; until_decimal: {until_decimal}")

        if leading_zeros and d > 0:
            leading_zeros = False

        if not leading_zeros:
            answer += str(d)

        if until_decimal <= 0:
            if r == 0: break
            if r in seen:
                answer += f"<repeat {len(seen) - seen.index(r)}>"
                break
            else:
                seen.append(r)


        if until_decimal == 0:
            answer += "0." if leading_zeros else "."
            leading_zeros = False

        until_decimal -= 1

        if until_decimal >= 0:
            first, rest = divmod(rest, 10 ** until_decimal)
        else:
            first, rest = rest, 0

    return answer


def show(label, n):
    s, e = integer_decode_float(n)
    print(f"{label:10} {s:b}")
    print(f"{label:10} {long_division(s, 2 ** abs(e))}")



if __name__ == "__main__":

    if True:
        show("0.05", 0.05)
        show("1.05", 1.05)
        show("1.05 - 1", 1.05 - 1)
        show("2.05", 2.05)
        show("2.05 - 2", 2.05 - 2)
        show("4.05", 4.05)
        show("4.05 - 4", 4.05 - 4)
        show("8.05", 8.05)
        show("8.05 - 8", 8.05 - 8)
        show("16.05", 16.05)
        show("16.05 - 16", 16.05 - 16)
        show("32.05", 32.05)
        show("32.05 - 32", 32.05 - 32)
        show("64.05", 64.05)
        show("64.05 - 64", 64.05 - 64)
        show("128.05", 128.05)
        show("256.05", 256.05)

    if False:

        print(long_division(7892, 123))
        print(long_division(78920, 123))
        print(long_division(1500, 25))
        print(long_division(150, 25))
        print(long_division(1, 3))
        print(long_division(2, 3))

    if False:
        print(long_division(7205759403792794, 2 ** 57)) # 0.05
        print(long_division(4728779608739021, 2 ** 52)) # 1.05
        print(long_division(7205759403792800, 2 ** 57)) # 1.05 - 1.0
        print()
        print(long_division(5539427541665710, 2 ** 52))
        print(long_division(8286623314361713, 2 ** 55))
        print()
        print(long_division(5557441940175192, 2 ** 52))
        print(long_division(8430738502437569, 2 ** 55))
        print()
        print(long_division(8646911284551352, 2 ** 57))
        print(long_division(4773815605012726, 2 ** 52))
        print()
        print(long_division(5764607523034235, 2 ** 60))
        print(long_division(4526117625507348, 2 ** 52))

    if False:
        print(long_division(7205759403792794, 144115188075855872))
        print(long_division(7205759403792800 + 1, 144115188075855872))
        print(long_division(4616189618054758, 2 ** 51))
