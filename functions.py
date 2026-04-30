import mysql.connector
import hashlib

# Estado temporal del carrito
# Nota: En producción, esto se gestionaría por usuario en la DB o sesión
carrito_servidor = []

def get_db_connection():
    """Establece la conexión con la base de datos."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='libreria_virtual'
    )

def hash_password(password):
    """Cifra la contraseña usando SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- USUARIOS ---

def register_user(form_data):
    """Registra un nuevo usuario desde los datos de un formulario."""
    try:
        nombre = form_data.get('nombre')
        email = form_data.get('email')
        password = form_data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, hash_password(password))
        )
        conn.commit()
        return True, "Usuario registrado correctamente"
    except Exception:
        return False, "El email ya existe o hubo un error en el registro"
    finally:
        if 'conn' in locals(): conn.close()

# En functions.py
def login_user(form_data):
    try:
        email = form_data.get('email')
        password = hash_password(form_data.get('password'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # CORRECCIÓN: Añadimos 'email' a la consulta
        cursor.execute(
            "SELECT id, nombre, email, es_admin FROM usuarios WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()
        return (True, user) if user else (False, "Credenciales incorrectas")
    # ... resto del código
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"
    finally:
        if 'conn' in locals(): conn.close()

# --- CATÁLOGO ---

def obtener_libros(args):
    """Obtiene libros con filtros de búsqueda, categoría y orden."""
    try:
        busqueda = args.get('q', '')
        categoria = args.get('category', '')
        orden = args.get('sort', '')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM libros WHERE 1=1"
        params = []

        if busqueda:
            query += " AND (titulo LIKE %s OR autor LIKE %s)"
            params.extend([f"%{busqueda}%", f"%{busqueda}%"])
        if categoria:
            query += " AND categoria = %s"
            params.append(categoria)
        
        if orden == "price-asc": query += " ORDER BY precio ASC"
        elif orden == "price-desc": query += " ORDER BY precio DESC"

        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        if 'conn' in locals(): conn.close()

# --- CARRITO ---

# Reemplaza la variable y las funciones de carrito en functions.py
carrito_servidor = {} # Ahora es un diccionario { id: {datos_libro, cantidad} }

def añadir_carrito(libro_id):
    try:
        libro_id_str = str(libro_id)
        if libro_id_str in carrito_servidor:
            carrito_servidor[libro_id_str]['cantidad'] += 1
            return True, sum(item['cantidad'] for item in carrito_servidor.values())

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, titulo, precio, imagen_url FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()
        
        if libro:
            libro['cantidad'] = 1
            carrito_servidor[libro_id_str] = libro
            return True, sum(item['cantidad'] for item in carrito_servidor.values())
        return False, "Libro no encontrado"
    finally:
        if 'conn' in locals(): conn.close()

def actualizar_cantidad_carrito(libro_id, cambio):
    libro_id_str = str(libro_id)
    if libro_id_str in carrito_servidor:
        carrito_servidor[libro_id_str]['cantidad'] += cambio
        if carrito_servidor[libro_id_str]['cantidad'] <= 0:
            carrito_servidor.pop(libro_id_str)
    return ver_carrito()

def ver_carrito():
    items = list(carrito_servidor.values())
    total = sum(float(item['precio']) * item['cantidad'] for item in items)
    cantidad_total = sum(item['cantidad'] for item in items)
    return {
        "items": items,
        "total": round(total, 2),
        "cantidad": cantidad_total
    }

def quitar_del_carrito(libro_id):
    global carrito_servidor
    for i, item in enumerate(carrito_servidor):
        if str(item['id']) == str(libro_id):
            carrito_servidor.pop(i)
            return True
    return False

# --- ADMINISTRACIÓN ---

def gestionar_libro_admin(form_data, eliminar_id=None):
    """Añade o borra libros del catálogo."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if eliminar_id:
            cursor.execute("DELETE FROM libros WHERE id = %s", (eliminar_id,))
        else:
            query = "INSERT INTO libros (titulo, autor, descripcion, precio, categoria, imagen_url) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (form_data['titulo'], form_data['autor'], form_data.get('descripcion'), form_data['precio'], form_data['categoria'], form_data.get('imagen_url')))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()