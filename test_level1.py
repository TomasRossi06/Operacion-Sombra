from level1 import GenerateDisplacement, DecodeCesar, CodeCesar

def test_GenerateDisplacement():
    assert(GenerateDisplacement() >= 1 )
    assert(GenerateDisplacement() <= 10 )


def test_CodeCesar():
    assert(CodeCesar("Agente", 1) == "bhfouf")
    assert(CodeCesar("Agente", 3) == "djhqwh")

def test_DecodeCesar():
    assert(DecodeCesar("bhfouf", 1) == "agente")
    assert(DecodeCesar("djhqwh", 3) == "agente")