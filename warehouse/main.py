import click
import json
from product import Product
from inventory import Inventory
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

    inventory = Inventory() 
    data = inventory.load_inventory()
    data.append(product.get_dict)

    inventory.save_inventory(data)

    click.echo('Product added successfully.')

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to delete')
def delete(id): #needs to say "ID not found" Raises error even after success (no such option: -i)
    if not InputValidator.validate_id(id): 
        click.echo('Invalid ID. Please provide a 4-digit integer.')
        return

    inventory = Inventory()
    data = inventory.load_inventory()
    data = [item for item in data if item['id'] != id]

    inventory.save_inventory(data)

    click.echo('Product deleted successfully.')
    display()

@cli.command()
def display():
    inventory = Inventory()
    data = inventory.load_inventory()

    click.echo(json.dumps(data, indent=2))

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to search')
def search(id):
        if not InputValidator.validate_id(id): 
            click.echo('Invalid ID. Please provide a 4-digit integer.')
            return
        
        inventory = Inventory()
        data = inventory.load_inventory()

        result = [item for item in data if item['id'] == id]

        click.echo(json.dumps(result, indent=2))

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to alter')
@click.option('-a', '--attribute', prompt=True, type=click.Choice(['name', 'quantity', 'price', 'location']), help='Attribute to alter (name, quantity, price, location)')
@click.option('-v', '--value', prompt=True, help='New value')
def alter(id, attribute, value):
    if not InputValidator.validate_id(id): 
        click.echo('Invalid ID. Please provide a 4-digit integer.')
        return

    inventory = Inventory() 
    data = inventory.load_inventory() 

    item_found = False
    for item in data: 
        if item['id'] == id: 
                item[attribute] = value
                item_found = True
                break
        
    if not item_found: 
        click.echo(f'Product with ID {id} not found in the inventory.')

    inventory.save_inventory(data)
    click.echo('Product altered successfully.')

if __name__ == '__main__':
    cli()
