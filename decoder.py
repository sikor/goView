from PyQt4 import QtGui

from polygon import Polygon
from segment import Segment
from point import Point
import tags


def as_entity(data):
    class_name = data[tags.class_name]
    if class_name == Point.__name__:
        return _as_point(data)
    if class_name == Segment.__name__:
        return _as_segment(data)
    if class_name == Polygon.__name__:
        return _as_polygon(data)
    return TypeError


def _as_color(data):
    return QtGui.QColor(data[0], data[1], data[2])


def _as_segment(data):
    p1 = data[tags.p1]
    p2 = data[tags.p2]
    result = Segment(p1, p2)
    if tags.color in data:
        result.color = _as_color(data[tags.color])
    return result


def _as_polygon(data):
    return Polygon(data[tags.points], tags.open_polygon in data and data[tags.open_polygon] == True)


def _as_point(data):
    result = Point(data[tags.x_pos], data[tags.y_pos])
    if tags.label in data:
        result.label = data[tags.label]
    if tags.color in data:
        result.color = _as_color(data[tags.color])
    return result

