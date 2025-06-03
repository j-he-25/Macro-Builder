from PyQt6 import QtWidgets, QtCore
from typing import Optional
from utils import Logging
from utils import CustomTitleBar


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
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window)

        self.title_bar = CustomTitleBar(self)

        # Actions
        col1 = QtWidgets.QVBoxLayout()
        self.click_button = QtWidgets.QPushButton("Add Click")
        self.key_button = QtWidgets.QPushButton("Add Key")
        self.hold_toggle = QtWidgets.QCheckBox("Hold")
        self.clear = QtWidgets.QPushButton("Clear")
        self.repeat_toggle = QtWidgets.QCheckBox("Repeat")
        self.submit = QtWidgets.QPushButton("Run")

        col1.addWidget(self.click_button)
        col1.addWidget(self.key_button)
        col1.addWidget(self.hold_toggle)
        col1.addWidget(self.clear)

        col1.addStretch(1)
        col1.addWidget(self.repeat_toggle)
        col1.addWidget(self.submit)

        # Command List
        col2 = QtWidgets.QVBoxLayout()
        self.command_list = QtWidgets.QListWidget()
        self.command_list.setDragEnabled(True)
        self.command_list.setAcceptDrops(True)
        self.command_list.setDropIndicatorShown(True)
        self.command_list.setDragDropMode(QtWidgets.QListWidget.DragDropMode.InternalMove)

        col2.addWidget(self.command_list)

        self.workspace = QtWidgets.QHBoxLayout()
        self.workspace.addLayout(col1, 30)
        self.workspace.addLayout(col2, 70)

        # Full Application
        self.master = QtWidgets.QVBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.master.addWidget(self.title_bar)
        self.master.addLayout(self.workspace)

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
            
            QPushButton:hover {
                border: 1px solid #000;
            }
            
            QPushButton:pressed {
                background-color: #3d6199;
                border-style: inset;
            }
        """)


    # Window Settings
    def settings(self) -> None:
        self.setWindowTitle("Macro Builder")
        self.setGeometry(250, 250, 600, 300)


    # Bring New Window to front and set as active window
    def bring_to_front(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()