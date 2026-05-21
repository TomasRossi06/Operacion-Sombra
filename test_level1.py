from level1 import generate_displacement, decode_cesar, code_cesar

def test_generate_displacement():
    assert(generate_displacement() >= 1 )
    assert(generate_displacement() <= 10 )


def test_code_cesar():
    assert(code_cesar("Agente", 1) == "bhfouf")
    assert(code_cesar("Agente", 3) == "djhqwh")

def test_decode_cesar():
    assert(decode_cesar("bhfouf", 1) == "agente")
    assert(decode_cesar("djhqwh", 3) == "agente")