from decimal import Decimal, getcontext
import time
import random
from math import sqrt 

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_exp(base, exp, mod):
    result = Decimal(1)
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    # if (n - result) == 1:
    #     result = -1

    return result


def millerRabin(n, numIter):
    """Retorna True se n for provavelmente primo, caso contrário False.
       k é o número de iterações do teste.
    """ 
    
    #cálculo de k e m tal que n-1 = 2^k * m
    k, m = 0, n - 1
    while m % 2 == 0:
        m //= 2
        k += 1
    
    #quantidade de a's a ser testado (numIter)
    for _ in range(numIter):
        a = Decimal(random.randint(2, int(n - 2)))
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
    if n % 2 == 0:
        newPrime = n+1
        
    else:
        newPrime = n+2

    newPrime = Decimal(newPrime)
    while(True):
        result = millerRabin(newPrime, 5)
        if result == False:
            newPrime = newPrime + 2
        else:
            break
    
    print(newPrime)

def prime_factors(n):
    """Retorna os fatores primos de n."""
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    for i in range(3, int(sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.add(i)
            n //= i
    if n > 2:
        factors.add(n)
    return factors

#FAZER A PARTE DE RETORNAR UM ELEMENTO DE ORDEM ALTA CASO N ENCONTRE UM GERADOR
def find_generator(p):
    """Encontra um gerador do grupo multiplicativo Zp*."""
    phi = p - 1
    factors = prime_factors(phi)
    print("FATORES DE ", p, ": ", factors)
    # powers = []
    # for factor in factors:
    #     powers.append(phi/factor)
    
    #range até P como fazer já que P é um Decimal (numero mto grande)
    for g in range(2, int(p)):
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

#precisão do número (530 digitos binarios)
getcontext().prec = 160

n = (input())
n = Decimal(n)

#Encontrando o menor primo maior que N
start_time = time.time()
nextPrime(n)
end_time = time.time()

execution_time = end_time - start_time
print("Tempo Gasto para achar o menor primo maior que N: ", execution_time)

#Encontrando um gerador de Zn
start_time = time.time()
g = find_generator(n)
end_time = time.time()

print("GERADOR: ", g)
execution_time = end_time - start_time
print("Tempo Gasto para achar(ou não) o gerador: ", execution_time)

#entrada: 1234567890123456789012345678901234568123
#saída: 1234567890123456789012345678901234568143