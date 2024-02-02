import sqlite3

def setup_database():
    with sqlite3.connect('book_collection.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                pages INTEGER,
                read INTEGER DEFAULT 0
            )
        ''')
        conn.commit()