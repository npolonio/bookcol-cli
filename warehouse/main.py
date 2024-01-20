import click
import json
from product import Product
from inventory_manager import InventoryManager
from input_validator import InputValidator

@click.group()
def cli():
    pass

@cli.command()
def display():
    inventory = InventoryManager()
    data = inventory.load_inventory()
   
    click.echo(json.dumps(data, indent=2))
   


@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID (4 digits long)')
@click.option('-n', '--name', prompt=True, type=str, help='Product Name')
@click.option('-q', '--quantity', prompt=True, type=int, help='Product Quantity')
@click.option('-p', '--price', prompt=True, type=float, help='Product Price')
@click.option('-l', '--location', prompt=True, type=str, help='Product Location')
def add(id, name, quantity, price, location): 
    InputValidator.validate_id(id)

    product = Product(id, name, quantity, float(price), location) 

    inventory = InventoryManager() 
    data = inventory.load_inventory()
    data.append(product.get_dict)

    inventory.save_inventory(data)

    click.echo('Product added successfully.')



@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to delete')
def delete(id): 
    if not InputValidator.validate_id(id):
        click.echo(f'Invalid ID: {id}')
        return
    
    inventory = InventoryManager()
    data = inventory.load_inventory()
    
    filtered_data = [item for item in data if item['id'] != id]

    if len(filtered_data) == len(data):
        click.echo(f'Product with ID {id} not found in the inventory.')
    else:
        inventory.save_inventory(filtered_data)
        click.echo(f'Product with ID {id} deleted successfully.')



@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to search')
def search(id): 
    InputValidator.validate_id(id)

    inventory = InventoryManager()
    data = inventory.load_inventory()

    result = [item for item in data if item['id'] == id]

    if not result:
        click.echo(f'Product with ID {id} not found in the inventory.')
    else:
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
    cli()
