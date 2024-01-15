from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from Conn_bd import connect_to_database, mostrar_productos

class ShowProductsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mostrar Productos")
        self.resize(800, 600)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)  # Ajusta el número de columnas según tus campos
        self.table_widget.setHorizontalHeaderLabels(
            ["ID", "Nombre Producto", "Precio", "Stock", "Proveedor", "Fecha de Elaboración", "Fecha de Vencimiento"]
        )

        self.refresh_button = QPushButton("Actualizar", self)
        self.refresh_button.clicked.connect(self.refresh_products)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.refresh_button)

        self.refresh_products()

    def refresh_products(self):
        # Obtener la lista de productos de la base de datos
        connection = connect_to_database()
        if connection:
            productos = mostrar_productos(connection)

            if productos:
                self.table_widget.setRowCount(len(productos))

                for row_index, product in enumerate(productos):
                    for col_index, value in enumerate(product):
                        item = QTableWidgetItem(str(value))
                        self.table_widget.setItem(row_index, col_index, item)
            else:
                print('No hay productos para mostrar.')

            connection.close()
