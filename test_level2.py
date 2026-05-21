from level2 import validate_patent, generate_patent, initialize, parking_lot, vehicles, target_patent

def test_validate_patent():
	assert validate_patent("AB1234") == "AB1234"
	assert validate_patent("abcd12") == "ABCD12"
	assert validate_patent("ZZ9999") == "ZZ9999"
	assert validate_patent("MNTP34") == "MNTP34"
	assert validate_patent("A12345") is None
	assert validate_patent("1234AB") is None
	assert validate_patent("ABCD123") is None

def test_generate_patent():
	for _ in range(20):
		p = generate_patent()
		assert validate_patent(p) is not None

def test_initialize():
	initialize()
	# Check that vehicles and parking_lot are consistent
	count = 0
	for row in parking_lot:
		for cell in row:
			if cell is not None:
				count += 1
				assert cell in vehicles
	assert 10 <= count <= 20
	assert target_patent in vehicles