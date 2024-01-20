class Product:
    def __init__(self, _id, name, quantity, price, location):
        self._id = _id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.location = location

    @property
    def id(self):
        return self._id

    @property
    def get_dict(self):
        return {
            "id": self._id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "location": self.location
        }

