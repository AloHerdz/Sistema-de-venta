from flask import Blueprint, request, jsonify
from app.models.cliente import Cliente
from app.models.base import db
from app.utils.auth_decorator import token_required

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['POST'])
@token_required
def crear_cliente():
    data = request.get_json()
    nombre = data.get('nombre')
    telefono = data.get('telefono')
    colonia = data.get('colonia')

    if not nombre or not telefono:
        return jsonify({"error": "Nombre y teléfono son requeridos"}), 400

    nuevo = Cliente(nombre=nombre, telefono=telefono, colonia=colonia)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201


@clientes_bp.route('/<int:id_cliente>', methods=['GET'])
@token_required
def obtener_cliente(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    if cliente:
        return jsonify(cliente.to_dict()), 200
    return jsonify({"error": "Cliente no encontrado"}), 404

# En la ruta actualizar_cliente:
@clientes_bp.route('/<int:id_cliente>', methods=['PUT'])
@token_required
def actualizar_cliente(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    nombre = data.get('nombre', cliente.nombre)
    telefono = data.get('telefono', cliente.telefono)

    if not nombre or not telefono:
        return jsonify({"error": "Nombre y teléfono no pueden ser vacíos"}), 400

    cliente.nombre = nombre
    cliente.telefono = telefono
    cliente.colonia = data.get('colonia', cliente.colonia)
    db.session.commit()
    return jsonify(cliente.to_dict()), 200


@clientes_bp.route('/<int:id_cliente>', methods=['DELETE'])
@token_required
def eliminar_cliente(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado"}), 200

# Buscar por nombre o telefono
@clientes_bp.route('/buscar', methods=['GET'])
@token_required
def buscar_cliente():
    nombre = request.args.get('nombre')
    telefono = request.args.get('telefono')

    query = Cliente.query
    if nombre:
        query = query.filter(Cliente.nombre.like(f"%{nombre}%"))
    if telefono:
        query = query.filter(Cliente.telefono.like(f"%{telefono}%"))

    resultados = query.all()
    return jsonify([c.to_dict() for c in resultados]), 200


@clientes_bp.route('/<int:id_cliente>/saldo', methods=['GET'])
@token_required
def obtener_saldo(id_cliente):
    from app.models.transaccion import Transaccion
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    
    # Calcular saldo
    # sumatorio_positivos = SUM(monto where tipo='+')
    # sumatorio_negativos = SUM(monto where tipo='-')
    sumatorio_positivos = db.session.query(db.func.sum(Transaccion.monto)).filter_by(id_cliente=id_cliente, tipo='+').scalar() or 0.0
    sumatorio_negativos = db.session.query(db.func.sum(Transaccion.monto)).filter_by(id_cliente=id_cliente, tipo='-').scalar() or 0.0

    saldo = sumatorio_positivos - sumatorio_negativos
    return jsonify({"id_cliente": id_cliente, "saldo": saldo}), 200
