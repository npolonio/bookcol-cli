class Item:
    def __init__(self, id, name, quantity, price):
        self._id = id
        self._name = name
        self._quantity = quantity
        self._price = price
    
    def __str__(self):
        return f"ID: {self._id}, Name: {self._name}, Quantity: {self._quantity}, Price: ${self._price}"
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def quantity(self):
        return self._quantity
    
    @property
    def price(self):
        return self._price
    
    @id.setter
    def id(self, new_id):
        self._id = new_id
    
    @name.setter
    def name(self, new_name):
        self._name = new_name
    
    @quantity.setter
    def quantity(self, new_quantity):
        self._quantity = new_quantity
    
    @price.setter
    def price(self, new_price):
        self._price = new_price

    def __iter__(self):
        yield self._id
        yield self._name
        yield self._quantity
        yield self._price
