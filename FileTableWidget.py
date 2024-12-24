import sqlite3
import os
from datetime import datetime
from PyQt5.QtWidgets import QTableWidget, QFileDialog, QTableWidgetItem


class FileTableWidget(QTableWidget):
    def __init__(self, parent=None, db_name='files_data.db'):
        super(FileTableWidget, self).__init__(parent)

        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['Filename', 'Create date', 'Add date', 'File extension', 'Size'])
        self.setSortingEnabled(True)

        self.db_name = os.path.join('db', db_name)
        self.conn = None
        self.init_db()
        self.load_data()

    def init_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            create_date DATETIME NOT NULL,
            add_date DATETIME NOT NULL,
            file_extension TEXT NOT NULL,
            size INTEGER NOT NULL
        )
        ''')
        self.conn.commit()

    def load_data(self):
        self.setRowCount(0)
        self.cursor.execute('SELECT filename, create_date, add_date, file_extension, size FROM files')
        rows = self.cursor.fetchall()

        for row in rows:
            if row:
                self.insertRow(self.rowCount())
                self.setItem(self.rowCount() - 1, 0, QTableWidgetItem(row[0]))
                self.setItem(self.rowCount() - 1, 1, QTableWidgetItem(row[1]))
                self.setItem(self.rowCount() - 1, 2, QTableWidgetItem(row[2]))
                self.setItem(self.rowCount() - 1, 3, QTableWidgetItem(row[3]))
                self.setItem(self.rowCount() - 1, 4, QTableWidgetItem(str(row[4])))

    def add_files_to_table(self):
        options = QFileDialog.Options()
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select files", "", "All Files (*)", options=options)

        if file_names:
            for file_name in file_names:
                try:
                    if not file_name:
                        continue

                    file_size = round(self.get_file_size(file_name) / 1024, 2)
                    file_extension = os.path.splitext(file_name)[1]

                    base_name = os.path.basename(file_name)
                    file_name_only = os.path.splitext(base_name)[0]

                    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    add_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    self.cursor.execute(
                        'INSERT INTO files (filename, create_date, add_date, file_extension, size) VALUES (?, ?, ?, ?, ?)',
                        (file_name_only, create_date, add_date, file_extension, f"{file_size} KB"))
                    self.conn.commit()

                    self.add_file(file_name_only, create_date, add_date, file_extension, f"{file_size} KB")

                except Exception as e:
                    print(f"Error adding file '{file_name}': {e}")  # Log the error

    def add_file(self, file_name, create_date, add_date, file_extension, file_size):
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, QTableWidgetItem(file_name))
        self.setItem(row_position, 1, QTableWidgetItem(create_date))
        self.setItem(row_position, 2, QTableWidgetItem(add_date))
        self.setItem(row_position, 3, QTableWidgetItem(file_extension))
        self.setItem(row_position, 4, QTableWidgetItem(str(file_size)))

    def clear_database(self):
        try:
            self.cursor.execute("DELETE FROM files")
            self.conn.commit()
            self.load_data()
            print("Database cleared successfully.")
        except Exception as e:
            print(f"Error clearing the database: {e}")

    def get_file_size(self, file_name):
        return os.path.getsize(file_name)

    def close_db(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def delete_database(self):
        self.close_db()
        if os.path.exists(self.db_name):
            os.remove(self.db_name)