import os
from pynput import keyboard, mouse
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

        self.connect_signals()

    # Handle Key press events
    def on_press(self, key: keyboard.Key) -> bool:
        try:
            self.view.log(f"Key pressed: {key}")
            if key == keyboard.Key.esc:
                self.view.log("ESC key pressed. Stopping listener.", 'INFO')
                self.model.stop()
                return False
        except Exception as e:
            self.view.log(f"Error: {e}" 'WARNING')
        
        if self.model.is_stopped():
            return False
        else:
            return True


    # Handle add click command
    def set_add_click(self) -> None:
        def on_add_click(x:int, y:int, button, pressed) -> bool:
            try:
                if pressed and button == mouse.Button.left:  # Capture only left clicks
                    self.model.commands.append(['CLICK', x, y])  # Save coordinates
                    self.view.log(f"Click command added at: {x}, {y}", 'INFO')
                return False
            except Exception as e:
                self.view.log(f"Error: {e}", 'WARNING')

        listener = mouse.Listener(on_click=on_add_click)
        listener.start()
        
        self.view.showMinimized()

        listener.join()

        self.view.showNormal()
        self.view.bring_to_front()


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


    # Start Execution of commands
    def start_execution(self) -> None:
        try:
            listener = keyboard.Listener(on_press=self.on_press)
            listener.start()
        except Exception as e:
            self.view.log(f'Keyboard Listener failed to start with exception: {e}', 'CRITICAL')

        self.view.showMinimized()

        self.automation_thread = threading.Thread(target=self.execute_commands, daemon=True)
        self.automation_thread.start()

        self.automation_thread.join()
        listener.stop()

        self.model.reset()
        self.view.showNormal()
        self.view.bring_to_front()


    # Connect buttons to actions
    def connect_signals(self) -> None:
        self.view.click_button.clicked.connect(self.set_add_click)
        self.view.submit.clicked.connect(self.start_execution)