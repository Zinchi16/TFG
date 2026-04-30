from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from functools import wraps
import functions as f
import stripe
import uuid # Para generar un token único
from mailer import enviar_recuperacion

# Configura tu clave secreta de Stripe
stripe.api_key = "sk_test_51TRsUeJ2EVvmvKFtKkF6k1N5xcKCQeo0oGbsiIGRI4vXdo9ArOzDD6GeauxwBl3NaScs6ObDY8lVk7jNTfBR6nnp00JccVcGCI"

api = Blueprint("api", __name__)

# --- DECORADOR PARA RUTAS PROTEGIDAS ---
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user' not in session:
            # Si no hay sesión, redirige al login automáticamente[cite: 15]
            return redirect(url_for('api.login'))
        return view(**kwargs)
    return wrapped_view

# --- RUTAS DE NAVEGACIÓN ---

@api.route("/")
def index():
    """Carga el catálogo principal[cite: 19]."""
    return render_template("index.html")

@api.route("/login", methods=["GET", "POST"])
def login():
    """Gestiona el acceso. Soporta envíos POST de formularios."""
    if request.method == "POST":
        data = request.form if request.form else request.json
        success, result = f.login_user(data)
        if success:
            session['user'] = result
            return redirect(url_for('api.index'))
        flash(result, "error")
    return render_template("login.html")

@api.route("/registro", methods=["GET", "POST"])
def registro():
    """Gestiona el alta de usuarios."""
    if request.method == "POST":
        data = request.form if request.form else request.json
        success, msg = f.register_user(data)
        if success:
            return redirect(url_for('api.login'))
        flash(msg, "error")
    return render_template("registro.html")



@api.route("/olvide-password", methods=["GET", "POST"])
def olvide_password():
    if request.method == "POST":
        email = request.form.get("email")
        token = str(uuid.uuid4())
        
        enviar_recuperacion(email, "Usuario", token)
        
        flash("Proceso finalizado. Revisa Mailtrap.", "success")

        return redirect(url_for('api.login')) 
    
    return render_template("login.html")

@api.route("/cuenta")
@login_required
def cuenta():
    """Muestra el perfil solo si está logueado[cite: 18]."""
    return render_template("cuenta.html", user=session['user'])

@api.route("/user-data")
@login_required
def get_user_data():
    return jsonify(session['user'])

@api.route("/carrito")
def carrito():
    """Muestra la vista del carrito[cite: 17]."""
    return render_template("carrito.html")

@api.route("/admin")
@login_required
def admin():
    """Panel de administración protegido[cite: 16]."""
    if not session['user'].get('es_admin'):
        return redirect(url_for('api.index'))
    return render_template("admin.html")

@api.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('api.index'))

# --- ENDPOINTS DE DATOS (FUNCIONALIDAD) ---

@api.route("/libros-data")
def get_libros():
    return jsonify(f.obtener_libros(request.args))

@api.route("/carrito-gestion", methods=["GET", "POST", "DELETE"])
def gestion_carrito():
    if request.method == "GET":
        return jsonify(f.ver_carrito())
    if request.method == "POST":
        return jsonify(f.añadir_carrito(request.json.get('id')))
    if request.method == "DELETE":
        f.quitar_del_carrito(request.args.get('id'))
        return jsonify({"status": "deleted"})
    
@api.route("/carrito/actualizar", methods=["POST"])
def actualizar_carrito():
    data = request.json
    # data debe ser { "id": 1, "cambio": 1 } para sumar o -1 para restar
    resultado = f.actualizar_cantidad_carrito(data.get('id'), data.get('cambio'))
    return jsonify(resultado)



@api.route("/crear-checkout", methods=["POST"])
@login_required # Protegemos la ruta para que solo usuarios logueados compren
def crear_checkout():
    carrito = f.ver_carrito() # Obtenemos los productos actuales
    
    if not carrito['items']:
        return jsonify({"error": "El carrito está vacío"}), 400

    # Convertimos los items del carrito al formato de Stripe
    line_items = []
    for item in carrito['items']:
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': item['titulo']},
                'unit_amount': int(item['precio'] * 100), # Stripe usa céntimos
            },
            'quantity': item['cantidad'],
        })

    try:
        # Creamos la sesión de pago
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            # URLs a las que volverá el usuario tras el pago
            success_url=url_for('api.pago_exitoso', _external=True),
            cancel_url=url_for('api.carrito', _external=True),
        )
        return jsonify({"url": checkout_session.url})
    except Exception as e:
        return jsonify(error=str(e)), 500

@api.route("/pago-exitoso")
def pago_exitoso():
    # 1. Recuperamos los datos necesarios de la sesión y el carrito[cite: 4, 5]
    usuario = session.get('user')
    carrito_actual = f.ver_carrito()
    
    if usuario and carrito_actual['items']:
        # 2. Enviamos el correo profesional
        from mailer import enviar_confirmacion_compra
        enviar_confirmacion_compra(usuario['email'], usuario['nombre'], carrito_actual)

    # 3. Vaciamos el carrito (como ya hacías)[cite: 5]
    f.carrito_servidor = {} 
    
    # 4. Mostramos la página de éxito[cite: 9]
    return render_template("pago_exitoso.html")