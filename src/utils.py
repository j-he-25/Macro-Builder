import os
from typing import Optional
from datetime import datetime
from enum import IntEnum
from pathlib import Path

class LogLevels(IntEnum):
    NONE = 0
    CRITICAL = 1
    ERROR = 2
    WARNING = 3
    INFO = 4
    DEBUG = 5

class Logging:
    def __init__(self, log_dir: Optional[str] = None, filename: Optional[str] = None, print_info: Optional[bool] = False, level: Optional[str] = 'CRITICAL'):
        
        self.log_file_path = None
        self.print = print_info
        self.level = LogLevels[level]
        
        try:
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            else:
                log_dir = self.get_log_directory()
        except Exception as e:
            print(f"Logger was not initialized with exception: {e}")
            return

        self.log_file_path = self.generate_log_file_path(log_dir, filename)

    # Generates a log directory based on my usual format
    def get_log_directory(self):
        log_dir = Path(__file__).resolve().parent.parent / 'log'
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir


    # Generate unique log file path
    def generate_log_file_path(self, log_dir: str, filename: Optional[str] = None) -> str:
        base_name = filename or datetime.now().strftime('%Y-%m-%d')
        file_path = os.path.join(log_dir, f"{base_name}.txt")

        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(log_dir, f"{base_name} ({counter}).txt")
            counter += 1

        return file_path

    # Log a message to console and log file
    def log(self, message: str, level: Optional[str] = 'DEBUG') -> None:
        if LogLevels[level] <= self.level:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            full_message = f"[{timestamp}] {message}"
            
            with open(self.log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(full_message + '\n')
                if self.print:
                    print(full_message)