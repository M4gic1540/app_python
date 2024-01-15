from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCalendarWidget, QMessageBox
from PyQt5.QtCore import QDate
from Conn_bd import connect_to_database, crear_tabla_productos, agregar_productos

class AddProductWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar Producto")
        self.resize(400, 300)

        self.lbl_name = QLabel("Nombre del Producto:", self)
        self.txt_name = QLineEdit(self)
        self.lbl_price = QLabel("Precio:", self)
        self.txt_price = QLineEdit(self)
        self.lbl_stock = QLabel("Stock:", self)
        self.txt_stock = QLineEdit(self)
        self.lbl_supplier = QLabel("Proveedor:", self)
        self.txt_supplier = QLineEdit(self)
        self.lbl_date_elab = QLabel("Fecha de Elaboración:", self)
        self.calendar_elab = QCalendarWidget(self)
        self.lbl_date_venc = QLabel("Fecha de Vencimiento:", self)
        self.calendar_venc = QCalendarWidget(self)
        self.btn_save = QPushButton("Guardar", self)
        self.btn_save.clicked.connect(self.confirm_and_add_product)
        self.btn_cancel = QPushButton("Cancelar", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.txt_name)
        layout.addWidget(self.lbl_price)
        layout.addWidget(self.txt_price)
        layout.addWidget(self.lbl_stock)
        layout.addWidget(self.txt_stock)
        layout.addWidget(self.lbl_supplier)
        layout.addWidget(self.txt_supplier)
        layout.addWidget(self.lbl_date_elab)
        layout.addWidget(self.calendar_elab)
        layout.addWidget(self.lbl_date_venc)
        layout.addWidget(self.calendar_venc)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_cancel)

    def confirm_and_add_product(self):
        # Llamando a la función agregar_productos y agregando la lógica de confirmación o mensaje
        product_data = self.add_product()
        confirmation = QMessageBox.question(self, 'Confirmación', '¿Está seguro de agregar este producto?',
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            # Lógica para agregar el producto a la base de datos
            connection = connect_to_database()
            if connection:
                crear_tabla_productos(connection)
                agregar_productos(connection, **product_data)
                connection.close()
                QMessageBox.information(self, 'Producto Agregado', 'El producto se ha agregado correctamente.')
                self.close()  # Cerrar la ventana después de agregar el producto
        else:
            # Puedes agregar más lógica si el usuario cancela la acción
            pass
    
    def add_product(self):
        name = self.txt_name.text()
        price = float(self.txt_price.text()) if self.txt_price.text() else 0.0
        stock = int(self.txt_stock.text()) if self.txt_stock.text() else 0
        supplier = self.txt_supplier.text()
        date_elab = self.calendar_elab.selectedDate().toString('yyyy-MM-dd')
        date_venc = self.calendar_venc.selectedDate().toString('yyyy-MM-dd')

        # Crear el diccionario del producto
        product = {'nombre_producto': name, 'precio': price, 'stock': stock, 'proveedor': supplier, 'fecha_elab': date_elab, 'fecha_venc': date_venc}
        return product
