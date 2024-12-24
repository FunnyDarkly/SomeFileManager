from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QTextBrowser, QDialog

class TagAddWindow(QDialog):
    def __init__(self, tag_manager, parent_widget):
        super(TagAddWindow, self).__init__(parent_widget)
        self.ui = uic.loadUi('static/ui/tag_add.ui', self)
        self.tag_manager = tag_manager

        self.text_browser = self.findChild(QTextBrowser, 'textBrowser')
        self.add_button = self.findChild(QPushButton, 'addButton')
        self.close_button = self.findChild(QPushButton, 'closeButton')

        self.load_tags()
        self.add_button.clicked.connect(self.add_tag_to_table)
        self.close_button.clicked.connect(self.close)

    def load_tags(self):
        tags = self.tag_manager.get_tags()
        for tag in tags:
            self.text_browser.append(f'ID: {tag[0]}, Tag: {tag[1]}')

    def add_tag_to_table(self):
        selected_tag = self.text_browser.toPlainText().strip()  # Simplified for example purposes
        # Process the selected tag and add to the active table
