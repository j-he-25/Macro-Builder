import os
from pynput import keyboard
from typing import Optional
import pyautogui
import threading
import time

class Controller:
    def __init__(self, model, view, config):
        self.model = model
        self.view = view
        self.config = config
        self.automation_thread = None

    # Handle Key press events
    def on_press(self, key) -> bool:
        try:
            self.view.log(f"Key pressed: {key}")
            if key == keyboard.Key.esc:
                self.view.log("ESC key pressed. Stopping listener.", 'INFO')
                self.model.stop()
                return False
            return True
        except Exception as e:
            self.view.log(f"Error: {e}" 'WARNING')


    # Handle add click command
    def on_add_click(self, x: int, y: int) -> None:
        self.model.commands.append(['CLICK', x, y])


    # Handle add press command
    def on_add_press(self, key: str) -> None:
        self.model.commands.append(['PRESS', key])
    

    # Handle repeat toggle
    def on_toggle_repeat(self, status) -> None:
        self.model.repeat = status


    # Execute commands in command list
    def execute_commands(self) -> None:
        self.view.log(f"Command Execution Initialized")
        while not self.model.is_stopped():
            for command in self.model.commands:
                try:
                    if command[0] == "CLICK":
                        pyautogui.click(command[1], command[2])
                        self.view.log(f'Command {command[0]} executed at {command[1]}, {command[2]}', 'INFO')
                    elif command[0] == "DOUBLECLICK":
                        pyautogui.doubleclick(command[1], command[2])
                        self.view.log(f'Command {command[0]} executed at {command[1]}, {command[2]}', 'INFO')
                    elif command[0] == "PRESS":
                        pyautogui.press(command[1])
                        self.view.log(f'Command {command[0]} executed with key {command[1]}', 'INFO')
                except Exception as e:
                    self.view.log(f"Error: {e}" 'WARNING')
                finally:
                    if self.model.is_stopped():
                        break
            if not self.model.repeat:
                self.model.stop()
        self.view.log("Command Execution Complete", 'INFO')



    # Start controller actions
    def start(self) -> None:
        self.view.log("Keyboard Listener Initiated", 'INFO')

        try:
            listener = keyboard.Listener(on_press=self.on_press)
            listener.start()
        except Exception as e:
            self.view.log(f'Keyboard Listener failed to start with exception: {e}', 'CRITICAL')

        self.automation_thread = threading.Thread(target=self.execute_commands, daemon=True)
        self.automation_thread.start()

        self.automation_thread.join()
        listener.join()
