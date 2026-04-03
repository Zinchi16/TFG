import mysql.connector
from mysql.connector import Error

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',      # Usuario por defecto en XAMPP
            password='',      # Contraseña por defecto en XAMPP (vacía)
            database='libreria_virtual'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos MySQL")
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Ejemplo de función para obtener libros (usada para el catálogo)
def obtener_libros():
    db = conectar_db()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libros")
        libros = cursor.fetchall()
        db.close()
        return libros
    return []