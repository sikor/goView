import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic



class GoViewUI(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('GoView.ui', self)
        self.ui.menuLayout.setAlignment( QtCore.Qt.AlignTop)



def main():
    app = QtGui.QApplication(sys.argv)
    ui = GoViewUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()