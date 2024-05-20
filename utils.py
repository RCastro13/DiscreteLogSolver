import math

"""
    Retorna um vetor com os primos que fatoram n
    * primos com multiplicidade são repetidos
    Complexidade O(sqrt(n))
    Baseado em https://cp-algorithms.com/algebra/factorization.html#wheel-factorization
"""
def wheel_fact(n):
    factors = []
    for d in [2, 3, 5]:
        while n % d == 0:
            factors.append(d)
            n //= d

    i = 0

    increments = [4, 2, 4, 2, 4, 6, 2, 6]
    for k in range(7, math.ceil(math.sqrt(n)), increments[i]):
        while n % d == 0:
            factors.append(d)
            n //= d
        if i == 8:
            i = 0
    if n > 1:
        factors.append(n)

    return factors
