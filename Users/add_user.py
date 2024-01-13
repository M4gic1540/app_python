from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCalendarWidget, QCheckBox, QMessageBox
from PyQt5.QtCore import QDate
import mysql.connector
from Conn_bd import connect_to_database, crear_tabla_usuario, agregar_user
import argon2
from argon2 import PasswordHasher

class AddUserWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar usuario")
        self.resize(400, 300)

        self.lbl_name = QLabel("Nombre:", self)
        self.txt_name = QLineEdit(self)
        self.lbl_surname = QLabel("Apellidos:", self)
        self.txt_surname = QLineEdit(self)
        self.lbl_email = QLabel("Email:", self)
        self.txt_email = QLineEdit(self)
        self.lbl_rut = QLabel("Rut:", self)
        self.txt_rut = QLineEdit(self)
        self.txt_rut.setMaxLength(13)
        self.lbl_password = QLabel("Contraseña:", self)
        self.pwd_password = QLineEdit(self)
        self.lbl_is_client = QLabel("¿Es cliente?:", self)
        self.chk_is_client = QCheckBox(self)
        self.lbl_date = QLabel("Fecha de nacimiento:", self)
        self.calendar = QCalendarWidget(self)
        self.btn_save = QPushButton("Guardar", self)
        self.btn_save.clicked.connect(self.confirm_and_add_user)
        self.btn_cancel = QPushButton("Cancelar", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.txt_name)
        layout.addWidget(self.lbl_surname)
        layout.addWidget(self.txt_surname)
        layout.addWidget(self.lbl_email)
        layout.addWidget(self.txt_email)
        layout.addWidget(self.lbl_rut)
        layout.addWidget(self.txt_rut)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.pwd_password)
        layout.addWidget(self.lbl_is_client)
        layout.addWidget(self.chk_is_client)
        layout.addWidget(self.lbl_date)
        layout.addWidget(self.calendar)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_cancel)
        
    def confirm_and_add_user(self):
        # Llamando a la función add_user y agregando la lógica de confirmación o mensaje
        user_data = self.add_user()
        if not self.validate_rut(user_data['rut']):
            return

        confirmation = QMessageBox.question(self, 'Confirmación', '¿Está seguro de agregar este usuario?',
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            # Lógica para agregar el usuario a la base de datos
            connection = connect_to_database()
            if connection:
                crear_tabla_usuario(connection)
                agregar_user(connection, user_data)
                connection.close()
                QMessageBox.information(self, 'Usuario Agregado', 'El usuario se ha agregado correctamente.')
                self.close()  # Cerrar la ventana después de agregar el usuario
        else:
            # Puedes agregar más lógica si el usuario cancela la acción
            pass
    
    def add_user(self):
        name = self.txt_name.text()
        surname = self.txt_surname.text()
        email = self.txt_email.text()
        rut = self.txt_rut.text()
        password = self.pwd_password.text()
        is_client = self.chk_is_client.isChecked()
        date = self.calendar.selectedDate().toString('yyyy-MM-dd')

        # Hashear la contraseña usando Argon2
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        
        # Crear el diccionario del usuario
        user = {'nombre': name, 'apellidos': surname, 'email': email, 'rut': rut, 'es_cliente': is_client, 'fecha_nacimiento': date, 'password': hashed_password}
        return user



    def validate_rut(self, rut):
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM users WHERE rut = %s", (rut,))
                result = cursor.fetchone()
                if result and result[0] > 0:
                    QMessageBox.warning(self, 'Error', f'El rut ingresado "{rut}" ya se encuentra registrado.')
                    return False
                return True
            except mysql.connector.Error as e:
                print(f'Error al validar el rut: {e}')
            finally:
                cursor.close()
                connection.close()
        return False
