import random
import decimal
from decimal import Decimal, getcontext

# Configurar a precisão necessária (ajuste conforme necessário)
getcontext().prec = 1024 

def miller_rabin(n, k):
    """Retorna True se n for provavelmente primo, caso contrário False.
       k é o número de iterações do teste.
    """
    n = Decimal(n)  
    
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    #d tal que d * 2^r = n-1
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    
    def mod_exp(base, exp, mod):
        result = Decimal(1)
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            base = (base * base) % mod
            exp //= 2
        return result
    
    for _ in range(k):
        a = Decimal(random.randint(2, int(n - 2)))
        x = mod_exp(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

n = 1234567890123456789012345678901234568124

k = 5

if n % 2 == 0:
    n = n + 1

while miller_rabin(n,k) == False:
    n = n + 2


if miller_rabin(n, k):
    print(f"{n} é provavelmente primo.")
else:
    print(f"{n} não é primo.")

# def millerRabin(n: Decimal, k:int, m:int):
    
#     vecA = []
#     for i in range(1, 6, 1): 
#         vecA.append(Decimal(random.randint(2, int(n - 2))))

#     for a in vecA:
#         if mdc(a, n) != 1:
#             print("Errei no mdc entre ", a , " e ", n)
#             return False
#         else:
#             x = mod_pow(a, m, n)

#             if mod(x,n) == 1 or mod(x,n) == -1:
#                 continue
#             else:
#                 for j in range(1, k, 1):
#                     x = x * x

#                     if mod(x, n) == -1:
#                         j = k-1
#                         break
#                     elif mod(x, n) == 1:
#                         print("Errei no mod j")
#                         return False
#                     else:
#                         continue

#     return True

def mod_pow(base, exp, n):
    if n == 1: return 0 

    i = 0
    c = 1 # acumula os resultados
    while (i < exp):
        c = base * c % n
        i += 1

    return c