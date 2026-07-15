import base64
import io
import math
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    return User.query.get(int(user_id))

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

# ==========================================
# === ROTA DE GERAÇÃO DE EXERCÍCIOS ATUALIZADA ===
# ==========================================

@app.route('/gerar_exercicios')
@login_required
def gerar_exercicios():
    # CAPTURA OS PARÂMETROS ENVIADOS PELO JAVASCRIPT
    # Se não forem informados, assume o padrão de 10 questões e tipo 'todos'
    qtd = int(request.args.get('qtd', 10))
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

    # Bancos de questões individuais para filtragem
    questoes_rl = []
    questoes_rc = []
    questoes_rlc = []

    # Geramos uma amostragem grande o suficiente para o sorteador extrair
    for _ in range(40):
        # Gerador RL
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

        # Gerador RC
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

        # Gerador RLC
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

    # Filtragem com base na escolha do usuário
    banco_filtrado = []
    if tipo_selecionado == 'RL':
        banco_filtrado = questoes_rl
    elif tipo_selecionado == 'RC':
        banco_filtrado = questoes_rc
    elif tipo_selecionado == 'RLC':
        banco_filtrado = questoes_rlc
    else:
        # Mistura tudo e embaralha os tipos
        banco_filtrado = questoes_rl + questoes_rc + questoes_rlc
        random.shuffle(banco_filtrado)

    # Garante o sorteio aleatório das questões filtradas
    random.shuffle(banco_filtrado)
    dados_finais = banco_filtrado[:qtd]

    # Passamos qtd e tipo adiante para a template saber como re-gerar a lista
    return render_template('exercicios.html', dados=dados_finais, qtd=qtd, tipo=tipo_selecionado)

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
# === CÁLCULOS: MÓDULO RLC =================
# ==========================================
@app.route('/calcular_rlc_serie', methods=['POST'])
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

        amp_vr = i_mag * r
        amp_vl = i_mag * xl
        min_v_visual = 0.15 * v

        amp_vr_visual = max(amp_vr, min_v_visual) if amp_vr > 0.01 else 0
        amp_vl_visual = max(amp_vl, min_v_visual) if amp_vl > 0.01 else 0

        escala_vr = amp_vr_visual / amp_vr if amp_vr > 0.01 else 1.0
        escala_vl = amp_vl_visual / amp_vl if amp_vl > 0.01 else 1.0

        label_vr = "VR" if escala_vr <= 1.05 else f"VR (escala x{escala_vr:.1f})"
        label_vl = "VL" if escala_vl <= 1.05 else f"VL (escala x{escala_vl:.1f})"

        amp_i_visual = 0.6 * v
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

        ax1.plot(t_ms, v_t, label='V (Fonte)', color='blue', linewidth=2.5)
        ax1.plot(t_ms, vr_t, label=label_vr, color='green', linewidth=1.5)
        ax1.plot(t_ms, vl_t, label=label_vl, color='purple', linewidth=1.5)
        ax1.plot(t_ms, i_t_escalada, label=label_i, color='red', linestyle='--', linewidth=2)

        ax1.set_title("Domínio do Tempo", fontsize=14, fontweight='bold')
        ax1.set_xlabel("Tempo (ms)")
        ax1.set_ylabel("Amplitude Visual")
        ticks_ms = np.linspace(0, 2 * periodo_ms, 9)
        ax1.set_xticks(ticks_ms)
        ax1.set_xticklabels([f"{tick:.3f}" for tick in ticks_ms])
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        ax1.legend(loc='upper right')

        ax2 = fig.add_subplot(122)
        i_visual = 0.5 * v

        ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V ({v:.1f}V) (0.0°)', width=0.005)

        vr_x = amp_vr_visual * math.cos(-theta_rad)
        vr_y = amp_vr_visual * math.sin(-theta_rad)
        ax2.quiver(0, 0, vr_x, vr_y, angles='xy', scale_units='xy', scale=1, color='green', label=f'VR ({amp_vr:.1f}V) ({-theta_deg:.1f}°)', width=0.005)

        vl_x = amp_vl_visual * math.cos(-theta_rad + np.pi / 2)
        vl_y = amp_vl_visual * math.sin(-theta_rad + np.pi / 2)
        ax2.quiver(0, 0, vl_x, vl_y, angles='xy', scale_units='xy', scale=1, color='purple', label=f'VL ({amp_vl:.1f}V) ({-theta_deg + 90:.1f}°)', width=0.005)

        i_x = i_visual * math.cos(-theta_rad)
        i_y = i_visual * math.sin(-theta_rad)
        ax2.quiver(0, 0, i_x, i_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'I ({i_mag:.2f}A) ({-theta_deg:.1f}°)', width=0.008)

        limite = max(v, amp_vr_visual, amp_vl_visual) * 1.2
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
        ax2.quiver(0, 0, ir_mag * fator_escala, 0, angles='xy', scale_units='xy', scale=1, color='green', label='IR (0.0°)')
        ax2.quiver(0, 0, 0, -il_mag * fator_escala, angles='xy', scale_units='xy', scale=1, color='purple', label='IL (-90.0°)')

        it_x = (it_mag * fator_escala) * math.cos(-theta_rad)
        it_y = (it_mag * fator_escala) * math.sin(-theta_rad)
        ax2.quiver(0, 0, it_x, it_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'IT (x{fator_escala}) ({-theta_deg:.1f}°)', width=0.005)

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
        ax2.quiver(0, 0, vr_x, vr_y, angles='xy', scale_units='xy', scale=1, color='green', label=f'VR ({theta_deg:.1f}°)')

        i_x = (i_mag * fator_escala) * math.cos(theta_rad)
        i_y = (i_mag * fator_escala) * math.sin(theta_rad)
        ax2.quiver(0, 0, i_x, i_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'I (x{fator_escala}) ({theta_deg:.1f}°)', width=0.005)

        vc_x = (i_mag * xc) * math.cos(theta_rad - np.pi / 2)
        vc_y = (i_mag * xc) * math.sin(theta_rad - np.pi / 2)
        ax2.quiver(0, 0, vc_x, vc_y, angles='xy', scale_units='xy', scale=1, color='orange', label=f'VC ({theta_deg - 90:.1f}°)')

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
        ax2.quiver(0, 0, ir_mag * fator_escala, 0, angles='xy', scale_units='xy', scale=1, color='green', label='IR (0.0°)')
        ax2.quiver(0, 0, 0, ic_mag * fator_escala, angles='xy', scale_units='xy', scale=1, color='orange', label='IC (90.0°)')

        it_x = (it_mag * fator_escala) * math.cos(theta_rad)
        it_y = (it_mag * fator_escala) * math.sin(theta_rad)
        ax2.quiver(0, 0, it_x, it_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'IT (x{fator_escala}) ({theta_deg:.1f}°)', width=0.005)

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

# ==========================================
# === GRÁFICOS: MÓDULO RLC =================
# ==========================================
@app.route('/graficos_rlc_serie', methods=['POST'])
def graficos_rlc_serie():
    try:
        dados = request.json
        v = float(dados['v'])
        r = float(dados['r'])
        l_mH = float(dados['l'])
        c_uF = float(dados['c'])
        f = float(dados['f'])

        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * np.pi * f

        xl = w * l
        xc = 1 / (w * c)
        x_total = xl - xc
        z = math.sqrt(r ** 2 + x_total ** 2)

        i = v / z if z != 0 else 0
        vr = i * r
        vl = i * xl
        vc = i * xc

        theta = math.degrees(math.atan2(vl - vc, vr))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Triângulo de Impedância
        ax1.quiver(0, 0, r, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'R = {r:.1f} Ω')
        ax1.quiver(r, 0, 0, x_total, angles='xy', scale_units='xy', scale=1, color='red', label=f'X_L - X_C = {x_total:.1f} Ω')
        ax1.quiver(0, 0, r, x_total, angles='xy', scale_units='xy', scale=1, color='green', label=f'Z = {z:.1f} Ω ∠ {theta:.1f}°')

        lim_z = max(r, abs(x_total)) * 1.2
        ax1.set_xlim(-0.1 * lim_z, lim_z)
        ax1.set_ylim(-lim_z if x_total < 0 else -0.1 * lim_z, lim_z if x_total > 0 else 0.1 * lim_z)
        ax1.grid(True, linestyle='--', alpha=0.6)
        ax1.axhline(0, color='black', linewidth=1)
        ax1.axvline(0, color='black', linewidth=1)
        ax1.set_title('Triângulo de Impedância')
        ax1.legend(loc='lower left')

        # Diagrama Fasorial
        max_v = max(v, vr, vl, vc)
        fator_escala_i = (max_v * 0.7) / i if i > 0 else 1

        ax2.quiver(0, 0, i * fator_escala_i, 0, angles='xy', scale_units='xy', scale=1, color='purple', width=0.005, label=f'I = {i:.2f} A ∠ 0° (Ref, esc. x{fator_escala_i:.1f})')
        ax2.quiver(0, 0, vr, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V_R = {vr:.1f} V ∠ 0°')
        ax2.quiver(0, 0, 0, vl, angles='xy', scale_units='xy', scale=1, color='orange', label=f'V_L = {vl:.1f} V ∠ +90°')
        ax2.quiver(0, 0, 0, -vc, angles='xy', scale_units='xy', scale=1, color='cyan', label=f'V_C = {vc:.1f} V ∠ -90°')
        ax2.quiver(0, 0, vr, vl - vc, angles='xy', scale_units='xy', scale=1, color='green', label=f'V_T = {v:.1f} V ∠ {theta:.1f}°')

        lim_v = max(max_v, i * fator_escala_i) * 1.2
        ax2.set_xlim(-0.1 * lim_v, lim_v)
        ax2.set_ylim(-lim_v, lim_v)
        ax2.grid(True, linestyle='--', alpha=0.6)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title('Diagrama Fasorial (Série)')
        ax2.legend(loc='lower left')

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

        theta = math.degrees(math.atan2(ic - il, ir))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Triângulo de Correntes
        ax1.quiver(0, 0, ir, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'I_R = {ir:.2f} A')
        ax1.quiver(ir, 0, 0, i_reativa, angles='xy', scale_units='xy', scale=1, color='red', label=f'I_C - I_L = {i_reativa:.2f} A')
        ax1.quiver(0, 0, ir, i_reativa, angles='xy', scale_units='xy', scale=1, color='green', label=f'I_T = {it:.2f} A ∠ {theta:.1f}°')

        lim_i = max(ir, abs(i_reativa)) * 1.2
        ax1.set_xlim(-0.1 * lim_i, lim_i)
        ax1.set_ylim(-lim_i if i_reativa < 0 else -0.1 * lim_i, lim_i if i_reativa > 0 else 0.1 * lim_i)
        ax1.grid(True, linestyle='--', alpha=0.6)
        ax1.axhline(0, color='black', linewidth=1)
        ax1.axvline(0, color='black', linewidth=1)
        ax1.set_title('Triângulo de Correntes')
        ax1.legend(loc='lower left')

        # Diagrama Fasorial
        max_i = max(it, ir, ic, il)
        fator_escala_v = (max_i * 0.7) / v if v > 0 else 1

        ax2.quiver(0, 0, v * fator_escala_v, 0, angles='xy', scale_units='xy', scale=1, color='purple', width=0.005, label=f'V = {v:.1f} V ∠ 0° (Ref, esc. x{fator_escala_v:.2f})')
        ax2.quiver(0, 0, ir, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'I_R = {ir:.2f} A ∠ 0°')
        ax2.quiver(0, 0, 0, ic, angles='xy', scale_units='xy', scale=1, color='orange', label=f'I_C = {ic:.2f} A ∠ +90°')
        ax2.quiver(0, 0, 0, -il, angles='xy', scale_units='xy', scale=1, color='cyan', label=f'I_L = {il:.2f} A ∠ -90°')
        ax2.quiver(0, 0, ir, i_reativa, angles='xy', scale_units='xy', scale=1, color='green', label=f'I_T = {it:.2f} A ∠ {theta:.1f}°')

        lim_fasor = max(v * fator_escala_v, max_i) * 1.2
        ax2.set_xlim(-0.1 * lim_fasor, lim_fasor)
        ax2.set_ylim(-max(il, abs(i_reativa)) * 1.2, max(ic, abs(i_reativa)) * 1.2)
        ax2.grid(True, linestyle='--', alpha=0.6)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
        ax2.set_title('Diagrama Fasorial (Paralelo)')
        ax2.legend(loc='lower left')

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
    app.run(host='0.0.0.0', port=5000, debug=True)