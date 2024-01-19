import click
import json
from product import Product
from inventorymanager import InventoryManager
from inputvalidator import InputValidator

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID (4 digits long)')
@click.option('-n', '--name', prompt=True, type=str, help='Product Name')
@click.option('-q', '--quantity', prompt=True, type=int, help='Product Quantity')
@click.option('-p', '--price', prompt=True, type=float, help='Product Price')
@click.option('-l', '--location', prompt=True, type=str, help='Product Location')
def add(id, name, quantity, price, location):
    try:
        if not (isinstance(id, int) and InputValidator.validate_id(id)):
            raise click.Abort('Error: {} is not a valid ID - It should be a 4 digit long integer.'.format(id))
    except click.Abort as e:
            click.echo(e)
            return
                
    product = Product(id, name, quantity, float(price), location) 

    inventory = InventoryManager() 
    data = inventory.load_inventory()
    data.append(product.get_dict)

    inventory.save_inventory(data)

    click.echo('Product added successfully.')

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to delete')
def delete(id): #Prints 'Product deleted successfully.' even when provided with invalid ID; Raises Error even when performs successfully
    InputValidator.validate_id(id)

    inventory = InventoryManager()
    data = inventory.load_inventory()
    data = [item for item in data if item['id'] != id]

    inventory.save_inventory(data)

    click.echo('Product deleted successfully.')
    display()

@cli.command()
def display():
    inventory = InventoryManager()
    data = inventory.load_inventory()

    click.echo(json.dumps(data, indent=2))

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to search')
def search(id):
    InputValidator.validate_id(id)

    inventory = InventoryManager()
    data = inventory.load_inventory()

    result = [item for item in data if item['id'] == id]

    click.echo(json.dumps(result, indent=2))

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to alter')
@click.option('-a', '--attribute', prompt=True, type=click.Choice(['name', 'quantity', 'price', 'location']), help='Attribute to alter (name, quantity, price, location)')
@click.option('-v', '--value', prompt=True, help='New value')
def alter(id, attribute, value):
    InputValidator.validate_id(id) #Checks if ID is valid

    inventory_manager = InventoryManager() #Creates instance of InventoryManager
    data = inventory_manager.load_inventory() #Loads info in inventory.txt through InventoryManager in a var "data"

    item_found = False #Creates a check var "item_found"
    for item in data: #Iterates through info in data by item - instance of Product
        if item['id'] == id: #Checks if present item share the same id value as provided in function call
                is_valid = InputValidator.validate_attribute(attribute, value)
                if(is_valid):
                    item[attribute] = value #Changes original attribute value with the one provided in function call
                    item_found = True #Changes value of check var "item_found" to communicate the process has been successful
                    break #Exists condition
        
    if not item_found: #If check var "item_found" value not changed demonstrates that item was not found
        click.echo(f'Product with ID {id} not found in the inventory.') #Prints message
        return #Finishes call

    inventory_manager.save_inventory(data) #Saves new information into inventory.txt through InventoryManager
    click.echo('Product altered successfully.') #Prints message

if __name__ == '__main__':
