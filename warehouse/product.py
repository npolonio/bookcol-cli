class Product:
    def __init__(self, product_id, name, quantity, price, location):
        self._id = product_id
        self._name = name
        self._quantity = quantity
        self._price = price
        self._location = location

    # Getters
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_quantity(self):
        return self._quantity

    def get_price(self):
        return self._price

    def get_location(self):
        return self._location

    # Setters
    def set_id(self, new_id):
        self._id = new_id

    def set_name(self, new_name):
        self._name = new_name

    def set_quantity(self, new_quantity):
        self._quantity = new_quantity

    def set_price(self, new_price):
        self._price = new_price

    def set_location(self, new_location):
        self._location = new_location