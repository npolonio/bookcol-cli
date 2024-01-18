import click
import json
from product import Product
from inventory import Inventory

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID')
@click.option('-n', '--name', prompt=True, type=str, help='Product Name')
@click.option('-q', '--quantity', prompt=True, type=int, help='Product Quantity')
@click.option('-p', '--price', prompt=True, type=float, help='Product Price')
@click.option('-l', '--location', prompt=True, type=str, help='Product Location')
def add(id, name, quantity, price, location):
    product = Product(id, name, quantity, float(price), location)
    inventory = Inventory()
    data = inventory.load_inventory()
    data.append(product.get_dict)
    inventory.save_inventory(data)
    click.echo('Product added successfully.')

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to delete')
def delete(id):
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
    inventory = Inventory()
    data = inventory.load_inventory()
    result = [item for item in data if item['id'] == id]
    click.echo(json.dumps(result, indent=2))

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to alter')
@click.option('-a', '--attribute', prompt=True, type=str, help='Attribute to alter (name, quantity, price, location)')
@click.option('-v', '--value', prompt=True, help='New value')
def alter(id, attribute, value):
    inventory = Inventory()
    data = inventory.load_inventory()
    for item in data:
        if item['id'] == id:
            item[attribute] = value
    inventory.save_inventory(data)
    click.echo('Product altered successfully.')

    search(id)

if __name__ == '__main__':
    cli()
