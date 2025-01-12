from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit
from tab_create_ui import Ui_Form as Ui_TabCreate
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
            self.create_tab_with_search_and_table(tab_name, tab_name)
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter a tab name.")

    def create_tab_with_search_and_table(self, db_name, tab_title):
        new_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(new_tab, tab_title)

        layout = QVBoxLayout(new_tab)

        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("Search...")
        search_bar.textChanged.connect(lambda: self.filter_table(search_bar.text(), table_widget))

        layout.addWidget(search_bar)

        table_widget = FileTableWidget(new_tab, db_name=f"{db_name}.db")
        layout.addWidget(table_widget)

    def filter_table(self, search_text, table_widget):
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, 0)
            if item is not None:
                if search_text in item.text():
                    table_widget.showRow(row)
                else:
                    table_widget.hideRow(row)
            else:
                table_widget.hideRow(row)
