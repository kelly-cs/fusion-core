
""" Unit Testing For Player """

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library
import os, sys

# third party library
import pytest

# local
path = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
print(path)
if path not in sys.path:
    print('inserting {!r} into sys.path'.format(path))
    sys.path.insert(0, path)

from classes.player import Player

if __name__ == '__main__':
    # test this file only
    pytest.main([__file__])