import sqlite3

def setup_database():
    """
    Function to set up a SQLite database for managing a book collection.

    This function establishes a connection to a SQLite database named 'book_collection.db'
    and creates a table named 'books' if it does not exist. The 'books' table has the following schema:
    
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
        Unique identifier for each book, automatically incremented.
    - title: TEXT
        Title of the book.
    - author: TEXT
        Author of the book.
    - pages: INTEGER
        Number of pages in the book.
    - read: INTEGER DEFAULT 0
        Flag indicating whether the book has been read (0 for not read, 1 for read).

    Returns:
        None
    """

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

        
