from flask import Flask
from app.models.base import db
from app.config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Importar blueprints
    from app.routes.clientes import clientes_bp
    from app.routes.transacciones import transacciones_bp
    from app.routes.auth import auth_bp
    from app.routes.frontend import frontend_bp

    # Registrar blueprints
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(transacciones_bp, url_prefix='/transacciones')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(frontend_bp, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
