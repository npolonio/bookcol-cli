import click
import logging
from product import Product
from inventory_manager import InventoryManager
from input_validator import InputValidator

logging.basicConfig(filename='inventory.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@click.group()
def cli():
    pass

# EXTRACTED FUNCTIONS: 

def load_inventory_data(inventory): 
    try: 
        return inventory.load_inventory()
    except Exception as e:
        message = f'Error loading inventory: {str(e)}'
        click.echo(message)
        logging.error(message)
        return []
    
def find_item_by_id(data, id):
    for item in data:
        if item['id'] == id:
            return item
    return None

def update_item_attribute(item, attribute, value):
    if InputValidator.validate_attribute(attribute, value):
        item[attribute] = value

def save_inventory(inventory, data):
    try:
        inventory.save_inventory(data)
    except Exception as e:
        message = f'Error saving inventory: {str(e)}'
        click.echo(message)
        logging.error(message)

def validate_inputs(id, quantity, price): 
    if not InputValidator.validate_id(id):
        return False

    if not InputValidator.validate_quantity(quantity):
        click.echo('Invalid product quantity. Please provide a valid value.')
        return False
    
    if not InputValidator.validate_price(price):
        click.echo('Invalid product price. Please provide a valid value')
        return False
    
    return True

def create_product(id, name, quantity, price, location):
    return Product(id, name, quantity, price, location)

def add_product_to_inventory(data, product, inventory):
    data.append(product.get_dict)
    inventory.save_inventory(data)


# COMMANDS

@cli.command()
@click.option('--sort-by', type=click.Choice(['id', 'name', 'quantity', 'price', 'location']), help='Sort products by the specified attribute')
def display(sort_by):
    inventory = InventoryManager()
    data = load_inventory_data(inventory)

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
    if not validate_inputs(id, quantity, price):
        return

    inventory = InventoryManager()
    data = load_inventory_data(inventory)

    if not find_item_by_id(data, id) == None:
        click.echo(f'Product with ID {id} already exists in the inventory.')
        return     

    product = create_product(id, name, quantity, price, location)
    add_product_to_inventory(data, product, inventory)

    click.echo('Product added successfully.')
    logging.info(f'Product added: {product}')
    return

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to delete')
def delete(id): # REFACTOR
    if not InputValidator.validate_id(id):
        click.echo(f'Invalid ID: {id}')
        return
    
    inventory = InventoryManager()
    data = load_inventory_data(inventory)
    
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
def search(id, min_price, max_price, location): # REFACTOR
    if id: InputValidator.validate_id(id)
    
    inventory = InventoryManager()
    data = load_inventory_data(inventory)

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
            product = Product(item_data['id'], item_data['name'], item_data['quantity'], item_data['price'], item_data['location'])
            product.format_output()

@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to alter')
@click.option('-a', '--attribute', prompt=True, type=click.Choice(['name', 'quantity', 'price', 'location']), help='Attribute to alter (name, quantity, price, location)')
@click.option('-v', '--value', prompt=True, help='New value')
def alter(id, attribute, value): 
    InputValidator.validate_id(id)
    inventory = InventoryManager() 
    data = load_inventory_data(inventory)

    item = find_item_by_id(data, id)
    if item:
        update_item_attribute(item, attribute, value)
        save_inventory(inventory, data)
        click.echo('Product altered successfully.')
        logging.info(f'Product altered - ID: {id}')

    else:
        message = f'Product with ID {id} not found in the inventory.'
        click.echo(message)
        logging.info(message)

@cli.command()
def inter():
    click.echo('Entering interactive mode. Type "exit" to quit.')

    while True:
        user_input = click.prompt('Enter a command', type=str, prompt_suffix='> ')

        if user_input.lower() == 'exit':
            click.echo('Exiting interactive mode.')
            break

        try: 
            cli(user_input.split())
        except SystemExit as e:
            if str(e) != '0': click.echo('Invalid command. Type "exit" to quit.')

if __name__ == '__main__':
    cli()
  
