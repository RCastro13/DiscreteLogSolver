import time
from sympy import primefactors, factorint
from functools import reduce
from sympy.ntheory.residue_ntheory import discrete_log
from math import isqrt
# import sys
# import concurrent.futures

# class TimeoutException(Exception):
#     pass

# def with_timeout(timeout):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             with concurrent.futures.ProcessPoolExecutor() as executor:
#                 future = executor.submit(func, *args, **kwargs)
#                 try:
#                     return future.result(timeout=timeout)
#                 except concurrent.futures.TimeoutError:
#                     print(f"Função '{func.__name__}' excedeu o limite de tempo de {timeout} segundos")
#                     sys.exit(1)  # Finaliza o programa com código de status 1 (erro)
#         return wrapper
#     return decorator

def mdc(a, b):
    """
    :param a: número
    :param b: número
    :return: retorna o mdc entre 'a' e 'b'
    """
    while b:
        a, b = b, a % b
    return a

def mod_exp(base, exp, mod):
    """
    :param base: base do expoente
    :param exp: expoente
    :param mod: módulo 
    :return: retorna 'base' elevado à 'exp' mod 'mod'
    """

    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    return result

def all_primes(n):
    """
    :param n: número a ser fatorado
    :return: retorna 'n' fatorado sem repetição de número (Ex.: 2,2 -> 4)
    """
    fatores = factorint(n)
    resultado = []
    for fator, potencia in fatores.items():
        resultado.extend([fator] * potencia)
    return resultado

def fatoraDistinctPrimes(n):
    """
    :param n: número a ser fatorado
    :return: retorna 'n' fatorado com repetição de fatores
    """
    return primefactors(n)

def fatoraPrimeExp(n):
    """
    :param n: número a ser fatorado
    :return: retorna 'n' fatorado sem repetição de número (Ex.: 2,2 -> 4)
    """
    return all_primes(n)

def millerRabin(n):
    """
    :param n: número recebido na entrada
    :return: retorna true or false caso 'n' seja ou não primo
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
    """
    :param n: número recebido na entrada
    :return: retorna o próximo primo após 'n'
    """
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

    end_time = time.time()
    execution_time = end_time - start_time
    print("Tempo Gasto para achar o menor primo maior que N: ", execution_time)

    return newPrime


def find_generator(p):
    """
    :param p: número primo
    :return: retorna um gerador do grupo multiplicativo Zp
    """
    start_time = time.time()

    #fatoração do modulo -1
    phi = p - 1
    factors = fatoraDistinctPrimes(phi)
    #print("FATORES DE ", phi, ": ", factors)

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

# def baby_step_giant_step(base, a, modulo):
#     start_time = time.time()
    
#     cols = isqrt(modulo) + 1
#     numMod = mod_exp(base, cols, modulo)

#     babySteps = []
#     for i in range(0, cols, 1):
#         babySteps.append((a * pow(base, i)) % modulo)

#     babyStepsMap = {valor: indice for indice, valor in enumerate(babySteps)}
    
#     for j in range(0, cols, 1):
#         giant_step = mod_exp(numMod, j, modulo)
#         if giant_step in babySteps:
#             firstIndex = j
#             secondIndex = babyStepsMap[giant_step]
#             resp = (cols * firstIndex) - secondIndex

#             end_time = time.time()
#             execution_time = end_time - start_time
#             print("Tempo Gasto para não achar o logaritmo discreto: ", execution_time)
#             return resp

#     end_time = time.time()
#     execution_time = end_time - start_time
#     print("Tempo Gasto para não achar o logaritmo discreto: ", execution_time)
    
#     return None

def chinese_remainder_theorem(residues, moduli):
    """
    :param residues: números congruentes no TCR
    :param moduli: módulos do TCR
    :return: retorna o valor de N -> aplicação do TCR
    """

    product = reduce(lambda x, y: x * y, moduli)
    result = 0
    for residue, modulus in zip(residues, moduli):
        p = product // modulus
        #_, inv, _ = egcd(p, modulus)
        inv = mdc(p, modulus)
        result += residue * inv * p
        
    return result % product

#@with_timeout(2)
def pohlig_hellman(base, a, modulo):
    """
    :param base: base do logaritmo discreto
    :param a: será calculado logaritmo de 'a'
    :param modulo: módulo do logaritmo
    :return: retorna o logaritmo discreto de 'a' na base 'base' modulo 'modulo'
    """

    #fatoração do modulo -1 
    phi = modulo - 1
    factors = fatoraPrimeExp(phi)
    print("FATORES DE ", phi, ": ", factors)

    #fatores mapeados com relação a sua potência
    powers = []
    primesWithPower = list(set(map(lambda n: n**factors.count(n), factors)))

    #cálculo das potências a serem utilizadas
    for prime in primesWithPower:
        powers.append(int((modulo-1) / prime))
    
    #cálculo dos intervalos máximos de cada variável
    intervals = []
    for power in powers:
        intervals.append(int((modulo-1) / power))

    #Encontrando os valores n1,n2...nk
    chineseNumbers = []
    tam = len(intervals)
    for j in range (0, tam, 1):
        leftMod = mod_exp(a, powers[j], modulo)
        rightMod = mod_exp(base, powers[j], modulo)
       
        # for i in range(1, intervals[j]):
        #     resp = mod_exp(rightMod, i, modulo)
        #     if resp == leftMod:
        #         chineseNumbers.append(i)
        #         print("FIZ APPEND DE ", i)
        #         break

        dlog = discrete_log(modulo, leftMod, rightMod)
        chineseNumbers.append(dlog)

    resp = chinese_remainder_theorem(chineseNumbers, intervals)

    return resp

n = int(input())
a = int(input())

#Encontrando o menor primo maior que N
newPrime = nextPrime(n)

#Encontrando um gerador de Zn
generator = find_generator(newPrime)

#Retornar o logaritmo discreto de 'a' módulo 'p' na base 'g'
start_time = time.time()
logDiscreto = pohlig_hellman(generator, a, newPrime)
end_time = time.time()
execution_time = end_time - start_time
print("Tempo Gasto para calcular o logaritmo discreto: ", execution_time)

print("O menor primo maior que", n, "é", newPrime)
print("Um gerador de Zn é", generator)
print("O logaritmo de", a, "na base", generator, "modulo", newPrime, "é", logDiscreto)

#entrada: 1234567890123456789012345678901234568123
#saída: 1234567890123456789012345678901234568143

# 933055546577785360646973913576501045393327462 

#entrada: 1399893231659162290225488582844000507360739523965724322028894458428263999898448734134121959642347774293805468812408356373767778163752959999999999999999999999860
#saida: 1399893231659162290225488582844000507360739523965724322028894458428263999898448734134121959642347774293805468812408356373767778163752960000000000000000000000001

# 195104852522228276355183353721555289374816359995982998376425824069640403494691062364260301737810926814837803979318182302657020606186867544174998092704540262400
# 195104852522228276355183353721555289374816359995982998376425824069640403494691062364260301737810926814837803979318182302657020606186867544174998092704540262400