import click

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    




'''@click.command()
@click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="2")
@click.argument("taskfile", type=click.Path(exists=False), required=False)
@click.option("-n", "--name", prompt="Enter task", help="Name of task")
@click.option("-d", "--description", prompt="Describe task", help="Description of task")
def add_task(name, description, priority, taskfile):
    filename = taskfile if taskfile is not None else "mytask.txt"
    with open(filename, "a+") as f: f.write(f"{name}: {description} [Priority: {PRIORITIES[priority]}]\n")'''