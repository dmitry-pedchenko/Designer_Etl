# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.Editor_Tab = QtWidgets.QWidget()
        self.Editor_Tab.setObjectName("Editor_Tab")
        self.gridLayout = QtWidgets.QGridLayout(self.Editor_Tab)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.tabWidget.addTab(self.Editor_Tab, "")
        self.Loader_Tab = QtWidgets.QWidget()
        self.Loader_Tab.setObjectName("Loader_Tab")
        self.tabWidget.addTab(self.Loader_Tab, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setDefaultUp(True)
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuHello = QtWidgets.QMenu(self.menubar)
        self.menuHello.setObjectName("menuHello")
        self.menuSystem = QtWidgets.QMenu(self.menubar)
        self.menuSystem.setObjectName("menuSystem")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setIconVisibleInMenu(False)
        self.actionSave.setObjectName("actionSave")
        self.actionConfiguration_Wizard = QtWidgets.QAction(MainWindow)
        self.actionConfiguration_Wizard.setObjectName("actionConfiguration_Wizard")
        self.actionEditor = QtWidgets.QAction(MainWindow)
        self.actionEditor.setObjectName("actionEditor")
        self.actionLoader = QtWidgets.QAction(MainWindow)
        self.actionLoader.setObjectName("actionLoader")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setIconVisibleInMenu(False)
        self.actionExit.setObjectName("actionExit")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuHello.addAction(self.actionPreferences)
        self.menuHello.addAction(self.actionOpen)
        self.menuHello.addAction(self.actionSave)
        self.menuHello.addAction(self.actionExit)
        self.menuSystem.addAction(self.actionConfiguration_Wizard)
        self.menuSystem.addAction(self.actionEditor)
        self.menuSystem.addAction(self.actionLoader)
        self.menubar.addAction(self.menuHello.menuAction())
        self.menubar.addAction(self.menuSystem.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Easy Loader"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Check Mode"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Editor_Tab), _translate("MainWindow", "Config Editor"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Loader_Tab), _translate("MainWindow", "Loader"))
        self.menuHello.setTitle(_translate("MainWindow", "File"))
        self.menuSystem.setTitle(_translate("MainWindow", "System"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionConfiguration_Wizard.setText(_translate("MainWindow", "Configuration Wizard"))
        self.actionEditor.setText(_translate("MainWindow", "Editor"))
        self.actionLoader.setText(_translate("MainWindow", "Loader"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
