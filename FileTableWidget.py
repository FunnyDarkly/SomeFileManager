import sqlite3, os, subprocess
from datetime import datetime
from PyQt5.QtWidgets import QTableWidget, QFileDialog, QTableWidgetItem, QMessageBox


class FileTableWidget(QTableWidget):
    def __init__(self, parent=None, db_name='files_data.db'):
        super(FileTableWidget, self).__init__(parent)

        self.setColumnCount(5)
        self.setSortingEnabled(True)

        self.db_name = os.path.join('db', db_name)
        self.conn = None
        self.init_db()
        self.load_data()

        self.itemChanged.connect(self.update_database_entry)


    def init_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            filename TEXT NOT NULL,
            create_date DATETIME NOT NULL,
            add_date DATETIME NOT NULL,
            file_extension TEXT NOT NULL,
            size INTEGER NOT NULL
        )
        ''')
        self.conn.commit()

    def load_data(self):
        self.clear()
        self.setRowCount(0)

        self.cursor.execute("PRAGMA table_info(files)")
        col_info = self.cursor.fetchall()

        column_names = [f'"{col[1]}"' for col in col_info if col[1] not in ('id', 'file_path')]
        self.cursor.execute(f"SELECT {', '.join(column_names)} FROM files")
        rows = self.cursor.fetchall()

        self.setColumnCount(len(column_names))
        for i, name in enumerate(column_names):
            header_name = name.strip('"')
            self.setHorizontalHeaderItem(i, QTableWidgetItem(header_name))

        for row_data in rows:
            row_index = self.rowCount()
            self.insertRow(row_index)
            for column_index, value in enumerate(row_data):
                self.setItem(row_index, column_index, QTableWidgetItem(str(value)))

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

                    file_path = file_name

                    self.cursor.execute(
                        'INSERT INTO files (file_path, filename, create_date, add_date, file_extension, size) VALUES (?, ?, ?, ?, ?, ?)',
                        (file_path, file_name_only, create_date, add_date, file_extension, f"{file_size} KB")
                    )
                    self.conn.commit()

                    self.add_file(file_name_only, create_date, add_date, file_extension, f"{file_size} KB")

                except Exception as e:
                    print(f"Error adding file '{file_name}': {e}")

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

    def add_column(self, column_name):
        try:
            self.cursor.execute("PRAGMA table_info(files)")
            existing_columns = [col[1] for col in self.cursor.fetchall()]

            if column_name in existing_columns:
                raise Exception(f"Column '{column_name}' already exists.")

            # Add the column to the database
            query = f'ALTER TABLE files ADD COLUMN {column_name} TEXT'
            self.cursor.execute(query)
            self.conn.commit()  # Commit the change to the database

            # Update the table view
            current_column_count = self.columnCount()
            self.insertColumn(current_column_count)  # Add a new column at the end
            self.setHorizontalHeaderItem(current_column_count, QTableWidgetItem(column_name))  # Set header name

            # Initialize new column data (e.g., populate with empty strings for new rows)
            for row in range(self.rowCount()):
                self.setItem(row, current_column_count, QTableWidgetItem(""))  # Default empty item

            print(f"Column '{column_name}' added successfully to the UI.")

        except Exception as e:
            print(f"Error adding column: {str(e)}")  # Debugging error message

    def delete_selected_column(self):
        selected_items = self.selectedItems()
        if selected_items:
            column_index = selected_items[0].column()

            column_name = self.horizontalHeaderItem(column_index).text()

            confirmation = QMessageBox.question(self, "Confirm Deletion",
                                                f"Are you sure you want to delete the column '{column_name}'?",
                                                QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.cursor.execute("PRAGMA table_info(files);")
                columns = [col[1] for col in self.cursor.fetchall() if col[1] != column_name]

                new_table_name = "files_temp"
                create_query = f"CREATE TABLE {new_table_name} ({', '.join(columns)})"
                self.cursor.execute(create_query)

                insert_query = f"INSERT INTO {new_table_name} ({', '.join(columns)}) SELECT {', '.join(columns)} FROM files"
                self.cursor.execute(insert_query)

                self.cursor.execute("DROP TABLE files")

                self.cursor.execute(f"ALTER TABLE {new_table_name} RENAME TO files")

                self.removeColumn(column_index)

                print(f"Deleted column: '{column_name}' from both the table and the database.")
                self.conn.commit()
            else:
                print("Column deletion canceled.")
        else:
            QMessageBox.warning(self, "Warning", "No cell selected. Please select a cell to delete its column.")

    def delete_selected_row(self):
        selected_items = self.selectedItems()
        if selected_items:
            row_index = selected_items[0].row()

            confirmation = QMessageBox.question(self, "Confirm Deletion",
                                                f"Are you sure you want to delete row {row_index + 1}?",
                                                QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                file_name = self.item(row_index, 0).text()

                try:
                    self.cursor.execute('DELETE FROM files WHERE filename = ?', (file_name,))

                    self.removeRow(row_index)

                    print(
                        f"Deleted row: {row_index + 1} with filename: '{file_name}' from both the table and the database.")
                    self.conn.commit()
                except sqlite3.Error as e:
                    QMessageBox.critical(self, "Database Error", f"Error deleting row from database: {str(e)}")
            else:
                print("Row deletion canceled.")
        else:
            QMessageBox.warning(self, "Warning", "No cell selected. Please select a cell to delete its row.")

    def update_database_entry(self, item):
        row = item.row()
        column = item.column()

        filename_item = self.item(row, 0)

        if filename_item:
            column_name = self.horizontalHeaderItem(column).text()  # Retrieve the header name

            new_value = item.text()  # Get the new value entered by the user

            try:
                self.cursor.execute(f'''
                    UPDATE files 
                    SET "{column_name}" = ?
                    WHERE filename = ?
                ''', (new_value, filename_item.text()))

                self.conn.commit()
            except Exception as e:
                print(f"Error updating database: {e}")

    def open_in_explorer(self):
        selected_items = self.selectedItems()
        if selected_items:
            file_name = selected_items[0].text()

            self.cursor.execute('SELECT file_path FROM files WHERE filename = ?', (file_name,))
            result = self.cursor.fetchone()

            if result:
                file_path = os.path.normpath(result[0])
                print(f"Opening file: {file_path}")

                if os.path.isfile(file_path):
                    subprocess.Popen(f'explorer.exe /select,"{file_path}"')
                else:
                    QMessageBox.warning(self, "Error", f"The file path '{file_path}' does not exist.")
            else:
                QMessageBox.warning(self, "File Not Found",
                                    f"No file found with the name '{file_name}' in the database.")
        else:
            QMessageBox.warning(self, "Warning", "No item selected.")