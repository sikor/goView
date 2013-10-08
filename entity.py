import json

import encoder


class Parent(object):
    def notify(self):
        pass


class Entity(object):
    default_label = ''

    def __init__(self, parents=[], label=default_label):
        self._label = label
        self._parents = parents

    def add_to_scene(self, scene):
        pass

    @property
    def parents(self):
        return self._parents

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label
        for parent in self.parents:
            parent.notify()

    def __str__(self):
        return json.dumps(self, sort_keys=True, separators=(', ', ': '), default=encoder.default)

