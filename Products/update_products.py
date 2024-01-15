from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCalendarWidget, QMessageBox
from Conn_bd import connect_to_database, actualizar_productos
from PyQt5.QtCore import QDate
import mysql.connector

class UpdateProductsWindow(QDialog):
    def __init__(self, product_id):
        super().__init__()

        self.product_id = product_id

        self.setWindowTitle("Actualizar Producto")
        self.resize(400, 300)

        self.lbl_name = QLabel("Nombre Producto:", self)
        self.txt_name = QLineEdit(self)
        self.lbl_price = QLabel("Precio:", self)
        self.txt_price = QLineEdit(self)
        self.lbl_stock = QLabel("Stock:", self)
        self.txt_stock = QLineEdit(self)
        self.lbl_provider = QLabel("Proveedor:", self)
        self.txt_provider = QLineEdit(self)
        self.lbl_date_elab = QLabel("Fecha de Elaboración:", self)
        self.calendar_elab = QCalendarWidget(self)
        self.lbl_date_venc = QLabel("Fecha de Vencimiento:", self)
        self.calendar_venc = QCalendarWidget(self)
        self.btn_update = QPushButton("Actualizar", self)
        self.btn_update.clicked.connect(self.confirm_and_update)
        self.btn_cancel = QPushButton("Cancelar", self)
        self.btn_cancel.clicked.connect(self.close)

        layout = QVBoxLayout(self)
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
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_cancel)

        self.load_product_data()

    def load_product_data(self):
        # Obtener los datos actuales del producto
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM productos WHERE id = %s', (self.product_id,))
                product_data = cursor.fetchone()

                if product_data:
                    self.txt_name.setText(str(product_data[1]))
                    self.txt_price.setText(str(product_data[2]))
                    self.txt_stock.setText(str(product_data[3]))
                    self.txt_provider.setText(str(product_data[4]))

                    elab_date = product_data[5]
                    self.calendar_elab.setSelectedDate(QDate.fromString(elab_date, 'yyyy-MM-dd'))

                    venc_date = product_data[6]
                    self.calendar_venc.setSelectedDate(QDate.fromString(venc_date, 'yyyy-MM-dd'))

                else:
                    print('Producto no encontrado.')

            except mysql.connector.Error as e:
                print(f'Error al cargar datos del producto: {e}')
            finally:
                cursor.close()
                connection.close()

    def confirm_and_update(self):
        # Llamando a la función actualizar_productos y agregando la lógica de confirmación o mensaje
        name = self.txt_name.text()
        price = self.txt_price.text()
        stock = self.txt_stock.text()
        provider = self.txt_provider.text()
        elab_date = self.calendar_elab.selectedDate().toString('yyyy-MM-dd')
        venc_date = self.calendar_venc.selectedDate().toString('yyyy-MM-dd')

        confirmation = QMessageBox.question(self, 'Confirmación', '¿Está seguro de actualizar este producto?',
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            # Lógica para actualizar el producto en la base de datos
            connection = connect_to_database()
            if connection:
                actualizar_productos(connection, self.product_id, name, price, stock, provider, elab_date, venc_date)
                connection.close()
                QMessageBox.information(self, 'Producto Actualizado', 'El producto se ha actualizado correctamente.')
                self.close()  # Cerrar la ventana después de actualizar el producto
        else:
            # Puedes agregar más lógica si el usuario cancela la acción
            pass
