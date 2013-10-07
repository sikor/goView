from PyQt4 import QtGui

from point import Point
import tags


def as_entity(data):
    class_name = data[tags.class_name]
    if class_name == Point.__name__:
        return _as_point(data)


def _as_point(data):
    result = Point(data[tags.x_pos], data[tags.y_pos])
    if tags.label in data:
        result.label = data[tags.label]
    if tags.color in data:
        result.color = QtGui.QColor(data[tags.color][0], data[tags.color][1], data[tags.color][2])
    return result

