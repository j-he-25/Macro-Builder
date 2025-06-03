import threading
from typing import Optional
from utils import Command

class Model:

    def __init__(self) -> None:
        self.stop_event = threading.Event()
        self.commands = []
        self.repeat = False
        self.hold = False

    def add_command(self, cmd: list) -> None:
        self.commands.append(Command(cmd))


    def stop(self) -> None:
        self.stop_event.set()


    def is_stopped(self) -> bool:
        return self.stop_event.is_set()


    def reset(self) -> None:
        self.stop_event.clear()
