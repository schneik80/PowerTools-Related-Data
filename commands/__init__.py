from .relateddata import entry as relateddata
from .confighub import entry as confighub

commands = [
    confighub,
    relateddata,
]


def start():
    for command in commands:
        command.start()


def stop():
    for command in commands:
        command.stop()
