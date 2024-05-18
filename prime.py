import sympy

# Número fornecido
n = 1234567890123456789012345678901234568124

# Encontrar o próximo primo após n
proximo_primo = sympy.nextprime(n)

print(f"O próximo primo após {n} é {proximo_primo}")
