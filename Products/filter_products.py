from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QVBoxLayout, QCalendarWidget, QTableWidget, \
                            QTableWidgetItem, QCheckBox, QDialog
from Conn_bd import connect_to_database, filtrar_productos

class FilterProductsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Filtrar Productos')
        self.setGeometry(100, 100, 800, 600)

        # Etiquetas y campos de entrada para filtrar productos
        self.lbl_nombre_producto = QLabel('Nombre del Producto:', self)
        self.txt_nombre_producto = QLineEdit(self)
        self.chk_nombre_producto = QCheckBox("Filtrar por Nombre", self)

        self.lbl_proveedor = QLabel('Proveedor:', self)
        self.txt_proveedor = QLineEdit(self)
        self.chk_proveedor = QCheckBox("Filtrar por Proveedor", self)

        self.lbl_fecha_elab = QLabel('Fecha de Elaboración:', self)
        self.calendar_elab = QCalendarWidget(self)
        self.chk_fecha_elab = QCheckBox("Filtrar por Fecha de Elaboración", self)

        self.lbl_fecha_venc = QLabel('Fecha de Vencimiento:', self)
        self.calendar_venc = QCalendarWidget(self)
        self.chk_fecha_venc = QCheckBox("Filtrar por Fecha de Vencimiento", self)

        # Botón para realizar el filtrado de productos
        btn_filter_products = QPushButton('Filtrar Productos', self)
        btn_filter_products.clicked.connect(self.filter_products)

        # Tabla para mostrar los resultados
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(7)  # Ajusta el número de columnas según tu estructura de datos
        self.table_widget.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Stock", "Proveedor", "Fecha Elab", "Fecha Venc"])

        # Diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.chk_nombre_producto)
        layout.addWidget(self.lbl_nombre_producto)
        layout.addWidget(self.txt_nombre_producto)
        layout.addWidget(self.chk_proveedor)
        layout.addWidget(self.lbl_proveedor)
        layout.addWidget(self.txt_proveedor)
        layout.addWidget(self.chk_fecha_elab)
        layout.addWidget(self.lbl_fecha_elab)
        layout.addWidget(self.calendar_elab)
        layout.addWidget(self.chk_fecha_venc)
        layout.addWidget(self.lbl_fecha_venc)
        layout.addWidget(self.calendar_venc)
        layout.addWidget(btn_filter_products)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

        self.selected_date_elab = None
        self.selected_date_venc = None

    def show_date_elab(self, date):
        self.selected_date_elab = date.toString('yyyy-MM-dd')

    def show_date_venc(self, date):
        self.selected_date_venc = date.toString('yyyy-MM-dd')

    def filter_products(self):
        # Obtener la información ingresada por el usuario para filtrar productos
        nombre_producto = self.txt_nombre_producto.text() if self.chk_nombre_producto.isChecked() else None
        proveedor = self.txt_proveedor.text() if self.chk_proveedor.isChecked() else None
        fecha_elab = self.calendar_elab.selectedDate().toString('yyyy-MM-dd') if self.chk_fecha_elab.isChecked() else None
        fecha_venc = self.calendar_venc.selectedDate().toString('yyyy-MM-dd') if self.chk_fecha_venc.isChecked() else None

        # Realizar la conexión a la base de datos y filtrar productos
        db_connection = connect_to_database()
        if db_connection:
            productos_filtrados = filtrar_productos(
                db_connection, nombre_producto, proveedor, fecha_elab, fecha_venc)

            # Limpiar la tabla antes de agregar nuevos resultados
            self.table_widget.setRowCount(0)

            # Insertar los resultados en la tabla
            for row, producto in enumerate(productos_filtrados):
                self.table_widget.insertRow(row)
                for col, value in enumerate(producto):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(row, col, item)

        db_connection.close()
