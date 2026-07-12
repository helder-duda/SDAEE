from flask import Flask, render_template, request, jsonify
import mimetypes
mimetypes.add_type('text/css', '.css')
import math
import io
import base64
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


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

        l = l_mH * 1e-3
        c = c_uF * 1e-6
        w = 2 * np.pi * f

        xl = w * l
        xc = 1 / (w * c)
        x_total = xl - xc

        # Geração do Gráfico (Triângulo de Impedância RLC)
        plt.figure(figsize=(6, 4))

        # Vetor R (eixo x)
        plt.quiver(0, 0, r, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'R = {r} Ω')
        # Vetor X_total (eixo y, a partir da ponta de R)
        plt.quiver(r, 0, 0, x_total, angles='xy', scale_units='xy', scale=1, color='red',
                   label=f'X_L - X_C = {x_total:.1f} Ω')
        # Vetor Z (hipotenusa)
        plt.quiver(0, 0, r, x_total, angles='xy', scale_units='xy', scale=1, color='green', label='Z (Impedância)')

        limite = max(r, abs(x_total)) * 1.2
        plt.xlim(-1, limite)
        plt.ylim(-limite if x_total < 0 else -1, limite if x_total > 0 else 1)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        plt.title('Triângulo de Impedância - RLC Série')
        plt.legend()

        # Salvar em Base64 para enviar ao HTML
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
        i_reativa = ic - il  # Corrente no capacitor vai para cima (+), indutor para baixo (-)

        # Geração do Gráfico (Diagrama Fasorial de Correntes)
        plt.figure(figsize=(6, 4))

        # Vetor Ir (eixo x)
        plt.quiver(0, 0, ir, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'I_R = {ir:.2f} A')
        # Vetor I_reativa (eixo y, a partir da ponta de Ir)
        plt.quiver(ir, 0, 0, i_reativa, angles='xy', scale_units='xy', scale=1, color='red',
                   label=f'I_C - I_L = {i_reativa:.2f} A')
        # Vetor I_total (hipotenusa)
        plt.quiver(0, 0, ir, i_reativa, angles='xy', scale_units='xy', scale=1, color='green',
                   label='I_T (Corrente Total)')

        limite = max(ir, abs(i_reativa)) * 1.2
        plt.xlim(-0.1 * limite, limite)
        plt.ylim(-limite if i_reativa < 0 else -0.1 * limite, limite if i_reativa > 0 else 0.1 * limite)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        plt.title('Diagrama Fasorial de Correntes - RLC Paralelo')
        plt.legend()

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