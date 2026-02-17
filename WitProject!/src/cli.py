import click
from core import WitManager  # אם core.py באותה תיקייה

@click.group()
def cli():
    """Mini Wit Version Control"""
    pass

@cli.command()
def init():
    manager = WitManager(".")
    manager.init()

@cli.command()
@click.argument("path", default=".")
def add(path):
    manager = WitManager(path)
    manager.add(path)

@cli.command()
@click.option("-m", "--message", required=True, help="Commit message")
def commit(message):
    manager = WitManager(".")
    manager.commit(message)

@cli.command()
def status():
    manager = WitManager(".")
    print(manager.status())

@cli.command()
@click.argument("commit_id")
def checkout(commit_id):
    manager = WitManager(".")
    manager.checkout(commit_id)

if __name__ == "__main__":
    cli()
