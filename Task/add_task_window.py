from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCalendarWidget, QCheckBox, QMessageBox
from PyQt5.QtCore import QDate
from Conn_bd import connect_to_database, agregar_tabla, agregar_tarea

class AddTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Agregar Tarea')
        self.setGeometry(200, 200, 300, 200)

        self.lbl_tarea = QLabel('Tarea:', self)
        self.txt_tarea = QLineEdit(self)

        self.lbl_estado = QLabel('Estado:', self)
        self.txt_estado = QCheckBox(self)

        self.lbl_fecha = QLabel('Fecha:', self)
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.show_date)

        btn_add_task = QPushButton('Agregar Tarea', self)
        btn_add_task.clicked.connect(self.confirm_and_add_task)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_tarea)
        layout.addWidget(self.txt_tarea)
        layout.addWidget(self.lbl_estado)
        layout.addWidget(self.txt_estado)
        layout.addWidget(self.lbl_fecha)
        layout.addWidget(self.calendar)
        layout.addWidget(btn_add_task)

        self.setLayout(layout)

        self.selected_date = None

    def show_date(self, date):
        self.selected_date = date.toString('yyyy-MM-dd')

    def confirm_and_add_task(self):
        # Mostrar un cuadro de diálogo de confirmación
        confirmation = QMessageBox.question(self, 'Confirmar',
                                           '¿Está seguro de los datos ingresados?',
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if confirmation == QMessageBox.Yes:
            # Datos confirmados, intentar agregar la tarea
            self.add_task()
            confirmation = QMessageBox.information(self, 'Tarea agregada', 'La tarea se agrego correctamente', QMessageBox.Ok)
        elif confirmation == QMessageBox.No:
            # El usuario rechazo la operación
            self.accept()
            confirmation = QMessageBox.information(self, 'Tarea no agregada', 'La tarea no se agrego', QMessageBox.Ok)

        elif confirmation == QMessageBox.Cancel:
            # El usuario canceló la operación
            self.reject()
            confirmation = QMessageBox.information(self, 'Tarea no agregada', 'Operacion cancelada', QMessageBox.Ok)
        else:
            # El usuario rechazo la operación
            self.reject()
            confirmation = QMessageBox.information(self, 'Tarea no agregada', 'Operación cancelada', QMessageBox.Retry)

    def add_task(self):
        nueva_tarea = {
            'tarea': self.txt_tarea.text(),
            'estado': self.txt_estado.isChecked(),
            'fecha_creacion': self.selected_date if self.selected_date else '2100-12-31'
        }

        db_connection = connect_to_database()
        if db_connection:
            try:
                agregar_tabla(db_connection)
                agregar_tarea(db_connection, nueva_tarea)
                self.close()
            except Exception as e:
                # Mostrar un cuadro de diálogo de error con el código de error
                QMessageBox.critical(self, 'Error al crear tarea', f'Error: {str(e)}', QMessageBox.Ok)
            finally:
                # Cerrar la conexión a la base de datos
                db_connection.close()
