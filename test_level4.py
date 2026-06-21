import os
from level4 import GetBasePath

def test_get_base_path():
    path = GetBasePath()
    assert os.path.isdir(path)