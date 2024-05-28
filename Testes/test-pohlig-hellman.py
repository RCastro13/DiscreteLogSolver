import Testes.pohligHellman as pohligHellman

def test_pohlig_hellman1():
    resp = pohligHellman.pohlig_hellman(5,8,43)
    assert resp == 15

def test_pohlig_hellman2():
    resp = pohligHellman.pohlig_hellman(5,22,53)
    assert resp == 9

def test_pohlig_hellman3():
    resp = pohligHellman.pohlig_hellman(7,15,131)
    assert resp == 8

def test_pohlig_hellman4():
    resp = pohligHellman.pohlig_hellman(11,50,997)
    assert resp == 411

def test_pohlig_hellman5():
    resp = pohligHellman.pohlig_hellman(7,777,14947)
    assert resp == 832

def test_pohlig_hellman6():
    resp = pohligHellman.pohlig_hellman(7,166,433)
    assert resp == 47

def test_pohlig_hellman7():
    resp = pohligHellman.pohlig_hellman(6,7531,8101)
    assert resp == 6689

def test_pohlig_hellman8():
    resp = pohligHellman.pohlig_hellman(3,525,809)
    assert resp == 309

def test_pohlig_hellman9():
    resp = pohligHellman.pohlig_hellman(7,12,41)
    assert resp == 13

def test_pohlig_hellman10():
    resp = pohligHellman.pohlig_hellman(2,70,131)
    assert resp == 13