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
        """Create a new tag."""
        if not tag_name or not tag_values:
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Tags (tag, tag_values) VALUES (?, ?)', (tag_name, tag_values))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Tag name must be unique
        finally:
            conn.close()

    def edit_tag(self, tag_id, new_tag_name, new_tag_values):
        """Edit an existing tag."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE Tags SET tag = ?, tag_values = ? WHERE id = ?', (new_tag_name, new_tag_values, tag_id))
        conn.commit()
        conn.close()

    def get_tags(self):
        """Retrieve all tags and their values."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, tag, tag_values FROM Tags')
        tags = cursor.fetchall()
        conn.close()
        return tags

    def delete_tag(self, tag_id):
        """Delete a tag by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Tags WHERE id = ?', (tag_id,))
        conn.commit()
        conn.close()

    def get_tag_by_id(self, tag_id):
        """Retrieve a tag by its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, tag, values FROM Tags WHERE id = ?', (tag_id,))
        tag = cursor.fetchone()
        conn.close()
        return tag
