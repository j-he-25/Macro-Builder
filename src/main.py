import sys
from model import Model
from view import View
from controller import Controller
from utils import Logging
from config import AppConfig
from PyQt6.QtWidgets import QApplication

def main() -> None:    
    config = AppConfig()
    logger = Logging(print_info=config.print_info, level=config.logging_level)

    app = QApplication(sys.argv)

    model = Model()
    view = View(logger)
    controller = Controller(model, view, config)
    
    view.show()
    view.bring_to_front()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()