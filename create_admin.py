# create_admin.py
from app.main import create_app
from app.models.base import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    username = "admin"
    password = "admin123"
    hash_pass = generate_password_hash(password)
    admin_user = Usuario(username=username, password_hash=hash_pass)
    db.session.add(admin_user)
    db.session.commit()
    print("Usuario admin creado con éxito")

    print(Usuario.query.all())
