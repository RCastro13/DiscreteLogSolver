import time
from functools import reduce
from sympy.ntheory.residue_ntheory import discrete_log
from sympy import factorint

#Calcula o logaritmo discreto de 'a' na base 'base' modulo 'modulo'

def all_primes(n):
    fatores = factorint(n)
    resultado = []
    for fator, potencia in fatores.items():
        resultado.extend([fator] * potencia)
    return resultado

def fatoraPrimeExp(n):
    return all_primes(n)

def mod_exp(base, exp, mod):

    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    return result

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x

def chinese_remainder_theorem(residues, moduli):
    product = reduce(lambda x, y: x * y, moduli)
    result = 0
    for residue, modulus in zip(residues, moduli):
        p = product // modulus
        _, inv, _ = egcd(p, modulus)
        result += residue * inv * p
    return result % product

def pohlig_hellman(base, a, modulo):
    """Implementa o algoritmo Pohlig-Hellman para calcular logaritmo discreto."""
    
    start_time = time.time()

    #fatoração do modulo -1 
    phi = modulo - 1
    factors = fatoraPrimeExp(phi)
    print("FATORES DE ", phi, ": ", factors)

    powers = []
    primesWithPower = list(set(map(lambda n: n**factors.count(n), factors)))
    print("LISTA: ", primesWithPower)

    for prime in primesWithPower:
        print(modulo-1, "/", prime, " = ", modulo/prime)
        powers.append(int((modulo-1)/prime))

    print("POTENCIAS: ", powers)
    
    intervals = []
    for power in powers:
        intervals.append(int((modulo-1) / power))

    print("INTERVALOS: ", intervals)

    chineseNumbers = []
    tam = len(intervals)
    #print("TAMANHO: ", tam)
    for j in range (0, tam, 1):
        #print("J: ", j)
    
        leftMod = mod_exp(a, powers[j], modulo)
        rightMod = mod_exp(base, powers[j], modulo)
        #print("RESULTADO DEVE SER leftmod: ", leftMod, " rightmod: ", rightMod, " NO INTERVALO DE ", intervals[j] - 1)
       
        #QUERO Q ", rightMod, "ELEVADO A i MODULO ", modulo, "SEJA IGUAL A ", leftMod)
        # for i in range(1, intervals[j]):
            
        #     resp = mod_exp(rightMod, i, modulo)
        #     if resp == leftMod:
        #         chineseNumbers.append(i)
        #         print("FIZ APPEND DE ", i)
        #         break

        dlog = discrete_log(modulo, leftMod, rightMod)
        chineseNumbers.append(dlog)
        print("ACHEI ", dlog)
    
    print("NUM MODS: ", chineseNumbers)

    resp = chinese_remainder_theorem(chineseNumbers, intervals)
    print(f"A solução é ", resp)

    end_time = time.time()

    execution_time = end_time - start_time
    print("Tempo Gasto para calcular o logaritmo discreto: ", execution_time)

    return resp