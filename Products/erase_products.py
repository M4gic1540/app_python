from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCalendarWidget, QCheckBox
from PyQt5.QtCore import QDate
from Conn_bd import connect_to_database, borrar_productos


class EraseProductsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Eliminar Producto')
        self.setGeometry(100, 100, 300, 200)

        self.lbl_id = QLabel('id de producto:' , self)
        self.txt_id = QLineEdit(self)

        btn_erase_product = QPushButton('Eliminar Producto', self)
        btn_erase_product.clicked.connect(self.erase_product)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(btn_erase_product)

        self.setLayout(layout)

    def erase_product(self):
        conn = connect_to_database()
        if conn:
            borrar_productos(conn, self.txt_id.text())
            self.close()
        else:
            print('Error de conexión a la base de datos')


        