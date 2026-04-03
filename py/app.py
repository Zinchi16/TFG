from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Simulación de un carrito en el servidor (hasta que creéis la tabla 'Pedidos')
carrito_servidor = []

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='libreria_virtual'
    )

# --- 1. CATÁLOGO Y FILTROS (Semana 4) ---
@app.route('/api/libros', methods=['GET'])
def listar_libros():
    try:
        # Capturamos lo que el usuario ha seleccionado en los filtros del HTML
        busqueda = request.args.get('q', '')
        categoria = request.args.get('category', '')
        orden = request.args.get('sort', '')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Construimos la consulta SQL de forma dinámica
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


# --- 2. GESTIÓN DEL CARRITO (Semana 5) ---
@app.route('/api/carrito', methods=['GET'])
def ver_carrito():
    # Devuelve lo que hay en el carrito y el total a pagar
    total = sum(float(item['precio']) for item in carrito_servidor)
    return jsonify({
        "items": carrito_servidor,
        "total": total,
        "cantidad": len(carrito_servidor)
    })

@app.route('/api/carrito/add', methods=['POST'])
def añadir_al_carrito():
    try:
        datos = request.json
        libro_id = datos.get('id')

        # Buscamos el libro en la DB para meter sus datos reales al carrito
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, titulo, precio, imagen_url FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()
        cursor.close()
        conn.close()

        if libro:
            carrito_servidor.append(libro)
            return jsonify({"mensaje": "Añadido correctamente", "cantidad": len(carrito_servidor)})
        else:
            return jsonify({"error": "Libro no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/carrito/clear', methods=['POST'])
def vaciar_carrito():
    carrito_servidor.clear()
    return jsonify({"mensaje": "Carrito vaciado"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)