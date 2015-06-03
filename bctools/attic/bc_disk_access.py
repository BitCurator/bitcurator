#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# BitCurator
#
# This code is distributed under the terms of the GNU General Public
# License, Version 3. See the text file "COPYING" for further details
# about the terms of this license.
#
# bc_disk_access --dfxmlfile <file> --filename <oufile>
#
# 1. Ex: Cat: 
# python3 bc_disk_access.py --image ~/aaa/charlie-work-usb-2009-12-11.aff \ 
#   [--dfxmlfile ~/aaa/charlie_xml] --filename \
#    Email/Charlie_2009-12-04_0941_Sent.txt --cat
#
# 2. Ex: filelist:
# $ python3 bc_disk_access.py 
#    --image ~/aaa/charlie-work-usb-2009-12-11.aff 
#    [--dfxmlfile ~/aaa/charlie_xml] \
#    --listfiles
# 3. Invoked through BitCurator GUI
#
#
# Notes:
# This GUI was constructed using PyQT4 Designer. Code manually added
# to QTreeView and for the functionality of all widgets.
#
# The "filename" attribute is read from an existing DFXML file using 
# fiwalk.fiwalk_using_sax() API. The list of file-paths is stored in 
# the dictionary fiDictList. 
#
# To store the Tree structure of the directory hierarchy, the 
# QStandardItemModel class of the QtPy4's Model/View framework is used:
# http://pyqt.sourceforge.net/Docs/PyQt4/qstandarditemmodel.html#details

import os, fiwalk, sys
from PyQt4 import QtCore, QtGui
import subprocess
from subprocess import Popen,PIPE
import threading
import time
#from bc_genrep_dfxml import bc_get_ftype_from_sax

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

try:
    from argparse import ArgumentParser
except ImportError:
    raise ImportError("This script requires ArgumentParser which is in Python 2.7 or Python 3.0")

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

global g_model
global g_image
global g_dfxmlfile
global isGenDfxmlFile
global g_breakout

class Ui_MainWindow(object):
    progressBar = "null"
    # Stdout handling for debugging
    oldstdout = sys.stdout
    sys.stdout = StringIO()

    def __init__(self, outdir=None):
        self.outdir = outdir

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(835, 565)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 7, 1, 1)

        self.DirectoryTree = QtGui.QTreeView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DirectoryTree.sizePolicy().hasHeightForWidth())

        # This line was added to get the horizontal scroll bar automatically when 
        # there is text longer than the window. However, you still needs one to drag 
        # the top bar to the right to make the scroll bar start working. Could be a bug with 
        # pyQT4 implementation.
        self.DirectoryTree.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

        self.DirectoryTree.setSizePolicy(sizePolicy)
        self.DirectoryTree.setSizeIncrement(QtCore.QSize(0, 0))
        self.DirectoryTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.DirectoryTree.setObjectName(_fromUtf8("DirectoryTree"))

        #.#
        self.DirectoryTree.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.gridLayout.addWidget(self.DirectoryTree, 1, 0, 1, 6)

        #.#
        self.model = QtGui.QStandardItemModel()
        self.DirectoryTree.setModel(self.model)
        self.DirectoryTree.setUniformRowHeights(True)
        global g_model 
        g_model = self.model

        g_model.setHorizontalHeaderLabels(['File System: \n  Entries in bold are directories \n  Entries in red are unallocated/deleted files '])


        self.pushButton_cancel = QtGui.QPushButton(self.centralwidget)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.gridLayout.addWidget(self.pushButton_cancel, 8, 1, 1, 1)

        self.pushButton_sall = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_sall.sizePolicy().hasHeightForWidth())
        self.pushButton_sall.setSizePolicy(sizePolicy)
        self.pushButton_sall.setObjectName(_fromUtf8("pushButton_sall"))
        self.gridLayout.addWidget(self.pushButton_sall, 8, 5, 1, 1)
        self.pushButton_close = QtGui.QPushButton(self.centralwidget)
        self.pushButton_close.setObjectName(_fromUtf8("pushButton_close"))
        self.gridLayout.addWidget(self.pushButton_close, 8, 0, 1, 1)

        #.#
        #self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar = ProgressBar()

        #.#
        global global_pb_da
        global_pb_da = self.progressBar

        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 8, 7, 1, 1)
        self.pushButton_export = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_export.sizePolicy().hasHeightForWidth())
        self.pushButton_export.setSizePolicy(sizePolicy)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.gridLayout.addWidget(self.pushButton_export, 8, 3, 1, 1)
        self.pushButton_dsall = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_dsall.sizePolicy().hasHeightForWidth())
        self.pushButton_dsall.setSizePolicy(sizePolicy)
        self.pushButton_dsall.setObjectName(_fromUtf8("pushButton_dsall"))
        self.gridLayout.addWidget(self.pushButton_dsall, 8, 6, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.setStyleSheet(_fromUtf8("background-color: rgb(200, 206, 200);\n"
"border-color: rgb(170, 0, 0);"))
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 1, 6, 1, 2)

        #.#
        global g_textEdit
        g_textEdit = self.textEdit

        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 835, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionSelect_All = QtGui.QAction(MainWindow)
        self.actionSelect_All.setObjectName(_fromUtf8("actionSelect_All"))
        self.actionDeSelect_All = QtGui.QAction(MainWindow)
        self.actionDeSelect_All.setObjectName(_fromUtf8("actionDeSelect_All"))
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionSelect_All)
        self.menuHelp.addAction(self.actionDeSelect_All)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.actionExit.triggered.connect(self.exitMenu)
        self.actionSelect_All.triggered.connect(self.selectAllMenu)
        self.actionDeSelect_All.triggered.connect(self.deSelectAllMenu)

        # File navigation for Export
        QtCore.QObject.connect(self.pushButton_export, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedExport)

        # Handle the Close button
        QtCore.QObject.connect(self.pushButton_close, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedClose)

        # Handle the Select button
        QtCore.QObject.connect(self.pushButton_sall, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedSelectAll)

        # Handle the DeSelect button
        QtCore.QObject.connect(self.pushButton_dsall, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedDeSelectAll)

        # Handle the Cancel button
        QtCore.QObject.connect(self.pushButton_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedCancel)

        '''
        # Handle the Dump button
        QtCore.QObject.connect(self.pushButton_dump, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedDump)
        '''

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def exitMenu(self):
        QtCore.QCoreApplication.instance().quit()

    def selectAllMenu(self):
        self.oldstdout = sys.stdout
        sys.stdout = StringIO()
        BcFileStructure.bcOperateOnFiles(BcFileStructure, 1, None)
        global g_textEdit
        g_textEdit.setText( sys.stdout.getvalue() )
        sys.stdout = self.oldstdout
        
    def deSelectAllMenu(self):
        BcFileStructure.bcOperateOnFiles(BcFileStructure, 0, None)
        global g_textEdit
        g_textEdit.setText( sys.stdout.getvalue() )
        sys.stdout = self.oldstdout

    def buttonClickedClose(self):
        # if dfxml file was internally generated, remove it.
        global isGenDfxmlFile
        if isGenDfxmlFile == True:
            os.system('rm '+g_dfxmlfile)
        QtCore.QCoreApplication.instance().quit()

    def buttonClickedCancel(self):
        # if dfxml file was internally generated, remove it.
        global isGenDfxmlFile
        if isGenDfxmlFile == True:
            os.system('rm '+g_dfxmlfile)
        print(">> Disk Access operation is aborted ")

        # Set the breakout flag to True to stop the export operation.
        global g_breakout
        g_breakout = True

        # Set the active flag to False
        ProgressBar._active = False

        # Set the progressbar maximum to > minimum so the spinning will stop
        global global_pb_da
        global_pb_da.progressbar.setRange(0,1)

        x = Ui_MainWindow
        global g_textEdit
        g_textEdit.setText( sys.stdout.getvalue() )
        sys.stdout = x.oldstdout

        x.oldstdout = sys.stdout
        sys.stdout = StringIO()

        # Set the flag in the thread to signal thread termination
        global g_thread1_da
        g_thread1_da.join()

    def buttonClickedExport(self):
        # If invoked thorugh reports_tab gui, the outdir provided is the 
        # exportDir and so there is no need to choose again. If invoked 
        # through command line, output directory to export the checked files
        # needs to be provided now, through file navigation
        if self.outdir == None:
            os.chdir(os.environ["HOME"])
            exportDir = QtGui.QFileDialog.getExistingDirectory(caption="Select an Output Directory to export files")
        else:
            exportDir = self.outdir

        ## Testing:
        ## print(">> D: Output Directory Selected: ", exportDir)
        
        # Invoke bcOperateOnfiles routine with check=2
        thread1 = daThread(2, exportDir)

        # Save the thread handle for later use in cancel task.
        global g_thread1_da
        g_thread1_da = thread1
        
        thread2 = guiThread()

        thread1.start()
        thread2.start()

    def buttonClickedSelectAll(self):
        BcFileStructure.bcOperateOnFiles(BcFileStructure, 1, None)

    def buttonClickedDeSelectAll(self):
        BcFileStructure.bcOperateOnFiles(BcFileStructure, 0, None)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Disk Image Access Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_export.setText(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_close.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_sall.setText(QtGui.QApplication.translate("MainWindow", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_dsall.setText(QtGui.QApplication.translate("MainWindow", "DeSelect All", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Command Line Output", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelect_All.setText(QtGui.QApplication.translate("MainWindow", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeSelect_All.setText(QtGui.QApplication.translate("MainWindow", "DeSelect All", None, QtGui.QApplication.UnicodeUTF8))

class BcFileStructure:

    acc_dict_array = ["filename", "partition", "inode", "name_type", "filesize", "alloc"]
    fiDictList = []
    parentlist = []
    file_item_of = dict()
    path_of = dict()

    x = Ui_MainWindow
    
    # bcOperateOnFiles()
    # Iterate through the leaves of the file structure and check/uncheck
    # all the files based on whether "check" is True or False.
    # This same routine is reused with the parameter "cehck" set to 2, 
    # to dump the contents of the "checked" files to the specified output 
    # directory. It is again used with check=3 to dump the contents of a
    # file to the textEdit window. 
    def bcOperateOnFiles(self, check, exportDir):
        ## print(">>D: Length of fiDictList: ", len(self.fiDictList))
        global g_breakout
        g_breakout = False
        for i in range(0, len(self.fiDictList) - 1):
            path = self.fiDictList[i]['filename']
            inode = self.fiDictList[i]['inode']
            if self.fiDictList[i]['name_type'] == 'd':
                isdir = True
            else:
                isdir = False
            pathlist = path.split('/')
            pathlen = len(pathlist)
            ## print("D: Path List: ", pathlist, len(pathlist))
            last_elem = pathlist[pathlen-1]
            if last_elem == "." or last_elem == "..":
                # Ignore . and ..
                continue 

            if isdir == False:
                # First get the name of the current file
                current_fileordir = pathlist[pathlen-1]
                # Now using the dict of files, file_item_of, get the item for this file
                unique_path = path + '-' + str(inode)
                current_item = self.file_item_of[unique_path]
                if check == 1:
                    if (current_item.checkState() == 0):
                        ## print("D: Setting File to Checked_state ", current_fileordir) 
                        current_item.setCheckState(2)
                elif check == 0:
                    current_item.setCheckState(0)
                elif check == 2:
                    if g_breakout == True:
                        break
                    # If "check" is 2, we use this routine to dump the 
                    # contents of the specified file to the specified output file. 
                    # If this file is "checked", download its contents.
                    # item.checkState has 0 if not checked, 1 if partially
                    # checked and 2 if checked. 
                    # http://qt.developpez.com/doc/4.6/qt/#checkstate-enum

                    if current_item.checkState() == 2:
                        ## print(">> D: File %s is Checked" %current_fileordir)
                        if not os.path.exists(exportDir):
                            os.mkdir(exportDir)

                        pathlist = path.split('/')
                        oldDir = newDir = exportDir
                        
                        # Iterate through the path list and make the directories
                        # in the path, if they don't already exist.
                        for k in range(0, len(pathlist)-1):
                            newDir = oldDir + '/' + pathlist[k]
                            if not os.path.exists(newDir):
                                os.mkdir(newDir)
                            oldDir = newDir
                        outfile = newDir + '/'+current_fileordir
                        ## print(">> D: Writing to Outfile: ", outfile, path)
                        
                        filestr.bcCatFile(path, inode, g_image, g_dfxmlfile, True, outfile)
                    elif current_item.checkState() == 1:
                        print("Partially checked state: ",current_item.checkState()) 
                        print("File %s is NOT Checked" %current_fileordir)
                        # FIXME: Test the above debug print stmts
                        g_textEdit.setText( sys.stdout.getvalue() )
                        sys.stdout = x.oldstdout
                elif check == 3:
                    # Dump the first checked File in textEdit window
                    if current_item.checkState() == 2:
                        print(">> D: File %s is Checked" %current_fileordir)

                        self.oldstdout = sys.stdout
                        sys.stdout = StringIO()
                        
                        ## print("D: >> Dumping the contents of the file ", path)
                        ## FIXME: Not tested with inode yet.
                        filestr.bcCatFile(path, inode, g_image, g_dfxmlfile, False, None)
                         
                        g_textEdit.setText( sys.stdout.getvalue() )
                        sys.stdout = self.oldstdout
                        
                        # We list only the first checked file.
                        return
                    elif current_item.checkState() == 1:
                        print("Partially checked state: ",current_item.checkState()) 
                        print("File %s is NOT Checked" %current_fileordir)
                        g_textEdit.setText( sys.stdout.getvalue() )
                        sys.stdout = self.oldstdout

    def bcHandleSpecialChars(self, filename):
        # Escape characters such as $, space, {, and }
        #filename = filename.replace("$", "\$")
        return re.escape(filename)
                    
    def bcGetFilenameFromPath(self, path):
        pathlist = path.split('/')
        pathlen = len(pathlist)

        filename = pathlist[pathlen-1]

        # Prepend special characters with backslash
        filename = self.bcHandleSpecialChars(filename)
        return filename

    # bcExtractFileStr()
    # This routine extracts the file structure given a disk image and the
    # corresponding dfxml file.
    def bcExtractFileStr(self, image, dfxmlfile, outdir):
        x = Ui_MainWindow

        ### Following 4 lines added for debugging
        global g_textEdit
        g_textEdit.append( sys.stdout.getvalue() )
        x.oldstdout = sys.stdout
        sys.stdout = StringIO()
        
        # Extract the information from dfxml file to create the 
        # dictionary only if it is not done before.
        if len(self.fiDictList) == 0:
            self.bcProcessDfxmlFileUsingSax(dfxmlfile)
            ## print("D: Length of dictionary fiDictList: ", len(self.fiDictList))

        parent0 = image
        parent0_item = QtGui.QStandardItem('Disk Image: {}'.format(image))
        current_fileordir = image
        parent_dir_item = parent0_item
        font = QtGui.QFont("Times",12,QtGui.QFont.Bold)
        parent_dir_item.setFont(font)

        global g_image
        global g_dfxmlfile
        g_image = re.escape(image)
        g_dfxmlfile = dfxmlfile

        # A dictionary item_of{} is maintained which contains each file/
        # directory and its corresponding " tree item" as its value.
        item_of = dict()
        item_of[image] = parent0_item

        global g_model
        g_model.appendRow(parent0_item)

        for i in range(0, len(self.fiDictList) - 1):
            path = self.fiDictList[i]['filename']
            inode = self.fiDictList[i]['inode']
            ## print("D: path, inode: ", path, inode)
            isdir = False
            if self.fiDictList[i]['name_type'] == 'd':
                isdir = True

            deleted = False
            if self.fiDictList[i]['alloc'] == False:
                deleted = True

            pathlist = path.split('/')
            pathlen = len(pathlist)
            ## print("D: Path LiSt: ", pathlist, len(pathlist))
            last_elem = pathlist[pathlen-1]
            if last_elem == "." or last_elem == "..":
                # Ignore . and ..
                continue 

            if isdir == True:
                ## print("D: It is  a Directory:  Pathlen: ", pathlen)
                if (pathlen < 2):
                    # If pathlen is < 2 it is a file/dir directly off the root.
                    parent_dir_item = parent0_item
                else:
                    parent_dir_item = item_of[pathlist[pathlen-2]]

                current_dir = pathlist[pathlen-1]
                current_item = QtGui.QStandardItem(current_dir)
                font = QtGui.QFont("Times",12,QtGui.QFont.Bold)
                current_item.setFont(font)

                # Add the directory item to the tree.
                parent_dir_item.appendRow(current_item)

                # DEBUG: Following 2 lines are added for debugging 
                g_textEdit.append(sys.stdout.getvalue() )
                sys.stdout = x.oldstdout

                # Save the item of this directory
                item_of[current_dir] = current_item
                
            else:
                # File: The file could be in any level - top level is the
                # child of parent0_item (disk img). The level is sensed by the
                # pathlen 
                current_fileordir = pathlist[pathlen-1]
                unique_current_file = current_fileordir + '-' + str(inode)
                current_item = QtGui.QStandardItem(unique_current_file)
                ## print("D: Found a file:  ", current_fileordir, current_item)
                ## print("D: Path length: ", pathlen)

                # We want just the filename in the GUI - without the inode
                current_item.setText(current_fileordir)

                g_textEdit.append( sys.stdout.getvalue() )
                sys.stdout = x.oldstdout

                current_item.setCheckable(True)
                current_item.setCheckState(0)

                if deleted == True:
                    current_item.setForeground(QtGui.QColor('red'))

                # Save the "item" of each file
                unique_path = path + '-' + str(inode)
                self.file_item_of[unique_path] = current_item

                if pathlen > 1:
                    parent_dir_item = item_of[pathlist[pathlen-2]]
                else:
                    parent_dir_item = parent0_item
            
                # Add the directory item to the tree.
                parent_dir_item.appendRow(current_item)

            parent = parent_dir_item

            # DEEBUG: The following 2 lines are added for debugging
            g_textEdit.append( sys.stdout.getvalue() )
            sys.stdout = x.oldstdout
            
    def bcCatFile(self, filename, inode, image, dfxmlfile, redirect_file, outfile):
        # Traverse the XML file, get the file_name, extract the inode number
        # of the file and run icat to extract the data.
        ## print(">>D: bcCatFile: Filename: ", filename)
        ## print(">>D: bcCatFile: image: ", image)
        ## print(">>D: bcCatFile: dfxmlfile: ", dfxmlfile)
        ## print(">>D: bcCatFile: outfile: ", outfile)
        x = Ui_MainWindow
        #x.oldstdout = sys.stdout
        #sys.stdout = StringIO()

        # Traverse through dfxmlfile to get the block containing 
        # "filename" to extract the inode. Do this just once.
        if len(self.fiDictList) == 0:
            self.bcProcessDfxmlFileUsingSax(dfxmlfile)
            ## print("D: Length of fiDictList ", len(self.fiDictList))

        # Dictionary is formed. Now traverse through the array and 
        # in each dictionary, get the inode and call iCat command.
        for i in range(0, len(self.fiDictList)-1):
            if (self.fiDictList[i]['filename'] == filename and self.fiDictList[i]['inode'] == inode):
                ## print("D: Extracting the contents of the file:inode ", \ 
                ##                  filename, self.fiDictList[i]['inode']) 

                # Get the offset of the 2nd partition using mmls cmd
                # ex: mmls -i aff ~/aaa/jo-favorites-usb-2009-12-11.aff
                if image.endswith(".E01") or image.endswith(".e01"):
                    imgtype = 'ewf'
                elif image.endswith(".aff") or image.endswith(".AFF"):
                    imgtype = 'aff'
                elif image.endswith(".iso") or image.endswith(".ISO"):
                    imgtype = 'iso'
                else:
                    imgtype = 'raw'

                # Extract the file-system type from dfxml file volume
                ftype = self.bc_get_ftype_from_sax(dfxmlfile) 
                
                # For FAT12 file-system there is no partiton information.
                # So skip the step for extracting partition offset.
                part2_start = 0
                if self.ftype != 'fat12' and self.ftype != 'iso9660' and imgtype != 'iso':
                    mmls_cmd = "mmls -i " + imgtype +" "+image +" | grep \"02:\""

                    ## print("D: Executing mmls command: ", mmls_cmd) 
                    part2 = subprocess.check_output(mmls_cmd, shell=True)
                    ## print("D: Extracting partition-2: ", part2)

                    part2_list = part2.split()
                    part2_start = int(part2_list[2])

                ## print("D: Start offset of Partition-2: ", part2_start)
                ## icat_cmd ex: icat -o 1 ~/aaa/charlie-work-usb-2009-12-11.aff 130 
                # redirect_file is set to True if the contents need to be 
                # written to a file.
                if (redirect_file == True):
                    outfile = self.bcHandleSpecialChars(outfile)

                    icat_cmd = "icat -o "+str(part2_start)+ " "+ \
                                image + " " + \
                                self.fiDictList[i]['inode'] + ' > ' + outfile
                    f2 = Popen(icat_cmd, shell = True, stdout=PIPE, stderr=PIPE)
                    (data, err) = f2.communicate()

                    # FIXME: Using subprocess.check_output is making icat_cmd
                    # fail for some instances. Revisit this. Till then the
                    # older call os.popen is used, which seems to work fine.
                    # subprocess.check_output(icat_cmd, shell=True)
                    ## print(">> Writing to file ", outfile)
                else:
                    # Only printable files are dumped on the textEdit wondow.
                    # The rest are redirected to a file in /tmp
                    if (filename.endswith('txt') or filename.endswith('xml')):
                        icat_cmd = "icat -o "+str(part2_start)+ " "+ image + " " + self.fiDictList[i]['inode']
                        ## print(">> D: Executing iCAT command: ", icat_cmd)
                        f2 = os.popen(icat_cmd)
                        icat_out = f2.read()
                        print(">> Dumping Contents of the file :", filename)
                        print("\n")
                        print(icat_out)

                    else:
                        # Strip the path to extract just the name of the file.
                        justFilename = self.bcGetFilenameFromPath(filename)                
                        icat_cmd = "icat -o "+str(part2_start)+ " "+ \
                                image + " " + \
                                self.fiDictList[i]['inode'] + ' > /tmp/'+justFilename
                        f2 = os.popen(icat_cmd)

                        # Open the file in the pdf reader if it is a PDF file
                        # else copy it to a file in /tmp
                        if justFilename.endswith('pdf'):
                            print(">>> Opening the PDF file /tmp/",justFilename)  
                            os.system('evince /tmp/'+justFilename)
                        else:
                            print(">>> File copied to: ", '/tmp/'+justFilename)

                return
 
    # Callback function for SAX processing of the dfxml file.
    def cb(self, fi):
        self.fiDictList.append({self.acc_dict_array[0]:fi.filename(), \
                           self.acc_dict_array[1]:fi.partition(), \
                           self.acc_dict_array[2]:fi.inode(), \
                           self.acc_dict_array[3]:fi.name_type(), \
                           self.acc_dict_array[4]:fi.filesize(),\
                           self.acc_dict_array[5]:fi.allocated() })

        
    # The fiwalk utility fiwalk_using_sax is invoked with a callback
    # to process the dfxml file contents.
    def bcProcessDfxmlFileUsingSax(self, dfxmlfile):
        fiwalk.fiwalk_using_sax(xmlfile=open(dfxmlfile, 'rb'),callback=self.cb)

    def cbv_ftype(self, fv):
        self.ftype = fv.ftype_str()

    def bc_get_ftype_from_sax(self, dfxmlfile):
        fiwalk.fiwalk_vobj_using_sax(xmlfile=open(dfxmlfile, 'rb'),callback=self.cbv_ftype)
       
# Generate the XML file using fiwalk
# Generates a temporary file <image_path>/dfxmlfile.xml
# If the file exists, the script terminates indicating the reason.
# User can remove it or rename it to continue.
# The Close routine removes this temporary file.
def bcGenerateDfxmlFile(image, dfxmlfile):
    # First check if the file image exists
    if not os.path.exists(image):
        print(">> Error. Image %s does not exist" %image)
        return None

    cmd = ['fiwalk', '-f', '-X', dfxmlfile, image]
    print(">> Generating XML File ", dfxmlfile)
    print(">> Invoking command for Fiwalk = ", cmd)

    ## subprocess.check_output(cmd, shell=True)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    (data, err) = p.communicate()
    if p.returncode:
        print(">>> Fiwalk command failed for image %s " %image)
        return None
    else:
        print(">>> Generated the file %s " %dfxmlfile)
        return dfxmlfile

# Thread which exports all the checked files 
class daThread(threading.Thread):
    def __init__(self, check, export_dir):
        self.check = check
        self.export_dir = export_dir
        super(daThread, self).__init__()
        self.stoprequest = threading.Event()

    def stopped(self):
        return self.stoprequest.isSet()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(daThread, self).join(timeout)

    def run(self):
        x = Ui_MainWindow
        print(">> File export operation in progress...")
        global g_textEdit
        g_textEdit.append( sys.stdout.getvalue() )
        sys.stdout = x.oldstdout

        BcFileStructure.bcOperateOnFiles(BcFileStructure, self.check, self.export_dir)

        ProgressBar._active = False

        # Set the progressbar maximum to > minimum so the spinning will stop
        global global_pb_da
        global_pb_da.progressbar.setRange(0,1)

        oldstdout = sys.stdout
        sys.stdout = StringIO()
        print(">> Copied checked files to the directory: ", self.export_dir)
        g_textEdit.append( sys.stdout.getvalue() )
        sys.stdout = oldstdout

    # A placeholder for any clean-up operations after cancel is pressed
    def stop(self):
        pass
        ## print(">> D: Terminating the Thread for \"Export Files\"")
        ## g_textEdit.append( sys.stdout.getvalue() )
        ## sys.stdout = oldstdout

# Thread which spins in a loop until the working thread which sets the completed flag.
class guiThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        progressbar = global_pb_da

        progressbar.startLoop()

class ProgressBar( QtGui.QWidget):
    _active = False
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)
        self.progressbar = QtGui.QProgressBar()
        main_layout = QtGui.QGridLayout()
        main_layout.addWidget(self.progressbar, 0, 1)
        self.setLayout(main_layout)
        self.setWindowTitle('Progress')

    def closeEvent(self):
        self._active = False

    def startLoop(self):
        self._active = True
        ProgressBar._active = True
        cntr = 0

        global global_pb_da
        global_pb_da.progressbar.setRange(0,0)

        while True:
            time.sleep(1.05)
            cntr = cntr + 1

            QtGui.qApp.processEvents()
            #print("D: ProgressBar._active = ", ProgressBar._active)
            if not ProgressBar._active:
                #print ("D: startLoop thread detected flag = ", ProgressBar._active)
                global g_thread1_da
                if g_thread1_da.stopped():
                    ## print("D: startLoop_bc: Thread Stopped ")
                    g_thread1_da.stop()
                break

        ProgressBar._active = False
                    
            
if __name__=="__main__":
    import sys, time, re

    parser = ArgumentParser(prog='bc_disk_access.py', description='File Access')
    parser.add_argument('--image', action='store', help="Image file ")
    parser.add_argument('--dfxmlfile', action='store', help="DFXML file ")
    parser.add_argument('--cat',action='store_true',help='list contents ')
    parser.add_argument('--listfiles',action='store_true',help='list file structure ')
    parser.add_argument('--filename',action='store',help='File name to list contents of ')
    parser.add_argument('--outdir',action='store',help='Output Directory ')

    args = parser.parse_args()

    ## print("D: Image: ", args.image)
    ## print("D: dfxmlfile: ", args.dfxmlfile)
    ## print("D: cat: ", args.cat)
    ## print("D: listfiles: ", args.listfiles)
    ## print("D: filename: ", args.filename)
    ## print("D: output file", args.outfile)
    # If dfxmlfile not given, run the fiwalk cmd to extract the dfxml file

    # First check if the file image exists
    if not os.path.exists(args.image):
        print("\n>> Error!! Image %s does not exist \n" %args.image)
        exit(0)

    global isGenDfxmlFile
    isGenDfxmlFile = False

    # If dfxml file not provided, generate it now.
    if (args.dfxmlfile == None):
        # Get the directory where "image" exists
        directory = os.path.dirname(args.image)
        dfxmlfile = directory+'/dfxmlfile.xml'

        if os.path.exists(dfxmlfile):
            print("\n>> File %s exists. Remove it and run the command again.\n" %dfxmlfile)
            exit(0)

        bcGenerateDfxmlFile(args.image, dfxmlfile)
        if dfxmlfile == None:
            print(">> Error: Fiwalk generation failed")
            exit(0)

        isGenDfxmlFile = True
        
    else:
        dfxmlfile = args.dfxmlfile
        if not os.path.exists(dfxmlfile):
            # dfxmlfile provided in the args, but it doesn't exist
            bcGenerateDfxmlFile(args.image, dfxmlfile)
            if dfxmlfile == None:
                print(">> Error: Fiwalk generation failed")
                exit(0)

            ###global isGenDfxmlFile
            isGenDfxmlfile = True

    filestr = BcFileStructure()

    # The following call is just to test bcCatFile, giving a filename
    # from the dfxml file. In reality, it will be invoked from a click on 
    # a file in the web browser.
    if (args.cat == True):
        if args.filename == None or dfxmlfile == None:
            print(">> Filename or dfxml file not provided. Exiting")
            exit(0) 

        if not os.path.exists(dfxmlfile):
            print(">> File %s doesnot exist " %dfxmlfile) 
            exit(0)

        # FIXME: Inode is set to 0 temporarily.
        filestr.bcCatFile(args.filename, 0, args.image, dfxmlfile, False, None)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # expand third container
    ## parent0_item = BcFileStructure.bcExtractFileStr.parent0
    ## index = model.indexFromItem(parent0)
    ## view.expand(index)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # select last row
    ## selmod = view.selectionModel()
    #index2 = model.indexFromItem(child3)
    ## index2 = model.indexFromItem(parent0)
    ## selmod.select(index2, QtGui.QItemSelectionModel.Select|QtGui.QItemSelectionModel.Rows)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if (args.listfiles == True):
        app = QtGui.QApplication(sys.argv)
        MainWindow = QtGui.QMainWindow()
        ui = Ui_MainWindow(args.outdir)
        ui.setupUi(MainWindow)

        filestr.bcExtractFileStr(args.image, dfxmlfile, args.outdir)
        MainWindow.show()
        sys.exit(app.exec_())
