import click

class Item:
    def __init__(self, item_id, name, quantity, price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def display_info(self): 
        return f"ID: {self.item_id}, Name: {self.name}, Quantity: {self.quantity}, Price: ${self.price}"
    
    def update_quantity(self, new_quantity): 
        self.quantity = new_quantity

    def update_price(self, new_price): 
        self.price = new_price
