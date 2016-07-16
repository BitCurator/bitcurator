import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bcReportsTabUIv3 import Ui_MainWindow

class Editor(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Editor, self).__init__()
        self.ui=Ui_MainWindow()
        self.setupUi(self)        
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()