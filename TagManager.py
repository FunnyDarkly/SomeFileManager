import sqlite3

class TagManager:
    def __init__(self, db_path='db/tags.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT NOT NULL UNIQUE,
            tag_values TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

    def create_tag(self, tag_name, tag_values):
        if not tag_name or not tag_values:
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Tags (tag, tag_values) VALUES (?, ?)', (tag_name, tag_values))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def edit_tag(self, tag_id, new_tag_name, new_tag_values):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''UPDATE Tags SET tag = ?, tag_values = ? WHERE id = ?''', (new_tag_name, new_tag_values, tag_id))
            conn.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False

        except Exception as e:
            print(f"Database error: {str(e)}")
            return False
        finally:
            conn.close()

    def get_tags(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, tag, tag_values FROM Tags')
        tags = cursor.fetchall()
        conn.close()
        return tags

    def delete_tag(self, tag_name):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Tags WHERE tag = ?', (tag_name,))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Database error: {str(e)}")
            return False
        finally:
            conn.close()

    def get_tag_by_id(self, tag_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id, tag, values FROM Tags WHERE id = ?', (tag_id,))
            tag = cursor.fetchone()
            return tag
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None
        finally:
            conn.close()

    def get_tag_by_name(self, tag_name):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT id, tag, tag_values FROM Tags WHERE tag = ?', (tag_name,))

            tag = cursor.fetchone()
            if tag:
                return tag  # Returns a tuple (id, tag, values)
            else:
                return None  # No tag found with the provided name
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None
        finally:
            conn.close()


