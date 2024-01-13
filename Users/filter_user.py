from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QCheckBox, QTableWidget, QTableWidgetItem, QCalendarWidget, QMessageBox
from Conn_bd import connect_to_database, filtrar_usuarios

# ... (importaciones anteriores)


class FilterUserWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Filtrar Usuarios')
        self.setGeometry(200, 200, 800, 600)

        # Widgets para la interfaz de filtrado
        self.id_checkbox = QCheckBox('Filtrar por ID')
        self.id_input = QLineEdit()

        self.nombre_checkbox = QCheckBox('Filtrar por Nombre')
        self.nombre_input = QLineEdit()

        self.apellido_checkbox = QCheckBox('Filtrar por Apellido')
        self.apellido_input = QLineEdit()

        self.email_checkbox = QCheckBox('Filtrar por Email')
        self.email_input = QLineEdit()

        self.rut_checkbox = QCheckBox('Filtrar por Rut')
        self.rut_input = QLineEdit()

        self.cliente_checkbox = QCheckBox('Filtrar por Cliente')
        self.cliente_input = QLineEdit()

        self.calendar_checkbox = QCheckBox('Filtrar por Fecha de Nacimiento')
        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.show_date)
        self.calendar.setGridVisible(True)

        self.filter_button = QPushButton('Filtrar')
        self.filter_button.clicked.connect(self.filter_user)

        # Widget para mostrar las tareas filtradas
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Apellidos", "Email", "Rut", "Cliente", "Fecha de Nacimiento"])

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.addWidget(self.id_checkbox)
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.nombre_checkbox)
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.apellido_checkbox)
        form_layout.addWidget(self.apellido_input)
        form_layout.addWidget(self.email_checkbox)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.rut_checkbox)
        form_layout.addWidget(self.rut_input)
        form_layout.addWidget(self.cliente_checkbox)
        form_layout.addWidget(self.cliente_input)
        form_layout.addWidget(self.calendar_checkbox)
        form_layout.addWidget(self.calendar)

        layout.addLayout(form_layout)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

    def filter_user(self):
        # Obtener los valores de los checkboxes
        connection = connect_to_database()

        if connection:
            user_id = self.id_input.text() if self.id_checkbox.isChecked() else None
            user_name = self.nombre_input.text() if self.nombre_checkbox.isChecked() else None
            user_last_name = self.apellido_input.text(
            ) if self.apellido_checkbox.isChecked() else None
            user_email = self.email_input.text() if self.email_checkbox.isChecked() else None
            user_rut = self.rut_input.text() if self.rut_checkbox.isChecked() else None
            user_client = self.cliente_input.text() if self.cliente_checkbox.isChecked() else None
            user_birthday = self.calendar.selectedDate().toString(
                'yyyy-MM-dd') if self.calendar_checkbox.isChecked() else None

            users = filtrar_usuarios(connection, user_id, user_name, user_last_name,
                                     user_email, user_rut, user_client, user_birthday)

            if users:
                self.table_widget.setRowCount(len(users))

                for row_index, user in enumerate(users):
                    for col_index, value in enumerate(user):
                        item = QTableWidgetItem(str(value))
                        self.table_widget.setItem(row_index, col_index, item)
            else:
                print('No hay usuarios para mostrar.')

            connection.close()

    def show_filtered_users(self, users):
        # Limpia la tabla antes de mostrar nuevos resultados
        self.table_widget.setRowCount()

        # Muestra los usuarios en la tabla
        if users:
            self.table_widget.setRowCount(len(users))

            for row_index, user in enumerate(users):
                for col_index, value in enumerate(user):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(row_index, col_index, item)
        else:
            print('No hay usuarios para mostrar.')

    def show_date(self, date):
        # Este método mostrará la fecha seleccionada en el calendario.
        # Puedes personalizar su lógica según tus necesidades.
        print("Fecha seleccionada:", date.toString('dd-MM-yyyy'))

        # self.accept()  # Puedes decidir si cerrar la ventana aquí o no
