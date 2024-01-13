from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCalendarWidget, QCheckBox
from PyQt5.QtCore import QDate
from Conn_bd import connect_to_database, borrar_tarea


class EraseTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Eliminar Tarea')
        self.setGeometry(100, 100, 300, 200)

        self.lbl_id = QLabel('Ingrese ID:' , self)
        self.txt_id = QLineEdit(self)

        btn_erase_task = QPushButton('Eliminar Tarea', self)
        btn_erase_task.clicked.connect(self.erase_task)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(btn_erase_task)

        self.setLayout(layout)

    def erase_task(self):
        conn = connect_to_database()
        if conn:
            borrar_tarea(conn, self.txt_id.text())
            self.close()