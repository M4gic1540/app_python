import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from Task.add_task_window import AddTaskWindow
from Task.update_task_window import UpdateTaskWindow
from Task.show_task import ShowTaskWindow
from Task.erase_task import EraseTaskWindow
from Task.filter_task import FilterTaskWindow
from Users.add_user import AddUserWindow
from Users.show_user import ShowUserWindow
from Users.erase_user import EraseUserWindow
from Users.update_user import UpdateUserWindow
from Users.filter_user import FilterUserWindow
from Products.add_products import AddProductWindow
from Products.show_products import ShowProductsWindow
from Products.update_products import UpdateProductsWindow
from Products.erase_products import EraseProductsWindow
from Products.filter_products import FilterProductsWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Gestor de Tareas')
        self.setGeometry(100, 100, 400, 400)

        # Crear acciones para agregar y actualizar tarea en el menú
        add_task_action = QAction('Agregar Tarea', self)
        add_task_action.triggered.connect(self.open_add_window)

        update_task_action = QAction('Actualizar Tarea', self)
        update_task_action.triggered.connect(self.open_update_window)

        # Crear acciones para mostrar las tareas
        show_task_action = QAction('Mostrar Tareas', self)
        # Conectar la acción al método show_tasks
        show_task_action.triggered.connect(self.show_tasks_window)

        # Crear acciones para eliminar las tareas
        erase_task_action = QAction('Eliminar Tareas', self)
        erase_task_action.triggered.connect(self.erase_tasks)

        filter_task_action = QAction('Filtrar Tareas', self)
        filter_task_action.triggered.connect(self.filter_tasks)

        # Agregar las acciones al menú
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('Control de Tareas')
        file_menu.addAction(add_task_action)
        file_menu.addAction(update_task_action)
        file_menu.addAction(show_task_action)
        file_menu.addAction(erase_task_action)
        file_menu.addAction(filter_task_action)

        # Crear el menú de usuarios

        # Crear acciones para agregar y actualizar usuarios en el menú
        add_user_action = QAction('Agregar Usuario', self)
        add_user_action.triggered.connect(self.open_add_user_window)

        update_user_action = QAction('Actualizar Usuario', self)
        update_user_action.triggered.connect(self.open_update_user_window)
#
        # Crear acciones para mostrar las tareas
        show_user_action = QAction('Todos los Usuario', self)
        # Conectar la acción al método show_tasks
        show_user_action.triggered.connect(self.show_user_window)
#
        ## Crear acciones para eliminar los users
        erase_user_action = QAction('Eliminar Usuario', self)
        erase_user_action.triggered.connect(self.erase_user_window)
#
        filter_user_action = QAction('Filtrar Usuario', self)
        filter_user_action.triggered.connect(self.filter_user_window)
        

        # Crear acciones para agregar y actualizar productos en el menú

        add_product_action = QAction('Agregar Productos', self)
        add_product_action.triggered.connect(self.add_product_window)

        update_product_action = QAction('Actualizar Productos', self)
        update_product_action.triggered.connect(self.update_products_window)

        show_product_action = QAction('Mostrar Productos', self)
        show_product_action.triggered.connect(self.show_product_window)

        erase_product_window = QAction('Eliminar Productos', self)
        erase_product_window.triggered.connect(self.erase_product_window)

        filter_product_action = QAction('Filtrar Productos', self)
        filter_product_action.triggered.connect(self.filter_product_window)



         #Agregar la barra de usuario
        main_menu = self.menuWidget()
        file_menu = main_menu.addMenu('Control de Usuario')
        file_menu.addAction(add_user_action)
        file_menu.addAction(update_user_action)
        file_menu.addAction(show_user_action)
        file_menu.addAction(erase_user_action)
        file_menu.addAction(filter_user_action)


        #agregar la barra de productos
        main_menu = self.menuWidget()
        file_menu = main_menu.addMenu('Control de Productos')
        file_menu.addAction(add_product_action)
        file_menu.addAction(update_product_action)
        file_menu.addAction(show_product_action)
        file_menu.addAction(erase_product_window)
        file_menu.addAction(filter_product_action)



    def open_add_window(self):
        add_window = AddTaskWindow(self)
        add_window.exec_()

    def open_update_window(self):
        update_window = UpdateTaskWindow(self)
        update_window.exec_()

    def show_tasks_window(self):
        # Crear la ventana de mostrar tareas
        show_task_window = ShowTaskWindow(self)
        show_task_window.exec_()  # Mostrar la ventana

    def erase_tasks(self):
        # Crear la ventana de eliminar tareas
        erase_task_window = EraseTaskWindow(self)
        erase_task_window.exec_()  # Mostrar la ventana

    def filter_tasks(self):
        # Crear la ventana de filtrar tareas
        filter_task_window = FilterTaskWindow(self)
        filter_task_window.exec_()  # Mostrar la ventana


    def open_add_user_window(self):
        add_user_window = AddUserWindow()  # Crear la ventana de agregar usuario
        add_user_window.exec_()  # Mostrar la ventana

    def show_user_window(self):
        # Crear la ventana de mostrar tareas
        show_user_window = ShowUserWindow()
        show_user_window.exec_()  # Mostrar la ventana

    def open_update_user_window(self):
        update_user_window = UpdateUserWindow()
        update_user_window.exec_()
        
    def erase_user_window(self):
        # Crear la ventana de eliminar tareas
        erase_user_window = EraseUserWindow()
        erase_user_window.exec_()

    def filter_user_window(self):
        # Crear la ventana de filtrar tareas
        filter_user_window = FilterUserWindow()
        filter_user_window.exec_()

    def add_product_window(self):
        add_product_window = AddProductWindow()
        add_product_window.exec_()

    def show_product_window(self):
        # Crear la ventana de mostrar tareas
        show_product_window = ShowProductsWindow()
        show_product_window.exec_()

    def update_products_window(self, product_id):
        product_id = product_id
        update_product_window = UpdateProductsWindow(product_id=product_id)
        update_product_window.exec_()

    def erase_product_window(self):
        erase_product_window = EraseProductsWindow()
        erase_product_window.exec_()

    def filter_product_window(self):
        # Crear la ventana de filtrar productos
        filter_product_window = FilterProductsWindow()
        filter_product_window.exec_()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
