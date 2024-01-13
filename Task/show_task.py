from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem
from Conn_bd import connect_to_database, mostrar_tareas

class ShowTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Mostrar Tareas')
        self.setGeometry(100, 100, 500, 200)

        # Crear la tabla para mostrar las tareas
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Establecer la cantidad de columnas

        # Establecer los títulos de las columnas
        headers = ['ID', 'Tarea', 'Estado', 'Fecha de Creación']
        self.table.setHorizontalHeaderLabels(headers)

        # Llamar a la función para cargar las tareas en la tabla
        self.load_tasks()

        # Diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_tasks(self):
        # Obtener la conexión a la base de datos y obtener las tareas
        db_connection = connect_to_database()
        if db_connection:
            tasks = mostrar_tareas(db_connection)
            if tasks:
                # Establecer la cantidad de filas de la tabla
                self.table.setRowCount(len(tasks))

                # Llenar la tabla con los datos de las tareas
                for row_num, task in enumerate(tasks):
                    for col_num, data in enumerate(task):
                        self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

            db_connection.close()  # Cerrar la conexión después de usarla


