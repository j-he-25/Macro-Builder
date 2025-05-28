import PyQt6
from typing import Optional
from utils import Logging

class View:
    def __init__(self, log: Logging) -> None:
        self.logger = log

    def log(self, message: str, level: Optional[str] = 'DEBUG') -> None:
        self.logger.log(message, level)