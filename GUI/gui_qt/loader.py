# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loader.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(999, 534)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(152, 12, 281, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 30, 268, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 60, 268, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.toolBox = QtWidgets.QToolBox(Form)
        self.toolBox.setGeometry(QtCore.QRect(90, 177, 811, 321))
        self.toolBox.setObjectName("toolBox")
        self.Debug = QtWidgets.QWidget()
        self.Debug.setGeometry(QtCore.QRect(0, 0, 811, 245))
        self.Debug.setObjectName("Debug")
        self.toolBox.addItem(self.Debug, "")
        self.Log = QtWidgets.QWidget()
        self.Log.setGeometry(QtCore.QRect(0, 0, 811, 245))
        self.Log.setObjectName("Log")
        self.toolBox.addItem(self.Log, "")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(440, 10, 291, 141))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_start = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout_2.addWidget(self.pushButton_start)
        self.pushButton_logs = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_logs.setObjectName("pushButton_logs")
        self.verticalLayout_2.addWidget(self.pushButton_logs)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Mode"))
        self.radioButton.setText(_translate("Form", "Test mode"))
        self.radioButton_2.setText(_translate("Form", "Load mode"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Debug), _translate("Form", "Debug"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Log), _translate("Form", "Log"))
        self.pushButton_start.setText(_translate("Form", "Start"))
        self.pushButton_logs.setText(_translate("Form", "Logs folder"))
        self.label.setText(_translate("Form", "Config name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
