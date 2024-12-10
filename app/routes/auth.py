from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.base import db
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username y password requeridos"}), 400

    user = Usuario.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Generar JWT
    payload = {
        "user_id": user.id_usuario,
        "exp": datetime.utcnow() + timedelta(hours=2)  # El token expira en 2 horas
    }

    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
    return jsonify({"token": token}), 200
