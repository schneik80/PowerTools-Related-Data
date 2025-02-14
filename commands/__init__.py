from .refrences import entry as refrences
from .relateddata import entry as relateddata

commands = [
    refrences,
    relateddata,
]

def start():
    for command in commands:
        command.start()

def stop():
    for command in commands:
        command.stop()
