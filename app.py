from flask import Flask, render_template, request, jsonify
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


# === ROTA: CALCULAR SÉRIE ===
@app.route('/calcular_serie', methods=['POST'])
def calcular_serie():
    dados = request.get_json()
    try:
        v = float(dados.get('v'))
        r = float(dados.get('r'))
        l_mh = float(dados.get('l'))  # Indutância em miliHenrys
        f = float(dados.get('f'))  # Frequência em Hz

        if f <= 0:
            return jsonify({'sucesso': False, 'erro': 'A frequência deve ser maior que zero.'})

        # 1. Cálculos Base
        l = l_mh / 1000.0  # Converte para Henrys
        w = 2 * math.pi * f  # Velocidade Angular (rad/s)
        xl = w * l  # Reatância Indutiva (Ohms)

        # 2. Impedância e Corrente
        z_mag = math.sqrt(r ** 2 + xl ** 2)
        i_mag = v / z_mag if z_mag != 0 else 0

        # 3. Tensões
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


# === ROTA: CALCULAR PARALELO ===
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


# === ROTA: GRÁFICOS SÉRIE ===
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
        theta_deg = math.degrees(theta_rad)  # Converte para graus para exibir na legenda

        i_mag = v / z_mag if z_mag != 0 else 0

        fator_escala = round(z_mag, 1)

        fig = plt.figure(figsize=(12, 5))

        # --- GRÁFICO 1: DOMÍNIO DO TEMPO ---
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

        # --- GRÁFICO 2: DIAGRAMA FASORIAL ---
        ax2 = fig.add_subplot(122)

        # Tensão (Referência)
        ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label=f'V (0.0°)')

        # VR (Em fase com a Corrente)
        vr_x = (i_mag * r) * math.cos(-theta_rad)
        vr_y = (i_mag * r) * math.sin(-theta_rad)
        ax2.quiver(0, 0, vr_x, vr_y, angles='xy', scale_units='xy', scale=1, color='green',
                   label=f'VR ({-theta_deg:.1f}°)')

        # VL (Adiantada 90° em relação à Corrente)
        vl_x = (i_mag * xl) * math.cos(-theta_rad + np.pi / 2)
        vl_y = (i_mag * xl) * math.sin(-theta_rad + np.pi / 2)
        ax2.quiver(0, 0, vl_x, vl_y, angles='xy', scale_units='xy', scale=1, color='purple',
                   label=f'VL ({-theta_deg + 90:.1f}°)')

        # Corrente (Atrasada de theta em relação à Tensão)
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


# === ROTA: GRÁFICOS PARALELO ===
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
        theta_deg = math.degrees(theta_rad)  # Converte para graus

        z_eq = v / it_mag if it_mag != 0 else 1
        fator_escala = round(z_eq, 1)

        fig = plt.figure(figsize=(12, 5))

        # --- GRÁFICO 1: DOMÍNIO DO TEMPO ---
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

        # --- GRÁFICO 2: DIAGRAMA FASORIAL ---
        ax2 = fig.add_subplot(122)

        # Tensão em 0 graus
        ax2.quiver(0, 0, v, 0, angles='xy', scale_units='xy', scale=1, color='blue', label='V (0.0°)')

        # Corrente do Resistor em fase com a Tensão
        ax2.quiver(0, 0, ir_mag * fator_escala, 0, angles='xy', scale_units='xy', scale=1, color='green',
                   label='IR (0.0°)')

        # Corrente do Indutor atrasada em 90 graus
        ax2.quiver(0, 0, 0, -il_mag * fator_escala, angles='xy', scale_units='xy', scale=1, color='purple',
                   label='IL (-90.0°)')

        # Corrente Total atrasada de theta
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

if __name__ == '__main__':
    app.run(debug=True)