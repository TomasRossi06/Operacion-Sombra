from level2 import ValidatePatent, GeneratePatent

def test_ValidatePatent():
	assert ValidatePatent("AB1234") == "AB1234"
	assert ValidatePatent("abcd12") == "ABCD12"
	assert ValidatePatent("ZZ9999") == "ZZ9999"
	assert ValidatePatent("MNTP34") == "MNTP34"
	assert ValidatePatent("A12345") is None
	assert ValidatePatent("1234AB") is None
	assert ValidatePatent("ABCD123") is None

def test_GeneratePatent():
	for i in range(20):
		p = GeneratePatent()
		assert ValidatePatent(p) is not None
