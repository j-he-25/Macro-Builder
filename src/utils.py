import os
from typing import Optional
from datetime import datetime
from enum import IntEnum
from PyQt6 import QtWidgets, QtCore
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


# Command class which all commands are stored as
class Command:
    def __init__(self, cmd: list) -> None:
        self.cmd = cmd
        self.label = self.get_command_label(cmd)

    def _repr__(self) -> str:
        return self.label
    
    @staticmethod
    def get_command_label(command: list) -> str:
        if command[0] in ["CLICK", "DOUBLECLICK"]:
            return f'{command[0]} at position ({command[1]}, {command[2]})'
        elif command[0] == "PRESS":
            return f"{command[0]} key '{command[1]}'"
        


# Class for custom title bars
class CustomTitleBar(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #333; color: white;")

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.title = QtWidgets.QLabel("Macro Builder")
        self.title.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.title)
        layout.addStretch()

        self.minimize_btn = QtWidgets.QPushButton("–")
        # self.maximize_btn = QtWidgets.QPushButton("🗖")
        self.close_btn =QtWidgets. QPushButton("✕")

        for btn in [self.minimize_btn, 
                    # self.maximize_btn, 
                    self.close_btn]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #444;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #555;
                }
            """)

        layout.addWidget(self.minimize_btn)
        # layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)
        # self.is_maximized = False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.window().move(self.window().pos() + delta)
            self.drag_pos = event.globalPosition().toPoint()