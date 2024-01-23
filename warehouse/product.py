import click

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
    
    def format_output(self): 
        click.echo(f"Product found with ID {self.id}:")
        click.echo(f"Product Name: {self.name}")
        click.echo(f"Product Quantity: {self.quantity}")
        click.echo(f"Product Price: {self.price}")
        click.echo(f"Product Location: {self.location}")

    @classmethod
    def create_from_dict(cls, data):
        return cls(data['id'], data['name'], data['quantity'],
                   data['price'], data['location'])


