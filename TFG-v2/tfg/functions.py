import mysql.connector
import hashlib

# --------- ESTADO ---------
carrito_servidor = []

# --------- DB ---------
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='libreria_virtual'
    )

# --------- SEGURIDAD ---------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --------- AUTH ---------
def register_user(datos):
    try:
        nombre = datos.get('nombre', '')
        email = datos.get('email')
        password = datos.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, hash_password(password))
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {"mensaje": "Usuario registrado correctamente"}, 200

    except mysql.connector.Error:
        return {"error": "El email ya existe o hubo un problema"}, 400


def login_user(datos):
    try:
        email = datos.get('email')
        password = datos.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nombre, password FROM usuarios WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user["password"] == hash_password(password):
            return {
                "mensaje": "Login exitoso",
                "user_id": user["id"],
                "nombre": user["nombre"]
            }, 200

        return {"error": "Email o contraseña incorrectos"}, 401

    except Exception as e:
        return {"error": str(e)}, 500


# --------- LIBROS ---------
def obtener_libros(args):
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

        if orden == "price-asc":
            query += " ORDER BY precio ASC"
        elif orden == "price-desc":
            query += " ORDER BY precio DESC"

        cursor.execute(query, params)
        libros = cursor.fetchall()
        cursor.close()
        conn.close()

        return libros, 200

    except Exception as e:
        return {"error": str(e)}, 500


# --------- CARRITO ---------
def ver_carrito():
    total = sum(float(item['precio']) for item in carrito_servidor)
    return {
        "items": carrito_servidor,
        "total": total,
        "cantidad": len(carrito_servidor)
    }, 200


def añadir_carrito(datos):
    try:
        libro_id = datos.get('id')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, titulo, precio, imagen_url FROM libros WHERE id = %s",
            (libro_id,)
        )
        libro = cursor.fetchone()
        cursor.close()
        conn.close()

        if not libro:
            return {"error": "Libro no encontrado"}, 404

        carrito_servidor.append(libro)
        return {"mensaje": "Añadido", "cantidad": len(carrito_servidor)}, 200

    except Exception as e:
        return {"error": str(e)}, 500


def vaciar_carrito():
    carrito_servidor.clear()
    return {"mensaje": "Carrito vaciado"}, 200


def quitar_del_carrito(id):
    for i, item in enumerate(carrito_servidor):
        if str(item['id']) == str(id):
            carrito_servidor.pop(i)
            break
    return {"mensaje": "Libro eliminado"}, 200