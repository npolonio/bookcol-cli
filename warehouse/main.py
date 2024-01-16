import click
import os

@click.group()
def commands():
    pass

def open_file(file):
    filename = file if file is not None else "inventory.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")  # create an empty file if it doesn't exist
    with open(filename, "r") as f:
        item_list = f.read().splitlines()
    return filename, item_list

#=====================================================================================
# ADD = ADDS NEW ITEM TO THE FILE
@click.command()
@click.argument("file", type=click.Path(), required=False)
@click.option("-i", "--id", prompt="Enter ID", help="ID of item")
@click.option("-n", "--name", prompt="Enter Name", help="Name of item")
@click.option("-q", "--quantity", prompt="Enter quantity", help="Quantity of item")
@click.option("-p", "--price", prompt="Enter price", help="Price of item")
def add(id, name, quantity, price, file):
    filename, item_list = open_file(file)
    with open(filename, "a+") as f:
        f.write(f"ID: {id}, Name: {name}, Quantity: {quantity}, Price: ${price}\n")

#=====================================================================================
# REMOVE = REMOVES ITEM FROM THE FILE
@click.command()
@click.argument("item_id", type=int, required=True)
def remove(item_id):
    filename, item_list = open_file(None)

    updated_list = [item for item in item_list if f"ID: {item_id}" not in item]

    with open(filename, "w") as f:
        f.write("\n".join(updated_list))
        f.write("\n")

#=====================================================================================
# DISPLAY = PRINTS ALL THE FILE'S ITEMS 
@click.command()
@click.argument("file", type=click.Path(exists=True), required=False)
def display(file):
    filename, item_list = open_file(file)

    for idx, item in enumerate(item_list):
        click.echo(f"({idx} - {item})")

#=====================================================================================
# SEARCH - SEARCHES ITEM BY ITS ID AND PRINTS 
@click.command()
@click.argument("item_id", type=int, required=True)
def search(item_id):
    filename, item_list = open_file(None)

    matching_items = [item for item in item_list if f"ID: {item_id}" in item]

    if matching_items:
        for item in matching_items:
            click.echo(item)
    else:
        click.echo(f"No item found with ID: {item_id}")


#=====================================================================================
# FILTER - FILTERS ALL THE FILE'S ITEMS BY ? AND PRINTS ONLY RELEVANT ITEMS
# Maybe implement at display
#=====================================================================================
# ALTER - ALTERS QUANTITY/PRICE OF ITEM
#=====================================================================================

commands.add_command(add)
commands.add_command(remove)
commands.add_command(display)
commands.add_command(search)
#commands.add_command(filter)
#commands.add_command(alter)

if __name__ == "__main__":
    commands()
