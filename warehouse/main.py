import click
import os

@click.group()
def commands():
    pass
#=====================================================================================
# OPEN FILE
def open_file(file):
    filename = file if file is not None else "inventory.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")  # create an empty file if it doesn't exist
    with open(filename, "r") as f:
        item_list = f.read().splitlines()
    return filename, item_list

#=====================================================================================
# FILTER ITEMS
@click.argument("method", type=click.Choice(["inclusive", "exclusive"]))
def filter_items(item_list, filter_criterion, method):
    if method == "inclusive": return [item for item in item_list if filter_criterion in item]

    elif method == "exclusive": return [item for item in item_list if filter_criterion not in item]

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
# DELETE = REMOVES ITEM FROM THE FILE BROKEN DELETES ALL BUT THE ONE WITH ID INPUT
@click.command()
@click.argument("item_id", type=int, required=True)
def delete(item_id):
    filename, item_list = open_file(None)

    updated_list = filter_items(item_list, f"ID: {item_id}", "exclusive")
   
    with open(filename, "w") as f:
        f.write("\n".join(updated_list))
        f.write("\n")

#=====================================================================================
# DISPLAY = PRINTS ALL THE FILE'S ITEMS 
@click.command()
@click.argument("file", type=click.Path(exists=True), required=False)
def display(file):
    filename, item_list = open_file(file)

    for index, item in enumerate(item_list):
        click.echo(f"({index} - {item})")

#=====================================================================================
# SEARCH - SEARCHES ITEM BY ITS ID AND PRINTS 
@click.command()
@click.argument("item_id", type=int, required=True)
def search(item_id):
    filename, item_list = open_file(None)

    matching_items = filter_items(item_list, f"ID: {item_id}", "inclusive")

    if matching_items:
        for item in matching_items:
            click.echo(item)
    else:
        click.echo(f"No item found with ID: {item_id}")

#=====================================================================================
# ALTER - ALTERS QUANTITY OR PRICE OF ITEM BY ITS ID - HAVE TO ALTER BOTH ATTRIBUTES
@click.command()
@click.argument("item_id", type=int, required=True)
@click.option("-q", "--quantity", type=int, help="New quantity of item")
@click.option("-p", "--price", type=float, help="New price of item")
def alter(item_id, quantity, price):
    if quantity is None and price is None:
        click.echo("Please provide either --quantity (-q) or --price (-p). Use -h or --help for more information.")
        return
    
    filename, item_list = open_file(None)

    matching_item = filter_items(item_list, f"ID: {item_id}", "inclusive")

    if not matching_item:
        click.echo(f"No item found with ID: {item_id}")
        return  # Stop execution if no matching item is found

    updated_list = []
    for item in item_list:
        if f"ID: {item_id}" in item:
            if quantity is not None:
                item = item.replace(f"Quantity: {item.split(', ')[2].split(': ')[1]}", f"Quantity: {quantity}")

            if price is not None:
                item = item.replace(f"Price: {item.split(', ')[3].split(': ')[1]}", f"Price: ${price}")

        updated_list.append(item)

    try:
        with open(filename, "w") as f:
            f.write("\n".join(updated_list))
            f.write("\n")
    except IOError as e:
        click.echo(f"Error writing to file: {e}")
        return

    click.echo(f"Item with ID {item_id} updated successfully")
    click.echo(f"({item})")

#=====================================================================================
commands.add_command(add)
commands.add_command(delete)
commands.add_command(display)
commands.add_command(search)
commands.add_command(alter)

if __name__ == "__main__":
    commands()
