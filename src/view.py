from PyQt6 import QtWidgets
from typing import Optional
from utils import Logging


class View(QtWidgets.QWidget):
    def __init__(self, log: Logging) -> None:
        super().__init__()
        self.setWindowTitle("Macro Builder")
        self.logger = log
        self.initUI()
        self.settings()


    def log(self, message: str, level: Optional[str] = 'DEBUG') -> None:
        self.logger.log(message, level)


    # App UI and Design
    def initUI(self) -> None:
        col1 = QtWidgets.QVBoxLayout()
        title1 = QtWidgets.QLabel("Menu")
        self.click_button = QtWidgets.QPushButton("Add Click")
        self.key_button = QtWidgets.QPushButton("Add Key")
        self.clear = QtWidgets.QPushButton("Clear")
        self.repeat_box = QtWidgets.QCheckBox("Repeat")
        self.submit = QtWidgets.QPushButton("Run")

        col1.addWidget(title1)
        col1.addWidget(self.click_button)
        col1.addWidget(self.key_button)
        col1.addWidget(self.clear)
        col1.addWidget(self.repeat_box)
        col1.addWidget(self.submit)

        col2 = QtWidgets.QVBoxLayout()
        self.command_list = QtWidgets.QListWidget()

        col2.addWidget(self.command_list)

        self.master = QtWidgets.QHBoxLayout()

        self.master.addLayout(col1, 30)
        self.master.addLayout(col2, 70)

        self.setLayout(self.master)

        self.setStyleSheet("""
            QWidget {
                background-color: #333;
                color: #fff;
            }
            
            QPushButton {
                background-color: #66a3ff;
                color: #333;
                border: 1px solid #fff;
                border-radius: 5px;
                padding: 5px 10px;
            }
        """)


    # Window Settings
    def settings(self) -> None:
        self.setWindowTitle("Macro Builder")
        self.setGeometry(250, 250, 600, 300)


    # Bring New Window to front and set as active window
    def bring_to_front(self) -> None:
        self.raise_()
        self.activateWindow()