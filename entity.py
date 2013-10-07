import json
import types

from PyQt4 import QtGui

import encoder


class Entity(object):
    default_label = ''

    def __init__(self, label=default_label):
        self._label = label

    def add_to_scene(self, q_painter):
        pass

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    def set_mouse_handling(self, item):
        if isinstance(item, QtGui.QGraphicsItem):
            item.setAcceptsHoverEvents(True)
            print('here')
            item.hoverEnterEvent = types.MethodType(lambda this, event: print('hover entered'), item)

    def __str__(self):
        return json.dumps(self, sort_keys=True, separators=(', ', ': '), default=encoder.default)

