from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QComboBox, QCheckBox
from utils.assets_manager import get_asset_path
from config import CONFIG_STATE, save_config_state

class ConfigWindow(QMainWindow):
    closed = Signal()

    def __init__(self) -> None:
        super().__init__()


        self.setWindowTitle("Configuracion de Overlay Timer")
        self.setGeometry(0,0, 400, 600)
        self.setStyleSheet(" background-color:white;")

        self.overlay_position_label = QLabel("Posicion")
        # self.overlay_position_label.setStyleSheet("font-weight: 600;color: #4d4d4d;")
        # self.overlay_position_label.setAlignment(Qt.AlignCenter)



        # Crear un QComboBox
        self.overlay_position_box = QComboBox()

        # self.overlay_position_box.setStyleSheet("""
        #     QComboBox {
        #         color: #424242;
        #         background-color:transparent;
        #         padding: 8px 7px; /* Padding interno del QComboBox */
        #         border: 1px solid #b3b3b3; /* Opcional: agregar un borde */
        #         border-radius: 10px;
        #     }
        #     QComboBox::drop-down {
        #         border: 0; /* Borde de la parte desplegable */

        #     }
        #     QComboBox QAbstractItemView {
        #         border: 1px solid #ccc; /* Borde del popup */
        #         background-color: #FFF; /* Fondo del popup */
        #         selection-background-color: #0078D4; /* Fondo de la opción seleccionada en el popup */
        #         selection-color: white; /* Color del texto de la opción seleccionada en el popup */
        #         border-radius: 10px;
        #     }
        #     QComboBox QAbstractItemView::item {
        #         padding: 5px; /* Padding interno de los items en el popup */
        #     }
        # """)
        # Agregar opciones al QComboBox
        self.overlay_position_box.addItem("Superior Derecha")
        self.overlay_position_box.addItem("Superior Izquierda")
        self.overlay_position_box.addItem("Superior Centro")

        self.check_box = QCheckBox("Mostrar overlay al iniciar")
        self.check_box.setChecked(CONFIG_STATE.overlay_config.show_at_start)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.overlay_position_label)
        layout.addWidget(self.overlay_position_box)
        layout.addWidget(self.check_box)

        self.setWindowIcon(QIcon(get_asset_path('timer_512_512.png')))
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.check_box.checkStateChanged.connect(self.handle_check_box)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.closed.emit()
        super().closeEvent(event)


    def handle_check_box(self, data: Qt.CheckState):
        if data == Qt.CheckState.Checked:
            CONFIG_STATE.overlay_config.show_at_start = True
        elif data == Qt.CheckState.Unchecked:
            CONFIG_STATE.overlay_config.show_at_start = False
        save_config_state()

