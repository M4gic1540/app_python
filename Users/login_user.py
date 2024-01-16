from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from Conn_bd import connect_to_database
import mysql.connector
from argon2 import PasswordHasher

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inicio de Sesión")
        self.resize(300, 150)

        self.lbl_rut = QLabel("Ingrese RUT de trabajador:", self)
        self.txt_rut = QLineEdit(self)
        self.lbl_password = QLabel("Contraseña:", self)
        self.pwd_password = QLineEdit(self)
        self.pwd_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Iniciar Sesión", self)
        self.btn_login.clicked.connect(self.try_login)

        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl_rut)
        layout.addWidget(self.txt_rut)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.pwd_password)
        layout.addWidget(self.btn_login)

        self.ph = PasswordHasher()

    def try_login(self):
        # Lógica para verificar las credenciales
        rut = self.txt_rut.text()
        password = self.pwd_password.text()

        # Mensajes de depuración
        print(f'RUT ingresado: {rut}')

        # Aquí debes verificar las credenciales con tu lógica específica
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT password, es_cliente FROM users WHERE rut = %s", (rut,))
                result = cursor.fetchone()

                if result:
                    hashed_password, es_cliente = result
                    print(f'Hash almacenado en la base de datos: {hashed_password}')

                    if self.ph.verify(hashed_password, password):
                        if not es_cliente:
                            print('Credenciales correctas bienvenido a la aplicación')
                            self.accept()
                        else:
                            print('Usuario es cliente, no permitido')
                            QMessageBox.warning(self, 'Error de inicio de sesión', 'Solo los administradores pueden ingresar.')
                    else:
                        print('Credenciales incorrectas')
                        QMessageBox.warning(self, 'Error de inicio de sesión', 'Credenciales incorrectas.')
                else:
                    print('Usuario no encontrado')
                    QMessageBox.warning(self, 'Error de inicio de sesión', 'Usuario no encontrado.')
            except mysql.connector.Error as e:
                print(f'Error al verificar las credenciales: {e}')
            except Exception as ex:
                print(f'Otro error: {ex}')
            finally:
                cursor.close()
                connection.close()
