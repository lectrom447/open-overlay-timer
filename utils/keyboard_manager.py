from PySide6.QtCore import  QThread, Signal
from pynput import keyboard

class KeyboardEventManagerThread(QThread):

    show_config_window_signal = Signal()
    toggle_overlay_signal = Signal()
    toggle_timer_signal = Signal()
    drag_overlay_started = Signal()
    drag_overlay_finished = Signal()

    def __init__(self) -> None:
        self.__keyboard_listener: keyboard.Listener | None = None
        super().__init__()

    def run(self):
        self.__keyboard_listener = keyboard.Listener(self.handle_key_press, self.handle_key_release)
        self.__keyboard_listener.start()
        self.__keyboard_listener.join()


    def stop(self):
        if not self.__keyboard_listener.is_alive(): return
        self.__keyboard_listener.stop()
        self.wait()

    def handle_key_press(self, key: keyboard.Key | keyboard.KeyCode):
        if key == keyboard.KeyCode.from_char('t'):
            self.toggle_overlay_signal.emit()
        elif key == keyboard.KeyCode.from_char('p'):
            self.toggle_timer_signal.emit()
        elif key == keyboard.KeyCode.from_char('.'):
            self.drag_overlay_started.emit()

    def handle_key_release(self, key: keyboard.Key | keyboard.KeyCode):
        if key == keyboard.KeyCode.from_char('.'):
            self.drag_overlay_finished.emit()