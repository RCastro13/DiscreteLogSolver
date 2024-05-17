# calcula base ^ exp mod n
def mod(base, exp, n):
    if exp == 1: return base % n

    i = 2 

    while (i < exp):
        base = pow(base, 2) % n
        i <<= 1

    return pow(base, exp - (i >> 1)) % n
