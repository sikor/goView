import sys
import json

from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4 import QtCore

import polygon
import segment
import point
import utils
import encoder
import decoder
import pointsToJSON
import segmentsToJSON



class GenerationDialog(QtGui.QDialog):
    def __init__(self, mainWindow):
        QtGui.QDialog.__init__(self)
        self.ui = uic.loadUi('GenerationForm.ui', self)
        self.mainWindow = mainWindow
        self.ui.shapeCombo.addItem("Rectangle axis and diagonals")
        self.ui.shapeCombo.addItem("Cirle")
        self.ui.shapeCombo.addItem("Quadrangle")
        self.ui.shapeCombo.addItem("Points Range")
        self.ui.buttonBox.accepted.connect(lambda: self.mainWindow.generateEntities(self.ui.numberOfPointsSpinBox.value(),
                                                                                self.ui.numberOfSegmentsSpinBox.value(),
                                                                                self.ui.numberOfPolygonsSpinBox.value()) )

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

        self.currentScale = 1
        self.ui.scaleSlider.valueChanged.connect(
            lambda: self.modifyScale()   )


        self.generationForm = GenerationDialog(self)

    def modifyScale(self):
        s = self.getScaleModification()
        self.ui.graphicsView.scale(s, s)

    def generateEntities(self, pointN, segmentN, polygonN):
        self.entities += [point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400))
                         for unused in range(pointN)]
        self.entities += [segment.Segment(point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
                                          point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)))
                          for unused in range(segmentN)]

        for i in range(0, polygonN):
            self.entities.append(polygon.Polygon([
                point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
                point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
                point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
                point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400)),
                point.Point(utils.random.uniform(0, 400), utils.random.uniform(0, 400))
            ]))

        self.refresh()


    def on_generate(self):
        self.generationForm.show()

    def on_clear(self):
        print(json.dumps(self.entities, sort_keys=True, indent=4, separators=(',', ': '), default=encoder.default))
        self.entities = []
        self.refresh()

    def getScaleModification(self):
        newScale = 15.0/(self.ui.scaleSlider.value())
        toReturn = newScale/self.currentScale
        self.currentScale = newScale
        #print(str(self.ui.scaleSlider.value())+ " "+ str(toReturn) + " "+ str(self.currentScale) )
        return toReturn


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