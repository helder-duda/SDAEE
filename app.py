import matplotlib
matplotlib.use('Agg')  # Configura o Matplotlib para rodar em modo servidor (sem Tkinter)

# Seus outros imports continuam abaixo normalmente...
import matplotlib.pyplot as plt
from flask import Flask
import base64
import io
import math
import random
import cmath
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User  # Importa o banco do seu arquivo models.py

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
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

# ==========================================
# === ROTAS DE LOGIN E PROTEÇÃO ============
# ==========================================
@app.route('/')
@login_required
def index():
    return render_template('index.html')

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

@app.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro():
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem cadastrar novos usuários.')
        return redirect(url_for('index'))

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

        if not check_password_hash(current_user.password, senha_atual):
            flash('Erro: A senha atual está incorreta.')
            return redirect(url_for('alterar_senha'))

        if nova_senha != confirmar_senha:
            flash('Erro: A nova senha e a confirmação não coincidem.')
            return redirect(url_for('alterar_senha'))

        current_user.password = generate_password_hash(nova_senha)
        db.session.commit()

        flash('Senha alterada com sucesso!')
        return redirect(url_for('index'))

    return render_template('alterar_senha.html')

import cmath
import math
def formatar_complexo(val):
    """
    Converte um número complexo em um dicionário com representação
    polar e retangular formatadas para exibição no frontend.
    """
    if val is None:
        return {"polar": "0 ∠ 0°", "retangular": "0 + 0j"}

    mod = abs(val)
    # Converte o ângulo de radianos para graus
    ang = math.degrees(cmath.phase(val))

    # Formatação do sinal do imaginário
    sinal = "+" if val.imag >= 0 else "-"
    real_str = f"{val.real:.2f}"
    imag_str = f"{abs(val.imag):.2f}"

    return {
        "polar": f"{mod:.2f} ∠ {ang:.2f}°",
        "retangular": f"{real_str} {sinal} {imag_str}j",
        "mod": round(mod, 2),
        "ang": round(ang, 2),
        "real": round(val.real, 2),
        "imag": round(val.imag, 2)
    }

# ==========================================
# === ROTA DE GERAÇÃO DE EXERCÍCIOS =======
# ==========================================
@app.route('/gerar_exercicios')
@login_required
def gerar_exercicios():
    qtd = int(request.args.get('qtd', 20))
    tipo_selecionado = request.args.get('tipo', 'todos').upper()

    def sortear():
        return {
            'v': random.choice([12, 24, 110, 127, 220]),
            'f': random.choice([50, 60, 400]),
            'r': random.randint(2, 50) * 10,
            'l': random.randint(10, 500),
            'c': random.randint(5, 100)
        }

    def plot_fasores(fasores):
        if not fasores:
            return None
        plt.figure(figsize=(3, 3))
        ax = plt.subplot(111)
        angulos_usados = {}

        for mag, ang, label, color in fasores:
            if mag == 0:
                continue
            ang_arredondado = round(ang, 1)
            angulos_usados[ang_arredondado] = angulos_usados.get(ang_arredondado, 0) + 1
            plot_mag = 1.0 - (angulos_usados[ang_arredondado] - 1) * 0.22
            rad = math.radians(ang)
            x = plot_mag * math.cos(rad)
            y = plot_mag * math.sin(rad)
            ax.annotate("", xy=(x, y), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=color, lw=2))
            offset = 1.35
            ax.text(x * offset, y * offset, f"{label}", color=color, ha='center', va='center', fontsize=9, fontweight='bold')

        limit = 1.5
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.set_aspect('equal')
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

    questoes_rl = []
    questoes_rc = []
    questoes_rlc = []

    for _ in range(40):
        q = sortear()
        xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
        z_mag = math.hypot(q['r'], xl)
        z_ang = math.degrees(math.atan2(xl, q['r']))
        i_mag = q['v'] / z_mag
        i_ang = -z_ang
        questoes_rl.append({
            'pergunta': f"Em um circuito RL série, uma fonte de {q['v']}V e frequência {q['f']}Hz alimenta um resistor de {q['r']}Ω e um indutor de {q['l']}mH. Calcule a impedância total (Z) e a corrente do circuito.",
            'resposta': f"<strong>Z</strong> = {z_mag:.2f}Ω ∠{z_ang:.1f}° <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}°",
            'grafico': plot_fasores([(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I', 'blue')])
        })

        q = sortear()
        xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
        z_mag = math.hypot(q['r'], xc)
        z_ang = math.degrees(math.atan2(-xc, q['r']))
        i_mag = q['v'] / z_mag
        i_ang = -z_ang
        questoes_rc.append({
            'pergunta': f"Dado um circuito RC série com R = {q['r']}Ω e C = {q['c']}μF, alimentado por {q['v']}V a {q['f']}Hz. Encontre a reatância capacitiva (Xc) e a corrente total.",
            'resposta': f"<strong>Xc</strong> = {xc:.2f}Ω <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}°",
            'grafico': plot_fasores([(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I', 'blue')])
        })

        q = sortear()
        xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
        xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
        x_tot = xl - xc
        z_mag = math.hypot(q['r'], x_tot)
        z_ang = math.degrees(math.atan2(x_tot, q['r']))
        i_mag = q['v'] / z_mag
        i_ang = -z_ang
        questoes_rlc.append({
            'pergunta': f"Um resistor de {q['r']}Ω, um indutor de {q['l']}mH e um capacitor de {q['c']}μF estão ligados em série. A fonte fornece {q['v']}V em {q['f']}Hz. Qual é a impedância do circuito e a corrente total?",
            'resposta': f"<strong>Z</strong> = {z_mag:.2f}Ω ∠{z_ang:.1f}° <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}°",
            'grafico': plot_fasores([(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I', 'blue')])
        })

        q = sortear()
        xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
        ir_mag = q['v'] / q['r']
        il_mag = q['v'] / xl
        i_mag = math.hypot(ir_mag, il_mag)
        i_ang = math.degrees(math.atan2(-il_mag, ir_mag))
        z_mag = q['v'] / i_mag
        z_ang = -i_ang
        questoes_rl.append({
            'pergunta': f"Em um circuito RL paralelo, uma fonte de {q['v']}V e frequência {q['f']}Hz alimenta um resistor de {q['r']}Ω e um indutor de {q['l']}mH. Calcule a impedância total equivalente (Z) e a corrente total do circuito.",
            'resposta': f"<strong>Z</strong> = {z_mag:.2f}Ω ∠{z_ang:.1f}° <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}° <br> (I_R = {ir_mag:.2f}A ∠0°, I_L = {il_mag:.2f}A ∠-90°)",
            'grafico': plot_fasores(
                [(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I_tot', 'blue'), (ir_mag, 0, 'Ir', 'green'),
                 (il_mag, -90, 'Il', 'purple')])
        })

        q = sortear()
        xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
        ir_mag = q['v'] / q['r']
        ic_mag = q['v'] / xc
        i_mag = math.hypot(ir_mag, ic_mag)
        i_ang = math.degrees(math.atan2(ic_mag, ir_mag))
        z_mag = q['v'] / i_mag
        z_ang = -i_ang
        questoes_rc.append({
            'pergunta': f"Dado um circuito RC paralelo com R = {q['r']}Ω e C = {q['c']}μF, alimentado por {q['v']}V a {q['f']}Hz. Encontre a reatância capacitiva (Xc), a impedância equivalente (Z) e a corrente total.",
            'resposta': f"<strong>Xc</strong> = {xc:.2f}Ω <br> <strong>Z</strong> = {z_mag:.2f}Ω ∠{z_ang:.1f}° <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}° <br> (I_R = {ir_mag:.2f}A ∠0°, I_C = {ic_mag:.2f}A ∠90°)",
            'grafico': plot_fasores(
                [(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I_tot', 'blue'), (ir_mag, 0, 'Ir', 'green'),
                 (ic_mag, 90, 'Ic', 'orange')])
        })

        q = sortear()
        xl = 2 * math.pi * q['f'] * (q['l'] / 1000)
        xc = 1 / (2 * math.pi * q['f'] * (q['c'] / 1000000))
        ir_mag = q['v'] / q['r']
        il_mag = q['v'] / xl
        ic_mag = q['v'] / xc
        i_reativa = ic_mag - il_mag
        i_mag = math.hypot(ir_mag, i_reativa)
        i_ang = math.degrees(math.atan2(i_reativa, ir_mag))
        z_mag = q['v'] / i_mag
        z_ang = -i_ang
        questoes_rlc.append({
            'pergunta': f"Um resistor de {q['r']}Ω, um indutor de {q['l']}mH e um capacitor de {q['c']}μF estão ligados em paralelo. A fonte fornece {q['v']}V em {q['f']}Hz. Qual é a impedância equivalente do circuito e a corrente total?",
            'resposta': f"<strong>Z</strong> = {z_mag:.2f}Ω ∠{z_ang:.1f}° <br> <strong>I</strong> = {i_mag:.2f}A ∠{i_ang:.1f}° <br> (I_R = {ir_mag:.2f}A ∠0°, I_L = {il_mag:.2f}A ∠-90°, I_C = {ic_mag:.2f}A ∠90°)",
            'grafico': plot_fasores(
                [(q['v'], 0, 'V', 'black'), (i_mag, i_ang, 'I_tot', 'blue'), (ir_mag, 0, 'Ir', 'green'),
                 (il_mag, -90, 'Il', 'purple'), (ic_mag, 90, 'Ic', 'orange')])
        })

    banco_filtrado = []
    if tipo_selecionado == 'RL':
        banco_filtrado = questoes_rl
    elif tipo_selecionado == 'RC':
        banco_filtrado = questoes_rc
    elif tipo_selecionado == 'RLC':
        banco_filtrado = questoes_rlc
    else:
        banco_filtrado = questoes_rl + questoes_rc + questoes_rlc
        random.shuffle(banco_filtrado)

    random.shuffle(banco_filtrado)
    dados_finais = banco_filtrado[:qtd]

    return render_template('exercicios.html', dados=dados_finais, qtd=qtd, tipo=tipo_selecionado)

# ==========================================
# === CÁLCULOS: MÓDULO RL ==================
# ==========================================
@app.route('/calcular_serie', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
# === CÁLCULOS: MÓDULO RLC =================
# ==========================================
@app.route('/calcular_rlc_serie', methods=['POST'])
@login_required
def calcular_rlc_serie():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        if f <= 0 or c_uF <= 0:
            return jsonify({'sucesso': False, 'erro': 'Frequência e Capacitância devem ser maiores que zero.'})

        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * math.pi * f

        xl = w * l
        xc = 1 / (w * c)
        z = math.sqrt(r**2 + (xl - xc)**2)
        i = v / z if z != 0 else 0

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
@login_required
def calcular_rlc_paralelo():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        if f <= 0 or r == 0 or l_mH == 0 or c_uF <= 0:
            return jsonify({'sucesso': False, 'erro': 'Os valores devem ser maiores que zero.'})

        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * math.pi * f

        xl = w * l
        xc = 1 / (w * c)
        ir = v / r
        il = v / xl
        ic = v / xc
        it = math.sqrt(ir**2 + (il - ic)**2)
        z = v / it if it != 0 else 0

        return jsonify({
            'sucesso': True,
            'z': f"{z:.2f}",
            'it': f"{it:.2f}",
            'il': f"{il:.2f}",
            'ic': f"{ic:.2f}"
        })
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})

# ==========================================
# === GRÁFICOS: MÓDULO RL ==================
# ==========================================
@app.route('/graficos_serie', methods=['POST'])
@login_required
def graficos_serie():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        l_mh = float(dados.get('l'))
        f = float(dados.get('f'))

        show_v = dados.get('show_v', True)
        show_vr = dados.get('show_vr', True)
        show_vl = dados.get('show_vl', True)
        show_i = dados.get('show_i', True)

        if f <= 0 or v == 0 or (r == 0 and l_mh == 0):
            return jsonify({'sucesso': False, 'erro': 'Valores inválidos para gráficos.'})

        l = l_mh / 1000.0
        w = 2 * math.pi * f
        xl = w * l

        z_mag = math.sqrt(r ** 2 + xl ** 2)
        theta_rad = math.atan2(xl, r)
        theta_deg = math.degrees(theta_rad)
        i_mag = v / z_mag if z_mag != 0 else 0

        amp_vr = i_mag * r
        amp_vl = i_mag * xl
        min_v_visual = 0.15 * v

        amp_vr_visual = max(amp_vr, min_v_visual) if amp_vr > 0.01 else 0
        amp_vl_visual = max(amp_vl, min_v_visual) if amp_vl > 0.01 else 0

        escala_vr = amp_vr_visual / amp_vr if amp_vr > 0.01 else 1.0
        escala_vl = amp_vl_visual / amp_vl if amp_vl > 0.01 else 1.0

        label_vr = "VR" if escala_vr <= 1.05 else f"VR (escala x{escala_vr:.1f})"
        label_vl = "VL" if escala_vl <= 1.05 else f"VL (escala x{escala_vl:.1f})"

        amp_i_visual = 0.5 * v
        escala_i = amp_i_visual / i_mag if i_mag > 0 else 1.0
        label_i = f"I (escala x{escala_i:.1f})"

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        periodo_ms = periodo * 1000
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        vr_t = amp_vr_visual * np.sin(w * t - theta_rad)
        vl_t = amp_vl_visual * np.sin(w * t - theta_rad + np.pi / 2)
        i_t_escalada = amp_i_visual * np.sin(w * t - theta_rad)

        if show_v:
            ax1.plot(t_ms, v_t, label='V (Fonte)', color='blue', linewidth=2.5)
        if show_vr:
            ax1.plot(t_ms, vr_t, label=label_vr, color='green', linewidth=1.5)
        if show_vl:
            ax1.plot(t_ms, vl_t, label=label_vl, color='purple', linewidth=1.5)
        if show_i:
            ax1.plot(t_ms, i_t_escalada, label=label_i, color='red', linestyle='--', linewidth=2)

        ax1.set_title("Domínio do Tempo (Série)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude Visual")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        if show_v or show_vr or show_vl or show_i:
            ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        if show_v:
            ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V ({v:.1f}V) (0.0°)', width=0.005)
        if show_vr:
            vr_x = amp_vr_visual * math.cos(-theta_rad)
            vr_y = amp_vr_visual * math.sin(-theta_rad)
            ax2.quiver(0, 0, vr_x, vr_y, angles='xy', scale_units='xy', scale=1, color='green', label=f'{label_vr} ({amp_vr:.1f}V) ({-theta_deg:.1f}°)', width=0.005)
        if show_vl:
            vl_x = amp_vl_visual * math.cos(-theta_rad + np.pi / 2)
            vl_y = amp_vl_visual * math.sin(-theta_rad + np.pi / 2)
            ax2.quiver(0, 0, vl_x, vl_y, angles='xy', scale_units='xy', scale=1, color='purple', label=f'{label_vl} ({amp_vl:.1f}V) ({-theta_deg + 90:.1f}°)', width=0.005)
        if show_i:
            i_x = amp_i_visual * math.cos(-theta_rad)
            i_y = amp_i_visual * math.sin(-theta_rad)
            ax2.quiver(0, 0, i_x, i_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'{label_i} ({i_mag:.2f}A) ({-theta_deg:.1f}°)', width=0.008)

        limite = max(v, amp_vr_visual, amp_vl_visual) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial (Série)", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        if show_v or show_vr or show_vl or show_i:
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
@login_required
def graficos_paralelo():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        l_mh = float(dados.get('l'))
        f = float(dados.get('f'))

        show_v = dados.get('show_v', True)
        show_ir = dados.get('show_ir', True)
        show_il = dados.get('show_il', True)
        show_i = dados.get('show_i', True)

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

        amp_it_visual = 0.5 * v
        fator_escala = amp_it_visual / it_mag if it_mag > 0 else 1.0

        amp_ir_visual = ir_mag * fator_escala
        amp_il_visual = il_mag * fator_escala
        min_i_visual = 0.15 * amp_it_visual

        amp_ir_visual_final = max(amp_ir_visual, min_i_visual) if ir_mag > 0.01 else 0
        amp_il_visual_final = max(amp_il_visual, min_i_visual) if il_mag > 0.01 else 0

        escala_ir_final = amp_ir_visual_final / ir_mag if ir_mag > 0.01 else 1.0
        escala_il_final = amp_il_visual_final / il_mag if il_mag > 0.01 else 1.0

        label_it = f"IT (escala x{fator_escala:.1f})"
        label_ir = "IR" if escala_ir_final <= 1.05 else f"IR (escala x{escala_ir_final:.1f})"
        label_il = "IL" if escala_il_final <= 1.05 else f"IL (escala x{escala_il_final:.1f})"

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        periodo_ms = periodo * 1000
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        ir_t = amp_ir_visual_final * np.sin(w * t)
        il_t = amp_il_visual_final * np.sin(w * t - np.pi / 2)
        it_t = amp_it_visual * np.sin(w * t - theta_rad)

        if show_v:
            ax1.plot(t_ms, v_t, label='V (Referência)', color='blue', linewidth=2.5)
        if show_i:
            ax1.plot(t_ms, it_t, label=label_it, color='red', linestyle='--', linewidth=2)
        if show_ir:
            ax1.plot(t_ms, ir_t, label=label_ir, color='green', linewidth=1.5)
        if show_il:
            ax1.plot(t_ms, il_t, label=label_il, color='purple', linewidth=1.5)

        ax1.set_title("Domínio do Tempo (Paralelo)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude Visual")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        if show_v or show_ir or show_il or show_i:
            ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        if show_v:
            ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V ({v:.1f}V) (0.0°)', width=0.005)
        if show_ir:
            ax2.quiver(0, 0, amp_ir_visual_final, 0, angles='xy', scale_units='xy', scale=1, color='green', label=f'{label_ir} ({ir_mag:.2f}A) (0.0°)', width=0.005)
        if show_il:
            ax2.quiver(0, 0, 0, -amp_il_visual_final, angles='xy', scale_units='xy', scale=1, color='purple', label=f'{label_il} ({il_mag:.2f}A) (-90.0°)', width=0.005)
        if show_i:
            it_x = amp_it_visual * math.cos(-theta_rad)
            it_y = amp_it_visual * math.sin(-theta_rad)
            ax2.quiver(0, 0, it_x, it_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'{label_it} ({it_mag:.2f}A) ({-theta_deg:.1f}°)', width=0.008)

        limite = max(v, amp_ir_visual_final, amp_il_visual_final) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial (Paralelo)", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        if show_v or show_ir or show_il or show_i:
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
@login_required
def graficos_rc_serie():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        c_uf = float(dados.get('c'))
        f = float(dados.get('f'))

        show_v = dados.get('show_v', True)
        show_vr = dados.get('show_vr', True)
        show_vc = dados.get('show_vc', True)
        show_i = dados.get('show_i', True)

        if f <= 0 or v == 0 or (r == 0 and c_uf == 0):
            return jsonify({'sucesso': False, 'erro': 'Valores inválidos para gráficos.'})

        c = c_uf * 1e-6
        w = 2 * math.pi * f
        xc = 1 / (w * c) if c != 0 else float('inf')

        z_mag = math.sqrt(r ** 2 + xc ** 2)
        theta_rad = math.atan2(xc, r)
        theta_deg = math.degrees(theta_rad)
        i_mag = v / z_mag if z_mag != 0 else 0

        amp_vr = i_mag * r
        amp_vc = i_mag * xc
        min_v_visual = 0.15 * v

        amp_vr_visual = max(amp_vr, min_v_visual) if amp_vr > 0.01 else 0
        amp_vc_visual = max(amp_vc, min_v_visual) if amp_vc > 0.01 else 0

        escala_vr = amp_vr_visual / amp_vr if amp_vr > 0.01 else 1.0
        escala_vc = amp_vc_visual / amp_vc if amp_vc > 0.01 else 1.0

        label_vr = "VR" if escala_vr <= 1.05 else f"VR (escala x{escala_vr:.1f})"
        label_vc = "VC" if escala_vc <= 1.05 else f"VC (escala x{escala_vc:.1f})"

        amp_i_visual = 0.5 * v
        escala_i = amp_i_visual / i_mag if i_mag > 0 else 1.0
        label_i = f"I (escala x{escala_i:.1f})"

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        periodo_ms = periodo * 1000
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        vr_t = amp_vr_visual * np.sin(w * t + theta_rad)
        vc_t = amp_vc_visual * np.sin(w * t + theta_rad - np.pi / 2)
        i_t_escalada = amp_i_visual * np.sin(w * t + theta_rad)

        if show_v:
            ax1.plot(t_ms, v_t, label='V (Fonte)', color='blue', linewidth=2.5)
        if show_vr:
            ax1.plot(t_ms, vr_t, label=label_vr, color='green', linewidth=1.5)
        if show_vc:
            ax1.plot(t_ms, vc_t, label=label_vc, color='orange', linewidth=1.5)
        if show_i:
            ax1.plot(t_ms, i_t_escalada, label=label_i, color='red', linestyle='--', linewidth=2)

        ax1.set_title("Domínio do Tempo (RC Série)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude Visual")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        if show_v or show_vr or show_vc or show_i:
            ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        if show_v:
            ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V ({v:.1f}V) (0.0°)', width=0.005)
        if show_vr:
            vr_x = amp_vr_visual * math.cos(theta_rad)
            vr_y = amp_vr_visual * math.sin(theta_rad)
            ax2.quiver(0, 0, vr_x, vr_y, angles='xy', scale_units='xy', scale=1, color='green', label=f'{label_vr} ({amp_vr:.1f}V) ({theta_deg:.1f}°)', width=0.005)
        if show_vc:
            vc_x = amp_vc_visual * math.cos(theta_rad - np.pi / 2)
            vc_y = amp_vc_visual * math.sin(theta_rad - np.pi / 2)
            ax2.quiver(0, 0, vc_x, vc_y, angles='xy', scale_units='xy', scale=1, color='orange', label=f'{label_vc} ({amp_vc:.1f}V) ({theta_deg - 90:.1f}°)', width=0.005)
        if show_i:
            i_x = amp_i_visual * math.cos(theta_rad)
            i_y = amp_i_visual * math.sin(theta_rad)
            ax2.quiver(0, 0, i_x, i_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'{label_i} ({i_mag:.2f}A) ({theta_deg:.1f}°)', width=0.008)

        limite = max(v, amp_vr_visual, amp_vc_visual) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial (RC Série)", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        if show_v or show_vr or show_vc or show_i:
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
@login_required
def graficos_rc_paralelo():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        c_uf = float(dados.get('c'))
        f = float(dados.get('f'))

        show_v = dados.get('show_v', True)
        show_ir = dados.get('show_ir', True)
        show_ic = dados.get('show_ic', True)
        show_i = dados.get('show_i', True)

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

        amp_it_visual = 0.5 * v
        fator_escala = amp_it_visual / it_mag if it_mag > 0 else 1.0

        amp_ir_visual = ir_mag * fator_escala
        amp_ic_visual = ic_mag * fator_escala
        min_i_visual = 0.15 * amp_it_visual

        amp_ir_visual_final = max(amp_ir_visual, min_i_visual) if ir_mag > 0.01 else 0
        amp_ic_visual_final = max(amp_ic_visual, min_i_visual) if ic_mag > 0.01 else 0

        escala_ir_final = amp_ir_visual_final / ir_mag if ir_mag > 0.01 else 1.0
        escala_ic_final = amp_ic_visual_final / ic_mag if ic_mag > 0.01 else 1.0

        label_it = f"IT (escala x{fator_escala:.1f})"
        label_ir = "IR" if escala_ir_final <= 1.05 else f"IR (escala x{escala_ir_final:.1f})"
        label_ic = "IC" if escala_ic_final <= 1.05 else f"IC (escala x{escala_ic_final:.1f})"

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        periodo_ms = periodo * 1000
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        ir_t = amp_ir_visual_final * np.sin(w * t)
        ic_t = amp_ic_visual_final * np.sin(w * t + np.pi / 2)
        it_t = amp_it_visual * np.sin(w * t + theta_rad)

        if show_v:
            ax1.plot(t_ms, v_t, label='V (Referência)', color='blue', linewidth=2.5)
        if show_i:
            ax1.plot(t_ms, it_t, label=label_it, color='red', linestyle='--', linewidth=2)
        if show_ir:
            ax1.plot(t_ms, ir_t, label=label_ir, color='green', linewidth=1.5)
        if show_ic:
            ax1.plot(t_ms, ic_t, label=label_ic, color='orange', linewidth=1.5)

        ax1.set_title("Domínio do Tempo (RC Paralelo)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude Visual")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        if show_v or show_ir or show_ic or show_i:
            ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        if show_v:
            ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V ({v:.1f}V) (0.0°)', width=0.005)
        if show_ir:
            ax2.quiver(0, 0, amp_ir_visual_final, 0, angles='xy', scale_units='xy', scale=1, color='green', label=f'{label_ir} ({ir_mag:.2f}A) (0.0°)', width=0.005)
        if show_ic:
            ax2.quiver(0, 0, 0, amp_ic_visual_final, angles='xy', scale_units='xy', scale=1, color='orange', label=f'{label_ic} ({ic_mag:.2f}A) (90.0°)', width=0.005)
        if show_i:
            it_x = amp_it_visual * math.cos(theta_rad)
            it_y = amp_it_visual * math.sin(theta_rad)
            ax2.quiver(0, 0, it_x, it_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'{label_it} ({it_mag:.2f}A) ({theta_deg:.1f}°)', width=0.008)

        limite = max(v, amp_ir_visual_final, amp_ic_visual_final) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial (RC Paralelo)", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        if show_v or show_ir or show_ic or show_i:
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
# === GRÁFICOS: MÓDULO RLC =================
# ==========================================
@app.route('/graficos_rlc_serie', methods=['POST'])
@login_required
def graficos_rlc_serie():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        show_v = dados.get('show_v', True)
        show_vr = dados.get('show_vr', True)
        show_vl = dados.get('show_vl', True)
        show_vc = dados.get('show_vc', True)
        show_i = dados.get('show_i', True)

        if f <= 0 or v == 0 or (r == 0 and l_mH == 0 and c_uF == 0):
            return jsonify({'sucesso': False, 'erro': 'Valores inválidos para gráficos.'})

        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * np.pi * f

        xl = w * l
        xc = 1 / (w * c) if c != 0 else float('inf')
        x_total = xl - xc
        z = math.sqrt(r ** 2 + x_total ** 2)

        i_mag = v / z if z != 0 else 0
        theta_rad = math.atan2(x_total, r)
        theta_deg = math.degrees(theta_rad)

        amp_vr = i_mag * r
        amp_vl = i_mag * xl
        amp_vc = i_mag * xc
        min_v_visual = 0.15 * v

        amp_vr_visual = max(amp_vr, min_v_visual) if amp_vr > 0.01 else 0
        amp_vl_visual = max(amp_vl, min_v_visual) if amp_vl > 0.01 else 0
        amp_vc_visual = max(amp_vc, min_v_visual) if amp_vc > 0.01 else 0

        escala_vr = amp_vr_visual / amp_vr if amp_vr > 0.01 else 1.0
        escala_vl = amp_vl_visual / amp_vl if amp_vl > 0.01 else 1.0
        escala_vc = amp_vc_visual / amp_vc if amp_vc > 0.01 else 1.0

        label_vr = "VR" if escala_vr <= 1.05 else f"VR (escala x{escala_vr:.1f})"
        label_vl = "VL" if escala_vl <= 1.05 else f"VL (escala x{escala_vl:.1f})"
        label_vc = "VC" if escala_vc <= 1.05 else f"VC (escala x{escala_vc:.1f})"

        amp_i_visual = 0.5 * v
        escala_i = amp_i_visual / i_mag if i_mag > 0 else 1.0
        label_i = f"I (escala x{escala_i:.1f})"

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        periodo_ms = periodo * 1000
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        vr_t = amp_vr_visual * np.sin(w * t - theta_rad)
        vl_t = amp_vl_visual * np.sin(w * t - theta_rad + np.pi / 2)
        vc_t = amp_vc_visual * np.sin(w * t - theta_rad - np.pi / 2)
        i_t_escalada = amp_i_visual * np.sin(w * t - theta_rad)

        if show_v:
            ax1.plot(t_ms, v_t, label='V (Fonte)', color='blue', linewidth=2.5)
        if show_vr:
            ax1.plot(t_ms, vr_t, label=label_vr, color='green', linewidth=1.5)
        if show_vl:
            ax1.plot(t_ms, vl_t, label=label_vl, color='purple', linewidth=1.5)
        if show_vc:
            ax1.plot(t_ms, vc_t, label=label_vc, color='orange', linewidth=1.5)
        if show_i:
            ax1.plot(t_ms, i_t_escalada, label=label_i, color='red', linestyle='--', linewidth=2)

        ax1.set_title("Domínio do Tempo (RLC Série)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude Visual")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        if show_v or show_vr or show_vl or show_vc or show_i:
            ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        if show_v:
            ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V ({v:.1f}V) (0.0°)', width=0.005)
        if show_vr:
            vr_x = amp_vr_visual * math.cos(-theta_rad)
            vr_y = amp_vr_visual * math.sin(-theta_rad)
            ax2.quiver(0, 0, vr_x, vr_y, angles='xy', scale_units='xy', scale=1, color='green', label=f'{label_vr} ({amp_vr:.1f}V) ({-theta_deg:.1f}°)', width=0.005)
        if show_vl:
            vl_x = amp_vl_visual * math.cos(-theta_rad + np.pi / 2)
            vl_y = amp_vl_visual * math.sin(-theta_rad + np.pi / 2)
            ax2.quiver(0, 0, vl_x, vl_y, angles='xy', scale_units='xy', scale=1, color='purple', label=f'{label_vl} ({amp_vl:.1f}V) ({-theta_deg + 90:.1f}°)', width=0.005)
        if show_vc:
            vc_x = amp_vc_visual * math.cos(-theta_rad - np.pi / 2)
            vc_y = amp_vc_visual * math.sin(-theta_rad - np.pi / 2)
            ax2.quiver(0, 0, vc_x, vc_y, angles='xy', scale_units='xy', scale=1, color='orange', label=f'{label_vc} ({amp_vc:.1f}V) ({-theta_deg - 90:.1f}°)', width=0.005)
        if show_i:
            i_x = amp_i_visual * math.cos(-theta_rad)
            i_y = amp_i_visual * math.sin(-theta_rad)
            ax2.quiver(0, 0, i_x, i_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'{label_i} ({i_mag:.2f}A) ({-theta_deg:.1f}°)', width=0.008)

        limite = max(v, amp_vr_visual, amp_vl_visual, amp_vc_visual) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial (RLC Série)", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        if show_v or show_vr or show_vl or show_vc or show_i:
            ax2.legend(loc='upper right')

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
@login_required
def graficos_rlc_paralelo():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        show_v = dados.get('show_v', True)
        show_ir = dados.get('show_ir', True)
        show_il = dados.get('show_il', True)
        show_ic = dados.get('show_ic', True)
        show_i = dados.get('show_i', True)

        if f <= 0 or v == 0 or r == 0 or l_mH == 0 or c_uF == 0:
            return jsonify({'sucesso': False, 'erro': 'Valores inválidos para gráficos.'})

        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * np.pi * f

        xl = w * l
        xc = 1 / (w * c)

        ir_mag = v / r
        il_mag = v / xl
        ic_mag = v / xc
        i_reativa = ic_mag - il_mag
        it_mag = math.sqrt(ir_mag ** 2 + i_reativa ** 2)

        theta_rad = math.atan2(i_reativa, ir_mag)
        theta_deg = math.degrees(theta_rad)

        amp_it_visual = 0.5 * v
        fator_escala = amp_it_visual / it_mag if it_mag > 0 else 1.0

        amp_ir_visual = ir_mag * fator_escala
        amp_il_visual = il_mag * fator_escala
        amp_ic_visual = ic_mag * fator_escala

        min_i_visual = 0.15 * amp_it_visual

        amp_ir_visual_final = max(amp_ir_visual, min_i_visual) if ir_mag > 0.01 else 0
        amp_il_visual_final = max(amp_il_visual, min_i_visual) if il_mag > 0.01 else 0
        amp_ic_visual_final = max(amp_ic_visual, min_i_visual) if ic_mag > 0.01 else 0

        escala_ir_final = amp_ir_visual_final / ir_mag if ir_mag > 0.01 else 1.0
        escala_il_final = amp_il_visual_final / il_mag if il_mag > 0.01 else 1.0
        escala_ic_final = amp_ic_visual_final / ic_mag if ic_mag > 0.01 else 1.0

        label_it = f"IT (escala x{fator_escala:.1f})"
        label_ir = "IR" if escala_ir_final <= 1.05 else f"IR (escala x{escala_ir_final:.1f})"
        label_il = "IL" if escala_il_final <= 1.05 else f"IL (escala x{escala_il_final:.1f})"
        label_ic = "IC" if escala_ic_final <= 1.05 else f"IC (escala x{escala_ic_final:.1f})"

        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121)
        periodo = 1 / f
        periodo_ms = periodo * 1000
        t = np.linspace(0, 2 * periodo, 200)
        t_ms = t * 1000

        v_t = v * np.sin(w * t)
        ir_t = amp_ir_visual_final * np.sin(w * t)
        il_t = amp_il_visual_final * np.sin(w * t - np.pi / 2)
        ic_t = amp_ic_visual_final * np.sin(w * t + np.pi / 2)
        it_t = amp_it_visual * np.sin(w * t + theta_rad)

        if show_v:
            ax1.plot(t_ms, v_t, label='V (Referência)', color='blue', linewidth=2.5)
        if show_i:
            ax1.plot(t_ms, it_t, label=label_it, color='red', linestyle='--', linewidth=2)
        if show_ir:
            ax1.plot(t_ms, ir_t, label=label_ir, color='green', linewidth=1.5)
        if show_il:
            ax1.plot(t_ms, il_t, label=label_il, color='purple', linewidth=1.5)
        if show_ic:
            ax1.plot(t_ms, ic_t, label=label_ic, color='orange', linewidth=1.5)

        ax1.set_title("Domínio do Tempo (RLC Paralelo)", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude Visual")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        if show_v or show_ir or show_il or show_ic or show_i:
            ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        if show_v:
            ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V ({v:.1f}V) (0.0°)', width=0.005)
        if show_ir:
            ax2.quiver(0, 0, amp_ir_visual_final, 0, angles='xy', scale_units='xy', scale=1, color='green', label=f'{label_ir} ({ir_mag:.2f}A) (0.0°)', width=0.005)
        if show_il:
            ax2.quiver(0, 0, 0, -amp_il_visual_final, angles='xy', scale_units='xy', scale=1, color='purple', label=f'{label_il} ({il_mag:.2f}A) (-90.0°)', width=0.005)
        if show_ic:
            ax2.quiver(0, 0, 0, amp_ic_visual_final, angles='xy', scale_units='xy', scale=1, color='orange', label=f'{label_ic} ({ic_mag:.2f}A) (90.0°)', width=0.005)
        if show_i:
            it_x = amp_it_visual * math.cos(theta_rad)
            it_y = amp_it_visual * math.sin(theta_rad)
            ax2.quiver(0, 0, it_x, it_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'{label_it} ({it_mag:.2f}A) ({theta_deg:.1f}°)', width=0.008)

        limite = max(v, amp_ir_visual_final, amp_il_visual_final, amp_ic_visual_final) * 1.2
        ax2.set_xlim(-limite, limite)
        ax2.set_ylim(-limite, limite)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title("Diagrama Fasorial (RLC Paralelo)", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_aspect('equal')
        if show_v or show_ir or show_il or show_ic or show_i:
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
# === CÁLCULO E ROTA: MÓDULO TRIFÁSICO Y-Y =
# ==========================================
def calcular_triphasico_yy(Van, Vbn, Vcn, Zfa, Zfb, Zfc, ZLa, ZLb, ZLc, ZA, ZB, ZC, Zo):
    # Impedâncias equivalentes por fase
    ZeqA = Zfa + ZLa + ZA
    ZeqB = Zfb + ZLb + ZB
    ZeqC = Zfc + ZLc + ZC

    if ZeqA == 0: ZeqA = 1e-6 + 0j
    if ZeqB == 0: ZeqB = 1e-6 + 0j
    if ZeqC == 0: ZeqC = 1e-6 + 0j

    # Tensão de deslocamento de neutro (V_Nn) via Millman
    if abs(Zo) < 1e-6:
        V_Nn = 0j
    else:
        numerador = (Van / ZeqA) + (Vbn / ZeqB) + (Vcn / ZeqC)
        denominador = (1 / ZeqA) + (1 / ZeqB) + (1 / ZeqC) + (1 / Zo)
        V_Nn = numerador / denominador

    # Correntes de Linha/Fase
    IAN = (Van - V_Nn) / ZeqA
    IBN = (Vbn - V_Nn) / ZeqB
    ICN = (Vcn - V_Nn) / ZeqC
    IN = IAN + IBN + ICN

    # Tensões de Fase na Carga
    VAN = IAN * ZA
    VBN = IBN * ZB
    VCN = ICN * ZC

    # Tensões de Linha na Carga
    VAB = VAN - VBN
    VBC = VBN - VCN
    VCA = VCN - VAN

    # Potências na Carga
    Sa = VAN * IAN.conjugate()
    Sb = VBN * IBN.conjugate()
    Sc = VCN * ICN.conjugate()
    Stotal = Sa + Sb + Sc

    return {
        "IAN": IAN, "IBN": IBN, "ICN": ICN, "IN": IN,
        "VAN": VAN, "VBN": VBN, "VCN": VCN,
        "VAB": VAB, "VBC": VBC, "VCA": VCA,
        "Sa": Sa, "Sb": Sb, "Sc": Sc, "Stotal": Stotal
    }

@app.route('/calcular_trifasico_yy', methods=['POST'])
@login_required
def rota_calcular_trifasico_yy():
    dados = request.get_json() or {}

    def converter(valor):
        if valor is None: return 0j
        texto = str(valor).strip().lower().replace(" ", "").replace("i", "j")
        if not texto: return 0j
        try: return complex(texto)
        except ValueError: return 0j

    def formatar_complexo(c):
        real = round(c.real, 2)
        imag = round(c.imag, 2)

        if imag == 0: retangular = f"{real}"
        elif real == 0: retangular = f"{imag}i"
        else: retangular = f"{real} + {imag}i" if imag > 0 else f"{real} - {abs(imag)}i"

        magnitude = round(abs(c), 2)
        angulo = round(math.degrees(cmath.phase(c)), 1)
        polar = f"{magnitude} ∠ {angulo}°"

        return {"polar": polar, "retangular": retangular}

    try:
        van_mod = float(dados.get('van_mod', 0) or 0)
        van_ang = float(dados.get('van_ang', 0) or 0)
        Van = cmath.rect(van_mod, math.radians(van_ang))

        vbn_mod = float(dados.get('vbn_mod', 0) or 0)
        vbn_ang = float(dados.get('vbn_ang', 0) or 0)
        Vbn = cmath.rect(vbn_mod, math.radians(vbn_ang))

        vcn_mod = float(dados.get('vcn_mod', 0) or 0)
        vcn_ang = float(dados.get('vcn_ang', 0) or 0)
        Vcn = cmath.rect(vcn_mod, math.radians(vcn_ang))
    except (ValueError, TypeError):
        Van, Vbn, Vcn = 0j, 0j, 0j

    Zfa, Zfb, Zfc = converter(dados.get('zfa')), converter(dados.get('zfb')), converter(dados.get('zfc'))
    ZLa, ZLb, ZLc = converter(dados.get('zla')), converter(dados.get('zlb')), converter(dados.get('zlc'))
    ZA, ZB, ZC = converter(dados.get('za')), converter(dados.get('zb')), converter(dados.get('zc'))
    Zo = converter(dados.get('zo'))

    try:
        res = calcular_triphasico_yy(Van, Vbn, Vcn, Zfa, Zfb, Zfc, ZLa, ZLb, ZLc, ZA, ZB, ZC, Zo)
        Sa, Sb, Sc, St = res["Sa"], res["Sb"], res["Sc"], res["Stotal"]

        return jsonify({
            "ian": formatar_complexo(res["IAN"]),
            "ibn": formatar_complexo(res["IBN"]),
            "icn": formatar_complexo(res["ICN"]),
            "in_n": formatar_complexo(res["IN"]),
            "van_c": formatar_complexo(res["VAN"]),
            "vbn_c": formatar_complexo(res["VBN"]),
            "vcn_c": formatar_complexo(res["VCN"]),
            "vab": formatar_complexo(res["VAB"]),
            "vbc": formatar_complexo(res["VBC"]),
            "vca": formatar_complexo(res["VCA"]),

            "pa": round(Sa.real, 2), "pb": round(Sb.real, 2), "pc": round(Sc.real, 2), "ptotal": round(St.real, 2),
            "qa": round(Sa.imag, 2), "qb": round(Sb.imag, 2), "qc": round(Sc.imag, 2), "qtotal": round(St.imag, 2),
            "sa": round(abs(Sa), 2), "sb": round(abs(Sb), 2), "sc": round(abs(Sc), 2), "stotal": round(abs(St), 2)
        })
    except Exception as e:
        return jsonify({"erro": f"Erro no cálculo: {str(e)}"}), 400

# ==========================================
# === GRÁFICOS TRIFÁSICOS YY (PLOTLY) ======
# ==========================================
@app.route('/graficos_trifasico_yy', methods=['POST'])
@login_required
def graficos_trifasico_yy():
    try:
        dados = request.get_json()

        def parse_complex(val):
            if not val: return 0j
            try:
                # Substitui i por j para conversão do Python
                s = str(val).replace('i', 'j').replace(' ', '')
                return complex(s)
            except:
                return 0j

        # Tensão da fonte
        van_m, van_a = float(dados.get('van_mod', 0)), float(dados.get('van_ang', 0))
        vbn_m, vbn_a = float(dados.get('vbn_mod', 0)), float(dados.get('vbn_ang', 0))
        vcn_m, vcn_a = float(dados.get('vcn_mod', 0)), float(dados.get('vcn_ang', 0))

        VAN = cmath.rect(van_m, math.radians(van_a))
        VBN = cmath.rect(vbn_m, math.radians(vbn_a))
        VCN = cmath.rect(vcn_m, math.radians(vcn_a))

        # Impedâncias
        zfa = parse_complex(dados.get('zfa'))
        zfb = parse_complex(dados.get('zfb'))
        zfc = parse_complex(dados.get('zfc'))

        zla = parse_complex(dados.get('zla'))
        zlb = parse_complex(dados.get('zlb'))
        zlc = parse_complex(dados.get('zlc'))

        za = parse_complex(dados.get('za'))
        zb = parse_complex(dados.get('zb'))
        zc = parse_complex(dados.get('zc'))
        zo = parse_complex(dados.get('zo'))

        # Impedâncias Totais por Fase
        Za_tot = zfa + zla + za
        Zb_tot = zfb + zlb + zb
        Zc_tot = zfc + zlc + zc

        # Correntes de Linha/Fase
        Ia = VAN / Za_tot if Za_tot != 0 else 0j
        Ib = VBN / Zb_tot if Zb_tot != 0 else 0j
        Ic = VCN / Zc_tot if Zc_tot != 0 else 0j
        In = Ia + Ib + Ic

        # Tensões na Carga
        Van_c = Ia * za
        Vbn_c = Ib * zb
        Vcn_c = Ic * zc

        # Tensões de Linha na Carga
        Vab = Van_c - Vbn_c
        Vbc = Vbn_c - Vcn_c
        Vca = Vcn_c - Van_c

        # Potências Totais (Complexas)
        Sa = Van_c * Ia.conjugate()
        Sb = Vbn_c * Ib.conjugate()
        Sc = Vcn_c * Ic.conjugate()
        Stotal = Sa + Sb + Sc

        def formatar_fasor(comp):
            mod = abs(comp)
            ang = math.degrees(cmath.phase(comp))
            return {
                'mod': round(mod, 2),
                'ang': round(ang, 2),
                'real': round(comp.real, 2),
                'imag': round(comp.imag, 2)
            }

        fasores = {
            'VAN': formatar_fasor(Van_c),
            'VBN': formatar_fasor(Vbn_c),
            'VCN': formatar_fasor(Vcn_c),
            'VAB': formatar_fasor(Vab),
            'VBC': formatar_fasor(Vbc),
            'VCA': formatar_fasor(Vca),
            'Ia':  formatar_fasor(Ia),
            'Ib':  formatar_fasor(Ib),
            'Ic':  formatar_fasor(Ic),
            'In':  formatar_fasor(In)
        }

        potencia = {
            'P': round(Stotal.real, 2),
            'Q': round(Stotal.imag, 2),
            'S_mod': round(abs(Stotal), 2)
        }

        return jsonify({'sucesso': True, 'fasores': fasores, 'potencia': potencia})

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})

# ==========================================
# === CÁLCULO E ROTA: MÓDULO TRIFÁSICO Y-DELTA
# ==========================================
def calcular_triphasico_ydelta(Van, Vbn, Vcn, Zfa, Zfb, Zfc, ZLa, ZLb, ZLc, ZAB, ZBC, ZCA):
    # Impedâncias de linha + fonte por fase
    Za_linha = Zfa + ZLa
    Zb_linha = Zfb + ZLb
    Zc_linha = Zfc + ZLc

    # Conversão da carga Delta (ZAB, ZBC, ZCA) para Y equivalente (ZA_eq, ZB_eq, ZC_eq)
    Z_delta_sum = ZAB + ZBC + ZCA
    if abs(Z_delta_sum) < 1e-6:
        Z_delta_sum = 1e-6 + 0j

    ZA_eq = (ZAB * ZCA) / Z_delta_sum
    ZB_eq = (ZAB * ZBC) / Z_delta_sum
    ZC_eq = (ZBC * ZCA) / Z_delta_sum

    # Impedâncias equivalentes totais por fase (Linha + Y equivalente da Carga)
    ZeqA = Za_linha + ZA_eq
    ZeqB = Zb_linha + ZB_eq
    ZeqC = Zc_linha + ZC_eq

    if ZeqA == 0: ZeqA = 1e-6 + 0j
    if ZeqB == 0: ZeqB = 1e-6 + 0j
    if ZeqC == 0: ZeqC = 1e-6 + 0j

    # Millman para neutro fictício n' do Y equivalente
    numerador = (Van / ZeqA) + (Vbn / ZeqB) + (Vcn / ZeqC)
    denominador = (1 / ZeqA) + (1 / ZeqB) + (1 / ZeqC)
    V_Nn = numerador / denominador if denominador != 0 else 0j

    # Correntes de Linha (Ia, Ib, Ic)
    Ia = (Van - V_Nn) / ZeqA
    Ib = (Vbn - V_Nn) / ZeqB
    Ic = (Vcn - V_Nn) / ZeqC

    # Tensões de Nó nos terminais A, B, C da carga Delta em relação ao neutro n
    VA = Van - Ia * Za_linha
    VB = Vbn - Ib * Zb_linha
    VC = Vcn - Ic * Zc_linha

    # Tensões de Linha aplicadas à Carga Delta
    VAB = VA - VB
    VBC = VB - VC
    VCA = VC - VA

    # Correntes de Fase na Carga Delta (IAB, IBC, ICA)
    IAB = VAB / ZAB if abs(ZAB) > 1e-6 else 0j
    IBC = VBC / ZBC if abs(ZBC) > 1e-6 else 0j
    ICA = VCA / ZCA if abs(ZCA) > 1e-6 else 0j

    # Potências na Carga Delta por Fase
    SAB = VAB * IAB.conjugate()
    SBC = VBC * IBC.conjugate()
    SCA = VCA * ICA.conjugate()
    Stotal = SAB + SBC + SCA

    return {
        "Ia": Ia, "Ib": Ib, "Ic": Ic,
        "VAB": VAB, "VBC": VBC, "VCA": VCA,
        "IAB": IAB, "IBC": IBC, "ICA": ICA,
        "SAB": SAB, "SBC": SBC, "SCA": SCA, "Stotal": Stotal
    }

import cmath
import math

@app.route('/calcular_trifasico_ydelta', methods=['POST'])
@login_required
def rota_calcular_trifasico_ydelta():
    try:
        dados = request.get_json() or {}

        def parse_complex(val):
            if not val:
                return 0j
            try:
                return complex(str(val).replace('i', 'j').replace(' ', ''))
            except:
                return 0j

        van_m, van_a = float(dados.get('van_mod', 0)), float(dados.get('van_ang', 0))
        vbn_m, vbn_a = float(dados.get('vbn_mod', 0)), float(dados.get('vbn_ang', 0))
        vcn_m, vcn_a = float(dados.get('vcn_mod', 0)), float(dados.get('vcn_ang', 0))

        Van = cmath.rect(van_m, math.radians(van_a))
        Vbn = cmath.rect(vbn_m, math.radians(vbn_a))
        Vcn = cmath.rect(vcn_m, math.radians(vcn_a))

        Zfa = parse_complex(dados.get('zfa'))
        Zfb = parse_complex(dados.get('zfb'))
        Zfc = parse_complex(dados.get('zfc'))

        ZLa = parse_complex(dados.get('zla'))
        ZLb = parse_complex(dados.get('zlb'))
        ZLc = parse_complex(dados.get('zlc'))

        ZAB = parse_complex(dados.get('zab'))
        ZBC = parse_complex(dados.get('zbc'))
        ZCA = parse_complex(dados.get('zca'))

        res = calcular_triphasico_ydelta(Van, Vbn, Vcn, Zfa, Zfb, Zfc, ZLa, ZLb, ZLc, ZAB, ZBC, ZCA)

        SAB, SBC, SCA = res["SAB"], res["SBC"], res["SCA"]
        St = res["Stotal"]

        return jsonify({
            # Correntes (chamando formatar_complexo)
            "ia": formatar_complexo(res["Ia"]),
            "ib": formatar_complexo(res["Ib"]),
            "ic": formatar_complexo(res["Ic"]),
            "iab": formatar_complexo(res["IAB"]),
            "ibc": formatar_complexo(res["IBC"]),
            "ica": formatar_complexo(res["ICA"]),

            # Tensões (Fase e Linha)
            "van": formatar_complexo(Van),
            "vbn": formatar_complexo(Vbn),
            "vcn": formatar_complexo(Vcn),
            "vab": formatar_complexo(res["VAB"]),
            "vbc": formatar_complexo(res["VBC"]),
            "vca": formatar_complexo(res["VCA"]),

            # Potências
            "pa": round(SAB.real, 2), "qa": round(SAB.imag, 2), "sa": round(abs(SAB), 2),
            "pb": round(SBC.real, 2), "qb": round(SBC.imag, 2), "sb": round(abs(SBC), 2),
            "pc": round(SCA.real, 2), "qc": round(SCA.imag, 2), "sc": round(abs(SCA), 2),

            "ptotal": round(St.real, 2),
            "qtotal": round(St.imag, 2),
            "stotal": round(abs(St), 2)
        })

    except Exception as e:
        return jsonify({"erro": f"Erro no cálculo: {str(e)}"}), 400

@app.route('/graficos_trifasico_ydelta', methods=['POST'])
@login_required
def graficos_trifasico_ydelta():
    try:
        dados = request.get_json() or {}

        def parse_complex(val):
            if not val: return 0j
            try: return complex(str(val).replace('i', 'j').replace(' ', ''))
            except: return 0j

        van_m, van_a = float(dados.get('van_mod', 0)), float(dados.get('van_ang', 0))
        vbn_m, vbn_a = float(dados.get('vbn_mod', 0)), float(dados.get('vbn_ang', 0))
        vcn_m, vcn_a = float(dados.get('vcn_mod', 0)), float(dados.get('vcn_ang', 0))

        Van = cmath.rect(van_m, math.radians(van_a))
        Vbn = cmath.rect(vbn_m, math.radians(vbn_a))
        Vcn = cmath.rect(vcn_m, math.radians(vcn_a))

        Zfa, Zfb, Zfc = parse_complex(dados.get('zfa')), parse_complex(dados.get('zfb')), parse_complex(dados.get('zfc'))
        ZLa, ZLb, ZLc = parse_complex(dados.get('zla')), parse_complex(dados.get('zlb')), parse_complex(dados.get('zlc'))
        ZAB, ZBC, ZCA = parse_complex(dados.get('zab')), parse_complex(dados.get('zbc')), parse_complex(dados.get('zca'))

        res = calcular_triphasico_ydelta(Van, Vbn, Vcn, Zfa, Zfb, Zfc, ZLa, ZLb, ZLc, ZAB, ZBC, ZCA)

        def dict_fasor(comp):
            return {
                'mod': round(abs(comp), 2),
                'ang': round(math.degrees(cmath.phase(comp)), 2),
                'real': round(comp.real, 2),
                'imag': round(comp.imag, 2)
            }

        fasores = {
            'VAN': dict_fasor(Van),
            'VBN': dict_fasor(Vbn),
            'VCN': dict_fasor(Vcn),
            'VAB': dict_fasor(res["VAB"]),
            'VBC': dict_fasor(res["VBC"]),
            'VCA': dict_fasor(res["VCA"]),
            'Ia':  dict_fasor(res["Ia"]),
            'Ib':  dict_fasor(res["Ib"]),
            'Ic':  dict_fasor(res["Ic"]),
            'IAB': dict_fasor(res["IAB"]),
            'IBC': dict_fasor(res["IBC"]),
            'ICA': dict_fasor(res["ICA"])
        }

        Stotal = res["Stotal"]
        potencia = {
            'P': round(Stotal.real, 2),
            'Q': round(Stotal.imag, 2),
            'S_mod': round(abs(Stotal), 2)
        }

        return jsonify({'sucesso': True, 'fasores': fasores, 'potencia': potencia})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})

@app.route('/calcular_trifasico_deltadelta', methods=['POST'])
def calcular_trifasico_deltadelta():
    try:
        data = request.get_json()

        # Tensões da Fonte (Delta: Vlinha = Vfase)
        vab_f_mod = float(data.get('vab_mod', 0))
        vab_f_ang = math.radians(float(data.get('vab_ang', 0)))
        vbc_f_mod = float(data.get('vbc_mod', 0))
        vbc_f_ang = math.radians(float(data.get('vbc_ang', 0)))
        vca_f_mod = float(data.get('vca_mod', 0))
        vca_f_ang = math.radians(float(data.get('vca_ang', 0)))

        Vab_fonte = cmath.rect(vab_f_mod, vab_f_ang)
        Vbc_fonte = cmath.rect(vbc_f_mod, vbc_f_ang)
        Vca_fonte = cmath.rect(vca_f_mod, vca_f_ang)

        # Impedâncias de Linha e Fonte
        Zfa = complex(str(data.get('zfa', '0')).replace('i', 'j'))
        Zfb = complex(str(data.get('zfb', '0')).replace('i', 'j'))
        Zfc = complex(str(data.get('zfc', '0')).replace('i', 'j'))

        Zla = complex(str(data.get('zla', '0')).replace('i', 'j'))
        Zlb = complex(str(data.get('zlb', '0')).replace('i', 'j'))
        Zlc = complex(str(data.get('zlc', '0')).replace('i', 'j'))

        Za = Zfa + Zla
        Zb = Zfb + Zlb
        Zc = Zfc + Zlc

        # Impedâncias da Carga (Delta)
        ZAB = complex(str(data.get('zab', '1')).replace('i', 'j'))
        ZBC = complex(str(data.get('zbc', '1')).replace('i', 'j'))
        ZCA = complex(str(data.get('zca', '1')).replace('i', 'j'))

        # Resolução por transformação Delta -> Y apenas para achar as Correntes de Linha exatas
        Zsum = ZAB + ZBC + ZCA
        Za_eq = (ZAB * ZCA) / Zsum
        Zb_eq = (ZAB * ZBC) / Zsum
        Zc_eq = (ZBC * ZCA) / Zsum

        # Tensões equivalente de fase para cálculo das correntes de linha
        Van_fonte = (Vab_fonte - Vca_fonte) / 3.0
        Vbn_fonte = (Vbc_fonte - Vab_fonte) / 3.0
        Vcn_fonte = (Vca_fonte - Vbc_fonte) / 3.0

        # Correntes de Linha
        Ia = Van_fonte / (Za + Za_eq)
        Ib = Vbn_fonte / (Zb + Zb_eq)
        Ic = Vcn_fonte / (Zc + Zc_eq)

        # Tensões nos terminais da Carga (Vlinha = Vfase na Carga Delta)
        # V_carga = V_fonte - Queda_de_tensao_na_linha
        VAB_carga = Vab_fonte - (Ia * Za - Ib * Zb)
        VBC_carga = Vbc_fonte - (Ib * Zb - Ic * Zc)
        VCA_carga = Vca_fonte - (Ic * Zc - Ia * Za)

        # Correntes de Fase na Carga (I_fase = V_carga / Z_carga)
        IAB = VAB_carga / ZAB
        IBC = VBC_carga / ZBC
        ICA = VCA_carga / ZCA

        # Potências por Fase na Carga
        S_ab = VAB_carga * IAB.conjugate()
        S_bc = VBC_carga * IBC.conjugate()
        S_ca = VCA_carga * ICA.conjugate()
        S_total = S_ab + S_bc + S_ca

        return jsonify({
            'ia': formatar_complexo(Ia),
            'ib': formatar_complexo(Ib),
            'ic': formatar_complexo(Ic),

            'iab': formatar_complexo(IAB),
            'ibc': formatar_complexo(IBC),
            'ica': formatar_complexo(ICA),

            'vab_carga': formatar_complexo(VAB_carga),
            'vbc_carga': formatar_complexo(VBC_carga),
            'vca_carga': formatar_complexo(VCA_carga),

            'vab_fonte': formatar_complexo(Vab_fonte),
            'vbc_fonte': formatar_complexo(Vbc_fonte),
            'vca_fonte': formatar_complexo(Vca_fonte),

            'sab': round(abs(S_ab), 2),
            'pab': round(S_ab.real, 2),
            'qab': round(S_ab.imag, 2),

            'sbc': round(abs(S_bc), 2),
            'pbc': round(S_bc.real, 2),
            'qbc': round(S_bc.imag, 2),

            'sca': round(abs(S_ca), 2),
            'pca': round(S_ca.real, 2),
            'qca': round(S_ca.imag, 2),

            'stotal': round(abs(S_total), 2),
            'ptotal': round(S_total.real, 2),
            'qtotal': round(S_total.imag, 2)
        })

    except Exception as e:
        return jsonify({'erro': f'Erro no cálculo Delta-Delta: {str(e)}'}), 400

@app.route('/graficos_trifasico_deltadelta', methods=['POST'])
def graficos_trifasico_deltadelta():
    try:
        data = request.get_json()

        # Tensões da Fonte (Delta)
        vab_f_mod = float(data.get('vab_mod', 0))
        vab_f_ang = float(data.get('vab_ang', 0))
        vbc_f_mod = float(data.get('vbc_mod', 0))
        vbc_f_ang = float(data.get('vbc_ang', 0))
        vca_f_mod = float(data.get('vca_mod', 0))
        vca_f_ang = float(data.get('vca_ang', 0))

        Vab_fonte = cmath.rect(vab_f_mod, math.radians(vab_f_ang))
        Vbc_fonte = cmath.rect(vbc_f_mod, math.radians(vbc_f_ang))
        Vca_fonte = cmath.rect(vca_f_mod, math.radians(vca_f_ang))

        # Impedâncias
        Zfa = complex(str(data.get('zfa', '0')).replace('i', 'j'))
        Zfb = complex(str(data.get('zfb', '0')).replace('i', 'j'))
        Zfc = complex(str(data.get('zfc', '0')).replace('i', 'j'))

        Zla = complex(str(data.get('zla', '0')).replace('i', 'j'))
        Zlb = complex(str(data.get('zlb', '0')).replace('i', 'j'))
        Zlc = complex(str(data.get('zlc', '0')).replace('i', 'j'))

        Za = Zfa + Zla
        Zb = Zfb + Zlb
        Zc = Zfc + Zlc

        ZAB = complex(str(data.get('zab', '1')).replace('i', 'j'))
        ZBC = complex(str(data.get('zbc', '1')).replace('i', 'j'))
        ZCA = complex(str(data.get('zca', '1')).replace('i', 'j'))

        # Equivalente Delta-Y
        Zsum = ZAB + ZBC + ZCA
        Za_eq = (ZAB * ZCA) / Zsum
        Zb_eq = (ZAB * ZBC) / Zsum
        Zc_eq = (ZBC * ZCA) / Zsum

        Van_fonte = (Vab_fonte - Vca_fonte) / 3.0
        Vbn_fonte = (Vbc_fonte - Vab_fonte) / 3.0
        Vcn_fonte = (Vca_fonte - Vbc_fonte) / 3.0

        Ia = Van_fonte / (Za + Za_eq)
        Ib = Vbn_fonte / (Zb + Zb_eq)
        Ic = Vcn_fonte / (Zc + Zc_eq)

        VAB_carga = Vab_fonte - (Ia * Za - Ib * Zb)
        VBC_carga = Vbc_fonte - (Ib * Zb - Ic * Zc)
        VCA_carga = Vca_fonte - (Ic * Zc - Ia * Za)

        IAB = VAB_carga / ZAB
        IBC = VBC_carga / ZBC
        ICA = VCA_carga / ZCA

        # Potências
        S_ab = VAB_carga * IAB.conjugate()
        S_bc = VBC_carga * IBC.conjugate()
        S_ca = VCA_carga * ICA.conjugate()
        S_total = S_ab + S_bc + S_ca

        def fasor_dict(c):
            mod, ang_rad = cmath.polar(c)
            return {
                'mod': float(mod),
                'ang': float(math.degrees(ang_rad)),
                'real': float(c.real),
                'imag': float(c.imag)
            }

        return jsonify({
            'sucesso': True,
            'fasores': {
                'VAB_fonte': fasor_dict(Vab_fonte),
                'VBC_fonte': fasor_dict(Vbc_fonte),
                'VCA_fonte': fasor_dict(Vca_fonte),
                'VAB_carga': fasor_dict(VAB_carga),
                'VBC_carga': fasor_dict(VBC_carga),
                'VCA_carga': fasor_dict(VCA_carga),
                'Ia': fasor_dict(Ia),
                'Ib': fasor_dict(Ib),
                'Ic': fasor_dict(Ic),
                'IAB': fasor_dict(IAB),
                'IBC': fasor_dict(IBC),
                'ICA': fasor_dict(ICA)
            },
            'potencia': {
                'P': float(S_total.real),
                'Q': float(S_total.imag),
                'S_mod': float(abs(S_total))
            }
        })
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400

# ==========================================
# MÓDULO DELTA-Y (Δ-Y)
# ==========================================

def resolver_circuito_dy(data):
    # Tensões da Fonte (Delta)
    vab_f_mod = float(data.get('vab_mod', 0))
    vab_f_ang = float(data.get('vab_ang', 0))
    vbc_f_mod = float(data.get('vbc_mod', 0))
    vbc_f_ang = float(data.get('vbc_ang', 0))
    vca_f_mod = float(data.get('vca_mod', 0))
    vca_f_ang = float(data.get('vca_ang', 0))

    Vab_fonte = cmath.rect(vab_f_mod, math.radians(vab_f_ang))
    Vbc_fonte = cmath.rect(vbc_f_mod, math.radians(vbc_f_ang))
    Vca_fonte = cmath.rect(vca_f_mod, math.radians(vca_f_ang))

    # Conversão da Fonte Delta -> Equivalente Estrela (Y) para simplificar a análise
    Van_fonte = (Vab_fonte - Vca_fonte) / 3.0
    Vbn_fonte = (Vbc_fonte - Vab_fonte) / 3.0
    Vcn_fonte = (Vca_fonte - Vbc_fonte) / 3.0

    # Impedâncias
    Zfa = complex(str(data.get('zfa', '0')).replace('i', 'j'))
    Zfb = complex(str(data.get('zfb', '0')).replace('i', 'j'))
    Zfc = complex(str(data.get('zfc', '0')).replace('i', 'j'))

    Zla = complex(str(data.get('zla', '0')).replace('i', 'j'))
    Zlb = complex(str(data.get('zlb', '0')).replace('i', 'j'))
    Zlc = complex(str(data.get('zlc', '0')).replace('i', 'j'))

    # Impedâncias da Carga (Estrela - Y)
    Za_carga = complex(str(data.get('za', '1')).replace('i', 'j'))
    Zb_carga = complex(str(data.get('zb', '1')).replace('i', 'j'))
    Zc_carga = complex(str(data.get('zc', '1')).replace('i', 'j'))

    # Impedância de Neutro (se houver)
    Zn = complex(str(data.get('zn', '0')).replace('i', 'j'))

    # Impedâncias Totais por Fase
    Za_total = Zfa + Zla + Za_carga
    Zb_total = Zfb + Zlb + Zb_carga
    Zc_total = Zfc + Zlc + Zc_carga

    # Tensão de Deslocamento de Neutro (Vn'n) se Zn existir ou sistema for desequilibrado
    Y_a = 1.0 / Za_total if Za_total != 0 else 0
    Y_b = 1.0 / Zb_total if Zb_total != 0 else 0
    Y_c = 1.0 / Zc_total if Zc_total != 0 else 0
    Y_n = 1.0 / Zn if Zn != 0 else 0

    Vnn = (Van_fonte * Y_a + Vbn_fonte * Y_b + Vcn_fonte * Y_c) / (Y_a + Y_b + Y_c + Y_n)

    # Correntes de Linha (que no Y são iguais às correntes de fase da carga)
    Ia = (Van_fonte - Vnn) * Y_a
    Ib = (Vbn_fonte - Vnn) * Y_b
    Ic = (Vcn_fonte - Vnn) * Y_c
    In = Ia + Ib + Ic

    # Tensões de Fase na Carga (Y)
    VAN_carga = Ia * Za_carga
    VBN_carga = Ib * Zb_carga
    VCN_carga = Ic * Zc_carga

    # Tensões de Linha na Carga
    VAB_carga = VAN_carga - VBN_carga
    VBC_carga = VBN_carga - VCN_carga
    VCA_carga = VCN_carga - VAN_carga

    # Potências
    S_a = VAN_carga * Ia.conjugate()
    S_b = VBN_carga * Ib.conjugate()
    S_c = VCN_carga * Ic.conjugate()
    S_total = S_a + S_b + S_c

    return {
        'Vab_fonte': Vab_fonte, 'Vbc_fonte': Vbc_fonte, 'Vca_fonte': Vca_fonte,
        'Van_fonte': Van_fonte, 'Vbn_fonte': Vbn_fonte, 'Vcn_fonte': Vcn_fonte,
        'Ia': Ia, 'Ib': Ib, 'Ic': Ic, 'In': In,
        'VAN_carga': VAN_carga, 'VBN_carga': VBN_carga, 'VCN_carga': VCN_carga,
        'VAB_carga': VAB_carga, 'VBC_carga': VBC_carga, 'VCA_carga': VCA_carga,
        'S_a': S_a, 'S_b': S_b, 'S_c': S_c, 'S_total': S_total
    }

@app.route('/calcular_trifasico_deltay', methods=['POST'])
def calcular_trifasico_deltay():
    try:
        data = request.get_json()
        res = resolver_circuito_dy(data)

        return jsonify({
            'ia': formatar_complexo(res['Ia']),
            'ib': formatar_complexo(res['Ib']),
            'ic': formatar_complexo(res['Ic']),
            'in': formatar_complexo(res['In']),

            # Correntes/Tensões de Fase e Linha na Carga
            'van_carga': formatar_complexo(res['VAN_carga']),
            'vbn_carga': formatar_complexo(res['VBN_carga']),
            'vcn_carga': formatar_complexo(res['VCN_carga']),

            'vab_carga': formatar_complexo(res['VAB_carga']),
            'vbc_carga': formatar_complexo(res['VBC_carga']),
            'vca_carga': formatar_complexo(res['VCA_carga']),

            'vab_fonte': formatar_complexo(res['Vab_fonte']),
            'vbc_fonte': formatar_complexo(res['Vbc_fonte']),
            'vca_fonte': formatar_complexo(res['Vca_fonte']),

            # Potências Individuais por Fase (Mod / Real / Imag)
            'sa': round(abs(res['S_a']), 2),
            'pa': round(res['S_a'].real, 2),
            'qa': round(res['S_a'].imag, 2),

            'sb': round(abs(res['S_b']), 2),
            'pb': round(res['S_b'].real, 2),
            'qb': round(res['S_b'].imag, 2),

            'sc': round(abs(res['S_c']), 2),
            'pc': round(res['S_c'].real, 2),
            'qc': round(res['S_c'].imag, 2),

            # Potência Total
            'stotal': round(abs(res['S_total']), 2),
            'ptotal': round(res['S_total'].real, 2),
            'qtotal': round(res['S_total'].imag, 2)
        })
    except Exception as e:
        return jsonify({'erro': f'Erro no cálculo Delta-Y: {str(e)}'}), 400

@app.route('/graficos_trifasico_deltay', methods=['POST'])
def graficos_trifasico_deltay():
    try:
        data = request.get_json()
        res = resolver_circuito_dy(data)

        def fasor_dict(c):
            mod, ang_rad = cmath.polar(c)
            return {
                'mod': float(mod),
                'ang': float(math.degrees(ang_rad)),
                'real': float(c.real),
                'imag': float(c.imag)
            }

        return jsonify({
            'sucesso': True,
            'fasores': {
                'VAB_fonte': fasor_dict(res['Vab_fonte']),
                'VBC_fonte': fasor_dict(res['Vbc_fonte']),
                'VCA_fonte': fasor_dict(res['Vca_fonte']),
                'VAN_carga': fasor_dict(res['VAN_carga']),
                'VBN_carga': fasor_dict(res['VBN_carga']),
                'VCN_carga': fasor_dict(res['VCN_carga']),
                'VAB_carga': fasor_dict(res['VAB_carga']),
                'VBC_carga': fasor_dict(res['VBC_carga']),
                'VCA_carga': fasor_dict(res['VCA_carga']),
                'Ia': fasor_dict(res['Ia']),
                'Ib': fasor_dict(res['Ib']),
                'Ic': fasor_dict(res['Ic']),
                'In': fasor_dict(res['In'])
            },
            'potencia': {
                'P': float(res['S_total'].real),
                'Q': float(res['S_total'].imag),
                'S_mod': float(abs(res['S_total']))
            }
        })
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400

@app.route('/calcular_correcao_fp', methods=['POST'])
def calcular_correcao_fp():
    try:
        dados = request.get_json()

        # Leitura dos parâmetros de entrada
        p_total = float(dados.get('p_total', 0))  # Potência ativa em Watts (W)
        fp_atual = float(dados.get('fp_atual', 0))  # Fator de potência atual
        vl = float(dados.get('v_linha', 220))  # Tensão de linha (V)
        f = float(dados.get('frequencia', 60))  # Frequência (Hz)
        fp_alvo = float(
            dados.get('fp_alvo', 0.92)
        )  # FP desejado (padrão >= 0.92)

        # Validações de segurança
        if fp_atual <= 0 or fp_atual >= 1 or fp_alvo <= 0 or fp_alvo > 1:
            return jsonify({
                'sucesso': False,
                'erro': 'O Fator de Potência deve estar entre 0 e 1.',
            })

        if fp_atual >= fp_alvo:
            return jsonify({
                'sucesso': False,
                'erro': (
                    'O FP atual já é maior ou igual ao FP alvo desejado.'
                ),
            })

        # Ângulos de fase (em radianos)
        theta_1 = math.acos(fp_atual)
        theta_2 = math.acos(fp_alvo)

        # Cálculo das Potências Reativas
        q1 = p_total * math.tan(theta_1)  # VAr atual
        q2 = p_total * math.tan(theta_2)  # VAr alvo
        qc_total = q1 - q2  # VAr capacitivo necessário

        # Potência aparente inicial e final
        s1 = p_total / fp_atual
        s2 = p_total / fp_alvo

        # Cálculo da Capacitância (Farais -> microFarads µF)
        omega = 2 * math.pi * f

        # Para ligação Delta (Δ)
        c_delta = (qc_total / (3 * omega * (vl**2))) * 1e6

        # Para ligação Estrela (Y)
        c_estrela = (qc_total / (omega * (vl**2))) * 1e6

        return jsonify({
            'sucesso': True,
            'p_total': round(p_total, 2),
            'fp_atual': round(fp_atual, 3),
            'fp_alvo': round(fp_alvo, 3),
            'q1_var': round(q1, 2),
            'q2_var': round(q2, 2),
            'qc_total_var': round(qc_total, 2),
            's1_va': round(s1, 2),
            's2_va': round(s2, 2),
            'c_delta_uf': round(c_delta, 2),
            'c_estrela_uf': round(c_estrela, 2),
        })

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)