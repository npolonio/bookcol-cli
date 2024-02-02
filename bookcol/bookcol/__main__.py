import click
import inquirer
from .db import setup_database
from . import commands


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        menu()


cli.add_command(commands.add)
cli.add_command(commands.alter)
cli.add_command(commands.delete)
cli.add_command(commands.search)
cli.add_command(commands.display)
cli.add_command(commands.filter)
cli.add_command(commands.backup)
cli.add_command(commands.restore)


def menu():
    questions = [
        inquirer.List('menu_choice',
                      message='Choose an action:',
                      choices=[
                          'Add a book',
                          'Alter a book',
                          'Delete a book',
                          'Search for a book',
                          'Display all books',
                          'Filter books',
                          'Backup collection',
                          'Restore collection',
                          'Exit'
                      ]),
    ]

    answer = inquirer.prompt(questions)

    if answer['menu_choice'] == 'Add a book':
        cli(['add'])
    elif answer['menu_choice'] == 'Alter a book':
        cli(['alter'])
    elif answer['menu_choice'] == 'Delete a book':
        cli(['delete'])
    elif answer['menu_choice'] == 'Search for a book':
        cli(['search'])
    elif answer['menu_choice'] == 'Display all books':
        cli(['display'])
    elif answer['menu_choice'] == 'Filter books':
        cli(['filter'])
    elif answer['menu_choice'] == 'Backup collection':
        cli(['backup'])
    elif answer['menu_choice'] == 'Restore collection':
        cli(['restore'])
    elif answer['menu_choice'] == 'Exit':
        click.echo('Goodbye!')
        exit()


if __name__ == "__main__":
    cli()
