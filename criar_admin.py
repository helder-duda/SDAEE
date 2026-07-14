from app import app, db
from models import User  # (Verifique se no seu modelo a classe é User ou Usuario)
from werkzeug.security import generate_password_hash

# É obrigatório rodar comandos de banco de dados dentro do app_context
with app.app_context():
    # 1. ESTA É A LINHA QUE FALTAVA: Ela cria as tabelas com a nova coluna
    db.drop_all()
    db.create_all()

    usuario = 'admin'
    senha = '12345'

    # 2. O script tenta buscar o usuário (agora não dará erro, pois a tabela está atualizada)
    admin = User.query.filter_by(username=usuario).first()

    if not admin:
        senha_criptografada = generate_password_hash(senha)

        # 3. Criamos o usuário passando o is_admin=True
        novo_admin = User(username=usuario, password=senha_criptografada, is_admin=True)
        db.session.add(novo_admin)
        db.session.commit()
        print("Administrador criado com sucesso!")
    else:
        print("Administrador já existe no banco.")