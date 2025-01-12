from PyQt5.QtWidgets import QPushButton, QListWidget, QDialog, QMessageBox
from FileTableWidget import FileTableWidget
from tag_add_ui import Ui_Form as Ui_TagAdd

class TagAddWindow(QDialog):
    def __init__(self, tag_manager, parent_widget):
        super(TagAddWindow, self).__init__(parent_widget)
        self.ui = Ui_TagAdd()
        self.ui.setupUi(self)

        self.tag_manager = tag_manager
        self.tag_list_widget = self.findChild(QListWidget, 'listWidget')
        self.add_button = self.findChild(QPushButton, 'addButton')
        self.close_button = self.findChild(QPushButton, 'closeButton')

        self.load_tags()
        self.add_button.clicked.connect(self.add_tag_to_table)
        self.close_button.clicked.connect(self.close)

    def load_tags(self):
        self.tag_list_widget.clear()
        try:
            tags = self.tag_manager.get_tags()
            for tag in tags:
                self.tag_list_widget.addItem(f'{tag[1]}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tags: {str(e)}")

    def add_tag_to_table(self):
        selected_items = self.tag_list_widget.selectedItems()
        if selected_items:
            selected_tag_name = selected_items[0].text()
            print(f"Adding tag as new column: {selected_tag_name}")

            main_window = self.parent()

            active_tab_index = main_window.tab_widget.currentIndex()
            active_tab_widget = main_window.tab_widget.widget(active_tab_index)

            table_widget = active_tab_widget.findChild(FileTableWidget)

            if table_widget:
                table_widget.add_column(selected_tag_name)
                QMessageBox.information(self, "Success", f"Tag '{selected_tag_name}' added as a new column!")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Could not find the table to add a column.")
        else:
            QMessageBox.warning(self, "Warning", "No tag selected to add.")
