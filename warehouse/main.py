import click
import logging
from product import Product
from inventory_manager import InventoryManager
from input_validator import InputValidator

logging.basicConfig(filename='inventory.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

@click.group()
def cli():
    pass

@cli.command()
@click.option('--sort-by', type=click.Choice(['id', 'name', 'quantity', 'price', 'location']), 
              help='Sort products by the specified attribute')
def display(sort_by):
    inventory = InventoryManager()
    data = inventory.load_inventory()

    if not data:
        message = 'No products found in the inventory'
        click.echo(message)
        logging.info(message)
        return

    if sort_by: data.sort(key=lambda x: x.get(sort_by, ''))

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
    logging.info(f'Product added: {product}')
    return

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to delete')
def delete(id):
    if not InputValidator.validate_id(id):
        click.echo(f'Invalid ID: {id}')
        return
    
    inventory = InventoryManager()
    data = inventory.load_inventory()
    
    product_to_delete = next((item for item in data if item['id'] == id), None)

    if not product_to_delete:
        message = f'Product with ID {id} not found in the inventory.'
        click.echo(message)
        logging.error(message)
        return
    
    confirmation = click.confirm(f'Are you sure you want to delete the product with ID {id}?')
    
    if not confirmation:
        message = 'Deletion canceled.'
        click.echo(message)
        logging.info(message)
        return

    filtered_data = [item for item in data if item['id'] != id]
    
    inventory.save_inventory(filtered_data)
    click.echo(f'Product with ID {id} deleted successfully.')
    logging.info(f'Product deleted: ID: {id}')

@cli.command()
@click.option('-i', '--id', type=int, help='Product ID to search')
@click.option('--min-price', type=float, help='Minimum price for filtering')
@click.option('--max-price', type=float, help='Maximum price for filtering')
@click.option('-l', '--location', type=str, help='Location for filtering')
def search(id, min_price, max_price, location):
    if id: InputValidator.validate_id(id)
    
    inventory = InventoryManager()
    data = inventory.load_inventory()

    results = []

    if id: results = [item for item in data if item['id'] == id]

    if min_price is not None: results = [item for item in results or data if item.get('price', 0) >= min_price]

    if max_price is not None: results = [item for item in results or data if item.get('price', float('inf')) <= max_price]

    if location: results = [item for item in results or data if item.get('location', '') == location]

    if not results: 
        message = 'No products found matching the specified criteria.'
        click.echo(message)
        logging.error(message)
    else:
        for item_data in results:
            product = Product(item_data['id'], item_data['name'], item_data['quantity'], 
                              item_data['price'], item_data['location'])
            product.format_output()

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to alter')
@click.option('-a', '--attribute', prompt=True, type=click.Choice(['name', 'quantity', 'price', 'location']), 
              help='Attribute to alter (name, quantity, price, location)')
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
        message = f'Product with ID {id} not found in the inventory.'
        click.echo(message)
        logging.info(message)
        return 

    inventory_manager.save_inventory(data)
    click.echo('Product altered successfully.')
    logging.info(f'Product altered: ID: {id}')

if __name__ == '__main__':
    cli()
