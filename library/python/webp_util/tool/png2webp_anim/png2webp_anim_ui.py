# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\webp_anim\library\python\webp_util\tool\png2webp_anim\png2webp_anim.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\webp_anim\library\python\webp_util\tool\png2webp_anim\png2webp_anim.ui' applies.
#
# Created: Thu Feb 24 19:22:22 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(624, 638)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dstLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.dstLineEdit.setObjectName("dstLineEdit")
        self.horizontalLayout.addWidget(self.dstLineEdit)
        self.dstToolButton = QtWidgets.QToolButton(self.groupBox)
        self.dstToolButton.setObjectName("dstToolButton")
        self.horizontalLayout.addWidget(self.dstToolButton)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.loopCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.loopCheckBox.setText("")
        self.loopCheckBox.setObjectName("loopCheckBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.loopCheckBox)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.losslessheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.losslessheckBox.setText("")
        self.losslessheckBox.setObjectName("losslessheckBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.losslessheckBox)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.qualitySpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.qualitySpinBox.setMinimum(1)
        self.qualitySpinBox.setMaximum(100)
        self.qualitySpinBox.setProperty("value", 80)
        self.qualitySpinBox.setObjectName("qualitySpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.qualitySpinBox)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.tableView = QtWidgets.QTableView(self.splitter)
        self.tableView.setWordWrap(False)
        self.tableView.setObjectName("tableView")
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logTextEdit = LogTextEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy)
        self.logTextEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setObjectName("logTextEdit")
        self.verticalLayout.addWidget(self.logTextEdit)
        self.verticalLayout_2.addWidget(self.splitter)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.webpButton = QtWidgets.QPushButton(self.centralwidget)
        self.webpButton.setMinimumSize(QtCore.QSize(100, 40))
        self.webpButton.setObjectName("webpButton")
        self.horizontalLayout_3.addWidget(self.webpButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(100, 40))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_3.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 624, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionUp = QtWidgets.QAction(MainWindow)
        self.actionUp.setObjectName("actionUp")
        self.actionDown = QtWidgets.QAction(MainWindow)
        self.actionDown.setObjectName("actionDown")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUp)
        self.menuEdit.addAction(self.actionDown)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "設定", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "出力ファイル", None, -1))
        self.dstToolButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "ループさせる", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "ロスレス圧縮を使う", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "クオリティ", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "ログ", None, -1))
        self.webpButton.setText(QtWidgets.QApplication.translate("MainWindow", "WebP", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindow", "Edit", None, -1))
        self.actionOpen.setText(QtWidgets.QApplication.translate("MainWindow", "Open", None, -1))
        self.actionOpen.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+O", None, -1))
        self.actionSave.setText(QtWidgets.QApplication.translate("MainWindow", "Save", None, -1))
        self.actionSave.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+S", None, -1))
        self.actionExit.setText(QtWidgets.QApplication.translate("MainWindow", "Exit", None, -1))
        self.actionExit.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Q", None, -1))
        self.actionCopy.setText(QtWidgets.QApplication.translate("MainWindow", "Copy", None, -1))
        self.actionCopy.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+C", None, -1))
        self.actionPaste.setText(QtWidgets.QApplication.translate("MainWindow", "Paste", None, -1))
        self.actionPaste.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+V", None, -1))
        self.actionUp.setText(QtWidgets.QApplication.translate("MainWindow", "Up", None, -1))
        self.actionUp.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+Up", None, -1))
        self.actionDown.setText(QtWidgets.QApplication.translate("MainWindow", "Down", None, -1))
        self.actionDown.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+Down", None, -1))
        self.actionDelete.setText(QtWidgets.QApplication.translate("MainWindow", "Delete", None, -1))
        self.actionDelete.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Del", None, -1))

from webp_util.gui.log import LogTextEdit
