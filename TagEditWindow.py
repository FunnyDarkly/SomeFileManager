from PyQt5.QtWidgets import QLineEdit, QPushButton, QListWidget, QDialog, QMessageBox, QListWidgetItem
from tag_edit_ui import Ui_Form as Ui_TagEdit

class TagEditWindow(QDialog):
    def __init__(self, tag_manager):
        super(TagEditWindow, self).__init__()
        self.ui = Ui_TagEdit()
        self.ui.setupUi(self)
        self.tag_manager = tag_manager

        self.tag_list_widget = self.findChild(QListWidget, 'listWidget')
        self.tag_name_edit = self.findChild(QLineEdit, 'tagName')
        self.tag_values_edit = self.findChild(QLineEdit, 'tagValues')
        self.submit_button = self.findChild(QPushButton, 'submitButton')
        self.close_button = self.findChild(QPushButton, 'closeButton')
        self.delete_button = self.findChild(QPushButton, 'deleteButton')

        self.load_tags()

        self.tag_list_widget.itemClicked.connect(self.load_tag_details)
        self.submit_button.clicked.connect(self.submit_changes)
        self.close_button.clicked.connect(self.close)
        self.delete_button.clicked.connect(self.delete_tag)

    def load_tags(self):
        self.tag_list_widget.clear()
        try:
            tags = self.tag_manager.get_tags()
            for tag in tags:
                self.tag_list_widget.addItem(f'{tag[1]}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tags: {str(e)}")

    def load_tag_details(self, item):
        try:
            if not item or not isinstance(item, QListWidgetItem):
                QMessageBox.warning(self, "Warning", "Invalid tag selection.")
                return

            tag_name = item.text()
            print(f"Searching for tag: '{tag_name}'")

            tag_data = self.tag_manager.get_tag_by_name(tag_name)
            if tag_data:
                print(f"Tag found: {tag_data}")
                self.tag_name_edit.setText(tag_data[1])
                self.tag_values_edit.setText(tag_data[2])
            else:
                QMessageBox.warning(self, "Warning", "No tag found with that name.")
                print("No tag data found for the selected name.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tag details: {str(e)}")

    def submit_changes(self):
        try:
            selected_items = self.tag_list_widget.selectedItems()
            if selected_items:
                selected_item = selected_items[0]
                tag_name = selected_item.text().strip()
                print(f"Tag name to submit: '{tag_name}'")

                tag = self.tag_manager.get_tag_by_name(tag_name)

                if tag:
                    new_tag_name = self.tag_name_edit.text().strip()
                    new_tag_values = self.tag_values_edit.text().strip()

                    if not new_tag_name:
                        QMessageBox.warning(self, "Warning", "Tag name cannot be empty.")
                        return
                    if not new_tag_values:
                        QMessageBox.warning(self, "Warning", "Tag values cannot be empty.")
                        return

                    success = self.tag_manager.edit_tag(tag[0], new_tag_name, new_tag_values)
                    if success:
                        QMessageBox.information(self, "Success", "Tag updated successfully!")
                        self.load_tags()
                    else:
                        QMessageBox.warning(self, "Warning", "Failed to update the tag.")
                else:
                    QMessageBox.warning(self, "Warning", "Tag not found.")
            else:
                QMessageBox.warning(self, "Warning", "No tag selected for editing.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit changes: {str(e)}")

    def delete_tag(self):
        selected_items = self.tag_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            tag_name = selected_item.text()
            print(f"Tag name to delete: '{tag_name}'")

            result = QMessageBox.question(self, "Confirm Deletion",
                                          f"Are you sure you want to delete the tag '{selected_item.text()}'?",
                                          QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                success = self.tag_manager.delete_tag(tag_name)
                if success:
                    QMessageBox.information(self, "Success", "Tag deleted successfully!")
                    self.load_tags()
                else:
                    QMessageBox.warning(self, "Warning", "Failed to delete the tag.")
        else:
            QMessageBox.warning(self, "Warning", "No tag selected for deletion.")