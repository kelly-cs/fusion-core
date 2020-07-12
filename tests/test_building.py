
""" Unit Testing For Building """

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library

# third party library

# local
from classes.building import Building

def test_unit_building(mocker):
    assert Building("barracks").build("marine") == True
    assert Building("barracks").build("what the heck is this") == KeyError

if __name__ == '__main__':
    # test this file only
    pytest.main([__file__])