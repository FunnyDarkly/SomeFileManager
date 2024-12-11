from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from tab_create import Ui_Form as Ui_TabCreate
from FileTableWidget import FileTableWidget

class TabCreateWindow(QtWidgets.QDialog):
    def __init__(self, tab_widget):
        super(TabCreateWindow, self).__init__()
        self.ui = Ui_TabCreate()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget

        self.ui.createButton.clicked.connect(self.create_new_tab)
        self.ui.closeButton.clicked.connect(self.close)

    def create_new_tab(self):
        tab_name = self.ui.lineEdit.text()
        if tab_name:
            new_tab = QtWidgets.QWidget()
            layout = QVBoxLayout(new_tab)

            file_table_widget = FileTableWidget(new_tab, db_name=f"{tab_name}.db")
            layout.addWidget(file_table_widget)

            self.tab_widget.addTab(new_tab, tab_name)
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter a tab name.")