# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2022-2026 IMA LLC

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
