from decimal import Decimal, getcontext
import time
import random

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

#precisão do número (530 digitos binarios)
getcontext().prec = 160

n = (input())
n = Decimal(n)

start_time = time.time()
nextPrime(n)
end_time = time.time()

execution_time = end_time - start_time
print("Tempo Gasto: ", execution_time)

#1234567890123456789012345678901234568143