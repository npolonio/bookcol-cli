import json
import os
import logging

logging.basicConfig(filename='inventory.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class InventoryManager:
    def __init__(self, file_path='inventory.txt'):
        self.file_path = file_path
        self.check_file_path()

    def check_file_path(self):
        if not os.path.isfile(self.file_path):
            self.create_file()

    def create_file(self):
        with open(self.file_path, 'w') as file:
            pass

    def load_inventory(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            self.create_file()
            return []

    def save_inventory(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)
        logging.info('Inventory saved successfully')
