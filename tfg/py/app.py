from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import hashlib

app = Flask(__name__)
CORS(app)

carrito_servidor = []

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='libreria_virtual'
    )

# --- SEGURIDAD: Encriptación de contraseñas ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        datos = request.json
        nombre = datos.get('nombre', '') # Recogemos el nombre
        email = datos.get('email')
        password = datos.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # INSERTAMOS EN LAS COLUMNAS EXACTAS DE TU FOTO
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, hash_password(password))
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado correctamente"})
    except mysql.connector.Error as err:
        return jsonify({"error": "El email ya existe o hubo un problema"}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        datos = request.json
        email = datos.get('email')
        password = datos.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # BUSCAMOS EN LA COLUMNA 'password' (Como en tu DB)
        cursor.execute("SELECT id, nombre, password FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user["password"] == hash_password(password):
            # Devolvemos también el nombre para poder decirle "¡Bienvenido, Aaron!"
            return jsonify({"mensaje": "Login exitoso", "user_id": user["id"], "nombre": user["nombre"]})
        else:
            return jsonify({"error": "Email o contraseña incorrectos"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- CATÁLOGO Y CARRITO (Sin cambios en las rutas) ---
@app.route('/api/libros', methods=['GET'])
def listar_libros():
    try:
        busqueda = request.args.get('q', '')
        categoria = request.args.get('category', '')
        orden = request.args.get('sort', '')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM libros WHERE 1=1"
        parametros = []
        if busqueda:
            query += " AND (titulo LIKE %s OR autor LIKE %s)"
            parametros.extend([f"%{busqueda}%", f"%{busqueda}%"])
        if categoria:
            query += " AND categoria = %s"
            parametros.append(categoria)
        if orden == 'price-asc':
            query += " ORDER BY precio ASC"
        elif orden == 'price-desc':
            query += " ORDER BY precio DESC"
        cursor.execute(query, parametros)
        libros = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(libros)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/carrito', methods=['GET'])
def ver_carrito():
    total = sum(float(item['precio']) for item in carrito_servidor)
    return jsonify({"items": carrito_servidor, "total": total, "cantidad": len(carrito_servidor)})

@app.route('/api/carrito/add', methods=['POST'])
def añadir_al_carrito():
    try:
        datos = request.json
        libro_id = datos.get('id')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, titulo, precio, imagen_url FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()
        cursor.close()
        conn.close()
        if libro:
            carrito_servidor.append(libro)
            return jsonify({"mensaje": "Añadido", "cantidad": len(carrito_servidor)})
        return jsonify({"error": "No encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vaciar el carrito completo
@app.route('/api/carrito/clear', methods=['POST'])
def vaciar_carrito():
    carrito_servidor.clear()
    return jsonify({"mensaje": "Carrito vaciado"})

# Quitar un libro específico 
@app.route('/api/carrito/remove/<id>', methods=['DELETE'])
def quitar_del_carrito(id):
    for i, item in enumerate(carrito_servidor):
        # Comparamos como texto para evitar fallos
        if str(item['id']) == str(id):
            carrito_servidor.pop(i) 
            break 
            
    return jsonify({"mensaje": "Libro eliminado"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)