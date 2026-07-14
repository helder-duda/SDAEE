from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User  # Importa o banco do seu arquivo models.py

import random
import math
import numpy as np
import io
import base64
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# ==========================================
# === CONFIGURAÇÕES DO BANCO E LOGIN =======
# ==========================================
app.config['SECRET_KEY'] = 'chave_secreta_iff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


# ==========================================
# === ROTAS DE LOGIN E PROTEÇÃO ============
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ROTA PRINCIPAL PROTEGIDA PELO @login_required
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/cadastro', methods=['GET', 'POST'])
@login_required  # 1. Primeira trava: Obriga a pessoa a estar logada no sistema
def cadastro():
    # 2. Segunda trava: Verifica se o usuário logado NÃO é um administrador
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem cadastrar novos usuários.')
        return redirect(url_for('index'))  # Expulsa o usuário comum de volta para a página inicial

    # Daqui para baixo, o código flui normalmente, pois sabemos que é o admin
    if request.method == 'POST':
        nome_usuario = request.form.get('username')
        senha_digitada = request.form.get('password')

        usuario_existente = User.query.filter_by(username=nome_usuario).first()
        if usuario_existente:
            flash('Erro: Esse nome de usuário já está em uso.')
            return redirect(url_for('cadastro'))

        senha_criptografada = generate_password_hash(senha_digitada)

        novo_usuario = User(username=nome_usuario, password=senha_criptografada)

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Novo usuário cadastrado com sucesso!')
        return redirect(url_for('index'))

    return render_template('cadastro.html')

@app.route('/alterar_senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    if request.method == 'POST':
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')

        # 1. Verifica se a senha atual digitada está correta
        if not check_password_hash(current_user.password, senha_atual):
            flash('Erro: A senha atual está incorreta.')
            return redirect(url_for('alterar_senha'))

        # 2. Verifica se a nova senha e a confirmação são iguais
        if nova_senha != confirmar_senha:
            flash('Erro: A nova senha e a confirmação não coincidem.')
            return redirect(url_for('alterar_senha'))

        # 3. Criptografa a nova senha e atualiza o banco de dados
        current_user.password = generate_password_hash(nova_senha)
        db.session.commit()

        flash('Senha alterada com sucesso!')
        return redirect(url_for('index'))

    # Se for GET, apenas mostra a página com o formulário
    return render_template('alterar_senha.html')


# ==========================================
# === ROTA DE GERAÇÃO DE EXERCÍCIOS ========
# ==========================================
@app.route('/gerar_exercicios')
@login_required
def gerar_exercicios():
    def sortear():
        return {
            'v': random.choice([12, 24, 110, 127, 220]),
            'f': random.choice([50, 60, 400]),
            'r': random.randint(2, 50) * 10,
            'l': random.randint(10, 500),
            'c': random.randint(5, 100)
        }

    def plot_fasores(fasores):
        """ Desenha fasores normalizados qualitativamente para evitar disparidade de grandezas """
        if not fasores: return None
        plt.figure(figsize=(3, 3))
        ax = plt.subplot(111)

        # Dicionário para controlar sobreposições no mesmo ângulo
        angulos_usados = {}

        for mag, ang, label, color in fasores:
            if mag == 0: continue

            # Arredonda o ângulo para checar se já existe uma seta naquela posição
            ang_arredondado = round(ang, 1)
            angulos_usados[ang_arredondado] = angulos_usados.get(ang_arredondado, 0) + 1

            # NORMALIZAÇÃO: O tamanho visual base é 1.0.
            # Se houver outra seta no mesmo ângulo, diminui 0.2 (0.8, 0.6...) para não esconder a seta de baixo
            plot_mag = 1.0 - (angulos_usados[ang_arredondado] - 1) * 0.22

            rad = math.radians(ang)
            x = plot_mag * math.cos(rad)
            y = plot_mag * math.sin(rad)

            ax.annotate("", xy=(x, y), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=color, lw=2))

            # Posição do texto sempre empurrada para fora da ponta da seta
            offset = 1.35
            ax.text(x * offset, y * offset, f"{label}", color=color, ha='center', va='center', fontsize=9,
                    fontweight='bold')

        # Como todos os fasores foram reescalados, o limite do gráfico passa a ser fixo
        limit = 1.5
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.set_aspect('equal')

        # Remove bordas externas e números dos eixos
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        img = io.BytesIO()
        plt.savefig(img, format='png', transparent=True, bbox_inches='tight')
        plt.close()
        return base64.b64encode(img.getvalue()).decode('utf8')
    dados = []

    # ---------------------------------------------------------
    # --- CIRCUITOS RL (1 a 3)
    # ---------------------------------------------------------
    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    z_mag = math.hypot(q['r'], xl)
    z_ang = math.degrees(math.atan2(xl, q['r']))
    i_mag = q['v'] / z_mag
    i_ang = -z_ang
    dados.append({
        'pergunta': f"Em um circuito RL série, uma fonte de {q['v']}V e frequência {q['f']}Hz alimenta um resistor de {q['r']}Ω e um indutor de {q['l']}mH. Calcule a impedância total (Z) e a corrente do circuito.",
        'resposta': f"<strong>Z</strong> = {z_mag:.2f}Ω ∠{z_ang:.1f}° <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}°",
        'grafico': plot_fasores([(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I', 'blue')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    ir = q['v'] / q['r']
    il = q['v'] / xl
    it_mag = math.hypot(ir, il)
    it_ang = math.degrees(math.atan2(-il, ir))
    dados.append({
        'pergunta': f"Um circuito RL paralelo é composto por um resistor de {q['r']}Ω e um indutor de {q['l']}mH ligados a uma fonte de {q['v']}V / {q['f']}Hz. Determine as correntes nos ramos e a corrente total.",
        'resposta': f"<strong>IR</strong> = {ir:.2f}A ∠0° <br> <strong>IL</strong> = {il:.2f}A ∠-90° <br> <strong>IT</strong> = {it_mag:.2f}A ∠{it_ang:.1f}°",
        'grafico': plot_fasores(
            [(q['v'], 0, 'V', 'black'), (ir, 0, 'IR', 'green'), (il, -90, 'IL', 'red'), (it_mag, it_ang, 'IT', 'blue')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    z = math.hypot(q['r'], xl)
    i = q['v'] / z
    vr = i * q['r']
    vl = i * xl
    dados.append({
        'pergunta': f"Em um circuito RL série (R = {q['r']}Ω, L = {q['l']}mH, V = {q['v']}V, f = {q['f']}Hz), determine a queda de tensão específica sobre o resistor (VR) e sobre o indutor (VL).",
        'resposta': f"<strong>I (Ref)</strong> = {i:.2f}A <br> <strong>VR</strong> = {vr:.2f}V ∠0° (em fase com I) <br> <strong>VL</strong> = {vl:.2f}V ∠90°",
        'grafico': plot_fasores([(i, 0, 'I(ref)', 'blue'), (vr, 0, 'VR', 'green'), (vl, 90, 'VL', 'red'),
                                 (q['v'], math.degrees(math.atan2(vl, vr)), 'V_Fonte', 'black')])
    })

    # ---------------------------------------------------------
    # --- CIRCUITOS RC (4 a 6)
    # ---------------------------------------------------------
    q = sortear()
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    z_mag = math.hypot(q['r'], xc)
    z_ang = math.degrees(math.atan2(-xc, q['r']))
    i_mag = q['v'] / z_mag
    i_ang = -z_ang
    dados.append({
        'pergunta': f"Dado um circuito RC série com R = {q['r']}Ω e C = {q['c']}μF, alimentado por {q['v']}V a {q['f']}Hz. Encontre a reatância capacitiva (Xc) e a corrente total.",
        'resposta': f"<strong>Xc</strong> = {xc:.2f}Ω <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}°",
        'grafico': plot_fasores([(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I', 'blue')])
    })

    q = sortear()
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    ir = q['v'] / q['r']
    ic = q['v'] / xc
    it_mag = math.hypot(ir, ic)
    it_ang = math.degrees(math.atan2(ic, ir))
    dados.append({
        'pergunta': f"Considere um circuito RC paralelo onde R = {q['r']}Ω, C = {q['c']}μF e a fonte é de {q['v']}V / {q['f']}Hz. Calcule a corrente total e o ângulo de defasagem.",
        'resposta': f"<strong>IT</strong> = {it_mag:.2f}A <br> <strong>Ângulo</strong> = {it_ang:.1f}° (Adiantado)",
        'grafico': plot_fasores(
            [(q['v'], 0, 'V', 'black'), (ir, 0, 'IR', 'green'), (ic, 90, 'IC', 'red'), (it_mag, it_ang, 'IT', 'blue')])
    })

    q = sortear()
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    z = math.hypot(q['r'], xc)
    i = q['v'] / z
    vr = i * q['r']
    vc = i * xc
    dados.append({
        'pergunta': f"Em um circuito RC série (R = {q['r']}Ω, C = {q['c']}μF, V = {q['v']}V, f = {q['f']}Hz), calcule a queda de tensão sobre o resistor (VR) e sobre o capacitor (VC).",
        'resposta': f"<strong>I (Ref)</strong> = {i:.2f}A <br> <strong>VR</strong> = {vr:.2f}V ∠0° <br> <strong>VC</strong> = {vc:.2f}V ∠-90°",
        'grafico': plot_fasores([(i, 0, 'I(ref)', 'blue'), (vr, 0, 'VR', 'green'), (vc, -90, 'VC', 'red'),
                                 (q['v'], math.degrees(math.atan2(-vc, vr)), 'V_Fonte', 'black')])
    })

    # ---------------------------------------------------------
    # --- CIRCUITOS RLC SÉRIE E PARALELO (7 a 15)
    # ---------------------------------------------------------
    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    x_tot = xl - xc
    z_mag = math.hypot(q['r'], x_tot)
    z_ang = math.degrees(math.atan2(x_tot, q['r']))
    i_mag = q['v'] / z_mag
    i_ang = -z_ang
    dados.append({
        'pergunta': f"Um resistor de {q['r']}Ω, um indutor de {q['l']}mH e um capacitor de {q['c']}μF estão ligados em série. A fonte fornece {q['v']}V em {q['f']}Hz. Qual é a impedância do circuito e a corrente total?",
        'resposta': f"<strong>Z</strong> = {z_mag:.2f}Ω ∠{z_ang:.1f}° <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}°",
        'grafico': plot_fasores([(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I', 'blue')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    ir = q['v'] / q['r']
    il = q['v'] / xl
    ic = q['v'] / xc
    it_mag = math.hypot(ir, ic - il)
    it_ang = math.degrees(math.atan2(ic - il, ir))
    dados.append({
        'pergunta': f"Para um circuito RLC paralelo com R = {q['r']}Ω, L = {q['l']}mH e C = {q['c']}μF ligado em {q['v']}V / {q['f']}Hz, determine a corrente em cada componente e a corrente total.",
        'resposta': f"<strong>IR</strong>={ir:.2f}A, <strong>IL</strong>={il:.2f}A, <strong>IC</strong>={ic:.2f}A <br> <strong>IT</strong> = {it_mag:.2f}A ∠{it_ang:.1f}°",
        'grafico': plot_fasores(
            [(ir, 0, 'IR', 'green'), (il, -90, 'IL', 'red'), (ic, 90, 'IC', 'orange'), (it_mag, it_ang, 'IT', 'blue')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    z = math.hypot(q['r'], xl - xc)
    i = q['v'] / z
    vr = i * q['r']
    vl = i * xl
    vc = i * xc
    comportamento = "Indutivo" if xl > xc else "Capacitivo"
    dados.append({
        'pergunta': f"Circuito RLC série (R = {q['r']}Ω, L = {q['l']}mH, C = {q['c']}μF, V = {q['v']}V / {q['f']}Hz). Calcule as tensões VR, VL e VC, e indique o comportamento do circuito.",
        'resposta': f"<strong>VR</strong>={vr:.2f}V, <strong>VL</strong>={vl:.2f}V, <strong>VC</strong>={vc:.2f}V <br> <strong>Comportamento:</strong> {comportamento}",
        'grafico': plot_fasores([(vr, 0, 'VR', 'green'), (vl, 90, 'VL', 'red'), (vc, -90, 'VC', 'orange'),
                                 (q['v'], math.degrees(math.atan2(vl - vc, vr)), 'V_Tot', 'black')])
    })

    q = sortear()
    fr = 1 / (2 * math.pi * math.sqrt((q['l'] / 1000) * (q['c'] / 1000000)))
    i_max = q['v'] / q['r']
    dados.append({
        'pergunta': f"Calcule a frequência de ressonância (fr) para um circuito RLC com L = {q['l']}mH e C = {q['c']}μF. Se R = {q['r']}Ω e V = {q['v']}V, qual será a corrente máxima?",
        'resposta': f"<strong>Frequência (fr)</strong> = {fr:.1f}Hz <br> <strong>Corrente Máx</strong> = {i_max:.2f}A ∠0°",
        'grafico': plot_fasores([(q['v'], 0, 'V', 'black'), (i_max, 0, 'I', 'blue')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    ir, il, ic = q['v'] / q['r'], q['v'] / xl, q['v'] / xc
    it = math.hypot(ir, ic - il)
    fp = ir / it
    classificacao = "Adiantado" if ic > il else "Atrasado"
    dados.append({
        'pergunta': f"Em um circuito RLC paralelo (V={q['v']}V, f={q['f']}Hz, R={q['r']}Ω, L={q['l']}mH, C={q['c']}μF). Determine o fator de potência (FP) e classifique-o.",
        'resposta': f"<strong>FP</strong> = {fp:.3f} ({classificacao})",
        'grafico': plot_fasores([(ir, 0, 'IR', 'green'), (it, math.degrees(math.atan2(ic - il, ir)), 'IT', 'blue')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    z = math.hypot(q['r'], xl - xc)
    i = q['v'] / z
    p = (i ** 2) * q['r']
    ql = (i ** 2) * xl
    qc = (i ** 2) * xc
    q_tot = ql - qc
    s = (i ** 2) * z
    dados.append({
        'pergunta': f"Dado um circuito RLC série (R = {q['r']}Ω, L = {q['l']}mH, C = {q['c']}μF, V = {q['v']}V / {q['f']}Hz). Calcule a potência ativa (P), reativa (Q) e aparente (S).",
        'resposta': f"<strong>P</strong> = {p:.1f} W <br> <strong>Q</strong> = {q_tot:.1f} VAr <br> <strong>S</strong> = {s:.1f} VA",
        'grafico': plot_fasores([(p, 0, 'P(W)', 'green'), (q_tot, 90 if q_tot > 0 else -90, 'Q(VAr)', 'red'),
                                 (s, math.degrees(math.atan2(q_tot, p)), 'S(VA)', 'black')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    defasagem = math.degrees(math.atan2(xl - xc, q['r']))
    dados.append({
        'pergunta': f"Qual é o ângulo de defasagem entre a tensão e a corrente total em um circuito RLC série (R = {q['r']}Ω, L = {q['l']}mH, C = {q['c']}μF, f = {q['f']}Hz)?",
        'resposta': f"<strong>Defasagem (θ_Z)</strong> = {defasagem:.2f}°",
        'grafico': plot_fasores([(q['r'], 0, 'R', 'green'), (xl - xc, 90 if xl > xc else -90, 'X', 'red'),
                                 (math.hypot(q['r'], xl - xc), defasagem, 'Z', 'blue')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    g, bl, bc = 1 / q['r'], 1 / xl, 1 / xc
    y_mag = math.hypot(g, bc - bl)
    zeq = 1 / y_mag
    dados.append({
        'pergunta': f"Encontre a impedância equivalente (Zeq) e a admitância total (Y) de um circuito RLC paralelo (R = {q['r']}Ω, L = {q['l']}mH, C = {q['c']}μF, f = {q['f']}Hz).",
        'resposta': f"<strong>Y</strong> = {y_mag:.4f} S <br> <strong>Zeq</strong> = {zeq:.2f} Ω",
        'grafico': plot_fasores([(g, 0, 'G', 'green'), (bc - bl, 90 if bc > bl else -90, 'B_liq', 'red'),
                                 (y_mag, math.degrees(math.atan2(bc - bl, g)), 'Y', 'blue')])
    })

    q = sortear()
    xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
    xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    xtot = xl - xc
    estado = "atrasada" if xtot > 0 else "adiantada"
    dados.append({
        'pergunta': f"Considere um RLC série (R = {q['r']}Ω, L = {q['l']}mH, C = {q['c']}μF). Determine a reatância total (X) em {q['f']}Hz e explique a relação V x I.",
        'resposta': f"<strong>X_Total</strong> = {xtot:.2f} Ω <br> A corrente está <strong>{estado}</strong> em relação à tensão.",
        'grafico': plot_fasores(
            [(xl, 90, 'XL', 'red'), (xc, -90, 'XC', 'orange'), (abs(xtot), 90 if xtot > 0 else -90, 'X_Liq', 'blue')])
    })

    # ---------------------------------------------------------
    # --- QUESTÕES INVERSAS (16 a 20)
    # ---------------------------------------------------------
    q = sortear()
    xl16 = 2 * math.pi * q['f'] * (q['l'] / 1000)
    z16 = math.hypot(q['r'], xl16)
    i16 = q['v'] / z16
    dados.append({
        'pergunta': f"Em um circuito RL série ({q['v']}V, {q['f']}Hz), o indutor é de {q['l']}mH e a corrente medida é de {i16:.2f}A. Calcule a resistência do resistor.",
        'resposta': f"<strong>R</strong> = {q['r']} Ω",
        'grafico': plot_fasores(
            [(q['v'], 0, 'V', 'black'), (i16, -math.degrees(math.atan2(xl16, q['r'])), 'I', 'blue')])
    })

    q = sortear()
    ir17 = q['v'] / q['r']
    xc17 = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    ic17 = q['v'] / xc17
    it17 = math.hypot(ir17, ic17)
    dados.append({
        'pergunta': f"Um circuito RC paralelo é alimentado por {q['v']}V / {q['f']}Hz. O resistor possui {q['r']}Ω e a corrente total é de {it17:.2f}A. Determine a capacitância em μF.",
        'resposta': f"<strong>C</strong> = {q['c']} μF",
        'grafico': plot_fasores([(ir17, 0, 'IR', 'green'), (ic17, 90, 'IC', 'red'),
                                 (it17, math.degrees(math.atan2(ic17, ir17)), 'IT', 'blue')])
    })

    q = sortear()
    fr18 = 1 / (2 * math.pi * math.sqrt((q['l'] / 1000) * (q['c'] / 1000000)))
    dados.append({
        'pergunta': f"Deseja-se sintonizar um RLC série para ressonância exata em {fr18:.1f}Hz. Se o capacitor tem {q['c']}μF, qual deve ser a indutância (mH)?",
        'resposta': f"<strong>L</strong> = {q['l']} mH",
        'grafico': plot_fasores([(1, 90, 'XL', 'red'), (1, -90, 'XC', 'orange')])
    })

    q = sortear()
    xl19 = 2 * math.pi * q['f'] * (q['l'] / 1000)
    z19 = math.hypot(q['r'], xl19)
    i19 = q['v'] / z19
    vr19, vl19 = i19 * q['r'], i19 * xl19
    dados.append({
        'pergunta': f"Em um RL série ({q['f']}Hz), a queda no indutor de {q['l']}mH é {vl19:.2f}V e no resistor é {vr19:.2f}V. Determine a corrente, R e a tensão da fonte (V).",
        'resposta': f"<strong>I</strong>={i19:.2f}A, <strong>R</strong>={q['r']}Ω, <strong>V_Fonte</strong>={q['v']}V",
        'grafico': plot_fasores([(vr19, 0, 'VR', 'green'), (vl19, 90, 'VL', 'red'),
                                 (q['v'], math.degrees(math.atan2(vl19, vr19)), 'V_Fonte', 'black')])
    })

    q = sortear()
    xc20 = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
    pot_ativa = (q['v'] ** 2) / q['r']
    pot_reativa = (q['v'] ** 2) / xc20
    dados.append({
        'pergunta': f"Um RC paralelo ({q['v']}V, {q['f']}Hz) consome P = {pot_ativa:.1f}W e Qc = {pot_reativa:.1f}VAr. Calcule os valores do resistor (Ω) e capacitor (μF).",
        'resposta': f"<strong>R</strong> = {q['r']} Ω <br> <strong>C</strong> = {q['c']} μF",
        'grafico': plot_fasores([(pot_ativa, 0, 'P(W)', 'green'), (pot_reativa, -90, 'Qc(VAr)', 'red'),
                                 (math.hypot(pot_ativa, pot_reativa), math.degrees(math.atan2(-pot_reativa, pot_ativa)),
                                  'S(VA)', 'blue')])
    })

    return render_template('exercicios.html', dados=dados)
# ==========================================
# === CÁLCULOS: MÓDULO RL ==================
# ==========================================
@app.route('/calcular_serie', methods=['POST'])
def calcular_serie():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        l_mh = float(dados.get('l'))
        f = float(dados.get('f'))

        if f <= 0:
            return jsonify({'sucesso': False, 'erro': 'A frequência deve ser maior que zero.'})

        l = l_mh / 1000.0
        w = 2 * math.pi * f
        xl = w * l
        z_mag = math.sqrt(r ** 2 + xl ** 2)
        i_mag = v / z_mag if z_mag != 0 else 0
        vr_mag = i_mag * r
        vl_mag = i_mag * xl

        return jsonify({
            'sucesso': True,
            'xl': round(xl, 2),
            'i': round(i_mag, 2),
            'vr': round(vr_mag, 2),
            'vl': round(vl_mag, 2)
        })
    except (TypeError, ValueError):
        return jsonify({'sucesso': False, 'erro': 'Valores inválidos.'})


@app.route('/calcular_paralelo', methods=['POST'])
def calcular_paralelo():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        l_mh = float(dados.get('l'))
        f = float(dados.get('f'))

        if f <= 0 or r == 0 or l_mh == 0:
            return jsonify({'sucesso': False, 'erro': 'R, L e Frequência devem ser maiores que zero.'})

        l = l_mh / 1000.0
        w = 2 * math.pi * f
        xl = w * l
        ir_mag = v / r
        il_mag = v / xl
        it_mag = math.sqrt(ir_mag ** 2 + il_mag ** 2)

        return jsonify({
            'sucesso': True,
            'xl': round(xl, 2),
            'it': round(it_mag, 2),
            'ir': round(ir_mag, 2),
            'il': round(il_mag, 2)
        })
    except (TypeError, ValueError):
        return jsonify({'sucesso': False, 'erro': 'Valores inválidos.'})


# ==========================================
# === CÁLCULOS: MÓDULO RC ==================
# ==========================================
@app.route('/calcular_rc_serie', methods=['POST'])
def calcular_rc_serie():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        c_uf = float(dados.get('c'))
        f = float(dados.get('f'))

        if f <= 0 or c_uf <= 0:
            return jsonify({'sucesso': False, 'erro': 'Frequência e Capacitância devem ser > 0.'})

        c = c_uf * 1e-6
        w = 2 * math.pi * f
        xc = 1 / (w * c)

        z_mag = math.sqrt(r ** 2 + xc ** 2)
        i_mag = v / z_mag if z_mag != 0 else 0
        vr_mag = i_mag * r
        vc_mag = i_mag * xc

        return jsonify({
            'sucesso': True,
            'xc': round(xc, 2),
            'i': round(i_mag, 3),
            'vr': round(vr_mag, 2),
            'vc': round(vc_mag, 2)
        })
    except (TypeError, ValueError):
        return jsonify({'sucesso': False, 'erro': 'Valores inválidos.'})


@app.route('/calcular_rc_paralelo', methods=['POST'])
def calcular_rc_paralelo():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        c_uf = float(dados.get('c'))
        f = float(dados.get('f'))

        if f <= 0 or r == 0 or c_uf <= 0:
            return jsonify({'sucesso': False, 'erro': 'Valores devem ser maiores que zero.'})

        c = c_uf * 1e-6
        w = 2 * math.pi * f
        xc = 1 / (w * c)

        ir_mag = v / r
        ic_mag = v / xc
        it_mag = math.sqrt(ir_mag ** 2 + ic_mag ** 2)

        return jsonify({
            'sucesso': True,
            'xc': round(xc, 2),
            'it': round(it_mag, 3),
            'ir': round(ir_mag, 3),
            'ic': round(ic_mag, 3)
        })
    except (TypeError, ValueError):
        return jsonify({'sucesso': False, 'erro': 'Valores inválidos.'})


# ==========================================
# === GRÁFICOS: MÓDULO RL ==================
# ==========================================
@app.route('/graficos_serie', methods=['POST'])
def graficos_serie():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        l_mh = float(dados.get('l'))
        f = float(dados.get('f'))

        if f <= 0 or v == 0 or (r == 0 and l_mh == 0):
            return jsonify({'sucesso': False, 'erro': 'Valores inválidos para gráficos.'})

        l = l_mh / 1000.0
        w = 2 * math.pi * f
        xl = w * l

        z_mag = math.sqrt(r ** 2 + xl ** 2)
        theta_rad = math.atan2(xl, r)
        theta_deg = math.degrees(theta_rad)
        i_mag = v / z_mag if z_mag != 0 else 0
        fator_escala = round(z_mag, 1)

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        periodo_ms = periodo * 1000
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        i_t_escalada = (i_mag * fator_escala) * np.sin(w * t - theta_rad)
        vr_t = (i_mag * r) * np.sin(w * t - theta_rad)
        vl_t = (i_mag * xl) * np.sin(w * t - theta_rad + np.pi / 2)

        ax1.plot(t_ms, v_t, label='V (Fonte)', color='blue', linewidth=2)
        ax1.plot(t_ms, i_t_escalada, label=f'I (escala x{fator_escala})', color='red', linestyle='--')
        ax1.plot(t_ms, vr_t, label='VR', color='green')
        ax1.plot(t_ms, vl_t, label='VL', color='purple')
        ax1.set_title("Domínio do Tempo", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V (0.0°)')

        vr_x = (i_mag * r) * math.cos(-theta_rad)
        vr_y = (i_mag * r) * math.sin(-theta_rad)
        ax2.quiver(0, 0, vr_x, vr_y, angles='xy', scale_units='xy', scale=1, color='green',
                   label=f'VR ({-theta_deg:.1f}°)')

        vl_x = (i_mag * xl) * math.cos(-theta_rad + np.pi / 2)
        vl_y = (i_mag * xl) * math.sin(-theta_rad + np.pi / 2)
        ax2.quiver(0, 0, vl_x, vl_y, angles='xy', scale_units='xy', scale=1, color='purple',
                   label=f'VL ({-theta_deg + 90:.1f}°)')

        i_x = (i_mag * fator_escala) * math.cos(-theta_rad)
        i_y = (i_mag * fator_escala) * math.sin(-theta_rad)
        ax2.quiver(0, 0, i_x, i_y, angles='xy', scale_units='xy', scale=1, color='red',
                   label=f'I (x{fator_escala}) ({-theta_deg:.1f}°)', width=0.005)

        limite = max(v, i_mag * xl, i_mag * r) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        ax2.legend(loc='upper right')

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return jsonify({'sucesso': True, 'imagem': img_base64})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})


@app.route('/graficos_paralelo', methods=['POST'])
def graficos_paralelo():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        l_mh = float(dados.get('l'))
        f = float(dados.get('f'))

        if f <= 0 or v == 0 or r == 0 or l_mh == 0:
            return jsonify({'sucesso': False, 'erro': 'Valores inválidos para gráficos.'})

        l = l_mh / 1000.0
        w = 2 * math.pi * f
        xl = w * l

        ir_mag = v / r
        il_mag = v / xl
        it_mag = math.sqrt(ir_mag ** 2 + il_mag ** 2)

        theta_rad = math.atan2(il_mag, ir_mag)
        theta_deg = math.degrees(theta_rad)
        z_eq = v / it_mag if it_mag != 0 else 1
        fator_escala = round(z_eq, 1)

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        periodo_ms = periodo * 1000
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        ir_t = (ir_mag * fator_escala) * np.sin(w * t)
        il_t = (il_mag * fator_escala) * np.sin(w * t - np.pi / 2)
        it_t = (it_mag * fator_escala) * np.sin(w * t - theta_rad)

        ax1.plot(t_ms, v_t, label='V (Referência)', color='blue', linewidth=2)
        ax1.plot(t_ms, it_t, label=f'IT (escala x{fator_escala})', color='red', linestyle='--')
        ax1.plot(t_ms, ir_t, label='IR', color='green')
        ax1.plot(t_ms, il_t, label='IL', color='purple')
        ax1.set_title("Domínio do Tempo (Paralelo)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label='V (0.0°)')
        ax2.quiver(0, 0, ir_mag * fator_escala, 0, angles='xy', scale_units='xy', scale=1, color='green',
                   label='IR (0.0°)')
        ax2.quiver(0, 0, 0, -il_mag * fator_escala, angles='xy', scale_units='xy', scale=1, color='purple',
                   label='IL (-90.0°)')

        it_x = (it_mag * fator_escala) * math.cos(-theta_rad)
        it_y = (it_mag * fator_escala) * math.sin(-theta_rad)
        ax2.quiver(0, 0, it_x, it_y, angles='xy', scale_units='xy', scale=1, color='red',
                   label=f'IT (x{fator_escala}) ({-theta_deg:.1f}°)', width=0.005)

        limite = max(v, ir_mag * fator_escala, il_mag * fator_escala) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        ax2.legend(loc='upper right')

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return jsonify({'sucesso': True, 'imagem': img_base64})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})


# ==========================================
# === GRÁFICOS: MÓDULO RC ==================
# ==========================================
@app.route('/graficos_rc_serie', methods=['POST'])
def graficos_rc_serie():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        c_uf = float(dados.get('c'))
        f = float(dados.get('f'))

        if f <= 0 or v == 0 or (r == 0 and c_uf == 0):
            return jsonify({'sucesso': False, 'erro': 'Valores inválidos para gráficos.'})

        c = c_uf * 1e-6
        w = 2 * math.pi * f
        xc = 1 / (w * c) if c != 0 else float('inf')

        z_mag = math.sqrt(r ** 2 + xc ** 2)
        theta_rad = math.atan2(xc, r)
        theta_deg = math.degrees(theta_rad)

        i_mag = v / z_mag if z_mag != 0 else 0
        fator_escala = round(z_mag, 1)

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        i_t_escalada = (i_mag * fator_escala) * np.sin(w * t + theta_rad)
        vr_t = (i_mag * r) * np.sin(w * t + theta_rad)
        vc_t = (i_mag * xc) * np.sin(w * t + theta_rad - np.pi / 2)

        ax1.plot(t_ms, v_t, label='V (Fonte)', color='blue', linewidth=2)
        ax1.plot(t_ms, i_t_escalada, label=f'I (escala x{fator_escala})', color='red', linestyle='--')
        ax1.plot(t_ms, vr_t, label='VR', color='green')
        ax1.plot(t_ms, vc_t, label='VC', color='orange')

        ax1.set_title("Domínio do Tempo (RC Série)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude")
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label='V (0.0°)')

        vr_x = (i_mag * r) * math.cos(theta_rad)
        vr_y = (i_mag * r) * math.sin(theta_rad)
        ax2.quiver(0, 0, vr_x, vr_y, angles='xy', scale_units='xy', scale=1, color='green',
                   label=f'VR ({theta_deg:.1f}°)')

        i_x = (i_mag * fator_escala) * math.cos(theta_rad)
        i_y = (i_mag * fator_escala) * math.sin(theta_rad)
        ax2.quiver(0, 0, i_x, i_y, angles='xy', scale_units='xy', scale=1, color='red',
                   label=f'I (x{fator_escala}) ({theta_deg:.1f}°)', width=0.005)

        vc_x = (i_mag * xc) * math.cos(theta_rad - np.pi / 2)
        vc_y = (i_mag * xc) * math.sin(theta_rad - np.pi / 2)
        ax2.quiver(0, 0, vc_x, vc_y, angles='xy', scale_units='xy', scale=1, color='orange',
                   label=f'VC ({theta_deg - 90:.1f}°)')

        limite = max(v, i_mag * xc, i_mag * r) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        ax2.legend(loc='upper right')

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return jsonify({'sucesso': True, 'imagem': img_base64})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})


@app.route('/graficos_rc_paralelo', methods=['POST'])
def graficos_rc_paralelo():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        c_uf = float(dados.get('c'))
        f = float(dados.get('f'))

        if f <= 0 or v == 0 or r == 0 or c_uf == 0:
            return jsonify({'sucesso': False, 'erro': 'Valores inválidos para gráficos.'})

        c = c_uf * 1e-6
        w = 2 * math.pi * f
        xc = 1 / (w * c)

        ir_mag = v / r
        ic_mag = v / xc
        it_mag = math.sqrt(ir_mag ** 2 + ic_mag ** 2)
        theta_rad = math.atan2(ic_mag, ir_mag)
        theta_deg = math.degrees(theta_rad)

        z_eq = v / it_mag if it_mag != 0 else 1
        fator_escala = round(z_eq, 1)

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        ir_t = (ir_mag * fator_escala) * np.sin(w * t)
        ic_t = (ic_mag * fator_escala) * np.sin(w * t + np.pi / 2)
        it_t = (it_mag * fator_escala) * np.sin(w * t + theta_rad)

        ax1.plot(t_ms, v_t, label='V (Referência)', color='blue', linewidth=2)
        ax1.plot(t_ms, it_t, label=f'IT (escala x{fator_escala})', color='red', linestyle='--')
        ax1.plot(t_ms, ir_t, label='IR', color='green')
        ax1.plot(t_ms, ic_t, label='IC', color='orange')
        ax1.set_title("Domínio do Tempo (RC Paralelo)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude")
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label='V (0.0°)')
        ax2.quiver(0, 0, ir_mag * fator_escala, 0, angles='xy', scale_units='xy', scale=1, color='green',
                   label='IR (0.0°)')
        ax2.quiver(0, 0, 0, ic_mag * fator_escala, angles='xy', scale_units='xy', scale=1, color='orange',
                   label='IC (90.0°)')

        it_x = (it_mag * fator_escala) * math.cos(theta_rad)
        it_y = (it_mag * fator_escala) * math.sin(theta_rad)
        ax2.quiver(0, 0, it_x, it_y, angles='xy', scale_units='xy', scale=1, color='red',
                   label=f'IT (x{fator_escala}) ({theta_deg:.1f}°)', width=0.005)

        limite = max(v, ir_mag * fator_escala, ic_mag * fator_escala) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        ax2.legend(loc='upper right')

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return jsonify({'sucesso': True, 'imagem': img_base64})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})
import math

@app.route('/calcular_rlc_serie', methods=['POST'])
def calcular_rlc_serie():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        # Conversão de unidades (mH para H e µF para F)
        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * math.pi * f

        # Cálculos Matemáticos
        xl = w * l
        xc = 1 / (w * c)
        z = math.sqrt(r**2 + (xl - xc)**2)
        i = v / z

        return jsonify({
            'sucesso': True,
            'z': f"{z:.2f}",
            'i': f"{i:.2f}",
            'xl': f"{xl:.2f}",
            'xc': f"{xc:.2f}"
        })
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})

@app.route('/calcular_rlc_paralelo', methods=['POST'])
def calcular_rlc_paralelo():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        # Conversão de unidades
        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * math.pi * f

        # Cálculos Matemáticos
        xl = w * l
        xc = 1 / (w * c)
        ir = v / r
        il = v / xl
        ic = v / xc
        it = math.sqrt(ir**2 + (il - ic)**2)
        z = v / it

        return jsonify({
            'sucesso': True,
            'z': f"{z:.2f}",
            'it': f"{it:.2f}",
            'il': f"{il:.2f}",
            'ic': f"{ic:.2f}"
        })
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})


@app.route('/graficos_rlc_serie', methods=['POST'])
def graficos_rlc_serie():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        # Cálculos base
        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * np.pi * f

        xl = w * l
        xc = 1 / (w * c)
        x_total = xl - xc
        z = math.sqrt(r ** 2 + x_total ** 2)

        i = v / z
        vr = i * r
        vl = i * xl
        vc = i * xc

        # Ângulo de defasagem da Tensão Total em relação à Corrente
        theta = math.degrees(math.atan2(vl - vc, vr))

        # Criar imagem com 2 gráficos lado a lado
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # ==========================================
        # GRÁFICO 1: Triângulo de Impedância
        # ==========================================
        ax1.quiver(0, 0, r, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'R = {r:.1f} Ω')
        ax1.quiver(r, 0, 0, x_total, angles='xy', scale_units='xy', scale=1, color='red',
                   label=f'X_L - X_C = {x_total:.1f} Ω')
        ax1.quiver(0, 0, r, x_total, angles='xy', scale_units='xy', scale=1, color='green',
                   label=f'Z = {z:.1f} Ω ∠ {theta:.1f}°')

        lim_z = max(r, abs(x_total)) * 1.2
        ax1.set_xlim(-0.1 * lim_z, lim_z)
        ax1.set_ylim(-lim_z if x_total < 0 else -0.1 * lim_z, lim_z if x_total > 0 else 0.1 * lim_z)
        ax1.grid(True, linestyle='--', alpha=0.6)
        ax1.axhline(0, color='black', linewidth=1)
        ax1.axvline(0, color='black', linewidth=1)
        ax1.set_title('Triângulo de Impedância')
        ax1.legend(loc='lower left')

        # ==========================================
        # GRÁFICO 2: Fasores (Com Escala e Ângulos)
        # ==========================================
        # Fator de escala para a Corrente I aparecer visível junto com as dezenas/centenas de Volts
        max_v = max(v, vr, vl, vc)
        fator_escala_i = (max_v * 0.7) / i if i > 0 else 1

        # A corrente I é a referência (ângulo 0)
        ax2.quiver(0, 0, i * fator_escala_i, 0, angles='xy', scale_units='xy', scale=1, color='purple', width=0.005,
                   label=f'I = {i:.2f} A ∠ 0° (Ref, esc. x{fator_escala_i:.1f})')
        ax2.quiver(0, 0, vr, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V_R = {vr:.1f} V ∠ 0°')
        ax2.quiver(0, 0, 0, vl, angles='xy', scale_units='xy', scale=1, color='orange',
                   label=f'V_L = {vl:.1f} V ∠ +90°')
        ax2.quiver(0, 0, 0, -vc, angles='xy', scale_units='xy', scale=1, color='cyan', label=f'V_C = {vc:.1f} V ∠ -90°')
        ax2.quiver(0, 0, vr, vl - vc, angles='xy', scale_units='xy', scale=1, color='green',
                   label=f'V_T = {v:.1f} V ∠ {theta:.1f}°')

        lim_v = max(max_v, i * fator_escala_i) * 1.2
        ax2.set_xlim(-0.1 * lim_v, lim_v)
        ax2.set_ylim(-lim_v, lim_v)
        ax2.grid(True, linestyle='--', alpha=0.6)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title('Diagrama Fasorial (Série)')
        ax2.legend(loc='lower left')

        # Salvar e enviar
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return jsonify({'sucesso': True, 'imagem': img_base64})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})


@app.route('/graficos_rlc_paralelo', methods=['POST'])
def graficos_rlc_paralelo():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        # Cálculos base
        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * np.pi * f

        xl = w * l
        xc = 1 / (w * c)

        ir = v / r
        il = v / xl
        ic = v / xc
        i_reativa = ic - il
        it = math.sqrt(ir ** 2 + i_reativa ** 2)

        # Ângulo de defasagem da Corrente Total em relação à Tensão
        theta = math.degrees(math.atan2(ic - il, ir))

        # Criar imagem com 2 gráficos lado a lado
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # ==========================================
        # GRÁFICO 1: Triângulo de Correntes
        # ==========================================
        ax1.quiver(0, 0, ir, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'I_R = {ir:.2f} A')
        ax1.quiver(ir, 0, 0, i_reativa, angles='xy', scale_units='xy', scale=1, color='red',
                   label=f'I_C - I_L = {i_reativa:.2f} A')
        ax1.quiver(0, 0, ir, i_reativa, angles='xy', scale_units='xy', scale=1, color='green',
                   label=f'I_T = {it:.2f} A ∠ {theta:.1f}°')

        lim_i = max(ir, abs(i_reativa)) * 1.2
        ax1.set_xlim(-0.1 * lim_i, lim_i)
        ax1.set_ylim(-lim_i if i_reativa < 0 else -0.1 * lim_i, lim_i if i_reativa > 0 else 0.1 * lim_i)
        ax1.grid(True, linestyle='--', alpha=0.6)
        ax1.axhline(0, color='black', linewidth=1)
        ax1.axvline(0, color='black', linewidth=1)
        ax1.set_title('Triângulo de Correntes')
        ax1.legend(loc='lower left')

        # ==========================================
        # GRÁFICO 2: Fasores (Com Escala e Ângulos)
        # ==========================================
        # Fator de escala para a Tensão V aparecer visível junto com as pequenas Correntes
        max_i = max(it, ir, ic, il)
        fator_escala_v = (max_i * 0.7) / v if v > 0 else 1

        # A tensão V é a referência (ângulo 0)
        ax2.quiver(0, 0, v * fator_escala_v, 0, angles='xy', scale_units='xy', scale=1, color='purple', width=0.005,
                   label=f'V = {v:.1f} V ∠ 0° (Ref, esc. x{fator_escala_v:.2f})')
        ax2.quiver(0, 0, ir, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'I_R = {ir:.2f} A ∠ 0°')
        ax2.quiver(0, 0, 0, ic, angles='xy', scale_units='xy', scale=1, color='orange',
                   label=f'I_C = {ic:.2f} A ∠ +90°')
        ax2.quiver(0, 0, 0, -il, angles='xy', scale_units='xy', scale=1, color='cyan', label=f'I_L = {il:.2f} A ∠ -90°')
        ax2.quiver(0, 0, ir, i_reativa, angles='xy', scale_units='xy', scale=1, color='green',
                   label=f'I_T = {it:.2f} A ∠ {theta:.1f}°')

        lim_fasor = max(v * fator_escala_v, max_i) * 1.2
        ax2.set_xlim(-0.1 * lim_fasor, lim_fasor)
        ax2.set_ylim(-max(il, abs(i_reativa)) * 1.2, max(ic, abs(i_reativa)) * 1.2)
        ax2.grid(True, linestyle='--', alpha=0.6)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title('Diagrama Fasorial (Paralelo)')
        ax2.legend(loc='lower left')

        # Salvar e enviar
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return jsonify({'sucesso': True, 'imagem': img_base64})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})

if __name__ == '__main__':
    app.run(debug=True)