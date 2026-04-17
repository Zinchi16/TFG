from flask import Blueprint, request, jsonify
import functions as f

api = Blueprint("api", __name__)

# ---------- AUTH ----------
@api.route("/api/register", methods=["POST"])
def register():
    data, status = f.register_user(request.json)
    return jsonify(data), status


@api.route("/api/login", methods=["POST"])
def login():
    data, status = f.login_user(request.json)
    return jsonify(data), status


# ---------- LIBROS ----------
@api.route("/api/libros", methods=["GET"])
def listar_libros():
    data, status = f.obtener_libros(request.args)
    return jsonify(data), status


# ---------- CARRITO ----------
@api.route("/api/carrito", methods=["GET"])
def get_carrito():
    data, status = f.ver_carrito()
    return jsonify(data), status


@api.route("/api/carrito/add", methods=["POST"])
def add_carrito():
    data, status = f.añadir_carrito(request.json)
    return jsonify(data), status


@api.route("/api/carrito/clear", methods=["POST"])
def clear_carrito():
    data, status = f.vaciar_carrito()
    return jsonify(data), status


@api.route("/api/carrito/remove/<id>", methods=["DELETE"])
def remove_carrito(id):
    data, status = f.quitar_carrito(id)
    return jsonify(data), status
