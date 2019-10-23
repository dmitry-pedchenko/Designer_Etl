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
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
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
        self.actionEditor.setCheckable(True)
        self.actionEditor.setObjectName("actionEditor")
        self.actionLoader = QtWidgets.QAction(MainWindow)
        self.actionLoader.setCheckable(True)
        self.actionLoader.setObjectName("actionLoader")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setIconVisibleInMenu(False)
        self.actionExit.setObjectName("actionExit")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionDictionary = QtWidgets.QAction(MainWindow)
        self.actionDictionary.setCheckable(True)
        self.actionDictionary.setObjectName("actionDictionary")
        self.actionConfig_Editor = QtWidgets.QAction(MainWindow)
        self.actionConfig_Editor.setCheckable(True)
        self.actionConfig_Editor.setObjectName("actionConfig_Editor")
        self.actionClose_Project = QtWidgets.QAction(MainWindow)
        self.actionClose_Project.setObjectName("actionClose_Project")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.menuHello.addAction(self.actionPreferences)
        self.menuHello.addAction(self.actionOpen)
        self.menuHello.addAction(self.actionClose_Project)
        self.menuHello.addAction(self.actionSave)
        self.menuHello.addAction(self.actionSave_as)
        self.menuHello.addAction(self.actionExit)
        self.menuSystem.addAction(self.actionConfiguration_Wizard)
        self.menuView.addAction(self.actionLoader)
        self.menuView.addAction(self.actionEditor)
        self.menuView.addAction(self.actionDictionary)
        self.menuView.addAction(self.actionConfig_Editor)
        self.menubar.addAction(self.menuHello.menuAction())
        self.menubar.addAction(self.menuSystem.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Easy Loader"))
        self.menuHello.setTitle(_translate("MainWindow", "File"))
        self.menuSystem.setTitle(_translate("MainWindow", "System"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionConfiguration_Wizard.setText(_translate("MainWindow", "Configuration Wizard"))
        self.actionEditor.setText(_translate("MainWindow", "Routing Map"))
        self.actionLoader.setText(_translate("MainWindow", "Loader"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionDictionary.setText(_translate("MainWindow", "Dictionary"))
        self.actionConfig_Editor.setText(_translate("MainWindow", "Config Editor"))
        self.actionClose_Project.setText(_translate("MainWindow", "Close Project"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
