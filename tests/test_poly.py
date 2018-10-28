import json
from pathlib import Path

import numpy as np

from polylabel import polylabel


FIXTURES = Path(__file__).parent / 'fixtures'


def fixture(filename):
    return json.load(open(FIXTURES / filename, 'r'))


def test_short():
    x = polylabel(fixture('short.json'))
    assert np.allclose(x[0], [3317.546875, 1330.796875])


def test_water1():
    water1 = fixture('water1.json')
    assert np.allclose(polylabel(water1)[0], [3865.85009765625, 2124.87841796875])
    assert np.allclose(polylabel(water1, 50)[0], [3854.296875, 2123.828125])


def test_works_on_degenerate_polygons():
    out = polylabel([[[0, 0], [1, 0], [2, 0], [0, 0]]])
    assert out[0] == [0, 0]
    out = polylabel([[[0, 0], [1, 0], [1, 1], [1, 0], [0, 0]]])
    assert out[0] == [0, 0]


def test_water2():
    water2 = fixture('water2.json')
    assert np.allclose(polylabel(water2, 1)[0], [3263.5, 3263.5])
