from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QVBoxLayout, QCheckBox, QCalendarWidget, QDialog

# Importar las funciones de Conn_bd.py
from Conn_bd import connect_to_database, actualizar_usuario

class UpdateUserWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Actualizar usuario')
        self.setGeometry(200, 200, 300, 200)

        # Etiquetas y campos de entrada para actualizar la tarea
        self.lbl_id = QLabel('ID de usuario a Actualizar:', self)
        self.txt_id = QLineEdit(self)

        self.lbl_nombre = QLabel('ingrese el Nuevo nombre:', self)
        self.txt_nombre = QLineEdit(self)

        self.lbl_apellido = QLabel('ingrese el Nuevo apellido:', self)
        self.txt_apellido = QLineEdit(self)

        self.lbl_email = QLabel('ingrese el Nuevo email:', self)
        self.txt_email = QLineEdit(self)

        self.lbl_rut = QLabel('ingrese el Nuevo rut:', self)
        self.txt_rut = QLineEdit(self)

        self.lbl_es_cliente = QLabel('es cliente?', self)
        self.txt_es_cliente = QCheckBox(self)

        self.lbl_fecha = QLabel('Fecha:', self)
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        # Botón para actualizar tarea
        btn_update_user = QPushButton('Actualizar usuario', self)
        btn_update_user.clicked.connect(self.update_user)

        # Diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_nombre)
        layout.addWidget(self.txt_nombre)
        layout.addWidget(self.lbl_apellido)
        layout.addWidget(self.txt_apellido)
        layout.addWidget(self.lbl_email)
        layout.addWidget(self.txt_email)
        layout.addWidget(self.lbl_rut)
        layout.addWidget(self.txt_rut)
        layout.addWidget(self.lbl_es_cliente)
        layout.addWidget(self.txt_es_cliente)
        layout.addWidget(self.lbl_fecha)
        layout.addWidget(self.calendar)
        layout.addWidget(btn_update_user)

        self.setLayout(layout)

        self.selected_date = None


    def show_date(self, date):
            self.selected_date = date.toString('yyyy-MM-dd')

    def update_user(self):
        # Obtener la información ingresada por el usuario para actualizar la tarea
        user_id = self.txt_id.text()
        nombre = self.txt_nombre.text()
        apellido = self.txt_apellido.text()
        email = self.txt_email.text()
        rut = self.txt_rut.text()
        es_cliente = self.txt_es_cliente.isChecked()
        fecha_nacimiento = self.calendar.selectedDate().toString('yyyy-MM-dd')

        # Realizar la conexión a la base de datos y actualizar la tarea
        db_connection = connect_to_database()
        if db_connection:
            actualizar_usuario(db_connection, user_id, nombre, apellido, email, rut, es_cliente, fecha_nacimiento)
            self.close()

        db_connection.close()