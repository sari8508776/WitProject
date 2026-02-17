import click
from core import WitManager
class cli(ui):


    @cli.command()
    def init():
        manager = WitManager(".")
        manager.init()

    @main.command()
    @click.argument('path', default='.')
    def add(path):
        wit=WitManager()
        # try:
        #    wit.add(path)






