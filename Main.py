import sys
import os
import random
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox
from FileTableWidget import FileTableWidget
from TabCreateWindow import TabCreateWindow
from TabEditWindow import TabEditWindow

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        uic.loadUi(os.path.join('static', 'ui', 'main.ui'), self)

        self.titles = [
            "File Manager 2.0: The upgrade nobody asked for",
            "Mediocre Manager: Because 'good enough' is sometimes just enough",
            "Just Another File Manager: Uninspired, but it works!",
            "Barely Better Files: Better than nothing, we promise!",
            "Almost Organized: Because perfect organization is overrated",
            "Better than Bad Files: We won’t let you down… too much!"
        ]
        self.setWindowTitle(random.choice(self.titles))

        self.tab_widget = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.layout = QVBoxLayout(self.tab_widget.widget(0))
        self.file_table_widget = FileTableWidget(self.tab_widget.widget(0), db_name='default_folder.db')
        self.layout.addWidget(self.file_table_widget)

        self.add_button = self.findChild(QtWidgets.QPushButton, 'fileaddButton')
        self.add_button.clicked.connect(self.add_files_to_active_table)

        self.tabcreateButton = self.findChild(QtWidgets.QPushButton, 'tabcreateButton')
        self.tabcreateButton.clicked.connect(self.open_tab_create_window)

        self.actionClear_database = self.findChild(QtWidgets.QAction, 'actionClear_database')
        self.actionClear_database.triggered.connect(self.clear_active_tab_database)

        self.actionEdit_tab = self.findChild(QtWidgets.QAction, 'actionEdit_tab')
        self.actionEdit_tab.triggered.connect(self.open_tab_edit_window)

        self.actionAdd_tab = self.findChild(QtWidgets.QAction, 'actionAdd_tab')
        self.actionAdd_tab.triggered.connect(self.open_tab_create_window)

        self.actionAdd_file_to_tab = self.findChild(QtWidgets.QAction, 'actionAdd_file_to_tab')
        self.actionAdd_file_to_tab.triggered.connect(self.add_files_to_active_table)

        self.tabeditButton = self.findChild(QtWidgets.QPushButton, 'tabeditButton')
        self.tabeditButton.clicked.connect(self.open_tab_edit_window)

    def add_files_to_active_table(self):
        current_index = self.tab_widget.currentIndex()
        current_tab = self.tab_widget.widget(current_index)

        table_widget = current_tab.findChild(FileTableWidget)

        if table_widget:
            table_widget.add_files_to_table()

    def open_tab_create_window(self):
        self.tab_create_window = TabCreateWindow(self.tab_widget)
        self.tab_create_window.show()

    def clear_active_tab_database(self):
        current_index = self.tab_widget.currentIndex()
        current_tab = self.tab_widget.widget(current_index)

        table_widget = current_tab.findChild(FileTableWidget)
        if table_widget:
            table_widget.clear_database()

    def open_tab_edit_window(self):
        current_index = self.tab_widget.currentIndex()
        current_tab_text = self.tab_widget.tabText(current_index)

        self.tab_edit_window = TabEditWindow(current_tab_text, current_index, self.tab_widget)
        self.tab_edit_window.exec_()

    def close_tab(self, index):
        if index < 0:
            return

        tab_widget = self.tab_widget.widget(index)

        if tab_widget:
            table_widget = tab_widget.findChild(FileTableWidget)
            if not table_widget:
                print("FileTableWidget not found.")
                return
            reply = QMessageBox.question(self, 'Confirmation',
                                         "Are you sure you want to delete this tab and its database?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.tab_widget.removeTab(index)
                    table_widget.delete_database()
                except Exception as e:
                    print(f"Error deleting database or removing tab: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())