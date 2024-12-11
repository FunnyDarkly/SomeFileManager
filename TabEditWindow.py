from PyQt5.QtWidgets import QDialog
from tab_edit import Ui_Form as Ui_TabEdit

class TabEditWindow(QDialog):
    def __init__(self, current_tab_text, tab_index, tab_widget):
        super(TabEditWindow, self).__init__()
        self.ui = Ui_TabEdit()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.current_index = tab_index

        self.ui.lineEdit.setText(current_tab_text)

        self.ui.changeButton.clicked.connect(self.change_tab_name)
        self.ui.closeButton.clicked.connect(self.close)

    def change_tab_name(self):
        new_tab_name = self.ui.lineEdit.text()
        if new_tab_name:
            self.tab_widget.setTabText(self.current_index, new_tab_name)
            self.close()