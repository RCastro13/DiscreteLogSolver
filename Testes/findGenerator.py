import time
from sympy import primefactors

def mod_exp(base, exp, mod):

    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    return result

def fatoraDistinctPrimes(n):
    return primefactors(n)

def find_generator(p):
    """Encontra um gerador do grupo multiplicativo Zp*."""
    start_time = time.time()

    #fatoração do modulo -1
    phi = p - 1
    factors = fatoraDistinctPrimes(phi)
    print("FATORES DE ", phi, ": ", factors)

    for g in range(2, p):
        is_generator = True
        for factor in factors:
            power = phi//factor
            if mod_exp(g, power, p) == 1:
                is_generator = False
                break
        if is_generator:
            print("GERADOR: ", g)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Tempo Gasto para achar o gerador: ", execution_time)
            return g
    
    return None