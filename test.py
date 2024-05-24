import main

#retorna True se o numero é primo
def test_miller_rabin():
    resp = main.millerRabin()
    assert resp == True

#retorna o menor primo maior que o recebido
def test_next_prime():
    resp = main.nextPrime()
    assert resp == 331

#retorna um gerador do grupo multiplicativo Zp
def test_find_generator():
    resp = main.find_generator()
    assert resp == 2

#retorna o logaritmo discreto de 'a' na base 'base' modulo 'modulo'
def test_pohlig_hellman():
    resp = main.pohlig_hellman()
    assert resp == 353