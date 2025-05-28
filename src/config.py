from dataclasses import dataclass

@dataclass
class AppConfig:
    # Levels consist of (most to least): DEBUG, INFO, WARNING, ERROR, CRITICAL, NONE
    logging_level = 'DEBUG'

    # Print log info to Terminal
    print_info = True