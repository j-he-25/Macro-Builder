from model import Model
from view import View
from controller import Controller
from utils import Logging
from config import AppConfig

def main() -> None:
    config = AppConfig()
    logger = Logging(print_info=config.print_info, level=config.logging_level)

    model = Model()
    view = View(logger)
    controller = Controller(model, view, config)
    controller.start()

if __name__ == "__main__":
    main()