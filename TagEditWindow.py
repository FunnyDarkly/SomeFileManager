import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLineEdit, QPushButton, QListWidget, QDialog, QMessageBox


class TagEditWindow(QDialog):
    def __init__(self, tag_manager):
        super(TagEditWindow, self).__init__()
        uic.loadUi('static/ui/tag_edit.ui', self)
        self.tag_manager = tag_manager

        # UI Elements
        self.tag_list_widget = self.findChild(QListWidget, 'tagListWidget')
        self.tag_name_edit = self.findChild(QLineEdit, 'tagName')
        self.tag_values_edit = self.findChild(QLineEdit, 'tagValues')
        self.submit_button = self.findChild(QPushButton, 'submitButton')
        self.close_button = self.findChild(QPushButton, 'closeButton')

        # Load tags into the ListWidget
        self.load_tags()

        # Connect signals
        self.tag_list_widget.itemClicked.connect(self.load_tag_details)
        self.submit_button.clicked.connect(self.submit_changes)
        self.close_button.clicked.connect(self.close)

    def load_tags(self):
        """Load all tags from the database and display them."""
        self.tag_list_widget.clear()  # Clear previous content
        try:
            tags = self.tag_manager.get_tags()  # Retrieve tags from the manager
            for tag in tags:
                self.tag_list_widget.addItem(f'ID: {tag[0]}, Tag: {tag[1]}')  # Add to the list
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tags: {str(e)}")

    def load_tag_details(self, item):
        """Load selected tag details into editing fields."""
        try:
            selected_text = item.text()  # Get the selected text
            tag_id = selected_text.split(':')[0].replace('ID: ', '')  # Extract the ID

            tag_data = self.tag_manager.get_tag_by_id(tag_id)  # Fetch data by ID
            if tag_data:
                self.tag_name_edit.setText(tag_data[1])  # Set the tag name
                self.tag_values_edit.setText(tag_data[2])  # Set the tag values
            else:
                QMessageBox.warning(self, "Warning", "Unable to fetch tag details.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tag details: {str(e)}")

    def submit_changes(self):
        """Submit changes to the selected tag."""
        try:
            selected_items = self.tag_list_widget.selectedItems()  # Get selected items
            if selected_items:
                selected_item = selected_items[0]  # Take the first selected item
                tag_id = selected_item.text().split(':')[0].replace('ID: ', '')  # Extract ID

                new_tag_name = self.tag_name_edit.text().strip()
                new_tag_values = self.tag_values_edit.text().strip()

                # Validate inputs
                if not new_tag_name:
                    QMessageBox.warning(self, "Warning", "Tag name cannot be empty.")
                    return
                if not new_tag_values:
                    QMessageBox.warning(self, "Warning", "Tag values cannot be empty.")
                    return

                # Update the tag in the database
                success = self.tag_manager.edit_tag(tag_id, new_tag_name, new_tag_values)
                if success:
                    QMessageBox.information(self, "Success", "Tag updated successfully!")
                    self.load_tags()  # Refresh the tag list
                else:
                    QMessageBox.warning(self, "Warning", "Failed to update the tag.")
            else:
                QMessageBox.warning(self, "Warning", "No tag selected for editing.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit changes: {str(e)}")
