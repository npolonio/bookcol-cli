import json
import os
import logging


class InventoryManager:
    def __init__(self, file_path='inventory.txt', log_filename='inventory.log'):
        self.file_path = file_path
        self.log_filename = log_filename
        self.create_file_if_not_exists()
        self.configure_logging()


    def configure_logging(self):
        logging.basicConfig(filename=self.log_filename, level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')


    def create_file_if_not_exists(self):
        if not os.path.isfile(self.file_path):
            self.create_file()
            logging.info(f'File created: {self.file_path}')


    def create_file(self):
        with open(self.file_path, 'w') as file:
            pass


    def load_inventory(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f'Error loading inventory: {e}')
            return []


    def save_inventory(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)
        logging.info('Inventory saved successfully')

