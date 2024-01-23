import click
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

    for item_data in data:
        product = Product.create_from_dict(item_data)
        product.format_output()
        click.echo('-' * 20)

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID (4 digits long)')
@click.option('-n', '--name', prompt=True, type=str, help='Product Name')
@click.option('-q', '--quantity', prompt=True, type=int, help='Product Quantity')
@click.option('-p', '--price', prompt=True, type=str, help='Product Price')
@click.option('-l', '--location', prompt=True, type=str, help='Product Location')
def add(id, name, quantity, price, location):
    if not InputValidator.validate_id(id):
        #click.echo('Invalid product ID. Please provide a valid 4-digit number')
        return

    if not InputValidator.validate_quantity(quantity):
        click.echo('Invalid product quantity. Please provide a valid value.')
        return
    
    if not InputValidator.validate_price(price):
        click.echo('Invalid product price. Please provide a valid value')
        return
   
    inventory = InventoryManager() 
    data = inventory.load_inventory()

    for item in data: 
        if item['id'] == id:
            click.echo(f'Product with ID {id} already exists in the inventory.')
            return
        
    product = Product(id, name, quantity, price, location)
    data.append(product.get_dict)

    inventory.save_inventory(data)

    click.echo('Product added successfully.')
    return

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
        for item_data in result:
            product = Product(item_data['id'], item_data['name'], item_data['quantity'], item_data['price'], item_data['location'])
            product.format_output()

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to alter')
@click.option('-a', '--attribute', prompt=True, type=click.Choice(['name', 'quantity', 'price', 'location']), help='Attribute to alter (name, quantity, price, location)')
@click.option('-v', '--value', prompt=True, help='New value')
def alter(id, attribute, value):
    InputValidator.validate_id(id)

    inventory_manager = InventoryManager() 
    data = inventory_manager.load_inventory()

    item_found = False 
    for item in data: 
        if item['id'] == id: 
                is_valid = InputValidator.validate_attribute(attribute, value)
                if(is_valid):
                    item[attribute] = value 
                    item_found = True
                    break
        
    if not item_found:
        click.echo(f'Product with ID {id} not found in the inventory.')
        return 

    inventory_manager.save_inventory(data)
    click.echo('Product altered successfully.')

if __name__ == '__main__':
    cli()
