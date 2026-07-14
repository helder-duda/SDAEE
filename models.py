from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Cria a instância do banco (mas ainda sem conectar ao Flask)
db = SQLAlchemy()

# ==========================================
# === MODELO DA TABELA DE USUÁRIOS =========
# ==========================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)