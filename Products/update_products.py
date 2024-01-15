from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QVBoxLayout, QCalendarWidget, QDialog
from Conn_bd import connect_to_database, actualizar_productos


class UpdateProductsWindow(QDialog):
    def __init__(self, product_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Actualizar Producto')
        self.setGeometry(200, 200, 400, 300)

        # Etiquetas y campos de entrada para actualizar el producto
        self.lbl_id = QLabel('ID del Producto a Actualizar:', self)
        self.txt_id = QLineEdit(self)

        self.lbl_name = QLabel('Ingrese el Nuevo Nombre:', self)
        self.txt_name = QLineEdit(self)

        self.lbl_price = QLabel('Ingrese el Nuevo Precio:', self)
        self.txt_price = QLineEdit(self)

        self.lbl_stock = QLabel('Ingrese el Nuevo Stock:', self)
        self.txt_stock = QLineEdit(self)

        self.lbl_provider = QLabel('Ingrese el Nuevo Proveedor:', self)
        self.txt_provider = QLineEdit(self)

        self.lbl_date_elab = QLabel('Fecha de Elaboración:', self)
        self.calendar_elab = QCalendarWidget(self)
        self.calendar_elab.setGridVisible(True)

        self.lbl_date_venc = QLabel('Fecha de vencimiento:', self)
        self.calendar_venc = QCalendarWidget(self)
        self.calendar_venc.setGridVisible(True)

        # Botón para actualizar producto
        btn_update_product = QPushButton('Actualizar Producto', self)
        btn_update_product.clicked.connect(self.update_product)

        # Diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.txt_name)
        layout.addWidget(self.lbl_price)
        layout.addWidget(self.txt_price)
        layout.addWidget(self.lbl_stock)
        layout.addWidget(self.txt_stock)
        layout.addWidget(self.lbl_provider)
        layout.addWidget(self.txt_provider)
        layout.addWidget(self.lbl_date_elab)
        layout.addWidget(self.calendar_elab)
        layout.addWidget(self.lbl_date_venc)
        layout.addWidget(self.calendar_venc)
        layout.addWidget(btn_update_product)

        self.setLayout(layout)

        self.selected_date_elab = None
        self.selected_date_venc = None

    def show_date_elab(self, date):
        self.selected_date_elab = date.toString('yyyy-MM-dd')

    def show_date_venc(self, date):
        self.selected_date_venc = date.toString('yyyy-MM-dd')

    def update_product(self):
        # Obtener la información ingresada por el usuario para actualizar el producto
        product_id_text = self.txt_id.text()
        
        # Verificar si el contenido de txt_id es un valor numérico
        if not product_id_text.isdigit():
            print('El ID del producto debe ser un número válido.')
            return
        
        product_id = int(product_id_text)  # Convertir el valor del campo txt_id a un entero
        name = self.txt_name.text()
        price = float(self.txt_price.text())
        stock = self.txt_stock.text()
        provider = self.txt_provider.text()
        elab_date = self.calendar_elab.selectedDate().toString('yyyy-MM-dd')
        venc_date = self.calendar_venc.selectedDate().toString('yyyy-MM-dd')

        # Realizar la conexión a la base de datos y actualizar el producto
        db_connection = connect_to_database()
        if db_connection:
            actualizar_productos(
                db_connection, product_id, name, price, stock, provider, elab_date, venc_date)
            self.close()

        db_connection.close()

