from PyQt5.QtWidgets import QDialog, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from Conn_bd import connect_to_database, mostrar_usuarios

class ShowUserWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mostrar Usuarios")
        self.resize(600, 400)

        self.table_users = QTableWidget(self)
        self.table_users.setColumnCount(7)  # Ajusta esto al número de columnas en tu tabla de usuarios
        self.table_users.setHorizontalHeaderLabels(["ID", "Nombre", "Apellidos", "Email", "Rut", "Es Cliente", "Fecha de Nacimiento"])

        self.btn_close = QPushButton("Cerrar", self)
        self.btn_close.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_users)
        layout.addWidget(self.btn_close)

        self.load_users()

    def load_users(self):
        connection = connect_to_database()
        if connection:
            users = mostrar_usuarios(connection)

            if users:
                self.table_users.setRowCount(len(users))

                for row_index, user in enumerate(users):
                    for col_index, value in enumerate(user):
                        item = QTableWidgetItem(str(value))
                        self.table_users.setItem(row_index, col_index, item)
            else:
                print('No hay usuarios para mostrar.')

            connection.close()
