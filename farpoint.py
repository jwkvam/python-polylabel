"""Farpoint module."""
from typing import Sequence, Tuple, Union
import logging
from math import sqrt, inf
from itertools import count, product
from queue import PriorityQueue

from shapely.geometry import Point, LineString, Polygon


__version__ = 0.4


class _Cell:
    def __init__(self, x, y, h, polygon):
        self.h = h
        self.y = y
        self.x = x
        self.d = _point_to_polygon_distance(x, y, polygon)

    @property
    def max(self):
        return self.d + self.h * sqrt(2)

    def __eq__(self, other):
        if not isinstance(other, _Cell):
            raise TypeError(f'{other} is not of type _Cell')
        return (self.x == other.x
                and self.y == other.y
                and self.h == other.h)

    def __lt__(self, other):
        if not isinstance(other, _Cell):
            raise TypeError(f'{other} is not of type _Cell')
        if self.x < other.x:
            return True
        if self.y < other.y:
            return True
        if self.h < other.h:
            return True
        return False


def _frange(x, y, jump):
    """range, but for floating point numbers."""
    while x < y:
        yield x
        x += jump


def _point_to_polygon_distance(x, y, polygon):
    """Signed distance from point to polygon outline.

    Negative if point is outside.
    """
    inside = False
    min_dist = inf

    for ring in polygon:
        b = ring[-1]
        for a in ring:

            if ((a[1] > y) != (b[1] > y) and
                    (x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0])):
                inside = not inside

            min_dist = min(min_dist, Point(x, y).distance(LineString([a, b])))
            b = a

    if not inside:
        return -min_dist
    return min_dist


def _get_centroid_cell(polygon):
    area = 0
    x = 0
    y = 0
    points = polygon[0]
    b = points[-1]  # prev
    for a in points:
        f = a[0] * b[1] - b[0] * a[1]
        x += (a[0] + b[0]) * f
        y += (a[1] + b[1]) * f
        area += f * 3
        b = a
    if area == 0:
        return _Cell(points[0][0], points[0][1], 0, polygon)
    return _Cell(x / area, y / area, 0, polygon)


def farpoint(*polygon: Union[Polygon, Sequence[Tuple[float, float]]],
             precision: float = 1.0) -> Tuple[Point, float]:
    """Find pole of inaccessibility."""
    cell_queue: PriorityQueue[Tuple[float, _Cell]] \
        = PriorityQueue()  # pylint: disable=unsubscriptable-object

    # find bounding box
    first_item = polygon[0][0]
    min_x = first_item[0]
    min_y = first_item[1]
    max_x = first_item[0]
    max_y = first_item[1]
    for p in polygon[0]:
        if p[0] < min_x:
            min_x = p[0]
        if p[1] < min_y:
            min_y = p[1]
        if p[0] > max_x:
            max_x = p[0]
        if p[1] > max_y:
            max_y = p[1]

    width = max_x - min_x
    height = max_y - min_y
    cell_size = min(width, height)
    h = cell_size / 2.0

    if cell_size == 0:
        return Point(min_x, min_y), 0

    # cover polygon with initial cells
    for x in _frange(min_x, max_x, cell_size):
        for y in _frange(min_y, max_y, cell_size):
            c = _Cell(x + h, y + h, h, polygon)
            cell_queue.put((-c.max, c))

    best_cell = _get_centroid_cell(polygon)

    bbox_cell = _Cell(min_x + width / 2, min_y + height / 2, 0, polygon)
    if bbox_cell.d > best_cell.d:
        best_cell = bbox_cell

    probes = cell_queue.qsize()
    while not cell_queue.empty():
        *_, cell = cell_queue.get()

        if cell.d > best_cell.d:
            best_cell = cell

            logging.debug(
                'found best %s after %s probes',
                round(1e4 * cell.d) / 1e4,
                probes
            )

        if cell.max - best_cell.d <= precision:
            continue

        h = cell.h / 2
        for mx, my in product((-h, h), repeat=2):
            c = _Cell(cell.x + mx, cell.y + my, h, polygon)
            cell_queue.put((-c.max, c))
            probes += 1

    logging.debug('number of probes: %s', probes)
    logging.debug('best distance: %s', best_cell.d)

    return Point(best_cell.x, best_cell.y), best_cell.d
