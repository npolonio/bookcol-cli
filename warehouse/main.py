import click
import os
from item import Item

@click.group()
def cli():
    pass

#FILE RELATED FUNCTIONS: OPEN-FILE; WRITE-FILE; FILTER-ITEMS
#OPEN-FILE = Opens a file and returns its name and content as a list. If the file doesn't exist, creates an empty file.
def open_file(filename=None):
    default_filename = "inventory.txt"

    if filename is None:
        filename = default_filename

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")  # create an empty file if it doesn't exist

    with open(filename, "r") as f:
        item_list = [Item(*line.split(', ')) for line in f.read().splitlines()]

    return filename, item_list


#WRITE-FILE = Writes on the file
def write_file(file, action, message):
    filename, item_list = open_file(file)

    with open(filename, action) as f:
        f.write(message + "\n")



#FILTER-ITEMS = Filters items based on the given criterion and method.
def filter_items(item_list, filter_criterion):
    return [item for item in item_list if filter_criterion in item]
  


#=========================================================================================================================
#COMMAND FUNCTIONS: ADD; DELETE; DISPLAY; SEARCH; ALTER;  
#ADD = Adds a new item in the file:
@click.command()
@click.argument("file", type=click.Path(), required=False)
@click.option("-i", "--id", prompt="Enter ID", help="ID of item")
@click.option("-n", "--name", prompt="Enter Name", help="Name of item")
@click.option("-q", "--quantity", prompt="Enter quantity", help="Quantity of item")
@click.option("-p", "--price", prompt="Enter price", help="Price of item")
def add(id, name, quantity, price, file):
    filename, item_list = open_file(file)

    new_item = Item(id, name, quantity, price)
    
    write_file(filename, "a", str(new_item))



#DELETE = Remove item in the file based on its ID number:
@click.command()
@click.option("-i", "--item_id", type=int, required=True)
def delete(item_id):
    filename, item_list = open_file(None)

    updated_list = [item for item in item_list if f"ID: {item_id}" not in item]

    write_file(filename, "w", "\n".join(updated_list))
    


#DISPLAY = Prints all the file's items:
@click.command()
@click.argument("file", type=click.Path(exists=True), required=False)
def display(file):
    filename, item_list = open_file(file)

    for index, item in enumerate(item_list):
        click.echo(f"({index} - {item})")



#SEARCH = Search item by its ID and prints it: 
@click.command()
@click.option("-i", "--item_id", type=int, required=True)
def search(item_id):
    filename, item_list = open_file(None)

    matching_items = filter_items(item_list, f"ID: {item_id}")

    if matching_items:
        for item in matching_items:
            click.echo(item)
    else:
        click.echo(f"No item found with ID: {item_id}")



#ALTER = Alters quantity or price of item by its ID: - Use Item class
@click.command()
@click.option("-i", "--item_id", type=int, required=True)
@click.option("-q", "--quantity", type=int, help="New quantity of item")
@click.option("-p", "--price", type=float, help="New price of item")
def alter(item_id, quantity, price):
    if quantity is None and price is None:
        click.echo("Please provide either --quantity (-q) or --price (-p). Use -h or --help for more information.")
        return
    
    filename, item_list = open_file(None) 

    #matching_items = [item for item in item_list if item.id == searching_item_id] #not able to find existing ID
    
    matching_items = filter_items(item_list, f"ID: {item_id}")


    if not matching_items:
        click.echo(f"No item found with ID: {item_id}")
        return

    matching_item = matching_items[0]

    if quantity is not None:
        matching_item.quantity = quantity
    
    if price is not None:
        matching_item.price = price

    try:
        write_file(filename, "w", "\n".join(str(item) for item in item_list))
    except IOError as e:
        click.echo(f"Error writing to file: {e}")
        return

    click.echo(f"Item with ID {item_id} updated successfully")
    click.echo(f"({matching_item})")



cli.add_command(add)
cli.add_command(delete)
cli.add_command(display)
cli.add_command(search)
cli.add_command(alter)

if __name__ == "__main__":
    cli()
