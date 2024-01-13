from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QCheckBox, QTableWidget, QTableWidgetItem, QCalendarWidget, QMessageBox
from Conn_bd import connect_to_database, filtrar_tareas

# ... (importaciones anteriores)

class FilterTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Filtrar Tareas')
        self.setGeometry(200, 200, 500, 200)

        # Widgets para la interfaz de filtrado
        self.id_checkbox = QCheckBox('Filtrar por ID')
        self.id_input = QLineEdit()

        self.nombre_checkbox = QCheckBox('Filtrar por Nombre de Tarea')
        self.nombre_input = QLineEdit()

        self.estado_checkbox = QCheckBox('Filtrar por Estado')
        self.estado_input = QLineEdit()

        self.calendar_checkbox = QCheckBox('Filtrar por Fecha')
        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.show_date)
        self.calendar.setGridVisible(True)

        self.filter_button = QPushButton('Filtrar')
        self.filter_button.clicked.connect(self.filter_tasks)

        # Widget para mostrar las tareas filtradas
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Tarea", "Estado", "Fecha de Creación"])

        # Layout para organizar los widgets
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        form_layout.addRow(self.id_checkbox, self.id_input)
        form_layout.addRow(self.nombre_checkbox, self.nombre_input)
        form_layout.addRow(self.estado_checkbox, self.estado_input)
        form_layout.addRow(self.calendar_checkbox, self.calendar)
        form_layout.addRow(self.filter_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

    def filter_tasks(self):
        # Obtener la conexión a la base de datos
        connection = connect_to_database()

        # Verificar si la conexión es válida
        if connection:
            # Ejemplo básico de cómo obtener los valores
            tarea_id = self.id_input.text() if self.id_checkbox.isChecked() else None
            tarea_nombre = self.nombre_input.text() if self.nombre_checkbox.isChecked() else None
            estado = self.estado_input.text() if self.estado_checkbox.isChecked() else None
            fecha_creacion = self.calendar.selectedDate().toString('yyyy-MM-dd') if self.calendar_checkbox.isChecked() else None

            # Llamar a la función de filtrado con los parámetros obtenidos
            tareas_filtradas = filtrar_tareas(connection, tarea_id=tarea_id, tarea_nombre=tarea_nombre, estado=estado, fecha_creacion=fecha_creacion)

            # Llenar la tabla con las tareas filtradas
            self.show_filtered_tasks(tareas_filtradas)

            # Cerrar la conexión a la base de datos
            connection.close()

    def show_filtered_tasks(self, tasks):
        # Limpiar la tabla antes de agregar nuevas filas
        self.table_widget.setRowCount(0)

        # Verificar si hay tareas filtradas
        if tasks:
            # Llenar la tabla con las tareas filtradas
            for row, tarea in enumerate(tasks):
                self.table_widget.insertRow(row)
                for col, value in enumerate(tarea):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(row, col, item)
        else:
            # Mostrar un mensaje si no hay tareas filtradas
            QMessageBox.information(self, 'Sin Tareas', 'No se encontraron tareas para los criterios seleccionados.')

    def show_date(self, date):
        # Este método mostrará la fecha seleccionada en el calendario.
        # Puedes personalizar su lógica según tus necesidades.
        print("Fecha seleccionada:", date.toString('dd-MM-yyyy'))

        # self.accept()  # Puedes decidir si cerrar la ventana aquí o no
