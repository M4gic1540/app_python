import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QCheckBox, QCalendarWidget, QDialog

# Importar las funciones de Conn_bd.py
from Conn_bd import connect_to_database, actualizar_tarea

class UpdateTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Actualizar Tarea')
        self.setGeometry(200, 200, 300, 200)

        # Etiquetas y campos de entrada para actualizar la tarea
        self.lbl_id = QLabel('ID de Tarea a Actualizar:', self)
        self.txt_id = QLineEdit(self)

        self.lbl_tarea = QLabel('Nueva Tarea:', self)
        self.txt_tarea = QLineEdit(self)

        self.lbl_estado = QLabel('Estado de la Tarea:', self)
        self.txt_estado = QCheckBox(self)

        # Botón para actualizar tarea
        btn_update_task = QPushButton('Actualizar Tarea', self)
        btn_update_task.clicked.connect(self.update_task)

        # Diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_tarea)
        layout.addWidget(self.txt_tarea)
        layout.addWidget(self.lbl_estado)  # Etiqueta para el estado de la tarea
        layout.addWidget(self.txt_estado)  # Checkbox para el estado de la tarea
        layout.addWidget(btn_update_task)

        self.setLayout(layout)

    def update_task(self):
        # Obtener la información ingresada por el usuario para actualizar la tarea
        tarea_id = self.txt_id.text()
        nueva_tarea = self.txt_tarea.text()
        estado = self.txt_estado.isChecked()

        # Realizar la conexión a la base de datos y actualizar la tarea
        db_connection = connect_to_database()
        if db_connection:
            actualizar_tarea(db_connection, tarea_id, nueva_tarea, estado)
            self.close()

        db_connection.close()