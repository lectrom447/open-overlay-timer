from PySide6.QtCore import Qt
from PySide6.QtWidgets import  QLabel, QWidget, QVBoxLayout
from utils.timer import TimerThread
from config import CONFIG_STATE

class TimerOverlay(QWidget):
    elapse_time = 0
    timer_running = False
    timer_thread: TimerThread | None = None

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(CONFIG_STATE.overlay_config.position_x, CONFIG_STATE.overlay_config.position_y, 300, 100)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.__position_locked = True
        # self.setStyleSheet("padding: 5px;")

        self.label = QLabel("00:00", self)
        self.label.setStyleSheet("color: white; font-size: 40pt;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, 200, 50)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.adjustSize()

    
    def mousePressEvent(self, event):
        if self.__position_locked: return
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.__position_locked: return
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()
        CONFIG_STATE.overlay_config.position_x = self.x()
        CONFIG_STATE.overlay_config.position_y = self.y()


    def safe_destroy(self):
        if self.timer_running:
            self.timer_running = False
            # self.timer_thread.join()
        self.destroy()


    def __update_label(self, text: str):
        self.label.setText(text)
        self.label.repaint()

    # Overlay Controls
    def lock_position(self):
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.__position_locked = True


    def unlock_position(self):
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        self.__position_locked = False

    # Timer Controls
    def start_timer(self):
        if self.timer_running: return
        self.timer_running = True
        self.timer_thread = TimerThread(self.label.text())
        self.timer_thread.start()
        self.timer_thread.time_changed.connect(self.__update_label)


    def stop_timer(self):
        if not self.timer_running: return
        self.timer_running = False
        self.timer_thread.stop()

    def toggle_timer(self):
        if self.timer_running:
            return self.stop_timer()

        self.start_timer()


    def reset_timer():
        print("Timer started")

    