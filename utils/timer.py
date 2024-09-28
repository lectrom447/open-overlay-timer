import time
from PySide6.QtCore import QThread, Signal


class TimerThread(QThread):
    time_changed = Signal(str)

    def __init__(self, start_at: str = None) -> None:
        super().__init__()
        self.timer_running = False
        self.elapse_time = self.__get_elapse_time(start_at) if start_at else 0

    def run(self) -> None:
        self.timer_running = True
        while self.timer_running:
            time.sleep(0.1)
            self.elapse_time += 1

            if (self.elapse_time % 10) == 0:
                self.time_changed.emit(self.__get_elapse_time_str())
            
    def __get_elapse_time_str(self) -> str:
        elapsed_seconds = self.elapse_time // 10

        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60

        return f"{minutes:02}:{seconds:02}"

    def __get_elapse_time(self, time: str):
        minutos_str, segundos_str = time.split(":") 
        minutos = int(minutos_str)
        segundos = int(segundos_str) + (minutos * 60)

        return segundos * 10
        

    def stop(self) -> None:
        self.timer_running = False
        self.wait()