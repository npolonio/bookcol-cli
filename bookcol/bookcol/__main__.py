import click
from .commands import menu
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


if __name__ == "__main__":
    cli()
