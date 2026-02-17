import click
from new import WitManager
from ui import UI

manager = WitManager(".")  # אובייקט manager גלובלי
ui = UI()  # אובייקט UI גלובלי אם צריך להציג הודעות

@click.group()
def wit():
    """Mini Wit Version Control"""
    pass

@wit.command()
def init():
    manager.init()
    ui.show_message(".wit initialized")

@wit.command()
@click.argument("path", default=".")
def add(path):
    manager.add(path)
    ui.show_message(f"Added {path} to staging")

@wit.command()
@click.option("-m", "--message", required=True, help="Commit message")
def commit(message):
    manager.commit(message)
    ui.show_message(f"Commit done: {message}")

@wit.command()
def status():
    status_info = manager.status()
    ui.show_status(status_info)

@wit.command()
@click.argument("commit_id")
def checkout(commit_id):
    ok = manager.checkout(commit_id)
    if ok:
        ui.show_message(f"Checked out {commit_id}")

def main():
    wit()  # מריץ את click group

if __name__ == "__main__":
    main()
