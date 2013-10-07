import point
import tags


def flat_point(obj):
    result = {tags.class_name: obj.__class__.__name__, tags.x_pos: obj.x, tags.y_pos: obj.y}
    if obj.label != point.Point.default_label:
        result[tags.label] = obj.label
    if obj.color != point.Point.default_color:
        result[tags.color] = [obj.color.red(), obj.color.green(), obj.color.blue()]
    return result


def default(o):
    if isinstance(o, point.Point):
        return flat_point(o)
    raise TypeError



