from PyQt5 import QtCore, QtWidgets
import sys
import form_wizard_page_1
import form_wizard_page_2
import form_wizard_page_3
import form_wizard_page_4
import form_wizard_page_5
import form_wizard_page_6
import form_wizard_page_7
import form_wizard_page_8
import Source_tree
import Receiver_tree


class WizardConfig(QtWidgets.QWizard):
    def __init__(self,):
        super().__init__()

        self.setPage(RoadMapConfiguration.AddDBParameters, Page1(self))
        self.setPage(RoadMapConfiguration.CheckMode, Page2(self))
        self.setPage(RoadMapConfiguration.AddCheckFileParameters, Page3(self))
        self.setPage(RoadMapConfiguration.WithDictMode, Page4(self))
        self.setPage(RoadMapConfiguration.SourceColumns, Page5(self))
        self.setPage(RoadMapConfiguration.TargetColumns, Page6(self))
        self.setPage(RoadMapConfiguration.DictColumnsParameters, Page7(self))
        self.setPage(RoadMapConfiguration.DictTables, Page8(self))

        self.resize(900, 500)




class Page1(QtWidgets.QWizardPage, form_wizard_page_1.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    # def validatePage(self) -> bool:
    #     return False


    # def nextId(self) -> int:
    #     if self.checkMode.currentText() == 'true':
    #         return RoadMapConfiguration.AddCheckFileParameters
    #     else:
    #         return RoadMapConfiguration.AddDBParameters



class Page2(QtWidgets.QWizardPage, form_wizard_page_2.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.adjustSize()


class Page3(QtWidgets.QWizardPage, form_wizard_page_3.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.treeWidget_of_Source = Source_tree.Source_tree()
        self.horizontalLayout.addWidget(self.treeWidget_of_Source)
        # self.treeWidget_of_Source.actionDuplicateColumn.triggered.connect(self.addColumnField)
        # self.treeWidget_of_Source.actionDuplicateReplace.triggered.connect(self.duplicateReplace)
        # self.treeWidget_of_Source.actionDeleteColumn.triggered.connect(self.deleteColumn)
        # self.treeWidget_of_Source.actionDeleteReplace.triggered.connect(self.deleteReplace)



class Page4(QtWidgets.QWizardPage, form_wizard_page_4.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class Page5(QtWidgets.QWizardPage, form_wizard_page_5.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class Page6(QtWidgets.QWizardPage, form_wizard_page_6.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class Page7(QtWidgets.QWizardPage, form_wizard_page_7.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class Page8(QtWidgets.QWizardPage, form_wizard_page_8.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)



class RoadMapConfiguration(QtWidgets.QWizard):

    AddDBParameters = 0
    CheckMode = 1
    AddCheckFileParameters = 2
    WithDictMode = 3
    SourceColumns = 4
    TargetColumns = 5
    DictColumnsParameters = 6
    DictTables = 7




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = WizardConfig()
    w.show()
    sys.exit(app.exec())