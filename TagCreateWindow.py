from PyQt5.QtWidgets import QLineEdit, QPushButton, QDialog, QMessageBox
from tag_create_ui import Ui_Form as Ui_TagCreate

class TagCreateWindow(QDialog):
    def __init__(self, tag_manager):
        super(TagCreateWindow, self).__init__()
        self.ui = Ui_TagCreate()
        self.ui.setupUi(self)
        self.tag_manager = tag_manager

        self.tag_name_edit = self.findChild(QLineEdit, 'tagName')
        self.tag_values_edit = self.findChild(QLineEdit, 'tagValues')
        self.create_button = self.findChild(QPushButton, 'createButton')
        self.close_button = self.findChild(QPushButton, 'closeButton')

        self.create_button.clicked.connect(self.create_tag)
        self.close_button.clicked.connect(self.close)

    def create_tag(self):
        tag_name = self.tag_name_edit.text().strip()
        tag_values = self.tag_values_edit.text()
        tag_values_list = tag_values.split(',')

        if self.tag_manager.create_tag(tag_name, ','.join(tag_values_list)):
            QMessageBox.information(self, "Success", "Tag created successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Tag creation failed. Tag name may already exist.")