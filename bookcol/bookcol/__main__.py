import click
import inquirer
import logging
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
    command_name = answer['menu_choice'].lower().replace(' ', '_')

    try:
        cli(['invoke', command_name])
    except click.ClickException as e:
        click.echo(f'Error: {e}')
        logging.error(e)


if __name__ == "__main__":
    cli()
