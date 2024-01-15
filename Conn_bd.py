import mysql.connector
from dotenv import dotenv_values


def connect_to_database():
    try:
        config = dotenv_values('Var.env')
        conn = mysql.connector.connect(
            host=config['MYSQL_HOST'],
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE'],
            port=config['MYSQL_PORT']
        )
        if conn.is_connected():
            print('Conexión exitosa a la base de datos MySQL')
            return conn
        else:
            print('Error en la conexión')
            return None
    except mysql.connector.Error as e:
        print(f'Error de conexión a MySQL: {e}')
        return None
    except Exception as ex:
        print(f'Error desconocido: {ex}')
        return None


def agregar_tabla(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS tareas (id INT AUTO_INCREMENT PRIMARY KEY, '
                       'tarea VARCHAR(255), estado BOOLEAN, fecha_creacion DATE)')
        connection.commit()
        print('Tabla tareas creada')
    except mysql.connector.Error as e:
        print(f'Error al crear la tabla: {e}')
    finally:
        cursor.close()


def agregar_tarea(connection, tarea):
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO tareas (tarea, estado, fecha_creacion) VALUES (%s, %s, %s)',
                       (tarea['tarea'], tarea['estado'], tarea['fecha_creacion']))
        connection.commit()
        print('Tarea agregada correctamente')
    except mysql.connector.Error as e:
        print(f'Error al agregar la tarea: {e}')
    finally:
        cursor.close()


def actualizar_tarea(connection, tarea_id, nueva_tarea, estado):
    try:
        cursor = connection.cursor()
        cursor.execute('UPDATE tareas SET tarea = %s, estado = %s WHERE id = %s',
                       (nueva_tarea, estado, tarea_id))
        connection.commit()
        print('Tarea actualizada correctamente')
    except mysql.connector.Error as e:
        print(f'Error al actualizar la tarea: {e}')
    finally:
        cursor.close()


def mostrar_tareas(connection):
    try:
        print('Conectando a la base de datos...')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tareas')
        tareas = cursor.fetchall()

        if not tareas:
            print('No hay tareas para mostrar.')

        return tareas
    except mysql.connector.Error as e:
        print(f'Error al seleccionar las tareas: {e}')
    finally:
        cursor.close()


def borrar_tarea(connection, tarea_id):
    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM tareas WHERE id = %s', (tarea_id,))
        connection.commit()
        print('Tarea borrada correctamente')
    except mysql.connector.Error as e:
        print(f'Error al borrar la tarea: {e}')
    finally:
        cursor.close()


def filtrar_tareas(connection, tarea_id=None, tarea_nombre=None, estado=None, fecha_creacion=None):
    try:
        cursor = connection.cursor()

        if tarea_id is not None:
            cursor.execute(
                'SELECT id, tarea, estado, fecha_creacion FROM tareas WHERE id = %s', (tarea_id,))
        elif tarea_nombre is not None:
            cursor.execute(
                'SELECT id, tarea, estado, fecha_creacion FROM tareas WHERE tarea = %s', (tarea_nombre,))
        elif estado is not None:
            cursor.execute(
                'SELECT id, tarea, estado, fecha_creacion FROM tareas WHERE estado = %s', (estado,))
        elif fecha_creacion is not None:
            cursor.execute(
                'SELECT id, tarea, estado, fecha_creacion FROM tareas WHERE fecha_creacion = %s', (fecha_creacion,))
        else:
            print('Debes proporcionar al menos un parámetro de filtrado.')

        tareas_filtradas = cursor.fetchall()

        if not tareas_filtradas:
            print('No hay tareas que coincidan con los criterios de filtrado.')

        return tareas_filtradas
    except mysql.connector.Error as e:
        print(f'Error al seleccionar las tareas filtradas: {e}')
    finally:
        cursor.close()

        # Cierre de la conexión a TASK

# Creación de la tabla "users"


def crear_tabla_usuario(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users ('
                       'id INT AUTO_INCREMENT PRIMARY KEY, '
                       'nombre VARCHAR(255), '
                       'apellidos VARCHAR(255), '
                       'email VARCHAR(255), '
                       'rut VARCHAR(13) NOT NULL UNIQUE, '
                       'es_cliente BOOLEAN, '
                       'fecha_nacimiento DATE, '
                       # Corrección en la posición de la coma
                       'password VARCHAR(255) NOT NULL, '
                       'INDEX idx_email (email), '
                       'INDEX idx_rut (rut))'
                       )
        connection.commit()
        print('Tabla usuario creada')
    except mysql.connector.Error as e:
        print(f'Error al crear la tabla: {e}')
    finally:
        cursor.close()


# Funciones de usuario

def agregar_user(connection, user):
    try:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO users (nombre, apellidos, email, rut, es_cliente, fecha_nacimiento, password) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (user['nombre'], user['apellidos'], user['email'], user['rut'], user['es_cliente'],
             user['fecha_nacimiento'], user['password']),
        )
        connection.commit()
        print('Usuario agregado correctamente')
    except mysql.connector.Error as e:
        print(f'Error al agregar el usuario: {e}')
    finally:
        cursor.close()


def mostrar_usuarios(connection):
    try:
        print('Conectando a la base de datos...')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        if not users:
            print('No hay usuarios para mostrar.')

        return users
    except mysql.connector.Error as e:
        print(f'Error al seleccionar los usuarios: {e}')
    finally:
        cursor.close()


def borrar_usuario(connection, user_id):
    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        connection.commit()
        print('Usuario borrado correctamente')
    except mysql.connector.Error as e:
        print(f'Error al borrar el usuario: {e}')
    finally:
        cursor.close()


def actualizar_usuario(connection, user_id, nombre, apellido, email, rut, es_cliente, fecha_nacimiento):
    # Implementa la lógica para actualizar el usuario en la base de datos
    try:
        cursor = connection.cursor()
        # Utiliza los parámetros proporcionados para actualizar el usuario
        cursor.execute('UPDATE users SET nombre=%s, apellidos=%s, email=%s, rut=%s, es_cliente=%s, fecha_nacimiento=%s WHERE id=%s',
                       (nombre, apellido, email, rut, es_cliente, fecha_nacimiento, user_id))
        connection.commit()
        print('Usuario actualizado correctamente')
    except mysql.connector.Error as e:
        print(f'Error al actualizar el usuario: {e}')
    finally:
        cursor.close()


def filtrar_usuarios(connection, user_id=None, nombre=None, apellidos=None, email=None, rut=None, es_cliente=None, fecha_nacimiento=None):
    try:
        cursor = connection.cursor()

        if user_id is not None:
            cursor.execute(
                'SELECT id, nombre, apellidos, email, rut, es_cliente, fecha_nacimiento FROM users WHERE id = %s', (user_id,))
        elif nombre is not None:
            cursor.execute(
                'SELECT id, nombre, apellidos, email, rut, es_cliente, fecha_nacimiento FROM users WHERE nombre = %s', (nombre,))
        elif apellidos is not None:
            cursor.execute(
                'SELECT id, nombre, apellidos, email, rut, es_cliente, fecha_nacimiento FROM users WHERE apellidos = %s', (apellidos,))
        elif email is not None:
            cursor.execute(
                'SELECT id, nombre, apellidos, email, rut, es_cliente, fecha_nacimiento FROM users WHERE email = %s', (email,))
        elif rut is not None:
            cursor.execute(
                'SELECT id, nombre, apellidos, email, rut, es_cliente, fecha_nacimiento FROM users WHERE rut = %s', (rut,))
        elif es_cliente is not None:
            cursor.execute(
                'SELECT id, nombre, apellidos, email, rut, es_cliente, fecha_nacimiento FROM users WHERE es_cliente = %s', (es_cliente,))
        elif fecha_nacimiento is not None:
            cursor.execute(
                'SELECT id, nombre, apellidos, email, rut, es_cliente, fecha_nacimiento FROM users WHERE fecha_nacimiento = %s', (fecha_nacimiento,))

        usuarios_filtrados = cursor.fetchall()

        if not usuarios_filtrados:
            print('No hay usuarios que coincidan con los criterios de filtrado.')

        return usuarios_filtrados
    except mysql.connector.Error as e:
        print(f'Error al seleccionar los usuarios filtrados: {e}')
    finally:
        cursor.close()

# Productos


def crear_tabla_productos(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS productos ('
                       'id INT AUTO_INCREMENT PRIMARY KEY, '
                       'nombre_producto VARCHAR(255), '
                       'precio DECIMAL(10,2), '
                       'stock INT, '
                       'proveedor VARCHAR(255), '
                       'fecha_elab DATE, '
                       'fecha_venc DATE, '
                       'INDEX idx_nombre_producto (nombre_producto), '
                       'INDEX idx_proveedor (proveedor)'
                       ')')
        connection.commit()
        print('Tabla productos creada correctamente')
    except mysql.connector.Error as e:
        print(f'Error al crear la tabla productos: {e}')
    finally:
        cursor.close()

def agregar_productos(connection, nombre_producto, precio, stock, proveedor, fecha_elab, fecha_venc):
    try:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre_producto, precio, stock, proveedor, fecha_elab, fecha_venc) VALUES (%s, %s, %s, %s, %s, %s)',
            (nombre_producto, precio, stock, proveedor, fecha_elab, fecha_venc)
        )
        connection.commit()
        print('Producto agregado correctamente')
    except mysql.connector.Error as e:
        print(f'Error al agregar el producto: {e}')
    finally:
        cursor.close()

def mostrar_productos(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        return productos
    except mysql.connector.Error as e:
        print(f'Error al mostrar los productos: {e}')
    finally:
        cursor.close()


def actualizar_productos(connection, id, nombre_producto, precio, stock, proveedor, fecha_elab, fecha_venc):
    try:
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE productos SET nombre_producto = %s, precio = %s, stock = %s, proveedor = %s, fecha_elab = %s, fecha_venc = %s WHERE id = %s',
            (nombre_producto, precio, stock, proveedor, fecha_elab, fecha_venc, id)
        )
        connection.commit()
        print('Producto actualizado correctamente')
    except mysql.connector.Error as e:
        print(f'Error al actualizar el producto: {e}')
    finally:
        cursor.close()

def borrar_productos(connection, id):
    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM productos WHERE id = %s', (id,))
        connection.commit()
        print('Producto borrado correctamente')
    except mysql.connector.Error as e:
        print(f'Error al borrar el producto: {e}')
    finally:
        cursor.close()


def filtrar_productos(connection, nombre_producto=None, proveedor=None, fecha_elab=None, fecha_venc=None):
    try:
        cursor = connection.cursor()
        query = 'SELECT * FROM productos WHERE '
        conditions = []

        if nombre_producto is not None:
            conditions.append('nombre_producto = %s')
        if proveedor is not None:
            conditions.append('proveedor = %s')
        if fecha_elab is not None:
            conditions.append('fecha_elab = %s')
        if fecha_venc is not None:
            conditions.append('fecha_venc = %s')

        if not conditions:
            print('No se proporcionaron criterios de filtrado.')
            return []

        where_clause = ' AND '.join(conditions)
        query += where_clause

        if nombre_producto is not None:
            cursor.execute(query, (nombre_producto,))
        elif proveedor is not None:
            cursor.execute(query, (proveedor,))
        elif fecha_elab is not None:
            cursor.execute(query, (fecha_elab,))
        elif fecha_venc is not None:
            cursor.execute(query, (fecha_venc,))

        productos_filtrados = cursor.fetchall()

        if not productos_filtrados:
            print('No hay productos que coincidan con los criterios de filtrado.')

        return productos_filtrados
    except mysql.connector.Error as e:
        print(f'Error al seleccionar los productos filtrados: {e}')
        return []
    finally:
        cursor.close()

