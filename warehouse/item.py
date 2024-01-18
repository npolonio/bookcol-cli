class Item:
    def __init__(self, id, name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
    
    def __str__(self):
         return f"ID: {self.id}, Name: {self.name}, 
         Quantity: {self.quantity}, Price: ${self.price}"
    
    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def getQuantity(self):
        return self.__quantity
    
    def getPrice(self):
        return self.__price
    
    def setId(self, new_id):
        self.__id = new_id
    
    def setName(self, new_name):
        self.__name = new_name
    
    def setQuantity(self, new_quantity):
        self.__quantity = new_quantity
    
    def setPrice(self, new_price):
        self.__price = new_price