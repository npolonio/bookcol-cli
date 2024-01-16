import click

@click.group()
def commands():
    pass

# ADD-ITEM
@click.command()
@click.argument("file", type=click.Path(), required=False)
@click.option("-id", "--id", prompt="Enter ID", help="ID of item")
@click.option("-n", "--name", prompt="Enter task", help="Name of item")
@click.option("-q", "--quantity", prompt="Enter quantity", help="Quantity of item")
@click.option("-p", "--price", prompt="Enter price", help="Price of item")
def add_item(id, name, quantity, price, file):
    filename = file if file is not None else "inventory.txt"
    with open(filename, "a+") as f:
        f.write(f"ID: {id}, Name: {name}, Quantity: {quantity}, Price: ${price}\n")



#=====================================================================================

# DELETE ITEM - DELETE BY ID INSTEAD OF INDEX
@click.command()
@click.argument("item_id", type=int, required=True)
def del_item(item_id):
    filename = "inventory.txt"
    with open(filename, "r") as f:
        item_list = f.read().splitlines()

    updated_list = [item for item in item_list if f"ID: {item_id}" not in item]

    with open(filename, "w") as f:
        f.write("\n".join(updated_list))
        f.write("\n")



#=====================================================================================

# LIST ITEMS
@click.command()
@click.argument("file", type=click.Path(exists=True), required=False)
def list_items(file):
    filename = file if file is not None else "inventory.txt"
    with open(filename, "r") as f:
        item_list = f.read().splitlines()

    for idx, item in enumerate(item_list):
        click.echo(f"({idx} - {item})")



#=====================================================================================


commands.add_command(add_item)
commands.add_command(del_item)
commands.add_command(list_items)

if __name__ == "__main__":
    commands()
