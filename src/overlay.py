from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui

class Overlay(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.resize(self.screen().geometry().size())
        self.move(0, 0)
        self.showFullScreen()
        self.hide()

        self.label = QtWidgets.QLabel("Press any key to continue...", self)
        self.label.setStyleSheet("color: white; font-size: 24px;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.hide()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.cross_cursor = QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor)


    def show_click_overlay(self) -> None:
        self.label.hide()
        self.setCursor(self.cross_cursor)
        self.show()

    def show_press_overlay(self) -> None:
        self.label.show()
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        self.show()

    def paintEvent(self, event) -> None:
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 128))