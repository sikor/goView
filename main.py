import sys
from PyQt4 import QtGui, uic
from PyQt4.Qt import *


class GoViewUI(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('GoView.ui', self)
        self.ui.menuLayout.setAlignment(Qt.AlignTop)



def main():
    app = QtGui.QApplication(sys.argv)
    ui = GoViewUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()