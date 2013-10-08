from PyQt4 import QtGui
from PyQt4 import QtCore
from entity import Entity


class Point(Entity):
    default_color = QtGui.QColor(0, 100, 200)
    lightness_threshold = QtGui.QColor(127, 127, 127).lightness()
    radius = 3

    def __init__(self, x, y, parents=[]):
        super().__init__(parents)
        self._x = x
        self._y = y
        self._color = Point.default_color
        self.label_impl = None
        self.ellipse = None

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        for parent in self.parents:
            parent.notify()
        if self.ellipse:
            self.ellipse.do_set_pos()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        if self.ellipse:
            self.ellipse.do_set_pos()
        for parent in self.parents:
            parent.notify()


    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        if self.ellipse:
            self.ellipse.do_set_color()

    #isinstace lets IDE infer type
    def add_to_scene(self, scene):
        if self.ellipse and self.ellipse.scene:
            return
        if isinstance(scene, QtGui.QGraphicsScene):
            self.ellipse = Ellipse(self, scene,
                                   QtCore.QRectF(self.x - Point.radius, self.y - Point.radius, 2 * Point.radius,
                                            2 * Point.radius))
            self.ellipse.do_set_color()

            scene.addItem(self.ellipse)
            self.label_impl = scene.addSimpleText(self.label)
            self.label_impl.setTransform(QtGui.QTransform(1, 0, 0, 0, -1, 0, 0, 0, 1))
            if isinstance(self.label_impl, QtGui.QGraphicsSimpleTextItem):
                self.label_impl.setPos(self.x + 5 * Point.radius, self.y)


class Ellipse(QtGui.QGraphicsEllipseItem):
    def __init__(self, this, scene, rect_f):
        super().__init__(rect_f)
        self.setAcceptHoverEvents(True)
        self.menu = QtGui.QMenu()
        set_color = QtGui.QAction('Set color', scene)
        set_color.triggered.connect(self.set_color)
        set_label = QtGui.QAction('Set label', scene)
        set_label.triggered.connect(self.set_label)
        self.menu.addAction(set_color)
        self.menu.addAction(set_label)
        self.this = this
        self.scene = scene
        self.dragged = False

    def set_label(self):
        value = QtGui.QInputDialog.getText(None, 'Enter new label', '', text=self.this.label, flags=QtCore.Qt.Tool)
        if len(value) == 2 and value[1]:
            self.this.label = value[0]
            self.this.label_impl.setText(self.this.label)

    def set_color(self):
        color = QtGui.QColorDialog.getColor(self.this.color)
        if color.isValid():
            self.this.color = color
            self.do_set_color()


    def do_set_color(self):
        if self.this.color.lightness() < Point.lightness_threshold:
            self.setPen(self.this.color)
            self.setBrush(self.this.color.lighter())
        else:
            self.setPen(self.this.color.darker())
            self.setBrush(self.this.color)

    def contextMenuEvent(self, event):
        if isinstance(event, QtGui.QGraphicsSceneContextMenuEvent):
            self.menu.exec(event.screenPos())

    def hoverEnterEvent(self, event):
        self.setOpacity(0.5)
        self.scene.show_coords(self.this.x, self.this.y)

    def hoverLeaveEvent(self, event):
        self.setOpacity(1.0)

    def mouseMoveEvent(self, event):
        if self.dragged:
            pos = event.scenePos()
            self.this.x = pos.x()
            self.this.y = pos.y()
            self.do_set_pos()
            self.scene.show_coords(self.this.x, self.this.y)

    def do_set_pos(self):
        self.setRect(QtCore.QRectF(
            self.this.x - Point.radius, self.this.y - Point.radius,
            2 * Point.radius, 2 * Point.radius))
        self.this.label_impl.setPos(self.this.x + 5 * Point.radius, self.this.y)

    def mousePressEvent(self, event):
        self.dragged = True

    def mouseReleaseEvent(self, event):
        self.dragged = False


