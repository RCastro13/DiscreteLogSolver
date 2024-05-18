# calcula base ^ exp mod n utilizando o método direto
# O(exp)
# uma implementação ainda mais eficiente - O(log exp) - utiliza o right-to-left binary method
# https://en.wikipedia.org/wiki/Modular_exponentiation#Right-to-left_binary_method
def mod_pow(base, exp, n):
    if n == 1: return 0 

    i = 0
    c = 1 # acumula os resultados
    while (i < exp):
        c = base * c % n
        i += 1

    return c
