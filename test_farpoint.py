"""Tests on various polygons."""
import json
from pathlib import Path

from shapely.geometry import Point

from farpoint import farpoint


FIXTURES = Path('fixtures')
THRESHOLD = 1e-6


def fixture(filename):
    """Load fixture."""
    return json.load(open(FIXTURES / filename, 'r'))


def test_short():
    """Test short fixture."""
    polys = fixture('short.json')
    x = farpoint(*polys)
    min_point = Point(3317.546875, 1330.796875)
    assert min_point.distance(x[0]) <= THRESHOLD

    min_dist = x[1]
    for poly in polys:
        for p in poly:
            assert Point(*p).distance(min_point) >= min_dist


def test_water1():
    """Test water1 fixture."""
    water1 = fixture('water1.json')
    assert Point(3865.85009765625, 2124.87841796875).distance(farpoint(*water1)[0]) <= THRESHOLD
    assert Point(3854.296875, 2123.828125).distance(farpoint(*water1, precision=50)[0]) <= THRESHOLD


def test_works_on_degenerate_polygons():
    """Test works on weird polygons."""
    out = farpoint([[0, 0], [1, 0], [2, 0], [0, 0]])
    assert Point(0, 0).distance(out[0]) <= THRESHOLD
    out = farpoint([[0, 0], [1, 0], [1, 1], [1, 0], [0, 0]])
    assert Point(0, 0).distance(out[0]) <= THRESHOLD


def test_water2():
    """Test water2 fixture."""
    water2 = fixture('water2.json')
    assert Point(3263.5, 3263.5).distance(farpoint(*water2)[0]) <= THRESHOLD
