import sys, random, json, os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QAction, QMenu
from FileTableWidget import FileTableWidget
from TabCreateWindow import TabCreateWindow
from TabEditWindow import TabEditWindow
from TagManager import TagManager
from TagCreateWindow import TagCreateWindow
from TagEditWindow import TagEditWindow
from TagAddWindow import TagAddWindow
from main_ui import Ui_MainWindow

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
        self.tab_widget.setMovable(True)
        self.tab_widget.clear()

        self.load_tabs()
        if self.tab_widget.count() == 0:
            self.tab_create_window = TabCreateWindow(self.tab_widget)
            self.tab_create_window.create_tab_with_search_and_table("Default folder", "Default folder")

        self.ui.fileaddButton.clicked.connect(self.add_files_to_active_table)

        self.ui.tabcreateButton.clicked.connect(self.open_tab_create_window)
        self.ui.tabeditButton.clicked.connect(self.open_tab_edit_window)

        self.ui.actionClear_database.triggered.connect(self.clear_active_tab_database)

        self.ui.actionEdit_tab.triggered.connect(self.open_tab_edit_window)
        self.ui.actionEdit_tag.triggered.connect(self.open_tag_edit_window)

        self.ui.actionAdd_tab.triggered.connect(self.open_tab_create_window)
        self.ui.actionAdd_file_to_tab.triggered.connect(self.add_files_to_active_table)
        self.ui.actionAdd_tag_to_tab.triggered.connect(self.open_tag_add_window)

        self.tag_manager = TagManager()

        self.ui.tagcreateButton.clicked.connect(self.open_tag_create_window)
        self.ui.tageditButton.clicked.connect(self.open_tag_edit_window)
        self.ui.tagaddButton.clicked.connect(self.open_tag_add_window)

        self.create_context_menu()

    def get_active_table_widget(self):
        current_index = self.tab_widget.currentIndex()
        current_tab = self.tab_widget.widget(current_index)
        table_widget = current_tab.findChild(FileTableWidget)
        return table_widget

    def add_files_to_active_table(self):
        table_widget = self.get_active_table_widget()
        if table_widget:
            table_widget.add_files_to_table()

    def open_tab_create_window(self):
        self.tab_create_window = TabCreateWindow(self.tab_widget)
        self.tab_create_window.show()

    def clear_active_tab_database(self):
        table_widget = self.get_active_table_widget()

        if table_widget:
            reply = QMessageBox.question(self,
                                         "Confirmation",
                                         "Are you sure you want to clear the database for this tab?",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                table_widget.clear_database()
                QMessageBox.information(self, "Success", "Database cleared successfully.")
            else:
                print("Database clearing canceled.")
        else:
            QMessageBox.warning(self, "Warning", "No active table found.")

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
                self.tab_widget.removeTab(index)
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

    def open_tag_create_window(self):
        self.tag_create_window = TagCreateWindow(self.tag_manager)
        self.tag_create_window.show()

    def open_tag_edit_window(self):
        self.tag_edit_window = TagEditWindow(self.tag_manager)
        self.tag_edit_window.show()

    def open_tag_add_window(self):
        self.tag_add_window = TagAddWindow(self.tag_manager, self)
        self.tag_add_window.show()

    def open_file_in_explorer(self):
        table_widget = self.get_active_table_widget()
        if table_widget:
            table_widget.open_in_explorer()

    def delete_selected_row(self):
        table_widget = self.get_active_table_widget()
        if table_widget:
            table_widget.delete_selected_row()

    def delete_selected_column(self):
        table_widget = self.get_active_table_widget()
        if table_widget:
            table_widget.delete_selected_column()

    def create_context_menu(self):
        self.context_menu = QMenu(self)

        self.open_in_explorer = QAction("Open in Explorer", self)
        self.open_in_explorer.triggered.connect(self.open_file_in_explorer)

        self.delete_row = QAction("Delete row", self)
        self.delete_row.triggered.connect(self.delete_selected_row)

        self.delete_column = QAction("Delete column", self)
        self.delete_column.triggered.connect(self.delete_selected_column)

        self.context_menu.addAction(self.open_in_explorer)
        self.context_menu.addAction(self.delete_row)
        self.context_menu.addAction(self.delete_column)

    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())

    def load_tabs(self):
        if os.path.exists('static/files/tabs.json'):
            with open('static/files/tabs.json', 'r') as file:
                tab_data = json.load(file)
                for tab in tab_data:
                    self.tab_create_window = TabCreateWindow(self.tab_widget)
                    self.tab_create_window.create_tab_with_search_and_table(tab['title'], tab['title'])

    def save_tabs(self):
        tab_data = []
        for index in range(self.tab_widget.count()):
            tab_title = self.tab_widget.tabText(index)
            tab_data.append({'title': tab_title})

        with open('static/files/tabs.json', 'w') as file:
            json.dump(tab_data, file, indent=4)

    def closeEvent(self, event):
        self.save_tabs()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())