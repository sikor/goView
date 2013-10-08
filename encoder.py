import tags
import point
import polygon
import segment


def _flat_color(obj):
    return [obj.red(), obj.green(), obj.blue()]


def _flat_point(obj):
    result = {tags.class_name: obj.__class__.__name__, tags.x_pos: obj.x, tags.y_pos: obj.y}
    if obj.label != point.Point.default_label:
        result[tags.label] = obj.label
    if obj.color != point.Point.default_color:
        result[tags.color] = _flat_color(obj.color)
    return result


def _flat_segment(obj):
    result = {tags.class_name: obj.__class__.__name__, tags.p1: _flat_point(obj.p1), tags.p2: _flat_point(obj.p2)}
    if obj.color != segment.Segment.default_color:
        result[tags.color] = _flat_color(obj.color)
    return result


def _flat_polygon(obj):
    result = {tags.class_name: obj.__class__.__name__}
    if obj.opened:
        result[tags.open_polygon] = obj.opened
    result[tags.points] = [_flat_point(the_point) for the_point in obj.points]
    return result


def default(o):
    if isinstance(o, point.Point):
        return _flat_point(o)
    if isinstance(o, segment.Segment):
        return _flat_segment(o)
    if isinstance(o, polygon.Polygon):
        return _flat_polygon(o)
    raise TypeError



