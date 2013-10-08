import sys
import json

from PyQt4 import QtGui
from PyQt4 import uic

import polygon
import segment
import point
import utils
import encoder
import decoder
import pointsToJSON
import segmentsToJSON


class Scene(QtGui.QGraphicsScene):
    def __init__(self, coords_label):
        super().__init__()
        self._entities = []
        self.coords_label = coords_label


    @property
    def entities(self):
        return self._entities

    @entities.setter
    def entities(self, entities):
        self._entities = entities
        self.refresh()

    def refresh(self):
        for item in self.items():
            item.scene = None
            self.removeItem(item)
        for entity in self._entities:
            entity.add_to_scene(self)

    def show_coords(self, x, y):
        self.coords_label.setText('x: ' + str(x)[:6] + '\ny: ' + str(y)[:6])


class GoViewUI(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.entities = []
        self.ui = uic.loadUi('GoView.ui', self)

        self.ui.clearButton.clicked.connect(lambda: self.on_clear())
        self.ui.generateButton.clicked.connect(lambda: self.on_generate())
        self.ui.loadButton.clicked.connect(lambda: self.on_load())
        self.ui.saveButton.clicked.connect(lambda: self.on_save())
        self.ui.loadPointsButton.clicked.connect(lambda: self.on_load_points())
        self.ui.loadSegmentsButton.clicked.connect(lambda: self.on_load_segments())

        self.scene = Scene(self.ui.coordsLabel)
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.scale(1, -1)
        self.ui.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)

    def on_generate(self):
        self.entities = [point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400))
                         for unused in range(10)]
        self.entities += [segment.Segment(point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
                                          point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)))
                          for unused in range(3)]
        self.entities.append(polygon.Polygon([
            point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
            point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
            point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
            point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
            point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400))
        ]))

        self.refresh()

    def on_clear(self):
        print(json.dumps(self.entities, sort_keys=True, indent=4, separators=(',', ': '), default=encoder.default))
        self.entities = []
        self.refresh()


    def refresh(self):
        self.scene.entities = []
        self.scene.entities = self.entities

    def on_save(self):
        file_name = QtGui.QFileDialog.getSaveFileName(None, "Choose file to save scene", "./data", "*.dat")
        if file_name == '':
            return
        file = open(file_name, 'w')
        file.write(json.dumps(self.entities, sort_keys=True, indent=4, separators=(',', ': '), default=encoder.default))


    def on_load(self):
        file_name = QtGui.QFileDialog.getOpenFileName(None, "Choose file to open scene", "./data", "*.dat")
        if file_name == '':
            return
        file = open(file_name)
        try:
            self.entities += json.loads(file.read(), object_hook=decoder.as_entity)
            self.refresh()
        except Exception as e:
            print(e)

    def on_load_points(self):
        file_name = QtGui.QFileDialog.getOpenFileName(None, "Choose file to open scene", "./data", "*.dat")
        if file_name == '':
            return
        try:
            self.entities += pointsToJSON.load(file_name)
            self.refresh()
        except Exception as e:
            print(e)

    def on_load_segments(self):
        file_name = QtGui.QFileDialog.getOpenFileName(None, "Choose file to open scene", "./data", "*.dat")
        if file_name == '':
            return
        try:
            self.entities += segmentsToJSON.load(file_name)
            self.refresh()
        except Exception as e:
            print(e)


def main():
    app = QtGui.QApplication(sys.argv)
    ui = GoViewUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()