#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# BitCurator
#
# bcReportsTabv3.py
#
# Revised implementation of GUI interface in PyQT5 for generating files 
# and reports for Bitcurator project.
#
# Created: Sat Jul 16 19:17:21 2016
#

import os
import sys
import time
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import *

from os.path import expanduser
from subprocess import Popen,PIPE

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