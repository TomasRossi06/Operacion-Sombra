import operator


from level3 import OperatorName


def test_OperatorName():
    assert OperatorName(operator.add) == "+"
    assert OperatorName(operator.sub) == "-"
    assert OperatorName(operator.mul) == "x"
    assert OperatorName(operator.truediv) == "/"
    assert OperatorName(operator.pow) == "^"
    assert OperatorName(operator.mod) == "%"
    assert OperatorName(operator.floordiv) == "//"


