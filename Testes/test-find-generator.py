import Testes.findGenerator as findGenerator

def test_find_generator1():
    resp = findGenerator.find_generator(17)
    assert resp == 3

def test_find_generator2():
    resp = findGenerator.find_generator(75689)
    assert resp == 3

def test_find_generator3():
    resp = findGenerator.find_generator(1234567890123456789012345678901234568143)
    assert resp == 3

def test_find_generator4():
    resp = findGenerator.find_generator(1399893231659162290225488582844000507360739523965724322028894458428263999898448734134121959642347774293805468812408356373767778163752960000000000000000000000001)
    assert resp == 131

def test_find_generator5():
    resp = findGenerator.find_generator(101)
    assert resp == 2

def test_find_generator6():
    resp = findGenerator.find_generator(281)
    assert resp == 3

def test_find_generator7():
    resp = findGenerator.find_generator(1234567890123456789012345678901234567890000001)
    assert resp == 13

def test_find_generator8():
    resp = findGenerator.find_generator(13)
    assert resp == 2

def test_find_generator9():
    resp = findGenerator.find_generator(875638204027394763524467537)
    assert resp == 13

def test_find_generator10():
    resp = findGenerator.find_generator(1000000000000000003)
    assert resp == 2