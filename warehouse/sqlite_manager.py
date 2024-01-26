import sqlite3
import click
import logging
from inventory_manager import InventoryManager

class SQLiteManager:
    def __init__(self, filename='inventory.db'):
        self.filename = filename

    def create_table(self):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                location TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save_data(self, data):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM inventory')
        cursor.executemany('''
            INSERT INTO inventory (id, name, quantity, price, location)
            VALUES (?, ?, ?, ?, ?)
        ''', [(item['id'], item['name'], item['quantity'], item['price'], item['location']) for item in data])
        conn.commit()
        conn.close()

# Modify backup_data and save_inventory functions

def backup_data(inventory, filename, sqlite_manager=SQLiteManager()):
    try:
        data = InventoryManager.load_inventory(inventory)

        # Save to inventory.txt
        inventory.save_inventory(data, filename)
        message = f'Backup successful. Data saved to {filename}.'
        click.echo(message)
        logging.info(message)

        # Save to SQLite
        sqlite_manager.create_table()
        sqlite_manager.save_data(data)

        message = f'Data saved to {sqlite_manager.filename}.'
        click.echo(message)
        logging.info(message)

    except Exception as e:
        message = f'Error during backup: {str(e)}'
        click.echo(message)
        logging.error(message)

# ...

def save_inventory(inventory, data, sqlite_manager=SQLiteManager()):
    try:
        # Save to inventory.txt
        inventory.save_inventory(data)

        # Save to SQLite
        sqlite_manager.create_table()
        sqlite_manager.save_data(data)

    except Exception as e:
        message = f'Error saving inventory: {str(e)}'
        click.echo(message)
        logging.error(message)

# ...
