import os
from pynput import keyboard, mouse
from typing import Optional
from overlay import Overlay
from PyQt6 import QtCore
import pyautogui
import threading
import time

class Controller(QtCore.QObject):
    gui_update_signal = QtCore.pyqtSignal()

    def __init__(self, model, view, config):
        super().__init__()
        self.model = model
        self.view = view
        self.config = config
        self.overlay = Overlay()
        self.input_listener = None

        self.gui_update_signal.connect(self.restore_window)

        self.view.repeat_toggle.setChecked(self.model.repeat)

        self.connect_signals()

    # Connect buttons to actions
    def connect_signals(self) -> None:
        self.view.click_button.clicked.connect(self.set_add_click)
        self.view.key_button.clicked.connect(self.set_add_key)

        self.view.clear.clicked.connect(self.clear_list)
        self.view.repeat_toggle.toggled.connect(self.on_toggle_repeat)
        self.view.submit.clicked.connect(self.start_execution)


    # Restore window after button behaviors complete
    def restore_window(self):
        self.view.log("Restoring Window", 'INFO')
        
        if hasattr(self, 'key_listener'):
            self.key_listener.join()

        self.view.bring_to_front()


# ------------------------------------------ Button Behaviors ------------------------------------------

# Run Button

    # Event to see if escape key has been pressed, Escape/Kill Switch for the execute function
    def check_escape(self, key: keyboard.Key) -> bool:
        try:
            self.view.log(f"Key pressed: {key}")
            if key == keyboard.Key.esc:
                self.view.log("ESC key pressed. Stopping listener.", 'INFO')
                self.model.stop()
                return False
            return True
        except Exception as e:
            self.view.log(f"Error: {e}" 'WARNING')


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
                    self.view.log(f"Error: {e}", 'WARNING')
                finally:
                    if self.model.is_stopped():
                        break
            if not self.model.repeat:
                self.model.stop()
        self.view.log("Command Execution Complete", 'INFO')


    # Start execution of commands when submit button is pressed
    def start_execution(self) -> None:
        try:
            self.input_listener = keyboard.Listener(on_press=self.check_escape)
            self.input_listener.start()
        except Exception as e:
            self.view.log(f'Keyboard Listener failed to start with exception: {e}', 'CRITICAL')

        self.view.showMinimized()

        automation_thread = threading.Thread(target=self.execute_commands, daemon=True)
        automation_thread.start()

        automation_thread.join()
        self.input_listener.stop()

        self.model.reset()
        self.gui_update_signal.emit()



# Add Click Button

    # Behavior for add click button
    def set_add_click(self) -> None:

        # Handle add click command
        def on_add_click(x:int, y:int, button: mouse.Button, pressed: bool) -> bool:
            try:
                if pressed and button == mouse.Button.left:
                    self.model.commands.append(['CLICK', x, y])
                    self.view.log(f"Click command added at: {x}, {y}", 'INFO')
            except Exception as e:
                self.view.log(f"Error: {e}", 'WARNING')
            
            self.overlay.hide()
            self.gui_update_signal.emit()
            self.view.log("Mouse Listener Closing", 'INFO')
            return False

        self.view.showMinimized()
        self.overlay.show_click_overlay()
        self.input_listener = mouse.Listener(on_click=on_add_click)
        self.input_listener.start()


# Add Key Button

    # Behavior for add key button
    def set_add_key(self) -> None:

        # Handle add press command
        def on_add_press(key: keyboard.Key) -> bool:
            try:
                self.view.log(f"Key pressed: {key.char}")
                self.model.commands.append(['PRESS', key.char])
                self.view.log(f"Press command added with letter {key.char}", 'INFO')
            except AttributeError:
                self.model.commands.append(['PRESS', str(key)])
                self.view.log(f"Press command added with letter {str(key)}", 'INFO')
            except Exception as e:
                self.view.log(f"Error: {e}", 'WARNING')

            self.overlay.hide()
            self.gui_update_signal.emit()
            self.view.log(f"Keyboard Listener Closing", 'INFO')
            return False
        
        self.view.showMinimized()
        self.overlay.show_press_overlay()
        self.input_listener = keyboard.Listener(on_press=on_add_press)
        self.input_listener.start()


# Clear Button

    # Clear the command list
    def clear_list(self) -> None:
        self.model.commands = []


# Repeat Toggle

    # Handle repeat toggle
    def on_toggle_repeat(self, checked: bool) -> None:
        self.model.repeat = checked


# Hold Key Toggle

    # Handle hold key toggle
    def on_toggle_hold(self, checked: bool) -> None:
        self.model.hold = checked