import click
import logging
import json
from product import Product
from inventory_manager import InventoryManager
from input_validator import InputValidator
from sqlite_manager import SQLiteManager


logging.basicConfig(filename='inventory.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@click.group()
def cli():
    pass


# FUNCTIONS ======================================================================================================================================== 


# INVENTORY FILE MANIPULATORS =========================================================================================================================


def load_inventory_data(inventory): 
    try: 
        return inventory.load_inventory()
    except Exception as e:
        message = f'Error loading inventory: {str(e)}'
        click.echo(message)
        logging.error(message)
        return []


def save_inventory(inventory, data, sqlite_manager=SQLiteManager()):
    try:
        inventory.save_inventory(data)

        sqlite_manager.create_table()
        sqlite_manager.save_data(data)

    except Exception as e:
        message = f'Error saving inventory: {str(e)}'
        click.echo(message)
        logging.error(message)


def create_product(id, name, quantity, price, location):
    return Product(id, name, quantity, price, location)


def add_product_to_inventory(data, product, inventory):
    data.append(product.to_dict)
    inventory.save_inventory(data)


def update_item_attribute(item, attribute, value):
    if InputValidator.validate_attribute(attribute, value):
        item[attribute] = value


# BACKUP/RESTORE ====================================================================================================================================


def backup_data(inventory, filename, sqlite_manager=SQLiteManager()):
    try:
        data = InventoryManager.load_inventory(inventory)
        inventory.save_inventory(data, filename)
        message = f'Backup successful. Data saved to {filename}.'
        click.echo(message)
        logging.info(message)

        sqlite_manager.create_table()
        sqlite_manager.save_data(data)
        message = f'Backup successful. Data saved to {sqlite_manager.filename}.'
        click.echo(message)
        logging.info(message)

    except Exception as e:
        message = f'Error during backup: {str(e)}'
        click.echo(message)
        logging.error(message)


def restore_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        message = 'Restore successful. Data loaded from backup.'
        click.echo(message)
        logging.info(message)
        return data
    except FileNotFoundError:
        message = 'Backup file not found. Unable to restore.'
        click.echo(message)
        logging.info(message)
        return []
    except Exception as e:
        message = f'Error during restore: {str(e)}'
        click.echo(message)
        logging.info(message)
        return []


def backup_inventory(inventory):
    try:
        data = load_inventory_data(inventory)
        backup_filename = 'inventory_backup.json'
        backup_data(data, backup_filename)
    except Exception as e:
        message = f'Error during backup: {str(e)}'
        click.echo(message)
        logging.error(message)


def restore_inventory(inventory):
    try:
        backup_filename = 'inventory_backup.json'
        restored_data = restore_data(backup_filename)
        if restored_data:
            inventory.save_inventory(restored_data)
            message = 'Inventory restored successfully.'
            click.echo(message)
            logging.info(message)
    except Exception as e:
        message = f'Error during restore: {str(e)}'
        click.echo(message)
        logging.error(message)


# HANDLERS ====================================================================================================================================================


def handle_invalid_id(id):
    message = f'Invalid ID: {id}'
    click.echo(message)
    logging.error(message)


def handle_product_not_found(id):
    message = f'Product with ID {id} not found in the inventory.'
    click.echo(message)
    logging.error(message)


def handle_deletion_canceled():
    message = 'Deletion canceled.'
    click.echo('-' * 20)
    click.echo(message)
    click.echo('-' * 20)
    logging.info(message)


def handle_success(message, log_message):
    click.echo('-' * 20)
    click.echo(message)
    click.echo('-' * 20)
    logging.info(log_message)


# FILTERS ====================================================================================================================================================


def find_product_by_id(data, id): 
    for item in data:
        if item['id'] == id:
            return item
    return None


def filter_by_id(data, item_id):
    return next((item for item in data if item.get('id') == item_id), None)


def filter_by_min_price(data, min_price):
    return [item for item in data if item.get('price', 0) >= min_price]


def filter_by_max_price(data, max_price):
    return [item for item in data if item.get('price', float('inf')) <= max_price]


def filter_by_location(data, location):
    return [item for item in data if item.get('location', '') == location]


def filter_results(data, item_id, min_price, max_price, location):
    results = []

    if item_id is not None:
        item = filter_by_id(data, item_id)
        results = [item] if item is not None else []

    if min_price is not None:
        results = filter_by_min_price(results or data, min_price)

    if max_price is not None:
        results = filter_by_max_price(results or data, max_price)

    if location:
        results = filter_by_location(results or data, location)

    return results


# DISPLAYER ====================================================================================================================================================


def display_results_for_search(results):
    if not results: 
        message = 'No products found matching the specified criteria.'
        click.echo(message)
        logging.error(message)
    else:
        for item_data in results:
            product = Product(item_data['id'], item_data['name'], item_data['quantity'], item_data['price'], item_data['location'])
            product.format_output()


# VALIDATORS =================================================================================================================================================
            

def validate_inputs_for_add(id, quantity, price): 
    if not InputValidator.validate_id(id):
        return False

    if not InputValidator.validate_quantity(quantity):
        click.echo('Invalid product quantity. Please provide a valid value.')
        return False
    
    if not InputValidator.validate_price(price):
        click.echo('Invalid product price. Please provide a valid value.')
        return False
    
    return True


# COMMANDS ====================================================================================================================================================


@cli.command()
@click.option('--sort-by', type=click.Choice(['id', 'name', 'quantity', 'price', 'location']), help='Sort products by the specified attribute')
def display(sort_by):
    inventory = InventoryManager()
    data = load_inventory_data(inventory)

    if not data:
        message = 'No products found in the inventory.'
        click.echo(message)
        logging.info(message)
        return

    if sort_by: 
        data.sort(key=lambda x: x.get(sort_by, ''))

    click.echo('-' * 20)
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
    if not validate_inputs_for_add(id, quantity, price):
        return

    inventory = InventoryManager()
    data = load_inventory_data(inventory)

    if not find_product_by_id(data, id) == None:
        handle_invalid_id(id)
        return     

    product = create_product(id, name, quantity, price, location)
    add_product_to_inventory(data, product, inventory)

    handle_success('Product added successfully.', f'Product added: {product}.')
    return


@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to search')
@click.option('--min-price', type=float, help='Minimum price for filtering')
@click.option('--max-price', type=float, help='Maximum price for filtering')
@click.option('-l', '--location', type=str, help='Location for filtering')
def search(id, min_price, max_price, location): #BROKEN
    if id: 
        try: 
            InputValidator.validate_id(id)
        except:
            handle_invalid_id(id)
            return

    inventory = InventoryManager()
    data = load_inventory_data(inventory)

    results = filter_results(data, id, min_price, max_price, location)

    click.echo('-' * 20)
    display_results_for_search(results)
    click.echo('-' * 20)


@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to alter')
@click.option('-a', '--attribute', prompt=True, type=click.Choice(['name', 'quantity', 'price', 'location']), help='Attribute to alter (name, quantity, price, location)')
@click.option('-v', '--value', prompt=True, help='New value')
def alter(id, attribute, value): 
    try:
        InputValidator.validate_id(id)
    except:
        handle_invalid_id(id)
        return

    inventory = InventoryManager() 
    data = load_inventory_data(inventory)

    item = find_product_by_id(data, id)
    if item:
        update_item_attribute(item, attribute, value)
        save_inventory(inventory, data)

        handle_success('Product altered successfully.', f'Product altered - ID: {id}.')

    else:
        handle_product_not_found(id)


@cli.command()
@click.option('-i', '--id', prompt=True, type=int, help='Product ID to delete')
def delete(id):
    if not InputValidator.validate_id(id):
        handle_invalid_id(id)
        return
    
    inventory = InventoryManager()
    data = load_inventory_data(inventory)
    
    product_to_delete = find_product_by_id(data, id)

    if not product_to_delete:
        handle_product_not_found(id)
        return
    
    confirmation = click.confirm(f'Are you sure you want to delete the product with ID {id}?')
    
    if not confirmation:
        handle_deletion_canceled()
        return

    filtered_data = [item for item in data if item['id'] != id]
    
    save_inventory(inventory, filtered_data)
    #handle_deletion_success(id)
    handle_success(f'Product with ID {id} deleted successfully.', f'Product deleted: ID: {id}.')


@cli.command()
def backup():
    inventory = InventoryManager()
    backup_inventory(inventory)


@cli.command()
def restore():
    inventory = InventoryManager()
    restore_inventory(inventory)


@cli.command()
def interact():
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

    
