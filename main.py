import sys
import json

from PyQt4 import QtGui
from PyQt4 import uic

import polygon
import segment
import point
import utils
import math
import encoder
import decoder
import pointsToJSON
import segmentsToJSON
from PyQt4 import QtCore


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

def on_rect():
    min = -100
    max = 100
    return point.Point(random.uniform(min,max),random.uniform(min,max))

def on_circle():
    r = 10

def on_vector():
    x = utils.random.uniform(-1000,1000)
    y = 0.05 * x + 0.05
    return point.Point(x,y)

def on_circle():
    a = utils.random.uniform(0, 2 *math.pi)
    return point.Point(math.sin(a)*100, math.cos(a) * 100)


def simple_predicate1(p):
    return -0.1+p.y-p.x*0.1+p.y

def simple_predicate2(p):
    return (-1 - p.x)*(0.1-p.y) - (1 - p.x)*(0-p.y)

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



        a = 0; b = 0; c =0
        for i in range(100000):
            p = self.entities[i]
            x = simple_predicate1(p)
            if x == 0:
                a+=1
                p.color= QtGui.QColor(255,0,0)
            elif x>0:
                b+=1
                p.color = QtGui.QColor(0,255,0)
            else:
                c+=1
                p.color = QtGui.QColor(0,0,255)

        print(a,b,c)
        #self.entities.append(segment.Segment(point.Point(-201,-10),point.Point(199,10)))


        #

        #self.refresh()

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
            #self.refresh()
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
