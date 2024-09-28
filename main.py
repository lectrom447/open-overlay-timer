import sys
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PySide6.QtGui import QIcon, QAction
from utils.assets_manager import get_asset_path
from utils.keyboard_manager import KeyboardEventManagerThread
from views.timer_overlay import TimerOverlay
from views.config_window import ConfigWindow
from config import CONFIG_STATE,save_config_state, load_config_state
    

class OverlayTimer(QApplication):
    def __init__(self):
        super().__init__()
        self.setQuitOnLastWindowClosed(False)


        load_config_state()
        self.configuration_window: ConfigWindow | None = None
        self.timer_overlay: TimerOverlay | None = None

        self.keyboard_event_manager_thread = KeyboardEventManagerThread()
        self.keyboard_event_manager_thread.start()
        self.keyboard_event_manager_thread.toggle_overlay_signal.connect(self.toggle_timer_overlay)
        self.keyboard_event_manager_thread.toggle_timer_signal.connect(self.toggle_timmer)
        self.keyboard_event_manager_thread.drag_overlay_started.connect(self.handle_drag_overlay_start)
        self.keyboard_event_manager_thread.drag_overlay_finished.connect(self.handle_drag_overlay_stop)

    # Timer Overlay Controls
    def show_timer_overlay(self):
        if not self.timer_overlay:
            self.timer_overlay = TimerOverlay()
        self.timer_overlay.show()

    def close_timer_overlay(self):
        if not self.timer_overlay: return
        self.timer_overlay.safe_destroy()
        self.timer_overlay = None

    def toggle_timer_overlay(self):
        if not self.timer_overlay:
            return self.show_timer_overlay()
        self.close_timer_overlay()

    def toggle_timmer(self):
        if not self.timer_overlay: return
        self.timer_overlay.toggle_timer()

    def handle_drag_overlay_start(self):
        if not self.timer_overlay: return
        self.timer_overlay.unlock_position()

    def handle_drag_overlay_stop(self):
        if not self.timer_overlay: return
        self.timer_overlay.lock_position()
        save_config_state()


    # Configuration Window Controls
    def open_configuration_window(self):
        if not self.configuration_window:
            self.configuration_window = ConfigWindow()
            self.configuration_window.closed.connect(self.close_configuration_window)
        self.configuration_window.show()


    def close_configuration_window(self):
        self.configuration_window = None


    def start_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(QIcon(get_asset_path('timer_16_16.png')), self)
        self.tray_icon.setToolTip("Overlay Timer")
        self.tray_icon.activated.connect(self.handle_tray_icon_click)
        self.tray_menu = QMenu()

        self.quit_action = QAction("Salir")
        self.quit_action.triggered.connect(self.close)
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def handle_tray_icon_click(self, reason:QSystemTrayIcon.ActivationReason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.open_configuration_window()

    def close(self):
        self.keyboard_event_manager_thread.stop()
        self.close_timer_overlay()
        self.quit()

    def run(self):
        self.start_tray_icon()

        if CONFIG_STATE.overlay_config.show_at_start:
            self.show_timer_overlay()
        sys.exit(self.exec())

if __name__ == "__main__":
    app = OverlayTimer()
    app.run()

