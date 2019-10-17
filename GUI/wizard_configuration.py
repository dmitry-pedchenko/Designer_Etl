from PyQt5 import QtCore, QtWidgets
import sys
import form_wizard_page_1
import form_wizard_page_2
import form_wizard_page_3
import form_wizard_page_4
import form_wizard_page_5
import form_wizard_page_6
import form_wizard_page_7


class WizardConfig(QtWidgets.QWizard):
    def __init__(self,):
        super().__init__()

        self.setPage(RoadMapConfiguration.CheckMode, WizardPage1(self))
        self.setPage(RoadMapConfiguration.AddDBParameters, WizardPage2(self))
        self.setPage(RoadMapConfiguration.AddCheckFileParameters, WizardPage3(self))
        self.setPage(RoadMapConfiguration.WithDictMode, WizardPage4(self))
        self.setPage(RoadMapConfiguration.SourceColumns, WizardPage5(self))
        self.setPage(RoadMapConfiguration.TargetColumns, WizardPage6(self))
        self.setPage(RoadMapConfiguration.DictColumnsParameters, WizardPage7(self))
        self.setPage(RoadMapConfiguration.DictTables, WizardPage7(self))


class WizardPage1(QtWidgets.QWizardPage, form_wizard_page_1.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setTitle("Chose mode")
        list_of_check_modes = ['true', 'false']
        self.checkMode.addItems(list_of_check_modes)

    def nextId(self) -> int:
        if self.checkMode.currentText() == 'true':
            return RoadMapConfiguration.AddCheckFileParameters
        else:
            return RoadMapConfiguration.AddDBParameters

class WizardPage2(QtWidgets.QWizardPage, form_wizard_page_2.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class WizardPage3(QtWidgets.QWizardPage, form_wizard_page_3.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class WizardPage4(QtWidgets.QWizardPage, form_wizard_page_4.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class WizardPage5(QtWidgets.QWizardPage, form_wizard_page_5.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class WizardPage6(QtWidgets.QWizardPage, form_wizard_page_6.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class WizardPage7(QtWidgets.QWizardPage, form_wizard_page_7.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)



class RoadMapConfiguration(QtWidgets.QWizard):
    CheckMode = 0
    AddDBParameters = 1
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