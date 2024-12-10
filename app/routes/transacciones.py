from flask import Blueprint, request, jsonify
from app.models.transaccion import Transaccion
from app.models.cliente import Cliente
from app.models.base import db
from app.utils.auth_decorator import token_required


transacciones_bp = Blueprint('transacciones', __name__)

@transacciones_bp.route('/<int:id_cliente>', methods=['POST'])
@token_required 
def crear_transaccion(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    monto = data.get('monto')
    tipo = data.get('tipo') # '+' o '-'
    fecha = data.get('fecha')  # Opcional

    if tipo not in ['+', '-']:
        return jsonify({"error": "Tipo de transacción inválido, debe ser '+' o '-'"}), 400

    # Validar monto
    try:
        monto = float(monto)
        if monto <= 0:
            return jsonify({"error": "El monto debe ser mayor a 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "El monto debe ser un valor numérico"}), 400

    from datetime import datetime
    if fecha:
        try:
            fecha_parsed = datetime.fromisoformat(fecha)
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS)"}), 400
    else:
        fecha_parsed = datetime.utcnow()

    from app.models.transaccion import Transaccion
    nueva = Transaccion(id_cliente=id_cliente, monto=monto, tipo=tipo, fecha=fecha_parsed)
    db.session.add(nueva)
    db.session.commit()

    return jsonify(nueva.to_dict()), 201


@transacciones_bp.route('/<int:id_cliente>', methods=['GET'])
@token_required 
def listar_transacciones(id_cliente):
    from app.models.transaccion import Transaccion
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Transaccion.query.filter_by(id_cliente=id_cliente)

    from datetime import datetime
    if start_date:
        try:
            start_parsed = datetime.fromisoformat(start_date)
            query = query.filter(Transaccion.fecha >= start_parsed)
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido en start_date"}), 400

    if end_date:
        try:
            end_parsed = datetime.fromisoformat(end_date)
            query = query.filter(Transaccion.fecha <= end_parsed)
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido en end_date"}), 400

    transacciones = [t.to_dict() for t in query.order_by(Transaccion.fecha.desc())]
    return jsonify(transacciones), 200



@transacciones_bp.route('/<int:id_cliente>/transaccion/<int:id_transaccion>', methods=['PUT'])
@token_required 
def actualizar_transaccion(id_cliente, id_transaccion):
    from app.models.transaccion import Transaccion
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    transaccion = Transaccion.query.filter_by(id_cliente=id_cliente, id_transaccion=id_transaccion).first()
    if not transaccion:
        return jsonify({"error": "Transacción no encontrada para este cliente"}), 404

    data = request.get_json()
    monto = data.get('monto', transaccion.monto)
    tipo = data.get('tipo', transaccion.tipo)
    fecha = data.get('fecha', None)

    # Validar tipo
    if tipo not in ['+', '-']:
        return jsonify({"error": "Tipo de transacción inválido"}), 400

    # Validar monto (que sea numérico y mayor a 0)
    try:
        monto = float(monto)
        if monto <= 0:
            return jsonify({"error": "El monto debe ser mayor a 0"}), 400
    except ValueError:
        return jsonify({"error": "El monto debe ser un valor numérico"}), 400

    transaccion.monto = monto
    transaccion.tipo = tipo

    # Manejo de la fecha si se envía
    # Se asume formato 'YYYY-MM-DD' o 'YYYY-MM-DDTHH:MM:SS'
    from datetime import datetime
    if fecha:
        try:
            # Intentar parsear ISO 8601
            transaccion.fecha = datetime.fromisoformat(fecha)
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS)"}), 400

    db.session.commit()
    return jsonify(transaccion.to_dict()), 200


@transacciones_bp.route('/<int:id_cliente>/transaccion/<int:id_transaccion>', methods=['DELETE'])
@token_required 
def eliminar_transaccion(id_cliente, id_transaccion):
    from app.models.transaccion import Transaccion
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    transaccion = Transaccion.query.filter_by(id_cliente=id_cliente, id_transaccion=id_transaccion).first()
    if not transaccion:
        return jsonify({"error": "Transacción no encontrada para este cliente"}), 404

    db.session.delete(transaccion)
    db.session.commit()
    return jsonify({"message": "Transacción eliminada correctamente"}), 200
