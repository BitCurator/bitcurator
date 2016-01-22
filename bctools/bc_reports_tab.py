#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# BitCurator
#
# bc_reports_tab5.py
#
# Implementation of GUI interface in PyQT4 for generating various files and
# reports for Bitcurator project.
# Form implementation generated from reading ui file 'bc_reports_tab7*.ui'
# Heavily modified manually
#
# Created: Sat Jul 6 20:33:35 2013
# by: PyQt4 UI code generator 4.9.1
#

import os
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from subprocess import Popen,PIPE
import sys, time
import threading
from bc_genrep_premis import BcPremisFile

from generate_report import *
from bc_utils import *
#from bc_disk_access import *
#from PyQt4.Qsci import *
from os.path import expanduser

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

# The following global variables are used as they are used in the
# threads which access attributes defined in other classes. In Python this
# seems to be the only simple solution for a case like this where the 
# GUI attributes are initialized only once by the main routine.
global_allrep = "null"
global_fw = "null"
#global_acc = "null"
g_textEdit_allrepcmdlineoutput = "null"
g_textEdit_fwcmdlineoutput = "null"
#g_textEdit_acc = "null"
g_xmlFwFilename = "null"
global_ann = "null"
g_textEdit_anncmdlineoutput = "null"
#g_acc_outdir = "null"
#g_acc_dfxmlfile = "null"
#g_acc_image = "null"

class Ui_MainWindow(object):
    #def __init__(self, parent=None):
        #self.setupUi(MainWindow)

    imageFileName = "null"
    allrepImageFileName = "null"
    fwImageFileName = "null"
    beImageFileName = "null"
    annImageFileName = "null"
    #accImageFileName = "null"
    xmlFileName = "null"
    fwXmlFileName = "null"
    allrepXmlFileName = "null"
    allrepBeFeatDir = "null"
    allrepOutDir = "null"
    TextFileName = "null"
    beDir = "null"
    annDir = "null"
    bcpyDir = "null"
    annBcpyDir = "null"
    allrepBcpyDir = "null"
    outputDirName = "null"
    beOutputDirName = "null"
    configFileName = "null"
    reportsDir = "null"
    annOutputDirName = "null"
    #accOutdirName = "null"
    annBeFeatDir = "null"
    repFwXmlFileName = "null"
    repOutDir = "null"
    repConfile = "null"
    allrepConfile = "null"
    repAnnDir = "null"
    progressBar_fw = "null"
    #progressBar_acc = "null"
    progressBar_allrep = "null"

    # The standard output from this point is placed by an in-memory
    # buffer. This was originally done much later, but due to the indroduction
    # of the threads which need to access these elements, this was put in
    # global location.
    oldstdout = sys.stdout
    sys.stdout = StringIO()

    global g_oldstdout
    g_oldstdout = oldstdout

    global g_fwXmlFileName
    g_fwXmlFileName =  fwXmlFileName

    global g_allrepXmlFileName
    g_allrepXmlFileName =  allrepXmlFileName

    def setupUi(self, MainWindow):
        # Save the current working directory
        self.cwd = os.getcwd()
        # Set the directory to user's home directory
        os.chdir(os.environ["HOME"])

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(609, 715)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_allrep = QtGui.QWidget()
        self.tab_allrep.setObjectName(_fromUtf8("tab_allrep"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab_allrep)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_allrephdr_bev = QtGui.QLabel(self.tab_allrep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_allrephdr_bev.setFont(font)
        self.label_allrephdr_bev.setWordWrap(True)
        self.label_allrephdr_bev.setObjectName(_fromUtf8("label_allrephdr_bev"))
        self.gridLayout_5.addWidget(self.label_allrephdr_bev, 1, 0, 1, 3)
        self.toolButton_allrep_beFeatDir = QtGui.QToolButton(self.tab_allrep)
        self.toolButton_allrep_beFeatDir.setObjectName(_fromUtf8("toolButton_allrep_beFeatDir"))
        self.gridLayout_5.addWidget(self.toolButton_allrep_beFeatDir, 5, 5, 1, 1)
        self.pushButton_bev = QtGui.QPushButton(self.tab_allrep)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_bev.sizePolicy().hasHeightForWidth())
        self.pushButton_bev.setSizePolicy(sizePolicy)
        self.pushButton_bev.setObjectName(_fromUtf8("pushButton_bev"))
        self.gridLayout_5.addWidget(self.pushButton_bev, 1, 3, 1, 3)
        self.pb_allrep_cancel = QtGui.QPushButton(self.tab_allrep)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_allrep_cancel.sizePolicy().hasHeightForWidth())
        self.pb_allrep_cancel.setSizePolicy(sizePolicy)
        self.pb_allrep_cancel.setObjectName(_fromUtf8("pb_allrep_cancel"))
        self.gridLayout_5.addWidget(self.pb_allrep_cancel, 12, 2, 1, 2)
        self.lineEdit_allrep_confile = QtGui.QLineEdit(self.tab_allrep)
        self.lineEdit_allrep_confile.setObjectName(_fromUtf8("lineEdit_allrep_confile"))
        self.gridLayout_5.addWidget(self.lineEdit_allrep_confile, 9, 0, 1, 5)
        self.toolButton_allrep_confile = QtGui.QToolButton(self.tab_allrep)
        self.toolButton_allrep_confile.setObjectName(_fromUtf8("toolButton_allrep_confile"))
        self.gridLayout_5.addWidget(self.toolButton_allrep_confile, 9, 5, 1, 1)
        self.toolButton_allrep_outdir = QtGui.QToolButton(self.tab_allrep)
        self.toolButton_allrep_outdir.setObjectName(_fromUtf8("toolButton_allrep_outdir"))
        self.gridLayout_5.addWidget(self.toolButton_allrep_outdir, 7, 5, 1, 1)
        self.pb_allrep_run = QtGui.QPushButton(self.tab_allrep)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_allrep_run.sizePolicy().hasHeightForWidth())
        self.pb_allrep_run.setSizePolicy(sizePolicy)
        self.pb_allrep_run.setObjectName(_fromUtf8("pb_allrep_run"))
        self.gridLayout_5.addWidget(self.pb_allrep_run, 12, 4, 1, 1)
        self.pb_allrep_close = QtGui.QPushButton(self.tab_allrep)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_allrep_close.sizePolicy().hasHeightForWidth())
        self.pb_allrep_close.setSizePolicy(sizePolicy)
        self.pb_allrep_close.setObjectName(_fromUtf8("pb_allrep_close"))
        self.gridLayout_5.addWidget(self.pb_allrep_close, 12, 1, 1, 1)
        self.label_allrep_image = QtGui.QLabel(self.tab_allrep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_allrep_image.setFont(font)
        self.label_allrep_image.setObjectName(_fromUtf8("label_allrep_image"))
        self.gridLayout_5.addWidget(self.label_allrep_image, 2, 0, 1, 1)
        self.label_allrep_beFeatDir = QtGui.QLabel(self.tab_allrep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_allrep_beFeatDir.setFont(font)
        self.label_allrep_beFeatDir.setObjectName(_fromUtf8("label_allrep_beFeatDir"))
        self.gridLayout_5.addWidget(self.label_allrep_beFeatDir, 4, 0, 1, 3)

        self.textEdit_allrep = QtGui.QTextEdit(self.tab_allrep)
        self.textEdit_allrep.setAutoFillBackground(True)
        self.textEdit_allrep.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_allrep.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_allrep.setMouseTracking(True)

        self.textEdit_allrep.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit_allrep.setObjectName(_fromUtf8("textEdit_allrep"))
        self.gridLayout_5.addWidget(self.textEdit_allrep, 11, 0, 1, 5)

        #.#
        global g_textEdit_allrepcmdlineoutput
        g_textEdit_allrepcmdlineoutput = self.textEdit_allrep

        self.label_allrep_confile = QtGui.QLabel(self.tab_allrep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_allrep_confile.setFont(font)
        self.label_allrep_confile.setObjectName(_fromUtf8("label_allrep_confile"))
        self.gridLayout_5.addWidget(self.label_allrep_confile, 8, 0, 1, 1)
        self.lineEdit_allrep_beFeatDir = QtGui.QLineEdit(self.tab_allrep)
        self.lineEdit_allrep_beFeatDir.setObjectName(_fromUtf8("lineEdit_allrep_beFeatDir"))
        self.gridLayout_5.addWidget(self.lineEdit_allrep_beFeatDir, 5, 0, 1, 5)
        self.toolButton_allrep_image = QtGui.QToolButton(self.tab_allrep)
        self.toolButton_allrep_image.setObjectName(_fromUtf8("toolButton_allrep_image"))
        self.gridLayout_5.addWidget(self.toolButton_allrep_image, 3, 5, 1, 1)
        self.label_allrephdr = QtGui.QLabel(self.tab_allrep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_allrephdr.setFont(font)
        self.label_allrephdr.setWordWrap(True)
        self.label_allrephdr.setObjectName(_fromUtf8("label_allrephdr"))
        self.gridLayout_5.addWidget(self.label_allrephdr, 0, 0, 1, 6)
        self.lineEdit_allrep_image = QtGui.QLineEdit(self.tab_allrep)
        self.lineEdit_allrep_image.setText(_fromUtf8(""))
        self.lineEdit_allrep_image.setObjectName(_fromUtf8("lineEdit_allrep_image"))
        self.gridLayout_5.addWidget(self.lineEdit_allrep_image, 3, 0, 1, 5)


        #.#
        #self.progressBar_allrep = QtGui.QProgressBar(self.tab_allrep)
        self.progressBar_allrep = ProgressBar()
        global global_allrep
        global_allrep = self.progressBar_allrep


        self.progressBar_allrep.setEnabled(True)
        self.progressBar_allrep.setProperty("value", 1)
        self.progressBar_allrep.setObjectName(_fromUtf8("progressBar_allrep"))
        self.gridLayout_5.addWidget(self.progressBar_allrep, 12, 0, 1, 1)
        self.lineEdit_allrep_outdir = QtGui.QLineEdit(self.tab_allrep)
        self.lineEdit_allrep_outdir.setObjectName(_fromUtf8("lineEdit_allrep_outdir"))
        self.gridLayout_5.addWidget(self.lineEdit_allrep_outdir, 7, 0, 1, 5)
        self.label_allrep_outdir = QtGui.QLabel(self.tab_allrep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_allrep_outdir.setFont(font)
        self.label_allrep_outdir.setObjectName(_fromUtf8("label_allrep_outdir"))
        self.gridLayout_5.addWidget(self.label_allrep_outdir, 6, 0, 1, 5)
        self.label_allrep_cmdlineoutput = QtGui.QLabel(self.tab_allrep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_allrep_cmdlineoutput.setFont(font)
        self.label_allrep_cmdlineoutput.setObjectName(_fromUtf8("label_allrep_cmdlineoutput"))
        self.gridLayout_5.addWidget(self.label_allrep_cmdlineoutput, 10, 0, 1, 1)
        self.tabWidget.addTab(self.tab_allrep, _fromUtf8(""))
        self.tab_fw = QtGui.QWidget()
        self.tab_fw.setObjectName(_fromUtf8("tab_fw"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_fw)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lineEdit_fw_xmlFile = QtGui.QLineEdit(self.tab_fw)
        self.lineEdit_fw_xmlFile.setObjectName(_fromUtf8("lineEdit_fw_xmlFile"))
        self.gridLayout_3.addWidget(self.lineEdit_fw_xmlFile, 5, 0, 1, 4)
        self.label_fw_image = QtGui.QLabel(self.tab_fw)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_fw_image.setFont(font)
        self.label_fw_image.setObjectName(_fromUtf8("label_fw_image"))
        self.gridLayout_3.addWidget(self.label_fw_image, 1, 0, 1, 1)
        self.lineEdit_fw_image = QtGui.QLineEdit(self.tab_fw)
        self.lineEdit_fw_image.setObjectName(_fromUtf8("lineEdit_fw_image"))
        self.gridLayout_3.addWidget(self.lineEdit_fw_image, 2, 0, 1, 4)
        self.toolButton_fw_xmlFile = QtGui.QToolButton(self.tab_fw)
        self.toolButton_fw_xmlFile.setObjectName(_fromUtf8("toolButton_fw_xmlFile"))
        self.gridLayout_3.addWidget(self.toolButton_fw_xmlFile, 5, 4, 1, 1)
        self.toolButton_fw_image = QtGui.QToolButton(self.tab_fw)
        self.toolButton_fw_image.setObjectName(_fromUtf8("toolButton_fw_image"))
        self.gridLayout_3.addWidget(self.toolButton_fw_image, 2, 4, 1, 1)

        #.#
        #self.progressBar_fw = QtGui.QProgressBar(self.tab_fw)
        self.progressBar_fw = ProgressBar()
        global global_fw
        global_fw =  self.progressBar_fw

        self.progressBar_fw.setProperty("value", 1)
        self.progressBar_fw.setObjectName(_fromUtf8("progressBar_fw"))
        self.gridLayout_3.addWidget(self.progressBar_fw, 10, 0, 1, 1)
        self.textEdit_fwcmdlineoutput = QtGui.QTextEdit(self.tab_fw)

        # Save some class-specific vars in global vars for later use in threads
        global g_textEdit_fwcmdlineoutput
        g_textEdit_fwcmdlineoutput = self.textEdit_fwcmdlineoutput

        self.textEdit_fwcmdlineoutput.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit_fwcmdlineoutput.setObjectName(_fromUtf8("textEdit_fwcmdlineoutput"))
        self.gridLayout_3.addWidget(self.textEdit_fwcmdlineoutput, 9, 0, 1, 4)
        self.pb_fw_cancel = QtGui.QPushButton(self.tab_fw)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_fw_cancel.sizePolicy().hasHeightForWidth())
        self.pb_fw_cancel.setSizePolicy(sizePolicy)
        self.pb_fw_cancel.setObjectName(_fromUtf8("pb_fw_cancel"))
        self.gridLayout_3.addWidget(self.pb_fw_cancel, 10, 2, 1, 1)
        self.label_fwcmdlineoutput = QtGui.QLabel(self.tab_fw)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_fwcmdlineoutput.setFont(font)
        self.label_fwcmdlineoutput.setObjectName(_fromUtf8("label_fwcmdlineoutput"))
        self.gridLayout_3.addWidget(self.label_fwcmdlineoutput, 8, 0, 1, 1)
        self.pb_fw_close = QtGui.QPushButton(self.tab_fw)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_fw_close.sizePolicy().hasHeightForWidth())
        self.pb_fw_close.setSizePolicy(sizePolicy)
        self.pb_fw_close.setObjectName(_fromUtf8("pb_fw_close"))
        self.gridLayout_3.addWidget(self.pb_fw_close, 10, 1, 1, 1)
        self.pb_fw_run = QtGui.QPushButton(self.tab_fw)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_fw_run.sizePolicy().hasHeightForWidth())
        self.pb_fw_run.setSizePolicy(sizePolicy)
        self.pb_fw_run.setObjectName(_fromUtf8("pb_fw_run"))
        self.gridLayout_3.addWidget(self.pb_fw_run, 10, 3, 1, 1)
        self.label_fwhdr = QtGui.QLabel(self.tab_fw)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_fwhdr.setFont(font)
        self.label_fwhdr.setWordWrap(True)
        self.label_fwhdr.setObjectName(_fromUtf8("label_fwhdr"))
        self.gridLayout_3.addWidget(self.label_fwhdr, 0, 0, 1, 5)
        self.label_fw_xmlFile = QtGui.QLabel(self.tab_fw)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_fw_xmlFile.setFont(font)
        self.label_fw_xmlFile.setObjectName(_fromUtf8("label_fw_xmlFile"))
        self.gridLayout_3.addWidget(self.label_fw_xmlFile, 4, 0, 1, 1)
        self.tabWidget.addTab(self.tab_fw, _fromUtf8(""))
        self.tab_ann = QtGui.QWidget()
        self.tab_ann.setObjectName(_fromUtf8("tab_ann"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_ann)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_ann_annDir = QtGui.QLabel(self.tab_ann)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ann_annDir.setFont(font)
        self.label_ann_annDir.setObjectName(_fromUtf8("label_ann_annDir"))
        self.gridLayout_4.addWidget(self.label_ann_annDir, 5, 0, 1, 4)
        self.pb_ann_close = QtGui.QPushButton(self.tab_ann)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_ann_close.sizePolicy().hasHeightForWidth())
        self.pb_ann_close.setSizePolicy(sizePolicy)
        self.pb_ann_close.setObjectName(_fromUtf8("pb_ann_close"))
        self.gridLayout_4.addWidget(self.pb_ann_close, 11, 2, 1, 1)
        self.toolButton_ann_annDir = QtGui.QToolButton(self.tab_ann)
        self.toolButton_ann_annDir.setObjectName(_fromUtf8("toolButton_ann_annDir"))
        self.gridLayout_4.addWidget(self.toolButton_ann_annDir, 6, 5, 1, 1)
        self.label_anncmdlineoutput = QtGui.QLabel(self.tab_ann)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_anncmdlineoutput.setFont(font)
        self.label_anncmdlineoutput.setObjectName(_fromUtf8("label_anncmdlineoutput"))
        self.gridLayout_4.addWidget(self.label_anncmdlineoutput, 9, 0, 1, 1)
        self.toolButton_ann_image = QtGui.QToolButton(self.tab_ann)
        self.toolButton_ann_image.setObjectName(_fromUtf8("toolButton_ann_image"))
        self.gridLayout_4.addWidget(self.toolButton_ann_image, 2, 5, 1, 1)
        self.label_ann_image = QtGui.QLabel(self.tab_ann)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ann_image.setFont(font)
        self.label_ann_image.setObjectName(_fromUtf8("label_ann_image"))
        self.gridLayout_4.addWidget(self.label_ann_image, 1, 0, 1, 1)
        self.label_ann_beFeatDir = QtGui.QLabel(self.tab_ann)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ann_beFeatDir.setFont(font)
        self.label_ann_beFeatDir.setObjectName(_fromUtf8("label_ann_beFeatDir"))
        self.gridLayout_4.addWidget(self.label_ann_beFeatDir, 3, 0, 1, 4)
        self.pb_ann_cancel = QtGui.QPushButton(self.tab_ann)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_ann_cancel.sizePolicy().hasHeightForWidth())
        self.pb_ann_cancel.setSizePolicy(sizePolicy)
        self.pb_ann_cancel.setObjectName(_fromUtf8("pb_ann_cancel"))
        self.gridLayout_4.addWidget(self.pb_ann_cancel, 11, 3, 1, 1)
        self.pb_ann_run = QtGui.QPushButton(self.tab_ann)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_ann_run.sizePolicy().hasHeightForWidth())
        self.pb_ann_run.setSizePolicy(sizePolicy)
        self.pb_ann_run.setObjectName(_fromUtf8("pb_ann_run"))
        self.gridLayout_4.addWidget(self.pb_ann_run, 11, 4, 1, 1)
        self.lineEdit_ann_image = QtGui.QLineEdit(self.tab_ann)
        self.lineEdit_ann_image.setText(_fromUtf8(""))
        self.lineEdit_ann_image.setObjectName(_fromUtf8("lineEdit_ann_image"))
        self.gridLayout_4.addWidget(self.lineEdit_ann_image, 2, 0, 1, 5)
        self.lineEdit_ann_bcpyDir = QtGui.QLineEdit(self.tab_ann)
        self.lineEdit_ann_bcpyDir.setText(_fromUtf8(""))
        self.lineEdit_ann_bcpyDir.setObjectName(_fromUtf8("lineEdit_ann_bcpyDir"))
        self.gridLayout_4.addWidget(self.lineEdit_ann_bcpyDir, 8, 0, 1, 5)
        self.toolButton_ann_beFeatDir = QtGui.QToolButton(self.tab_ann)
        self.toolButton_ann_beFeatDir.setObjectName(_fromUtf8("toolButton_ann_beFeatDir"))
        self.gridLayout_4.addWidget(self.toolButton_ann_beFeatDir, 4, 5, 1, 1)
        self.label_ann_bcpyDir = QtGui.QLabel(self.tab_ann)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ann_bcpyDir.setFont(font)
        self.label_ann_bcpyDir.setObjectName(_fromUtf8("label_ann_bcpyDir"))
        self.gridLayout_4.addWidget(self.label_ann_bcpyDir, 7, 0, 1, 4)
        self.label_annhdr = QtGui.QLabel(self.tab_ann)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_annhdr.setFont(font)
        self.label_annhdr.setWordWrap(True)
        self.label_annhdr.setObjectName(_fromUtf8("label_annhdr"))
        self.gridLayout_4.addWidget(self.label_annhdr, 0, 0, 1, 6)
        self.lineEdit_ann_annDir = QtGui.QLineEdit(self.tab_ann)
        self.lineEdit_ann_annDir.setObjectName(_fromUtf8("lineEdit_ann_annDir"))
        self.gridLayout_4.addWidget(self.lineEdit_ann_annDir, 6, 0, 1, 5)
        self.lineEdit_ann_beFeatDir = QtGui.QLineEdit(self.tab_ann)
        self.lineEdit_ann_beFeatDir.setText(_fromUtf8(""))
        self.lineEdit_ann_beFeatDir.setObjectName(_fromUtf8("lineEdit_ann_beFeatDir"))
        self.gridLayout_4.addWidget(self.lineEdit_ann_beFeatDir, 4, 0, 1, 5)
        self.toolButton_ann_bcpyDir = QtGui.QToolButton(self.tab_ann)
        self.toolButton_ann_bcpyDir.setObjectName(_fromUtf8("toolButton_ann_bcpyDir"))
        self.gridLayout_4.addWidget(self.toolButton_ann_bcpyDir, 8, 5, 1, 1)

        #.#        
        #self.progressBar_ann = QtGui.QProgressBar(self.tab_ann)
        self.progressBar_ann = ProgressBar()
        global global_ann
        global_ann = self.progressBar_ann

        self.progressBar_ann.setProperty("value", 1)
        self.progressBar_ann.setObjectName(_fromUtf8("progressBar_ann"))
        self.gridLayout_4.addWidget(self.progressBar_ann, 11, 0, 1, 1)
        self.textEdit_ann = QtGui.QTextEdit(self.tab_ann)
        self.textEdit_ann.setAutoFillBackground(True)

        #.#
        global g_textEdit_anncmdlineoutput
        g_textEdit_anncmdlineoutput = self.textEdit_ann

        self.textEdit_ann.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit_ann.setObjectName(_fromUtf8("textEdit_ann"))
        self.gridLayout_4.addWidget(self.textEdit_ann, 10, 0, 1, 5)
        self.tabWidget.addTab(self.tab_ann, _fromUtf8(""))
        self.tab_rep = QtGui.QWidget()
        self.tab_rep.setObjectName(_fromUtf8("tab_rep"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_rep)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lineEdit_rep_outdir = QtGui.QLineEdit(self.tab_rep)
        self.lineEdit_rep_outdir.setObjectName(_fromUtf8("lineEdit_rep_outdir"))
        self.gridLayout_2.addWidget(self.lineEdit_rep_outdir, 6, 0, 1, 4)
        self.label_rephdr = QtGui.QLabel(self.tab_rep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_rephdr.setFont(font)
        self.label_rephdr.setWordWrap(True)
        self.label_rephdr.setObjectName(_fromUtf8("label_rephdr"))
        self.gridLayout_2.addWidget(self.label_rephdr, 0, 0, 1, 5)
        self.label_rep_fwxmlfile = QtGui.QLabel(self.tab_rep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_rep_fwxmlfile.setFont(font)
        self.label_rep_fwxmlfile.setObjectName(_fromUtf8("label_rep_fwxmlfile"))
        self.gridLayout_2.addWidget(self.label_rep_fwxmlfile, 1, 0, 1, 1)
        self.lineEdit_rep_fwxmlfile = QtGui.QLineEdit(self.tab_rep)
        self.lineEdit_rep_fwxmlfile.setText(_fromUtf8(""))
        self.lineEdit_rep_fwxmlfile.setObjectName(_fromUtf8("lineEdit_rep_fwxmlfile"))
        self.gridLayout_2.addWidget(self.lineEdit_rep_fwxmlfile, 2, 0, 1, 4)
        self.toolButton_rep_fwxmlfile = QtGui.QToolButton(self.tab_rep)
        self.toolButton_rep_fwxmlfile.setObjectName(_fromUtf8("toolButton_rep_fwxmlfile"))
        self.gridLayout_2.addWidget(self.toolButton_rep_fwxmlfile, 2, 4, 1, 1)
        self.label_rep_annDir = QtGui.QLabel(self.tab_rep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_rep_annDir.setFont(font)
        self.label_rep_annDir.setObjectName(_fromUtf8("label_rep_annDir"))
        self.gridLayout_2.addWidget(self.label_rep_annDir, 3, 0, 1, 1)
        self.lineEdit_rep_annDir = QtGui.QLineEdit(self.tab_rep)
        self.lineEdit_rep_annDir.setText(_fromUtf8(""))
        self.lineEdit_rep_annDir.setObjectName(_fromUtf8("lineEdit_rep_annDir"))
        self.gridLayout_2.addWidget(self.lineEdit_rep_annDir, 4, 0, 1, 4)
        self.toolButton_rep_annDir = QtGui.QToolButton(self.tab_rep)
        self.toolButton_rep_annDir.setObjectName(_fromUtf8("toolButton_rep_annDir"))
        self.gridLayout_2.addWidget(self.toolButton_rep_annDir, 4, 4, 1, 1)
        self.label_rep_outdir = QtGui.QLabel(self.tab_rep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_rep_outdir.setFont(font)
        self.label_rep_outdir.setObjectName(_fromUtf8("label_rep_outdir"))
        self.gridLayout_2.addWidget(self.label_rep_outdir, 5, 0, 1, 1)
        self.toolButton_rep_outdir = QtGui.QToolButton(self.tab_rep)
        self.toolButton_rep_outdir.setObjectName(_fromUtf8("toolButton_rep_outdir"))
        self.gridLayout_2.addWidget(self.toolButton_rep_outdir, 6, 4, 1, 1)
        self.label_rep_confile = QtGui.QLabel(self.tab_rep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_rep_confile.setFont(font)
        self.label_rep_confile.setObjectName(_fromUtf8("label_rep_confile"))
        self.gridLayout_2.addWidget(self.label_rep_confile, 7, 0, 1, 1)
        self.lineEdit_rep_confile = QtGui.QLineEdit(self.tab_rep)
        self.lineEdit_rep_confile.setObjectName(_fromUtf8("lineEdit_rep_confile"))
        self.gridLayout_2.addWidget(self.lineEdit_rep_confile, 8, 0, 1, 4)
        self.toolButton_rep_confile = QtGui.QToolButton(self.tab_rep)
        self.toolButton_rep_confile.setObjectName(_fromUtf8("toolButton_rep_confile"))
        self.gridLayout_2.addWidget(self.toolButton_rep_confile, 8, 4, 1, 1)
        self.label_rep_cmdlineoutput = QtGui.QLabel(self.tab_rep)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_rep_cmdlineoutput.setFont(font)
        self.label_rep_cmdlineoutput.setObjectName(_fromUtf8("label_rep_cmdlineoutput"))
        self.gridLayout_2.addWidget(self.label_rep_cmdlineoutput, 9, 0, 1, 1)
        self.pb_rep_run = QtGui.QPushButton(self.tab_rep)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_rep_run.sizePolicy().hasHeightForWidth())
        self.pb_rep_run.setSizePolicy(sizePolicy)
        self.pb_rep_run.setObjectName(_fromUtf8("pb_rep_run"))
        self.gridLayout_2.addWidget(self.pb_rep_run, 11, 3, 1, 1)
        self.pb_rep_cancel = QtGui.QPushButton(self.tab_rep)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_rep_cancel.sizePolicy().hasHeightForWidth())
        self.pb_rep_cancel.setSizePolicy(sizePolicy)
        self.pb_rep_cancel.setObjectName(_fromUtf8("pb_rep_cancel"))
        self.gridLayout_2.addWidget(self.pb_rep_cancel, 11, 2, 1, 1)
        self.pb_rep_close = QtGui.QPushButton(self.tab_rep)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_rep_close.sizePolicy().hasHeightForWidth())
        self.pb_rep_close.setSizePolicy(sizePolicy)
        self.pb_rep_close.setObjectName(_fromUtf8("pb_rep_close"))
        self.gridLayout_2.addWidget(self.pb_rep_close, 11, 1, 1, 1)

        #.#
        #self.progressBar_rep = QtGui.QProgressBar(self.tab_rep)
        self.progressBar_rep = ProgressBar()
        global global_rep
        global_rep = self.progressBar_rep


        self.progressBar_rep.setProperty("value", 1)
        self.progressBar_rep.setObjectName(_fromUtf8("progressBar_rep"))
        self.gridLayout_2.addWidget(self.progressBar_rep, 11, 0, 1, 1)
        self.textEdit_rep = QtGui.QTextEdit(self.tab_rep)
        self.textEdit_rep.setAutoFillBackground(True)

        global g_textEdit_repcmdlineoutput
        g_textEdit_repcmdlineoutput = self.textEdit_rep

 
        self.textEdit_rep.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit_rep.setObjectName(_fromUtf8("textEdit_rep"))
        self.gridLayout_2.addWidget(self.textEdit_rep, 10, 0, 1, 4)
        self.tabWidget.addTab(self.tab_rep, _fromUtf8(""))

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 609, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionShow_Help = QtGui.QAction(MainWindow)
        self.actionShow_Help.setObjectName(_fromUtf8("actionShow_Help"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionPaste)
        self.menuHelp.addAction(self.actionShow_Help)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # File navigation for All Run tab
        QtCore.QObject.connect(self.toolButton_allrep_image, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getAllrepImageFileName)

        QtCore.QObject.connect(self.toolButton_allrep_beFeatDir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getAllrepBeFeatDir)

        QtCore.QObject.connect(self.toolButton_allrep_outdir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getAllrepOutDir)

        QtCore.QObject.connect(self.toolButton_allrep_confile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getAllrepConfigFile)

        QtCore.QObject.connect(self.pb_allrep_run, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedOkAllrep)
        QtCore.QObject.connect(self.pb_allrep_close, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedClose)
        QtCore.QObject.connect(self.pb_allrep_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedCancel_allrep)

        # File navigation for Fiwalk XML Generation tab
        
        QtCore.QObject.connect(self.toolButton_fw_image, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getFwImageFileName)

        QtCore.QObject.connect(self.toolButton_fw_xmlFile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getFwOutputXmlFilePath)

        QtCore.QObject.connect(self.pb_fw_run, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedOkFw)
        QtCore.QObject.connect(self.pb_fw_close, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedClose)
        QtCore.QObject.connect(self.pb_fw_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedCancel_fw)

        # File navigation for Annotated files Tab
        QtCore.QObject.connect(self.toolButton_ann_image, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getAnnImageFileName)

        QtCore.QObject.connect(self.toolButton_ann_beFeatDir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getBeFeatDir)
        QtCore.QObject.connect(self.toolButton_ann_annDir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getAnnOutputDir)
        QtCore.QObject.connect(self.toolButton_ann_bcpyDir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getAnnBcpyDir)

        QtCore.QObject.connect(self.pb_ann_run, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedOkAnn)
        QtCore.QObject.connect(self.pb_ann_close, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedClose)
        QtCore.QObject.connect(self.pb_ann_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedCancel_ann)

        # File navigation for Reports Tab
        QtCore.QObject.connect(self.toolButton_rep_fwxmlfile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getRepFwXmlFileName)
        QtCore.QObject.connect(self.toolButton_rep_outdir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getRepOutputDir)
        QtCore.QObject.connect(self.toolButton_rep_confile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getRepConfigFile)
        QtCore.QObject.connect(self.toolButton_rep_annDir, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getRepBeAnnotatedDir)

        QtCore.QObject.connect(self.pb_rep_run, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedOkRep)
        QtCore.QObject.connect(self.pb_rep_close, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedClose)
        QtCore.QObject.connect(self.pb_rep_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buttonClickedCancel_rep)


        self.actionExit.triggered.connect(self.exitMenu)
        self.actionCopy.triggered.connect(self.copyMenu)
        self.actionCut.triggered.connect(self.cutMenu)
        self.actionPaste.triggered.connect(self.pasteMenu)


        self.progressBar_fw.show()
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setTabOrder(self.tabWidget, self.pushButton_bev)
        MainWindow.setTabOrder(self.pushButton_bev, self.lineEdit_allrep_image)
        MainWindow.setTabOrder(self.lineEdit_allrep_image, self.toolButton_allrep_image)
        MainWindow.setTabOrder(self.toolButton_allrep_image, self.lineEdit_allrep_beFeatDir)
        MainWindow.setTabOrder(self.lineEdit_allrep_beFeatDir, self.toolButton_allrep_beFeatDir)
        MainWindow.setTabOrder(self.toolButton_allrep_beFeatDir, self.lineEdit_allrep_outdir)
        MainWindow.setTabOrder(self.lineEdit_allrep_outdir, self.toolButton_allrep_outdir)
        MainWindow.setTabOrder(self.toolButton_allrep_outdir, self.lineEdit_allrep_confile)
        MainWindow.setTabOrder(self.lineEdit_allrep_confile, self.toolButton_allrep_confile)
        MainWindow.setTabOrder(self.toolButton_allrep_confile, self.pb_allrep_close)
        MainWindow.setTabOrder(self.pb_allrep_close, self.pb_allrep_cancel)
        MainWindow.setTabOrder(self.pb_allrep_cancel, self.pb_allrep_run)
        MainWindow.setTabOrder(self.pb_allrep_run, self.textEdit_allrep)
        MainWindow.setTabOrder(self.textEdit_allrep, self.lineEdit_fw_image)
        MainWindow.setTabOrder(self.lineEdit_fw_image, self.toolButton_fw_image)
        MainWindow.setTabOrder(self.toolButton_fw_image, self.lineEdit_fw_xmlFile)
        MainWindow.setTabOrder(self.lineEdit_fw_xmlFile, self.toolButton_fw_xmlFile)
        MainWindow.setTabOrder(self.toolButton_fw_xmlFile, self.textEdit_fwcmdlineoutput)
        MainWindow.setTabOrder(self.textEdit_fwcmdlineoutput, self.pb_fw_close)
        MainWindow.setTabOrder(self.pb_fw_close, self.pb_fw_cancel)
        MainWindow.setTabOrder(self.pb_fw_cancel, self.pb_fw_run)
        MainWindow.setTabOrder(self.pb_fw_run, self.lineEdit_ann_image)
        MainWindow.setTabOrder(self.lineEdit_ann_image, self.toolButton_ann_image)
        MainWindow.setTabOrder(self.toolButton_ann_image, self.lineEdit_ann_beFeatDir)
        MainWindow.setTabOrder(self.lineEdit_ann_beFeatDir, self.toolButton_ann_beFeatDir)
        MainWindow.setTabOrder(self.toolButton_ann_beFeatDir, self.lineEdit_ann_annDir)
        MainWindow.setTabOrder(self.lineEdit_ann_annDir, self.toolButton_ann_annDir)
        MainWindow.setTabOrder(self.toolButton_ann_annDir, self.lineEdit_ann_bcpyDir)
        MainWindow.setTabOrder(self.lineEdit_ann_bcpyDir, self.toolButton_ann_bcpyDir)
        MainWindow.setTabOrder(self.toolButton_ann_bcpyDir, self.textEdit_ann)
        MainWindow.setTabOrder(self.textEdit_ann, self.pb_ann_close)
        MainWindow.setTabOrder(self.pb_ann_close, self.pb_ann_cancel)
        MainWindow.setTabOrder(self.pb_ann_cancel, self.pb_ann_run)
        MainWindow.setTabOrder(self.pb_ann_run, self.lineEdit_rep_fwxmlfile)
        MainWindow.setTabOrder(self.lineEdit_rep_fwxmlfile, self.toolButton_rep_fwxmlfile)
        MainWindow.setTabOrder(self.toolButton_rep_fwxmlfile, self.lineEdit_rep_annDir)
        MainWindow.setTabOrder(self.lineEdit_rep_annDir, self.toolButton_rep_annDir)
        MainWindow.setTabOrder(self.toolButton_rep_annDir, self.lineEdit_rep_outdir)
        MainWindow.setTabOrder(self.lineEdit_rep_outdir, self.toolButton_rep_outdir)
        MainWindow.setTabOrder(self.toolButton_rep_outdir, self.lineEdit_rep_confile)
        MainWindow.setTabOrder(self.lineEdit_rep_confile, self.toolButton_rep_confile)
        MainWindow.setTabOrder(self.toolButton_rep_confile, self.textEdit_rep)
        MainWindow.setTabOrder(self.textEdit_rep, self.pb_rep_close)
        MainWindow.setTabOrder(self.pb_rep_close, self.pb_rep_cancel)
        MainWindow.setTabOrder(self.pb_rep_cancel, self.pb_rep_run)


    def exitMenu(self):
        QtCore.QCoreApplication.instance().quit()

    def cutMenu(self):

        cutData = myClipBoard.text("plain",QClipboard.Selection)
        print ("The clipboard has ",  cutData)
        print ("SELECTION ",  QClipboard.Selection)
        print ("CLIPBOARD ",  QClipboard.Clipboard)
        print ("OWNS_CLIPBOARD ",  QClipboard.ownsClipboard())
        print ("OWNS_FINDBUF ",  QClipboard.ownsFindBuffer())
        print ("OWNS_Selection ",  QClipboard.ownsSelection())
        myClipBoard.setText(cutData.text(), QClipboard.Selection)

    def copyMenu(self):
        print("Copying text ")

    def pasteMenu(self):
        print("PASTINGg text ")

    #
    # buttonClickCancel_allrep: Handle Cancel button for Run All tab 
    #
    def buttonClickedCancel_allrep(self):
        print(">> Run All Task Cancelled ")

        # Set the active flag to False
        ProgressBar._active = False

        # Set the progressbar maximum to > minimum so the spinning will stop
        global global_allrep
        global_allrep.progressbar.setRange(0,1)

        x = Ui_MainWindow
        global g_textEdit_allrepcmdlineoutput
        g_textEdit_allrepcmdlineoutput.append( sys.stdout.getvalue() )
        sys.stdout = x.oldstdout

        x.oldstdout = sys.stdout
        sys.stdout = StringIO()

        # Set the flag in the thread to signal thread termination
        global g_thread1_allrep_all
        g_thread1_allrep_all.join()

    #
    # buttonClickCancel_fw: Handle Cancel button for Fiwalk tab 
    #
    def buttonClickedCancel_fw(self):
        print(">> Fiwalk XML Generation Task Cancelled ")
        # Set the progressbar maximum to > minimum so the spinning will stop
        global global_fw
        global_fw.progressbar.setRange(0,1)

        # Set the active flag to False
        ProgressBar._active = False

        x = Ui_MainWindow
        global g_textEdit_fwcmdlineoutput
        g_textEdit_fwcmdlineoutput.append( sys.stdout.getvalue() )
        sys.stdout = x.oldstdout

        x.oldstdout = sys.stdout
        sys.stdout = StringIO()

        # Set the flag in the thread to signal thread termination
        global g_thread1_fw
        g_thread1_fw.join()


    #
    # buttonClickCancel_ann: Handle Cancel button for Annotate tab 
    #
    def buttonClickedCancel_ann(self):
        print(">> Annotated File Generation Task Cancelled ")
        # Set the progressbar maximum to > minimum so the spinning will stop
        global global_ann
        global_ann.progressbar.setRange(0,1)

        # Set the active flag to False
        ProgressBar._active = False

        x = Ui_MainWindow
        global g_textEdit_anncmdlineoutput
        g_textEdit_anncmdlineoutput.append( sys.stdout.getvalue() )
        sys.stdout = x.oldstdout

        x.oldstdout = sys.stdout
        sys.stdout = StringIO()

        # Set the flag in the thread to signal thread termination
        global g_thread1_ann
        g_thread1_ann.join()

    def buttonClickedCancel_rep(self):
        print(">> Reports Generation Task Cancelled ")
        # Set the progressbar maximum to > minimum so the spinning will stop
        global global_rep
        global_rep.progressbar.setRange(0,1)

        # Set the active flag to False
        ProgressBar._active = False

        x = Ui_MainWindow
        global g_textEdit_repcmdlineoutput
        g_textEdit_repcmdlineoutput.append( sys.stdout.getvalue() )
        sys.stdout = x.oldstdout

    #
    # buttonClickClose: Handle Close button for all tabs 
    #
    def buttonClickedClose(self):
        QtCore.QCoreApplication.instance().quit()

    def getImageFileName(self):
        # Navigation
        image_file = QtGui.QFileDialog.getOpenFileName(caption="Select an image file")
        print(">> Image file selected: ", image_file)

        self.lineEdit_image.setText(image_file)
        
        self.imageFileName = image_file

    def getFwImageFileName(self):
        # Navigation
        image_file = QtGui.QFileDialog.getOpenFileName(caption="Select an image file")
        print(">> Image file selected: ", image_file)

        self.lineEdit_fw_image.setText(image_file)
        
        self.fwImageFileName = image_file

    def getAllrepImageFileName(self):
        # Navigation
        image_file = QtGui.QFileDialog.getOpenFileName(caption="Select an image file")
        print(">> Image file selected: ", image_file)

        self.lineEdit_allrep_image.setText(image_file)
        
        self.allrepImageFileName = image_file

    def getBeImageFileName(self):
        # Navigation
        image_file = QtGui.QFileDialog.getOpenFileName(caption="Select an image file")
        print(">> Image file selected: ", image_file)

        self.lineEdit_be_image.setText(image_file)
        
        self.beImageFileName = image_file

    def getAnnImageFileName(self):
        # Navigation
        image_file = QtGui.QFileDialog.getOpenFileName(caption="Select an image file")
        print(">> Image file selected: ", image_file)

        self.lineEdit_ann_image.setText(image_file)
        
        self.annImageFileName = image_file

    def getbcpyDir(self):
        # Navigation
        bcpyDir = QtGui.QFileDialog.getExistingDirectory(caption="Create a directory for the annotation")
        print(">> BC Python Directory Selected: ", bcpyDir)

        self.lineEdit_bcpydir.setText(bcpyDir)
        
        self.bcpyDir = bcpyDir

    ##'''
    ## All reports
    def getOutputDir(self):
        # Since This directory should not exist, use getSaveFileName
        # to let the user create a new directory.
        outdir = QtGui.QFileDialog.getSaveFileName()

        ## print(">> Output Directory Selected by navigating: ", outdir)
        print(">> Output Directory Selected for All Reports ", outdir)

        self.lineEdit_outdir.setText(outdir)
        self.outputDirName = outdir

        if os.path.exists(self.outputDirName):
            raise RuntimeError(out_dir+" exists")

            self.textEdit.setText( sys.stdout.getvalue() )
            sys.stdout = self.oldstdout

            #exit(1)

        os.mkdir(self.outputDirName)
    ##'''

    def getBeOutputDir(self):
        # Since This directory should not exist, use getSaveFileName
        # to let the user create a new directory.
        outdir = QtGui.QFileDialog.getSaveFileName(caption="Select the bulk extractor feature directory")

        ## print(">> BE Output Directory Selected by navigating: ", outdir)
        print(">> BE Output Directory Selected for Bulk Extractor ", outdir)

        self.lineEdit_be_outDir.setText(outdir)
        self.beOutputDirName = outdir

        if os.path.exists(self.beOutputDirName):
            raise RuntimeError(outdir+" exists")

            self.textEdit_becmdlineoutput.setText( sys.stdout.getvalue() )
            sys.stdout = self.oldstdout

            ##exit(1)

        os.mkdir(self.beOutputDirName)

    def getBeFeatDir(self):
        beFeatDir = QtGui.QFileDialog.getExistingDirectory(caption="Select the bulk extractor feature directory")
        print(">> Annotate: bulk_extractor feature directory selected: ", beFeatDir)

        self.lineEdit_ann_beFeatDir.setText(beFeatDir)
        
        self.annBeFeatDir = beFeatDir

    def getAllrepBeFeatDir(self):
        beFeatDir = QtGui.QFileDialog.getExistingDirectory(caption="Select the bulk extractor feature directory")
        print(">> Annotate: bulk_extractor feature directory selected: ", beFeatDir)

        self.lineEdit_allrep_beFeatDir.setText(beFeatDir)
        
        self.allrepBeFeatDir = beFeatDir

    def getAnnOutputDir(self):
        # Since This directory should not exist, use getSaveFileName
        # to let the user create a new directory.
        ann_outdir = QtGui.QFileDialog.getSaveFileName(caption="Create a directory for the annotation")

        ## print(">> Annotated files Directory Selected by navigating: ", ann_outdir)
        print(">> Output Directory Selected for Annotated Output ", ann_outdir)
        self.lineEdit_ann_annDir.setText(ann_outdir)
        self.annOutputDirName = ann_outdir

        if os.path.exists(self.annOutputDirName):
            raise RuntimeError(ann_outdir+" exists")

            self.textEdit_ann.setText( sys.stdout.getvalue() )
            sys.stdout = self.oldstdout

            ##exit(1)

        os.mkdir(self.annOutputDirName)

    def getAnnBcpyDir(self):
        # Navigation
        bcpyDir = QtGui.QFileDialog.getExistingDirectory(caption="")
        print(">> BC Python Directory Selected: ", bcpyDir)

        self.lineEdit_ann_bcpyDir.setText(bcpyDir)
        
        self.annBcpyDir = bcpyDir

    def getFwOutputXmlFilePath(self):
        # Navigation
        xml_output_file = QtGui.QFileDialog.getSaveFileName(caption="Select a location and enter a filename")
        ## print("D: Fiwalk XML File Selected: ", xml_output_file)

        self.lineEdit_fw_xmlFile.setText(xml_output_file)
        
        self.xmlFileName = xml_output_file
        self.TextFileName = xml_output_file + '.txt'

    # get: Routine to let the user choose the XML file -
    # by navigating trough the directories
    def getRepFwXmlFileName(self):
        # Navigation
        xml_file = QtGui.QFileDialog.getOpenFileName(caption="Select a fiwalk XML file")
        # print("D: Fiwalk XML File Selected: ", xml_file)

        self.lineEdit_rep_fwxmlfile.setText(xml_file)

        self.repFwXmlFileName = xml_file
        return xml_file
    
    # getRepBeAnnotatedDir: Routine to let the user choose the Directory name
    # containing the annotated files by navigating
    def getRepBeAnnotatedDir(self):
        ann_dir = QtGui.QFileDialog.getExistingDirectory(caption="Select an annotated features directory")
        # print("D: Annotated Directory Selected by navigating: ", ann_dir)

        self.lineEdit_rep_annDir.setText(ann_dir)
        self.repAnnDir = ann_dir
        return ann_dir

    # getOutputDir: Routine to let the user choose the Directory name
    # to output the reports by navigating
    def getRepOutputDir(self):
        # Since This directory should not exist, use getSaveFileName
        # to let the user create a new directory.
        outdir = QtGui.QFileDialog.getSaveFileName(caption="Create a report directory")

        # print("D: Output Directory Selected by navigating: ", outdir)

        self.lineEdit_rep_outdir.setText(outdir)
        self.repOutDir = outdir
        return outdir

    # getAllrepOutputDir: Routine to let the user choose the Directory name
    # to output the reports by navigating
    def getAllrepOutDir(self):
        # Since This directory should not exist, use getSaveFileName
        # to let the user create a new directory.
        outdir = QtGui.QFileDialog.getSaveFileName(caption="Enter a folder name for a new output directory")
        #outdir_dialog = QtGui.QFileDialog(caption="Find or create an output directory")
        #outdir_dialog.setFileMode(QtGui.QFileDialog.Directory)
        #outdir_dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        #result = outdir_dialog.exec_()
        #if result:
        #    outdir = outdir_dialog.selectedFiles()[0]
            # print("D: Output Directory Selected by navigating: ", outdir)
        self.lineEdit_allrep_outdir.setText(outdir)
        self.allrepOutDir = outdir
        #else:
        #    print(">> Warning! No output directory selected! ")
        return outdir

    # getConfigFile: Select the config file from the directory structure.
    def getRepConfigFile(self):
        config_file = QtGui.QFileDialog.getOpenFileName()
        # print("D: Config File Selected by navigating: ", config_file)

        self.lineEdit_rep_confile.setText(config_file)
        self.repConfile = config_file
        return config_file
    
    # getAllrepConfigFile: Select the config file from the directory structure.
    def getAllrepConfigFile(self):
        config_file = QtGui.QFileDialog.getOpenFileName()
        self.lineEdit_allrep_confile.setText(config_file)
        self.allrepConfile = config_file
        return config_file
    
    def buttonClickedOkAllrep(self):
        self.oldstdout = sys.stdout
        sys.stdout = StringIO()

        # Check the parameters and run the reports
        if self.bc_allrep_check_parameters() == -1:
            print(">> Report Generation is Aborted ")
            self.textEdit_allrep.setText( sys.stdout.getvalue() )
            sys.stdout = self.oldstdout
            return
            ##exit (1)

        premis_img_info = {'version':0, 'acq_date':0, 'imagesize':0}

        # All set to go. Generate premis events for the disk image and BE
        premis_img_info = bc_utils.bcGetImageInfo(self.allrepImageFileName)

        ## Check directory creation (in case user typed it in)
        if not os.path.exists(self.allrepOutDir):
            os.mkdir(self.allrepOutDir)
        ## Now, assume that self.allrepOutDir exists (user used navigation
        ## button) - this is the only way it is created in check_parameters step.
        genAllrepOutDir = self.allrepOutDir+"/reports"
        if not os.path.exists(genAllrepOutDir):
            os.mkdir(genAllrepOutDir)

        ## NOTE: Since the directory "reports" is not yet created, the xml code
        # is temporarily put directly under the output directory. Since the
        # entire string is being written to reports/premis.xml in the end, 
        # it doesn't matter. But this needs to be fixed. 
        ## premis_outfile = self.allrepOutDir +"/reports/premis.xml"
        premis_outfile = genAllrepOutDir +"/premis.xml"

        ## print("D: >>> Generating diskImage part of the Premis File ", premis_outfile)
        a = BcPremisFile()
        a.bcGenPremisXmlDiskImage(self.allrepImageFileName, premis_img_info, premis_outfile)

        print(">> Generating XML File for the image ", self.allrepImageFileName)
        print('')

        # Create the XML file in the given directory, if doesn't exist. 
        if not os.path.exists(self.allrepOutDir):
            os.mkdir(self.allrepOutDir)
        self.allrepXmlFileName = self.allrepOutDir + "/fiwalk-output.xml"

        global g_allrepXmlFileName
        g_allrepXmlFileName = self.allrepXmlFileName

        if os.path.exists(self.allrepXmlFileName):
            os.remove(self.allrepXmlFileName)
        
        fwcmd = ['fiwalk', '-f', '-X', self.allrepXmlFileName, self.allrepImageFileName]
        # Now setup cmd for identify_filenames on the Feature files to 
        # generat the annotated reports.

        # Create the directory for annotated output under the output dir
        self.allrepAnnDir = self.allrepOutDir + '/' + 'annotated-features'
        os.mkdir(self.allrepAnnDir)

        identify_cmd = self.allrepBcpyDir + '/' + 'identify_filenames.py'
        anncmd = ['python3',identify_cmd,'--all','--image_filename',\
          self.allrepImageFileName, self.allrepBeFeatDir, self.allrepAnnDir]

    
        # Now set up cmd for generating reports
        genrep_outdir = self.allrepOutDir + '/reports'

        # Start two threads - one for executing the above command and
        # a second one to start a progress bar on the gui which keeps
        # spinning till the first thread finishes the command execution
        # and signals the second one by setting a flag. 
        thread1 = bcThread_allrep_all(fwcmd, anncmd, self.allrepAnnDir, \
                               PdfReport, FiwalkReport, \
                               self.allrepXmlFileName, self.allrepOutDir, \
                               genrep_outdir, self.allrepConfile, \
                               self.allrepBeFeatDir, \
                               self.allrepImageFileName )

        # Save the thread handle for later use in cancel task.
        global g_thread1_allrep_all
        g_thread1_allrep_all = thread1

        thread2 = guiThread("allrep")
        thread2.start()
        thread1.start()

        self.textEdit_allrep.setText( sys.stdout.getvalue() )
        sys.stdout = self.oldstdout

    # buttonClickedOkFw: Routine invoked when the "Run" (formerly OK) 
    # button on the Fiwalk tab is pressed.
    def buttonClickedOkFw(self):
        self.oldstdout = sys.stdout
        sys.stdout = StringIO()
        # If Image file is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_fw_image.text() != self.fwImageFileName:
            self.fwImageFileName = ui.lineEdit_fw_image.text()
            ## print("D: Image File Selected from the box: ", self.imageFileName)

        # If output XML file is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_fw_xmlFile.text() != self.fwXmlFileName:
            self.fwXmlFileName = ui.lineEdit_fw_xmlFile.text()
            self.fwTextFileName = self.fwXmlFileName + '.txt'

            # Thread uses it. so copy to the global value
            global g_fwXmlFileName
            g_fwXmlFileName = self.fwXmlFileName

        # PREMIS Event
        premis_img_info = {'version':0, 'acq_date':0, 'imagesize':0}

        # All set to go. Generate premis events for the disk image and BE
        premis_img_info = bc_utils.bcGetImageInfo(self.fwImageFileName)

        # If running from fiwalk tab, use the same directory as ouput
        # xml file directory to generate the premis event log.
        xmlpath = os.path.dirname(g_fwXmlFileName)
        premis_outfile = xmlpath+"/premis.xml"

        ## print("D: Generating diskImage part of the Premis File ", premis_outfile)
        a = BcPremisFile()
        a.bcGenPremisXmlDiskImage(self.fwImageFileName, premis_img_info, premis_outfile)

        cmd = ['fiwalk', '-f', '-X', self.fwXmlFileName, self.fwImageFileName]
        print("\n>> Generating XML File ", self.fwXmlFileName)
        print("\n>> Invoking command for Fiwalk = ", cmd)

        self.textEdit_fwcmdlineoutput.setText( sys.stdout.getvalue() )
        sys.stdout = self.oldstdout

        self.oldstdout = sys.stdout
        sys.stdout = StringIO()

        # Start two threads - one for executing the above command and
        # a second one to start a progress bar on the gui which keeps
        # spinning till the first thread finishes the command execution
        # and signals the second one by setting a flag. 
        thread1 = bcThread_fw(cmd)

        # Save the thread handle for later use in cancel task.
        global g_thread1_fw
        g_thread1_fw = thread1

        thread2 = guiThread("fiwalk")
        thread1.start()
        thread2.start()

        # Terminate the redirecting of the stdout to the in-memory buffer.
        #### Commented for now, as it is called from the thread : FIXME
        ####self.textEdit_fwcmdlineoutput.setText( sys.stdout.getvalue() )
        ####sys.stdout = self.oldstdout

    def buttonClickedOkBe(self):
        # The standard output from this point is placed by an in-memory
        # buffer.
        ## FIXME: Redirecting the stdout seems to make the code hang
        ## here. So commenting it out for now. Need to be fixed.
        ## self.oldstdout = sys.stdout
        ## sys.stdout = StringIO()

        # If Image file is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_be_image.text() != self.beImageFileName:
            self.beImageFileName = ui.lineEdit_be_image.text()
            # print("D: Image File Selected from the box: ", self.beimageFileName)

        # If output Dir is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_be_outDir.text() != self.beOutputDirName:
            self.beOutputDirName = ui.lineEdit_be_outDir.text()
            print("D: Output Dir fir Bulk Extractor Selected from the box: ", self.beOutputDirName)

        cmd = ['bulk_extractor', self.beImageFileName, '-o', self.beOutputDirName]
        print(">> Command executed for bulk_extractor = ", cmd)

        (data, err) = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()

        if len(err) > 0 :
           #sys.stderr.write("Debug: type(err) = %r.\n" % type(err))
           # Terminate the redirecting of the stdout to the in-memory buffer.
           print(">> Error! bulk_extractor terminated with error: \n", err)
           self.textEdit_becmdlineoutput.setText( sys.stdout.getvalue() )
           sys.stdout = self.oldstdout
           raise ValueError("bulk_extractor error (" + str(err).strip() + "): "+" ".join(cmd))
        else:
           print("\n>> Success. bulk_extractor created feature files in the directory: ", self.beOutputDirName)
           print("\n")
        
        # Terminate the redirecting of the stdout to the in-memory buffer.
        self.textEdit_becmdlineoutput.setText( sys.stdout.getvalue() )
        sys.stdout = self.oldstdout

    # buttonClickedOkAnn: Routine invoked when the "Run" (formerly OK) 
    # button on the Annotate tab is pressed.
    def buttonClickedOkAnn(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()

        # If Image file is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_ann_image.text() != self.annImageFileName:
            self.annImageFileName = ui.lineEdit_ann_image.text()
            # print("D: Image File Selected from the box: ", self.annimageFileName)

        # If beFeature Dir is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_ann_beFeatDir.text() != self.annBeFeatDir:
            self.annBeFeatDir = ui.lineEdit_ann_beFeatDir.text()
            # print("D: Output Dir fir Bulk Extractor Selected from the box: ", self.annBeFeatDir)

        # If annOutputDir Dir is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_ann_annDir.text() != self.annOutputDirName:
            self.annOutputDirName = ui.lineEdit_ann_annDir.text()
            # print("D: Ann Output Dir Selected from the box: ", self.annOutputDirName)

        # If annBcpyDir Dir is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_ann_bcpyDir.text() != self.annBcpyDir:
            self.annBcpyDir = ui.lineEdit_ann_bcpyDir.text()
            # print("D: Ann Bcpy Dir Selected from the box: ", self.annBcpyDir)

        # If bcpyDir doesn't exist, default it to
        # /usr/share/dfxml/python

        if not os.path.exists(self.annBcpyDir):
            # print("D: Setting default directory for BC python directory")
            self.annBcpyDir = "/usr/share/dfxml/python"

        identify_cmd = self.annBcpyDir + '/' + 'identify_filenames.py'
        #print("D: annBcpyDir: ", self.annBcpyDir)

        cmd = ['python3',identify_cmd,'--all','--image_filename',\
          self.annImageFileName, self.annBeFeatDir, self.annOutputDirName]
        print("\n>> Running identify_filanames script : ", cmd)

        self.textEdit_ann.setText( sys.stdout.getvalue() )
        sys.stdout = self.oldstdout

        self.oldstdout = sys.stdout
        sys.stdout = StringIO()

        # Start two threads - one for executing the above command and
        # a second one to start a progress bar on the gui which keeps
        # spinning till the first thread finishes the command execution
        # and signals the second one by setting a flag. 
        thread1 = bcThread_ann(cmd, self.annOutputDirName)
        global g_thread1_ann
        g_thread1_ann = thread1

        thread2 = guiThread("ann")
        thread1.start()
        thread2.start()

    # buttonClickedOkRep: Routine invoked when the "Run" (formerly OK) 
    # button on the Reports tab is pressed.
    def buttonClickedOkRep(self):
        import fiwalk
        self.oldstdout = sys.stdout
        sys.stdout = StringIO()
        use_config_file = True

        # The standard output from this point is placed by an in-memory
        # buffer.
        self.oldstdout = sys.stdout
        sys.stdout = StringIO()

        # Check if the indicated files exist. If not, return after
        # printing the error. Also terminate the redirecting of the
        # stdout to the in-memory buffer.
        if self.bc_rep_check_parameters() == -1:
            print(">> Report Generation is Aborted ")
            self.textEdit_rep.setText( sys.stdout.getvalue() )
            sys.stdout = self.oldstdout
            return
        
        ## It is assumed that self.repOutDir exists - since it is 
        ## created in check_parameters step.
        genRepOutDir = self.repOutDir+"/reports"
        if not os.path.exists(genRepOutDir):
            os.mkdir(genRepOutDir)

        premis_outfile = genRepOutDir + "/premis.xml"
        
        # Get the image fullpath from "command_line" part of dfxml file:
        a = BcPremisFile()
        dfxml_command_line = fiwalk.fiwalk_xml_command_line(self.repFwXmlFileName)
        imageName = a.extractImageName(dfxml_command_line, "fw")

        # Now we have the image location, generate premis events for
        # disk image
        premis_img_info = bc_utils.bcGetImageInfo(imageName)
        premis_outfile = genRepOutDir +"/premis.xml"

        print(">> REP: Generating PREMIS events for Diskimage")
        a.bcGenPremisXmlDiskImage(imageName, premis_img_info, premis_outfile)

        print(">> REP: Generating FW Premis : ", self.repFwXmlFileName)
        # Also generate Fiwalk premis events as we have the xml available:
        a.bcGenPremisXmlFiwalk(self.repFwXmlFileName, premis_outfile, False)

        # Start two threads - one for executing the above command and
        # a second one to start a progress bar on the gui which keeps
        # spinning till the first thread finishes the command execution
        # and signals the second one by setting a flag. 
        thread1 = bcThread_rep(PdfReport, FiwalkReport, \
                               self.repFwXmlFileName,self.repAnnDir, \
                               self.repOutDir, self.repConfile)
        thread2 = guiThread("rep")
        thread1.start()
        thread2.start()


    def bcRunCmd(self, cmd, err):
        (data, err) = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
        if len(err) > 0:
            ## print("\n>> [D] bcRunCmd: Failure!!! command executed: ", cmd)
            return (-1)
        else:
            ## print("\n>> [D] bcRunCmd: Success!!! command executed: ", cmd)
            return (0)

    # getConfigFile: Select the config file from the directory structure.
    def getConfigFile(self):
        config_file = QtGui.QFileDialog.getOpenFileName()
        ## print(">> [D] Config File Selected navigating: ", config_file)
        print(">> Config File Selected: ", config_file)

        self.lineEdit_confile.setText(config_file)
        self.configFileName = config_file
        return config_file

    def bc_rep_check_parameters(self):
        # If XML file not selected using menu, check if it is typed in the box:
        if ui.lineEdit_rep_fwxmlfile.text() != self.repFwXmlFileName:
            self.repFwXmlFileName = ui.lineEdit_rep_fwxmlfile.text()
            # print("D:Fiwalk XML FIle Selected from the box: ", self.repFwXmlFileName)
        if not os.path.exists(self.repFwXmlFileName):
            print("XML File %s does not exist. Aborting" %self.repFwXmlFileName)
            return (-1)

        # If Annotated file is not selected using menu, check if it is typed in the box:
        if ui.lineEdit_rep_annDir.text() != self.repAnnDir:
            self.repAnnDir = ui.lineEdit_rep_annDir.text()
            # print("D: Annotated Directory Selected from the box: ", self.repAnnDir)

        if not os.path.exists(self.repAnnDir):
            print("BE Annotated Directory %s does not exist. Aborting" %self.repAnnDir)
            return (-1)

        # If Outdir is not selected using menu, check if it is typed in the text box:
        if ui.lineEdit_rep_outdir.text() != self.repOutDir:
            self.repOutDir = ui.lineEdit_rep_outdir.text()
            # print("D: Output Directory selected from the box: ", self.repOutDir)
        # The directory is not supposed to exist. Return -1 if it does.
        if (os.path.exists(self.repOutDir)):
            print(">> Error: Output Directory %s exists. " %self.repOutDir)
            return (-1)
        else:
            os.mkdir(self.repOutDir)

        if ui.lineEdit_rep_confile.text() != self.repConfile:
            self.repConfile = ui.lineEdit_rep_confile.text()
            # print("D: Config File selected from the box: ", self.repConfile)

        # If config file is not provided by the user, user the default one
        if not os.path.exists(self.repConfile):
            print(">> Using default configuration file: /etc/bitcurator/bc_report_config.txt")
            self.configFileName = "/etc/bitcurator/bc_report_config.txt"

        return (0)
    

    # bc_allrep_check_parameters: Check if the selected files exist. Also
    # if the text entered in the boxes doesn't match what was selected
    # by navigating through directory structure, use the text in the
    # box as the final selection.
    def bc_allrep_check_parameters(self):
        # If Image file is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_allrep_image.text() != self.allrepImageFileName:
            self.allrepImageFileName = ui.lineEdit_allrep_image.text()
            ## print("D: Image File Selected from the box: ", self.allrepImageFileName)

        if not os.path.exists(self.allrepImageFileName):
            print("Image File %s does not exist. Aborting" %self.imageFileName)
            return (-1)

        # If beFeature Dir is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_allrep_beFeatDir.text() != self.allrepBeFeatDir:
            self.allrepBeFeatDir = ui.lineEdit_allrep_beFeatDir.text()

        if not os.path.exists(self.allrepBeFeatDir):
            print("BE Feature Directory %s does not exist. Aborting" %self.repAnnDir)
            return (-1)

        # If allrepOutputDir Dir is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_allrep_outdir.text() != self.allrepOutDir:
            self.allrepOutDir = ui.lineEdit_allrep_outdir.text()

        # If allrepConfile Dir is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_allrep_confile.text() != self.allrepConfile:
            self.allrepConfile = ui.lineEdit_allrep_confile.text()

        # The directory is not supposed to exist. Return -1 if it does.
        #
        # Removed this check 8/23/2014 - allow previously created dirs - KW
        #
        #if (os.path.exists(self.allrepOutDir)):
        #    print(">> Error: Output Directory %s exists. " %self.allrepOutDir)
        #    return (-1)
        #else:
        #    os.mkdir(self.allrepOutDir)

        # If config file is not provided by the user, user the default one
        # FIXME: Check for confile is already done earlier. So no need to 
        # do it here. Remove this code after confirming that.
        if not os.path.exists(self.allrepConfile):
            print(">> Using the default config file: /etc/bitcurator/bc_report_config.txt")
            self.configFileName = "/etc/bitcurator/bc_report_config.txt"
            self.allrepConfile = "/etc/bitcurator/bc_report_config.txt"

        # The directory that contains identify_filenames script is set to default: 
        self.allrepBcpyDir = "/usr/share/dfxml/python"
        return (0)

    def bc_allrep_check_parameters_old(self):
        
        # If Image file not selected through menu, see if it is typed in the box:

        if ui.lineEdit_image.text() != self.imageFileName:
            self.imageFileName = ui.lineEdit_image.text()
            # print("D:Image FIle Selected from the box: ", self.imageFileName)
        if not os.path.exists(self.imageFileName):
            print("Image File %s does not exist. Aborting" %self.imageFileName)
            return (-1)

        # If Bitcurator Python dir is not selected through menu, see if it is
        # typed in the text box:
        if ui.lineEdit_bcpydir.text() != self.bcpyDir:
            self.bcDir = ui.lineEdit_bcpydir.text()
            # print("D: BC Python Directory Selected from the box: ", self.bcpyDir)

        if not os.path.exists(self.bcpyDir):
            print("BC Python Directory %s does not exist. Aborting" %self.bcpyDir)
            return (-1)

        # If Outdir is not selected through menu, see if it is typed
        # in the text box:
        if ui.lineEdit_outdir.text() != self.outputDirName:
            self.outputDirName = ui.lineEdit_outdir.text()
            # print("D: Output Directory selected from the box: ", self.outputDirName)
        # Check for outdir is already done earlier. So no need to do it here.

        if ui.lineEdit_confile.text() != self.configFileName:
            self.configFileName = ui.lineEdit_configFile.text()
            # print("D: Config File selected from the box: ", self.configFileName)

        # If config file is not provided by the user, user the default one
        if not os.path.exists(self.configFileName):
            print(">> Using the default config file: /etc/bitcurator/bc_report_config.txt")
            self.configFileName = "/etc/bitcurator/bc_report_config.txt"

        return (0)

    # BE Viewer launching routine
    def on_pushButton_bev_clicked(self):
        
        cmdstr = '/usr/local/bin/BEViewer'
        print(">> Launching BEViewer >> ")
        
        # Note: We can't use Popen here as the call to Popen blocks, which
        # doesn't let us get back to the GUI when the viewer is launched.
        # startDetached apparently seems to fix that issue.

        QtCore.QProcess.startDetached(cmdstr)
        self.textEdit_allrep.append(sys.stdout.getvalue() )
        sys.stdout = self.oldstdout

        oldstdout = sys.stdout
        sys.stdout = StringIO()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Bitcurator Reports", None, QtGui.QApplication.UnicodeUTF8))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fw), QtGui.QApplication.translate("MainWindow", "Fiwalk XML", None, QtGui.QApplication.UnicodeUTF8))

        self.pushButton_bev.clicked.connect(self.on_pushButton_bev_clicked)
 

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ann), QtGui.QApplication.translate("MainWindow", "Annotated Features", None, QtGui.QApplication.UnicodeUTF8))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_rep), QtGui.QApplication.translate("MainWindow", "Reports", None, QtGui.QApplication.UnicodeUTF8))

        # Tab: Reports
        self.lineEdit_rep_fwxmlfile.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_rep_fwxmlfile.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rep_fwxmlfile.setText(QtGui.QApplication.translate("MainWindow", "Fiwalk XML File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rep_outdir.setText(QtGui.QApplication.translate("MainWindow", "Output Directory For Reports (new)", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_rep_outdir.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_rep_outdir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rep_confile.setText(QtGui.QApplication.translate("MainWindow", "Config File (optional)", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_rep_confile.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/file", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_rep_confile.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rep_cmdlineoutput.setText(QtGui.QApplication.translate("MainWindow", "Command Line Output", None, QtGui.QApplication.UnicodeUTF8))

        # Reports Tab: bush buttons
        self.pb_rep_run.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_rep_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_rep_close.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))

        self.label_rep_annDir.setText(QtGui.QApplication.translate("MainWindow", "Annotated Feature Files Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_rep_annDir.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_rep_annDir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rephdr.setText(QtGui.QApplication.translate("MainWindow", "Produces Office Open XML and PDF reports to assist in disk image analysis.", None, QtGui.QApplication.UnicodeUTF8))

        # Run All (allrep) tab
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_allrep), QtGui.QApplication.translate("MainWindow", "Run All", None, QtGui.QApplication.UnicodeUTF8))
        self.label_allrep_image.setText(QtGui.QApplication.translate("MainWindow", "Image File", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_allrep_confile.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_allrep_image.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_allrep_run.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_allrep_outdir.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_allrep_confile.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_allrep_image.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_allrep_outdir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_allrep_confile.setText(QtGui.QApplication.translate("MainWindow", "Config File (Optional)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_allrep_outdir.setText(QtGui.QApplication.translate("MainWindow", "Output Directory (fiwalk output, annotated features, and reports will appear in here)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_allrephdr.setText(QtGui.QApplication.translate("MainWindow", "Run fiwalk, annotate the bulk_extractor output, and generate Office / PDF reports.", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_allrep_close.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label_allrep_cmdlineoutput.setText(QtGui.QApplication.translate("MainWindow", "Command Line Output", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_allrep_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_bev.setText(QtGui.QApplication.translate("MainWindow", "Launch BEViewer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_allrephdr_bev.setText(QtGui.QApplication.translate("MainWindow", "If you haven\'t run bulk_extractor yet, use the button to the right to launch and run it first.", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_allrep_beFeatDir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_allrep_beFeatDir.setText(QtGui.QApplication.translate("MainWindow", "Bulk Extractor Feature Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_allrep_beFeatDir.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_allrep), QtGui.QApplication.translate("MainWindow", "Run All", None, QtGui.QApplication.UnicodeUTF8))
        
        
        # Tab-2: Fiwalk XML
        self.lineEdit_fw_image.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fw_image.setText(QtGui.QApplication.translate("MainWindow", "Image File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fw_xmlFile.setText(QtGui.QApplication.translate("MainWindow", "Output XML File", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_fw_xmlFile.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_fw_image.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))

        ## Fiwalk - push buttons
        self.pb_fw_close.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_fw_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_fw_run.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))

        self.toolButton_fw_xmlFile.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fw), QtGui.QApplication.translate("MainWindow", "Fiwalk XML", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fwhdr.setText(QtGui.QApplication.translate("MainWindow", "Fiwalk produces a DFXML file showing the volumes, directories, and files contained within a disk image.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fwcmdlineoutput.setText(QtGui.QApplication.translate("MainWindow", "Command Line Output", None, QtGui.QApplication.UnicodeUTF8))

        # Tab-4: Annotated Files
        self.label_ann_image.setText(QtGui.QApplication.translate("MainWindow", "Image File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ann_beFeatDir.setText(QtGui.QApplication.translate("MainWindow", "Bulk Extractor Feature Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ann_annDir.setText(QtGui.QApplication.translate("MainWindow", "Annotated Feature Files Directory (new)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ann_bcpyDir.setText(QtGui.QApplication.translate("MainWindow", "Bulk Extractor Python Directory (optional)", None, QtGui.QApplication.UnicodeUTF8))

        ## Annotated Files: Push buttons
        self.pb_ann_close.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_ann_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_ann_run.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))

        self.lineEdit_ann_image.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/File", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_ann_beFeatDir.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_ann_annDir.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/Path/To/Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_ann_bcpyDir.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "/usr/share/dfxml/python", None, QtGui.QApplication.UnicodeUTF8))

        self.toolButton_ann_image.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_ann_beFeatDir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_ann_annDir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_ann_bcpyDir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))

        self.label_anncmdlineoutput.setText(QtGui.QApplication.translate("MainWindow", "Command Line Output", None, QtGui.QApplication.UnicodeUTF8))
        self.label_annhdr.setText(QtGui.QApplication.translate("MainWindow", "Produces reports that link each bulk_extractor feature to a specific file in a disk image.", None, QtGui.QApplication.UnicodeUTF8))


        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))

        ''' FIXME: Do we need this??
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_2.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        '''

        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Help.setText(QtGui.QApplication.translate("MainWindow", "Show Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))


def bc_tempFixXMLAttributes(premis_outfile): 
    #of_premis.close()
    with open('premis_outfile', 'w') as testfile:
        testfile.writelines(['<?xml version="1.0" encoding="UTF-8"?>'] + testfile.readlines())
    testfile.close()


# Thread for running the allrep (run all) command
class bcThread_allrep_all(threading.Thread):
    def __init__(self, fwcmd, anncmd, allrepAnnDir, PdfReport, FiwalkReport,\
                 allrepXmlFileName, allrepOutDir, genrep_outdir, \
                 allrepConfile, allrepBeFeatDir, allrepImageFileName ):
        threading.Thread.__init__(self)
        self.fwcmd = fwcmd
        self.anncmd = anncmd
        self.annoutdir = allrepAnnDir
        self.PdfReport = PdfReport
        self.FiwalkReport = FiwalkReport
        self.allrepXmlFileName = allrepXmlFileName
        self.allrepAnnDir = allrepAnnDir
        self.allrepOutDir = allrepOutDir
        self.genrepOutDir = genrep_outdir
        self.allrepConfile = allrepConfile
        self.allrepBeFeatDir = allrepBeFeatDir
        self.allrepImageFileName = allrepImageFileName
        super(bcThread_allrep_all, self).__init__()
        self.stoprequest = threading.Event()
        self.process = None

    def join(self, timeout=None):
        self.stoprequest.set()
        super(bcThread_allrep_all, self).join(timeout)

    def stopped(self):
        return self.stoprequest.isSet()

    def run(self):
      # While loop for handling "cancel" signal outside Popen calls
      while not self.stoprequest.isSet():
        # Run fiwalk first
        print(">> Running fiwalk with the following flags: ", self.fwcmd)
        print('')
        print("Please be patient; fiwalk may take some time to run.")
        print('')

        p = self.process = Popen(self.fwcmd, stdout=PIPE, stderr=PIPE)
        (data, err) = p.communicate()
        if p.returncode:
            ProgressBar._active = False
           
            x = Ui_MainWindow
            print(">> ERROR!!! Run All terminated with error: \n", err)
            global g_textEdit_allrepcmdlineoutput
            g_textEdit_allrepcmdlineoutput.append( sys.stdout.getvalue() )
            sys.stdout = x.oldstdout

            # Set the progressbar maximum to > minimum so the spinning will stop
            global global_allrep
            global_allrep.progressbar.setRange(0,1)

            # Buffer the stdout to stringio again.
            x.oldstdout = sys.stdout
            sys.stdout = StringIO()
        else:
       
            # If cancel button was pressed after Popen finished, check here.
            # FIXME: Additional testing needed
            if self.stoprequest.isSet():
                ## print("D: Breaking out of the loop - 3")
                break
            print("\n>> Success. fiwalk created the following file: ")

            global g_allrepXmlFileName
            print(" o ", g_allrepXmlFileName) 

            # Generate the premis file in the reports directory: self.allrepOutDir
            print(">> Generating PREMIS event for fiwalk in:", self.genrepOutDir)
            
            if not os.path.exists(self.genrepOutDir):
                os.mkdir(self.genrepOutDir)
            premis_outfile = self.genrepOutDir +"/premis.xml"

            a = BcPremisFile()
            a.bcGenPremisXmlFiwalk(self.allrepXmlFileName, premis_outfile, True)

            a = BcPremisFile()
            beReportsXmlFile = self.allrepBeFeatDir+'/report.xml'
            ## print("D: BE reports XML FIle: ", beReportsXmlFile)
            a.bcGenPremisXmlBulkExtractor(beReportsXmlFile, premis_outfile, False)

            print("\n>> Creating annotated features ")

            # Dump the text in stdout to textEdit screen.
            # Note: setText for some reason, wouldn't work when used with
            # global value. append seems to work
            x = Ui_MainWindow
            g_textEdit_allrepcmdlineoutput.append( sys.stdout.getvalue() )
            sys.stdout = x.oldstdout

            # Buffer the stdout to stringio again.
            oldstdout = sys.stdout
            sys.stdout = StringIO()

            # Now run the identify_filenames cmd.
            p = self.process = Popen(self.anncmd, stdout=PIPE, stderr=PIPE)
            (data, err) = p.communicate()

            if p.returncode:
                print(">> ERROR!!! identify_filenames terminated with error: \n", err)
                ProgressBar._active = False
                x = Ui_MainWindow
                g_textEdit_allrepcmdlineoutput.append( sys.stdout.getvalue() )
                sys.stdout = x.oldstdout

                # In case the progress bar is spinning, stop it
                global_allrep.progressbar.setRange(0,1)
            else:
               
                # If cancel button was pressed after Popen finished, check here.
                # FIXME: Test this part more.
                if self.stoprequest.isSet():
                    ## print("D: Breaking out of the loop - 2")
                    break
                print(">> Success. Annotated feature files created in the directory: \n o ", self.annoutdir)

                # Now run the reports generation routine
                # Generate the reports now.
                print("\n>> Generating BitCurator Reports: \n")

                g_textEdit_allrepcmdlineoutput.append( sys.stdout.getvalue() )
                sys.stdout = x.oldstdout
                x.oldstdout = sys.stdout
                sys.stdout = StringIO()

                ## print("D: bcThread_allrep_rep: XmlFile: ", self.allrepXmlFileName)
                ## print("D: bcThread_allrep_rep: AnnDir: ", self.allrepAnnDir)
                ## print("D: bcThreadprevails_allrep_rep: Outdir: ", self.allrepOutDir)
                ## print("D: bcThread_allrep_rep: Confile: ", self.allrepConfile)

                bc_get_reports(self.PdfReport, self.FiwalkReport, \
                                 self.allrepXmlFileName, \
                                 self.allrepAnnDir, \
                                 self.genrepOutDir, \
                                 self.allrepConfile,
                                 self.allrepBeFeatDir)
                # Set the progresbar active flag so the other thread can
                # get out of the while loop.
                ProgressBar._active = False

                # If cancel button was pressed after Popen finished, check here.
                # FIXME: Additional testing needed
                if self.stoprequest.isSet():
                    ## print("D: Breaking out of the loop - 3")
                    break
                #print("\n>> Success!!! BitCurator Reports generated in the directory: \n o ", self.allrepOutDir)
                print("\n>> Success. BitCurator reports generated in the directory: \n o ", self.genrepOutDir)

                # Set the progressbar maximum to > minimum so the spinning will stop
                global_allrep.progressbar.setRange(0,1)
                
                x = Ui_MainWindow

                # Terminate the redirecting of the stdout to the in-memory buffer.
                g_textEdit_allrepcmdlineoutput.append( sys.stdout.getvalue() )
                sys.stdout = x.oldstdout
                x.oldstdout = sys.stdout
                sys.stdout = StringIO()
                break

    def stop(self):
        if self.process is not None:
            print(">> Terminating the thread for \"Run All\"")
            self.process.terminate()
        else:
            Popen.terminate(self.process)


                
# Thread for running the fiwalk command
class bcThread_fw(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
        super(bcThread_fw, self).__init__()
        self.stoprequest = threading.Event()
        self.process = None

    def stopped(self):
        return self.stoprequest.isSet()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(bcThread_fw, self).join(timeout)

    def run(self):
        p = self.process = Popen(self.cmd, stdout=PIPE, stderr=PIPE)
        (data, err) = p.communicate()
        if p.returncode:
           ProgressBar._active = False
           
           x = Ui_MainWindow

           # We don't want to display this as an error as pressing the cancel
           # button could bring us here as well.
           ## print(">> D: ERROR!!! Fiwalk terminated with error: \n", err)
           print(">> Fiwalk terminated \n")

           # print("D: >> Generating Premis event ")
           # If running from fowalk tab, use the same directory as ouput
           # xml file directory to generate the premis event log.
           global g_fwXmlFileName
           xmlpath = os.path.dirname(g_fwXmlFileName)
           premis_outfile = xmlpath+"/premis.xml"

           a = BcPremisFile()
           a.bcGenPremisXmlFiwalk(g_fwXmlFileName, premis_outfile, True, True)
        
           global g_textEdit_fwcmdlineoutput
           g_textEdit_fwcmdlineoutput.append( sys.stdout.getvalue() )
           sys.stdout = x.oldstdout

           # Set the progressbar maximum to > minimum so the spinning will stop
           global global_fw
           global_fw.progressbar.setRange(0,1)

           x.oldstdout = sys.stdout
           sys.stdout = StringIO()
        else:

            # Set the progresbar active flag so the other thread can
            # get out of the while loop.
            ProgressBar._active = False
            #print("D: bcThread_fw: Progressbar Active Flag Set to: ", ProgressBar._active)

            print("\n>> Success!!! Fiwalk created the following file(s): \n")

            # Set the progressbar maximum to > minimum so the spinning will stop
            global_fw.progressbar.setRange(0,1)

            print(" o ", g_fwXmlFileName) 

            ## print("D: Generating Premis event >>> ")

            # If running from fowalk tab, use the same directory as ouput
            # xml file directory to generate the premis event log.
            xmlpath = os.path.dirname(g_fwXmlFileName)
            premis_outfile = xmlpath+"/premis.xml"
            ## print("D: Premis Outfile: ", premis_outfile)
            a = BcPremisFile()
            a.bcGenPremisXmlFiwalk(g_fwXmlFileName, premis_outfile, True, True)

            x = Ui_MainWindow
            # Note: setText for some reason, wouldn't work when used with
            # global value. append seems to work
            # g_textEdit_fwcmdlineoutput.setText( sys.stdout.getvalue() )
            g_textEdit_fwcmdlineoutput.append( sys.stdout.getvalue() )
            sys.stdout = x.oldstdout
            x.oldstdout = sys.stdout
            sys.stdout = StringIO()
                

# Thread for running the identify_filenames command
class bcThread_ann(threading.Thread):
    def __init__(self, cmd, outdir):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.outdir = outdir
        super(bcThread_ann, self).__init__()
        self.stoprequest = threading.Event()
        self.process = None

    def stopped(self):
        return self.stoprequest.isSet()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(bcThread_ann, self).join(timeout)

    def run(self):
        p = self.process = Popen(self.cmd, stdout=PIPE, stderr=PIPE)
        (data, err) = p.communicate()
        if p.returncode:
            print(">> ERROR!!! identify_filenames terminated with error: \n", err)
            ProgressBar._active = False
            x = Ui_MainWindow
            g_textEdit_anncmdlineoutput.append( sys.stdout.getvalue() )
            sys.stdout = x.oldstdout

            # In case the progress bar is spinning, stop it
            global_ann.progressbar.setRange(0,1)
        else:
            # Set the progresbar active flag so the other thread can
            # get out of the while loop.
            ProgressBar._active = False

            print("\n>> Success!!! Annotated feature files created in the directory: ", self.outdir)

            # Set the progressbar maximum to > minimum so the spinning will stop
            global_ann.progressbar.setRange(0,1)
           
            x = Ui_MainWindow

            g_textEdit_anncmdlineoutput.append( sys.stdout.getvalue() )
            sys.stdout = x.oldstdout

    def stop(self):
        if self.process is not None:
            print(">> Terminating the Thread for \"Annotate Files\"")
            self.process.terminate()
        else:
            Popen.terminate(self.process)

class bcThread_rep(threading.Thread):
    def __init__(self, PdfReport, FiwalkReport, \
                       repFwXmlFileName,repAnnDir, \
                       repOutDir, repConfile):
        threading.Thread.__init__(self)
        self.PdfReport = PdfReport
        self.FiwalkReport = FiwalkReport
        self.repFwXmlFileName = repFwXmlFileName
        self.repAnnDir = repAnnDir
        self.repOutDir = repOutDir
        self.repConfile = repConfile
        super(bcThread_rep, self).__init__()
        self.stoprequest = threading.Event()
        self.process = None

    def stopped(self):
        return self.stoprequest.isSet()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(bcThread_rep, self).join(timeout)

    def run(self):
        # Generate the reports now.
        bc_get_reports(PdfReport, FiwalkReport, self.repFwXmlFileName, \
                                 self.repAnnDir, \
                                 self.repOutDir, \
                                 self.repConfile, None)

        # Set the progresbar active flag so the other thread can
        # get out of the while loop.
        ProgressBar._active = False

        print("\n>> Success! Reports generated in the directory: ", self.repOutDir)

        # Set the progressbar maximum to > minimum so the spinning will stop
        global global_rep
        global_rep.progressbar.setRange(0,1)

        x = Ui_MainWindow
        global g_textEdit_repcmdlineoutput

        # Terminate the redirecting of the stdout to the in-memory buffer.
        g_textEdit_repcmdlineoutput.append( sys.stdout.getvalue() )
        sys.stdout = x.oldstdout

    def stop(self):
        if self.process is not None:
            print(">> Terminating the thread for \"Reports\"")
            self.process.terminate()
        else:
            Popen.terminate(self.process)

# This is the thread which spins in a loop till the other thread which
# does the work sets the flag once the task is completed.
class guiThread(threading.Thread):
    def __init__(self, cmd_type):
        threading.Thread.__init__(self)
        self.cmd_type = cmd_type

    def run(self):
        if self.cmd_type == "fiwalk":
            global global_fw
            progressbar = global_fw
        elif self.cmd_type == "ann":
            global global_ann
            progressbar = global_ann
        elif self.cmd_type == "rep":
            global global_rep
            progressbar = global_rep
        elif self.cmd_type == "allrep":
            global global_allrep
            progressbar = global_allrep
        #elif self.cmd_type == "acc":
        #    global global_acc
        #    progressbar = global_acc

        progressbar.startLoop_bc(self.cmd_type)

class ProgressBar(QtGui.QWidget):
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

    def startLoop_bc(self, cmd_type):
        self._active = True
        ProgressBar._active = True 
        cntr = 0

        if cmd_type == "fiwalk":
            global global_fw
            global_fw.progressbar.setRange(0,0)
        elif cmd_type == "ann":
            global global_ann
            global_ann.progressbar.setRange(0,0)
        elif cmd_type == "rep":
            global global_rep
            global_rep.progressbar.setRange(0,0)
        elif cmd_type == "allrep":
            global global_allrep
            global_allrep.progressbar.setRange(0,0)
        #elif cmd_type == "acc":
        #    global global_acc
        #    global_acc.progressbar.setRange(0,0)

        while True:
            time.sleep(1.05)
            cntr = cntr + 1
            '''
            # Note: If we need to periodically display something when the process
            # bar is spinning, the following can be uncommented, but we need
            # a routing to empty the textEdit buffer for each textEdit window.
            ## if cntr%5 == 0:
                # print("D: CNTR: ", cntr)
                # FIXME: Refine this 
                ## print(">> Task Still running >>")
            '''
            QtGui.qApp.processEvents()
            #print("D: ProgressBar._active = ", ProgressBar._active)
            if not ProgressBar._active:
                #print ("D: startLoop_bc thread detected flag = ", ProgressBar._active)
                if cmd_type == "allrep":
                    global g_thread1_allrep_all
                    if g_thread1_allrep_all.stopped():
                        ## print("D: startLoop_bc: Run All Thread Stopped ")
                        g_thread1_allrep_all.stop()
                if cmd_type == "fiwalk":
                    global g_thread1_fw
                    if g_thread1_fw.stopped():
                        ## print("D: startLoop_bc: Fiwalk Thread Stopped ")
                        g_thread1_fw.stop()
                if cmd_type == "ann":
                    global g_thread1_ann
                    if g_thread1_ann.stopped():
                        ## print("D: startLoop_bc: Ann Thread Stopped ")
                        g_thread1_ann.stop()
                break
        ProgressBar._active = False

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
