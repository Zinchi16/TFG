from flask import Flask
from routes import api  # Importa tu blueprint de rutas

app = Flask(__name__, static_folder='static')
# ... tu clave secreta y blueprints ...

# --- CONFIGURACIÓN CRÍTICA ---
# Cambia 'mi_clave_secreta_super_segura' por una cadena aleatoria larga
app.secret_key = 'una_clave_muy_secreta_y_unica_12345' 

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)