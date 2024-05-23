from decimal import Decimal, getcontext
import time
import random
from math import sqrt, ceil
from sympy import primefactors, mod_inverse, factorint
from sympy.ntheory.modular import crt

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_exp(base, exp, mod):
    #result = Decimal(1)
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    # if (n - result) == 1:
    #     result = -1

    return result


def millerRabin(n, primeList):
    """Retorna True se n for provavelmente primo, caso contrário False.
       k é o número de iterações do teste.
    """ 
    
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

def nextPrime(n, primeList):
    if n % 2 == 0:
        newPrime = n+1
        
    else:
        newPrime = n+2

    #newPrime = Decimal(newPrime)
    while(True):
        result = millerRabin(newPrime, primeList)
        if result == False:
            newPrime = newPrime + 2
        else:
            break
    
    print(newPrime)

    return newPrime


#FAZER A PARTE DE RETORNAR UM ELEMENTO DE ORDEM ALTA CASO N ENCONTRE UM GERADOR
def find_generator(p, factors):
    """Encontra um gerador do grupo multiplicativo Zp*."""
    # phi = p - 1
    # #factors = prime_factors(phi)
    # factors = primefactors(phi)
    #print("FATORES DE ", p, ": ", factors)
    # powers = []
    # for factor in factors:
    #     powers.append(phi/factor)
    
    #range até P como fazer já que P é um Decimal (numero mto grande)
    for g in range(2, p):
        is_generator = True
        for factor in factors:
            power = phi/factor
            if mod_exp(g, power, p) == 1:
                is_generator = False
                break
        if is_generator:
            return g
        
    #solução imediata mas sem certeza ----------------> conferir
    #gen = find_generator(p-1)
    #print("Não achei gerador inicialmente, mas um número com ordem alta é ", gen)
    
    return None

def extended_gcd(a, b):
    """Algoritmo de Euclides Estendido para encontrar o inverso modular."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Encontra o inverso modular de a módulo m."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("O inverso modular não existe.")
    else:
        return x % m

#Calcula o logaritmo discreto de 'a' na base 'base' modulo 'modulo'
def pohlig_hellman(base, a, modulo, factors):
    """Implementa o algoritmo Pohlig-Hellman para calcular logaritmo discreto."""
    
    powers = []
    primesWithPower = list(set(map(lambda n: n**factors.count(n), factors)))
    print(primesWithPower)

    for prime in primesWithPower:
        print(modulo-1, "/", prime, " = ", modulo/prime)
        powers.append((modulo-1)/prime)

    print("POTENCIAS: ", powers)

    
    
    # for i in range(len(factors)):
    #     n = 


    # logs = []
    # moduli = []
    
    # for q in factors:
    #     e = factors.count(q)
    #     q_power_e = pow(q, e)
    #     moduli.append(q_power_e)
        
    #     x = 0
    #     a_q = mod_exp(int(a), int(n // q), modulo)
    #     g_q = mod_exp(int(base), int(n // q), modulo)
        
    #     for i in range(e):
    #         g_inv = mod_inverse(mod_exp(int(g_q), x, modulo), modulo)
    #         a_i = mod_exp(int(a_q * g_inv), int(n // pow(q, (i + 1))), modulo)
    #         for j in range(q):
    #             if mod_exp(int(g_q), j, modulo) == a_i:
    #                 x += j * pow(q, i)
    #                 break
        
    #     logs.append(x)
    
    # # Resolver o sistema de congruências usando o teorema chinês do resto
    # log_a = crt(moduli, logs)[0]
    


    return None

def all_primes(n):
    fatores = factorint(n)
    resultado = []
    for fator, potencia in fatores.items():
        resultado.extend([fator] * potencia)
    return resultado

#precisão do número (530 digitos binarios)
getcontext().prec = 160

#fazer testes com quantidades diferentes de numeros primos
primeList = [2,3,5,7,11,13,17,19,23]

n = int(input())
#n = Decimal(n)
a = int(input())

#Encontrando o menor primo maior que N
start_time = time.time()
#newPrime = Decimal(nextPrime(n, primeList))
newPrime = nextPrime(n, primeList)
end_time = time.time()

execution_time = end_time - start_time
print("Tempo Gasto para achar o menor primo maior que N: ", execution_time)

phi = newPrime - 1
factors = primefactors(phi)
#print("TOTAL: ", len(factors))
print("FATORES DE ", phi, ": ", factors)

#Encontrando um gerador de Zn
start_time = time.time()
generator = find_generator(newPrime, factors)
end_time = time.time()

print("GERADOR: ", generator)
execution_time = end_time - start_time
print("Tempo Gasto para achar o gerador: ", execution_time)

#factors = all_primes(int(phi))
factors = all_primes(phi)
print("FATORES DE ", phi, ": ", factors)

#Retornar o logaritmo discreto de 'a' módulo 'p' na base 'g'
start_time = time.time()
log_a = pohlig_hellman(generator, a, newPrime, factors)
end_time = time.time()

execution_time = end_time - start_time
print("Tempo Gasto para calcular o logaritmo discreto: ", execution_time)
#print(f"O logaritmo discreto de {a} na base {generator} módulo {newPrime} é {log_a}")

#entrada: 1234567890123456789012345678901234568123
#saída: 1234567890123456789012345678901234568143


# TEST EXAMPLES(h, g, p)         SOLUTIONS
    #PohlingHellman(18, 2, 29)          11
    #PohlingHellman(166, 7, 433)        47
    #PohlingHellman(7531, 6, 8101)      6689
    #PohlingHellman(525, 3, 809)        309
    #PohlingHellman(12, 7, 41)          13
    #PohlingHellman(70, 2, 131)         13
    #PohlingHellman(525, 2, 809)        no solution
    #PohlingHellman(525, -2, 131)       0