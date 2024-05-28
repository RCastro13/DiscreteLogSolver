import time
from sympy import primefactors, factorint
from functools import reduce
from sympy.ntheory.residue_ntheory import discrete_log

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_exp(base, exp, mod):

    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    return result

def all_primes(n):
    fatores = factorint(n)
    resultado = []
    for fator, potencia in fatores.items():
        resultado.extend([fator] * potencia)
    return resultado

def fatoraDistinctPrimes(n):
    return primefactors(n)

def fatoraPrimeExp(n):
    return all_primes(n)

def millerRabin(n):
    """Retorna True se n for provavelmente primo, caso contrário False.
       k é o número de iterações do teste.
    """ 
    #Lista de 60 primos para teste da função
    primeList = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281]
    
    #cálculo de k e m tal que n-1 = 2^k * m
    k, m = 0, n - 1
    while m % 2 == 0:
        m //= 2
        k += 1
    
    #quantidade de a's a ser testado (numIter)
    for a in primeList:
        #a = Decimal(random.randint(2, int(n - 2)))
        if mdc(a,n) != 1:
            return False
        
        x = mod_exp(a, m, n)

        #se x mod n = 1 ou -1 então 'n' é possível primo
        if x == 1 or x == n - 1:
            continue
        
        for i in range(1, k):
            x = mod_exp(x, 2, n)
            #se x mod n = -1 então 'n' é possível primo
            if x == n - 1:
                break
        else:
            return False #SE EU USAR UM ELIF X==1 AO INVES DESSE ELSE DO FOR NÃO FUNCIONA
            
    return True

def nextPrime(n):
    start_time = time.time()

    if n % 2 == 0:
        newPrime = n+1
        
    else:
        newPrime = n+2

    while(True):
        result = millerRabin(newPrime)
        if result == False:
            newPrime = newPrime + 2
        else:
            break
    
    print("NOVO PRIMO: ", newPrime)

    end_time = time.time()
    execution_time = end_time - start_time
    print("Tempo Gasto para achar o menor primo maior que N: ", execution_time)

    return newPrime


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

#Calcula o logaritmo discreto de 'a' na base 'base' modulo 'modulo'
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

# def baby_step_giant_step(base, a, modulo):
#     start_time = time.time()
#     # Calcula o menor inteiro k tal que (modulo - 1) <= k * k
#     m = int(modulo ** 0.5) + 1

#     # Pré-calcular base ^ -m (mod modulo)
#     base_inv_m = pow(base, -m, modulo)

#     # Armazena os valores de base^j (mod modulo) em uma tabela
#     baby_steps = {}
#     x = 1
#     for j in range(m):
#         baby_steps[x] = j
#         x = (x * base) % modulo

#     # Calcula base^(m * i) (mod modulo) para i = 0, 1, ..., m-1
#     x = a
#     for i in range(m):
#         if x in baby_steps:
#             end_time = time.time()

#             execution_time = end_time - start_time
#             print("Tempo Gasto para calcular o logaritmo discreto: ", execution_time)
#             return i * m + baby_steps[x]
#         x = (x * base_inv_m) % modulo

#     end_time = time.time()

#     execution_time = end_time - start_time
#     print("Tempo Gasto para calcular o logaritmo discreto: ", execution_time)
#     return None  # Se não encontrar uma solução

n = int(input())
a = int(input())

#Encontrando o menor primo maior que N
newPrime = nextPrime(n)

#Encontrando um gerador de Zn
generator = find_generator(newPrime)

#Retornar o logaritmo discreto de 'a' módulo 'p' na base 'g'
logDiscreto = pohlig_hellman(generator, a, newPrime)
#logDiscreto = baby_step_giant_step(generator, a, newPrime)
#logDiscreto = discrete_log(newPrime, a, generator)

#SAIDA FINAL (COMENTADA POR ENQUANTO)
print("O menor primo maior que", n, "é", newPrime)
print("Um gerador de Zn é", generator)
print("O logaritmo de", a, "na base", generator, "modulo", newPrime, "é", logDiscreto)

#entrada: 1234567890123456789012345678901234568123
#saída: 1234567890123456789012345678901234568143

#entrada: 1399893231659162290225488582844000507360739523965724322028894458428263999898448734134121959642347774293805468812408356373767778163752959999999999999999999999860
#saida: 1399893231659162290225488582844000507360739523965724322028894458428263999898448734134121959642347774293805468812408356373767778163752960000000000000000000000001


# TEST EXAMPLES(h, g, p)         SOLUTIONS
    #PohlingHellman(18, 2, 29)          11
    #PohlingHellman(166, 7, 433)        47
    #PohlingHellman(7531, 6, 8101)      6689
    #PohlingHellman(525, 3, 809)        309
    #PohlingHellman(12, 7, 41)          13
    #PohlingHellman(70, 2, 131)         13
    #PohlingHellman(525, 2, 809)        no solution
    #PohlingHellman(525, -2, 131)       0