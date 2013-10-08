from PyQt4 import QtGui

import point
import entity


class Segment(entity.Entity, entity.Parent):
    default_color = QtGui.QColor(0, 0, 0)

    def __init__(self, p1, p2):
        super().__init__()
        self.line = None
        self._color = Segment.default_color
        self._p1 = p1
        self._p2 = p2
        self.p1.parents.append(self)
        self.p2.parents.append(self)

    def notify(self):
        if self.line:
            self.line.do_set_line()


    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, new):
        self._p1 = new

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, new):
        self._p2 = new

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    def add_to_scene(self, scene):
        if isinstance(scene, QtGui.QGraphicsScene):
            self.line = Line(self, scene, self.p1, self.p2)
            scene.addItem(self.line)
            self.p1.add_to_scene(scene)
            self.p2.add_to_scene(scene)


class Line(QtGui.QGraphicsLineItem):
    def __init__(self, this, scene, p1, p2):
        super().__init__(p1.x, p1.y, p2.x, p2.y)
        self.setAcceptHoverEvents(True)
        self.menu = QtGui.QMenu()
        set_color = QtGui.QAction('Set color', scene)
        set_color.triggered.connect(self.set_color)
        self.menu.addAction(set_color)
        self.this = this
        self.scene = scene
        self.dragged = False
        self.ref_pos = None
        self.ref_p1 = self.this.p1
        self.ref_p2 = self.this.p2

    def set_color(self):
        color = QtGui.QColorDialog.getColor(self.this.color)
        if color.isValid():
            self.this.color = color
            self.do_set_color()


    def do_set_color(self):
        self.setPen(self.this.color)

    def contextMenuEvent(self, event):
        if isinstance(event, QtGui.QGraphicsSceneContextMenuEvent):
            self.menu.exec(event.screenPos())

    def hoverEnterEvent(self, event):
        self.setOpacity(0.5)

    def hoverLeaveEvent(self, event):
        self.setOpacity(1.0)

    def mouseMoveEvent(self, event):
        if self.dragged:
            delta_x = event.scenePos().x() - self.ref_pos.x()
            delta_y = event.scenePos().y() - self.ref_pos.y()
            self.this.p1.x = self.ref_p1.x + delta_x
            self.this.p1.y = self.ref_p1.y + delta_y

            self.this.p2.x = self.ref_p2.x + delta_x
            self.this.p2.y = self.ref_p2.y + delta_y
            self.do_set_line()

    def do_set_line(self):
        self.setLine(self.this.p1.x, self.this.p1.y, self.this.p2.x, self.this.p2.y)

    def mousePressEvent(self, event):
        self.ref_pos = event.scenePos()
        self.ref_p1 = point.Point(self.this.p1.x, self.this.p1.y)
        self.ref_p2 = point.Point(self.this.p2.x, self.this.p2.y)
        self.dragged = True

    def mouseReleaseEvent(self, event):
        self.dragged = False
