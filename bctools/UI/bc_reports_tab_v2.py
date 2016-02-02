import sys
from PyQt4 import QtGui
from bcReportsTabFrame import Ui_MainWindow

class Editor(QtGui.QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()