// ==========================================
// BANCO DE DADOS DE EXERCÍCIOS (20 QUESTÕES)
// ==========================================
const bancoDeExercicios = {
    "normal": [
        {
            "id": 1,
            "tipo": "Normal (RLC)",
            "enunciado": "Um circuito RLC série é alimentado por uma fonte de tensão de $V_s = 220\\angle{0^\\circ}\\text{ V}$. Os valores dos componentes são $R = 15\\ \\Omega$, $X_L = 30\\ \\Omega$ e $X_C = 10\\ \\Omega$. Calcule a impedância total do circuito ($Z_{eq}$) e a corrente total da fonte ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $Z_{eq} = 25\\angle{53,13^\\circ}\\ \\Omega$ ; $I_s = 8,8\\angle{-53,13^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $Z_{eq} = (15 + j20)\\ \\Omega$ ; $I_s = (5,28 - j7,04)\\text{ A}$"
        },
        {
            "id": 2,
            "tipo": "Normal (RC)",
            "enunciado": "Um resistor de $R = 12\\ \\Omega$ está em paralelo com um capacitor de reatância $X_C = 16\\ \\Omega$. O circuito é alimentado por uma fonte de tensão de $V_s = 48\\angle{30^\\circ}\\text{ V}$. Determine a corrente em cada ramo ($I_R$, $I_C$) e a corrente total ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $I_R = 4\\angle{30^\\circ}\\text{ A}$ ; $I_C = 3\\angle{120^\\circ}\\text{ A}$ ; $I_s = 5\\angle{66,87^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $I_R = (3,46 + j2)\\text{ A}$ ; $I_C = (-1,5 + j2,6)\\text{ A}$ ; $I_s = (1,96 + j4,6)\\text{ A}$"
        },
        {
            "id": 3,
            "tipo": "Normal (RL)",
            "enunciado": "Um circuito RL série possui uma fonte de tensão de $V_s = 100\\angle{0^\\circ}\\text{ V}$, um resistor de $R = 3\\ \\Omega$ e um indutor com reatância $X_L = 4\\ \\Omega$. Encontre a impedância equivalente total ($Z_{eq}$) do circuito e determine a intensidade da corrente total ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $Z_{eq} = 5\\angle{53,13^\\circ}\\ \\Omega$ ; $I_s = 20\\angle{-53,13^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $Z_{eq} = (3 + j4)\\ \\Omega$ ; $I_s = (12 - j16)\\text{ A}$"
        },
        {
            "id": 4,
            "tipo": "Normal (RC)",
            "enunciado": "Considere um circuito RC série alimentado por $V_s = 120\\angle{-10^\\circ}\\text{ V}$. Sendo $R = 8\\ \\Omega$ e $X_C = 6\\ \\Omega$, determine a impedância equivalente em formato polar ($Z_{eq}$) e a corrente drenada pelo circuito ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $Z_{eq} = 10\\angle{-36,87^\\circ}\\ \\Omega$ ; $I_s = 12\\angle{26,87^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $Z_{eq} = (8 - j6)\\ \\Omega$ ; $I_s = (10,7 + j5,42)\\text{ A}$"
        },
        {
            "id": 5,
            "tipo": "Normal (RL)",
            "enunciado": "Um circuito composto por um resistor de $R = 30\\ \\Omega$ em paralelo com um indutor de reatância $X_L = 40\\ \\Omega$ é ligado a uma fonte de $V_s = 60\\angle{0^\\circ}\\text{ V}$. Calcule os fasores da corrente no resistor ($I_R$), no indutor ($I_L$) e a corrente global de entrada ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $I_R = 2\\angle{0^\\circ}\\text{ A}$ ; $I_L = 1,5\\angle{-90^\\circ}\\text{ A}$ ; $I_s = 2,5\\angle{-36,87^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $I_R = (2 + j0)\\text{ A}$ ; $I_L = (0 - j1,5)\\text{ A}$ ; $I_s = (2 - j1,5)\\text{ A}$"
        },
        {
            "id": 6,
            "tipo": "Normal (RLC)",
            "enunciado": "Um circuito RLC série possui uma impedância composta por $R = 40\\ \\Omega$, $X_L = 50\\ \\Omega$ e $X_C = 20\\ \\Omega$. Sabendo que o circuito está conectado a uma fonte de $V_s = 200\\angle{45^\\circ}\\text{ V}$, calcule a impedância equivalente ($Z_{eq}$) e o fasor de corrente ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $Z_{eq} = 50\\angle{36,87^\\circ}\\ \\Omega$ ; $I_s = 4\\angle{8,13^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $Z_{eq} = (40 + j30)\\ \\Omega$ ; $I_s = (3,96 + j0,57)\\text{ A}$"
        },
        {
            "id": 7,
            "tipo": "Normal (RLC)",
            "enunciado": "Uma fonte senoidal de $V_s = 100\\angle{0^\\circ}\\text{ V}$ alimenta um circuito RLC paralelo com parâmetros $R = 20\\ \\Omega$, $X_L = 10\\ \\Omega$ e $X_C = 25\\ \\Omega$. Determine a corrente de entrada total ($I_s$) fornecida pela fonte de tensão.",
            "resposta": "<b>Forma Polar:</b> $I_s = 7,81\\angle{-50,19^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $I_s = (5 - j6)\\text{ A}$"
        },
        {
            "id": 8,
            "tipo": "Normal (RL)",
            "enunciado": "Uma bobina real é representada por um circuito série contendo resistência interna $R = 12\\ \\Omega$ e reatância indutiva $X_L = 5\\ \\Omega$. Se alimentada por uma fonte $V_s = 50\\angle{60^\\circ}\\text{ V}$, quais serão os fasores de impedância total ($Z_{eq}$) e corrente total ($I_s$)?",
            "resposta": "<b>Forma Polar:</b> $Z_{eq} = 13\\angle{22,62^\\circ}\\ \\Omega$ ; $I_s = 3,85\\angle{37,38^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $Z_{eq} = (12 + j5)\\ \\Omega$ ; $I_s = (3,06 + j2,34)\\text{ A}$"
        },
        {
            "id": 9,
            "tipo": "Normal (RC)",
            "enunciado": "Um circuito RC série com $R = 12\\ \\Omega$ e $X_C = 5\\ \\Omega$ é energizado por uma tensão alternada de $V_s = 110\\angle{0^\\circ}\\text{ V}$. Descubra os valores fasoriais correspondentes à impedância equivalente ($Z_{eq}$) e à corrente total do circuito ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $Z_{eq} = 13\\angle{-22,62^\\circ}\\ \\Omega$ ; $I_s = 8,46\\angle{22,62^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $Z_{eq} = (12 - j5)\\ \\Omega$ ; $I_s = (7,81 + j3,25)\\text{ A}$"
        },
        {
            "id": 10,
            "tipo": "Normal (RLC)",
            "enunciado": "Determine a corrente fasorial total ($I_s$) e a impedância de malha ($Z_{eq}$) para um circuito RLC série alimentado por $V_s = 10\\angle{-20^\\circ}\\text{ V}$ cujos parâmetros são $R = 6\\ \\Omega$, $X_L = 15\\ \\Omega$ e $X_C = 7\\ \\Omega$.",
            "resposta": "<b>Forma Polar:</b> $Z_{eq} = 10\\angle{53,13^\\circ}\\ \\Omega$ ; $I_s = 1\\angle{-73,13^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $Z_{eq} = (6 + j8)\\ \\Omega$ ; $I_s = (0,29 - j0,96)\\text{ A}$"
        }
    ],
    "engenharia_reversa": [
        {
            "id": 11,
            "tipo": "Normal Engenharia Reversa (RLC)",
            "enunciado": "Um engenheiro analisa um circuito RLC série desconhecido contendo $R = 10\\ \\Omega$, $X_L = 20\\ \\Omega$ e $X_C = 10\\ \\Omega$. Através de uma medição local direta, ele descobre que a tensão sobre o capacitor é de $V_C = 50\\angle{-45^\\circ}\\text{ V}$. Descubra os parâmetros físicos globais do circuito: a corrente da fonte ($I_s$) e a tensão da fonte ($V_s$).",
            "resposta": "<b>Forma Polar:</b> $I_s = 5\\angle{45^\\circ}\\text{ A}$ ; $V_s = 70,7\\angle{90^\\circ}\\text{ V}$<br><b>Forma Retangular:</b> $I_s = (3,54 + j3,54)\\text{ A}$ ; $V_s = (0 + j70,7)\\text{ V}$"
        },
        {
            "id": 12,
            "tipo": "Engenharia Reversa (RL)",
            "enunciado": "Em um circuito paralelo RL com $R = 20\\ \\Omega$ e $X_L = 15\\ \\Omega$, a corrente medida localmente no ramo do indutor é de $I_L = 8\\angle{-30^\\circ}\\text{ A}$. Realize a engenharia reversa para determinar a tensão nos terminais do circuito ($V_s$) e a corrente total gerada pela fonte de alimentação ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $V_s = 120\\angle{60^\\circ}\\text{ V}$ ; $I_s = 10\\angle{6,87^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $V_s = (60 + j103,92)\\text{ V}$ ; $I_s = (9,93 + j1,20)\\text{ A}$"
        },
        {
            "id": 13,
            "tipo": "Engenharia Reversa (Misto)",
            "enunciado": "Consulte um circuito misto onde uma fonte de tensão desconhecida alimenta um resistor $R_1 = 5\\ \\Omega$ em série com um paralelo composto por um capacitor de $X_C = 10\\ \\Omega$ e um indutor de $X_L = 10\\ \\Omega$. Sabendo que a corrente medida no capacitor é de $I_C = 4\\angle{90^\\circ}\\text{ A}$, determine a corrente de entrada ($I_s$) e a tensão total da fonte ($V_s$).",
            "resposta": "<b>Forma Polar:</b> $I_s = 0\\angle{0^\\circ}\\text{ A}$ (Ressonância Paralela) ; $V_s = 40\\angle{0^\\circ}\\text{ V}$<br><b>Forma Retangular:</b> $I_s = (0 + j0)\\text{ A}$ ; $V_s = (40 + j0)\\text{ V}$"
        },
        {
            "id": 14,
            "tipo": "Engenharia Reversa (RL)",
            "enunciado": "A partir de um circuito RL série desconhecido com $R = 8\\ \\Omega$ e $X_L = 6\\ \\Omega$, mediu-se sobre o resistor uma queda de tensão local de $V_R = 16\\angle{20^\\circ}\\text{ V}$. Por meio de engenharia reversa, deduza a corrente total da malha ($I_s$) e a tensão aplicada pela fonte de alimentação ($V_s$).",
            "resposta": "<b>Forma Polar:</b> $I_s = 2\\angle{20^\\circ}\\text{ A}$ ; $V_s = 20\\angle{56,87^\\circ}\\text{ V}$<br><b>Forma Retangular:</b> $I_s = (1,88 + j0,68)\\text{ A}$ ; $V_s = (10,93 + j16,75)\\text{ V}$"
        },
        {
            "id": 15,
            "tipo": "Engenharia Reversa (RC)",
            "enunciado": "No diagnóstico de um circuito RC série onde $R = 15\\ \\Omega$ e $X_C = 20\\ \\Omega$, obteve-se um registro de corrente no capacitor de $I_C = 4\\angle{30^\\circ}\\text{ A}$. Descubra os parâmetros físicos de excitação total do circuito: a corrente da fonte ($I_s$) e a tensão da fonte ($V_s$).",
            "resposta": "<b>Forma Polar:</b> $I_s = 4\\angle{30^\\circ}\\text{ A}$ ; $V_s = 100\\angle{-23,13^\\circ}\\text{ V}$<br><b>Forma Retangular:</b> $I_s = (3,46 + j2)\\text{ A}$ ; $V_s = (91,96 - j39,28)\\text{ V}$"
        },
        {
            "id": 16,
            "tipo": "Normal Engenharia Reversa (RC)",
            "enunciado": "Em um circuito paralelo RC composto por $R = 10\\ \\Omega$ e $X_C = 10\\ \\Omega$, o instrumento de teste acusa uma corrente local no resistor de $I_R = 5\\angle{45^\\circ}\\text{ A}$. Calcule fasorialmente a tensão da fonte de alimentação global ($V_s$) e a corrente total consumida pelo circuito ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $V_s = 50\\angle{45^\\circ}\\text{ V}$ ; $I_s = 7,07\\angle{90^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $V_s = (35,36 + j35,36)\\text{ V}$ ; $I_s = (0 + j7,07)\\text{ A}$"
        },
        {
            "id": 17,
            "tipo": "Engenharia Reversa (RL)",
            "enunciado": "Em uma malha série RL composta por $R = 50\\ \\Omega$ e $X_L = 120\\ \\Omega$, uma ponta de prova acusa que a tensão desenvolvida especificamente nos terminais do indutor vale $V_L = 240\\angle{120^\\circ}\\text{ V}$. Calcule por engenharia reversa a corrente total do circuito ($I_s$) e a tensão fornecida pela fonte principal ($V_s$).",
            "resposta": "<b>Forma Polar:</b> $I_s = 2\\angle{30^\\circ}\\text{ A}$ ; $V_s = 260\\angle{97,38^\\circ}\\text{ V}$<br><b>Forma Retangular:</b> $I_s = (1,73 + j1)\\text{ A}$ ; $V_s = (-33,40 + j257,85)\\text{ V}$"
        },
        {
            "id": 18,
            "tipo": "Normal Engenharia Reversa (RLC)",
            "enunciado": "Um circuito série com parâmetros $R = 4\\ \\Omega$, $X_L = 12\\ \\Omega$ e $X_C = 9\\ \\Omega$ é alimentado por uma fonte desconhecida. Um multímetro de bancada afere que a tensão de queda no resistor é $V_R = 12\\angle{-15^\\circ}\\text{ V}$. Encontre a corrente total ($I_s$) e a tensão fasorial da fonte de alimentação ($V_s$).",
            "resposta": "<b>Forma Polar:</b> $I_s = 3\\angle{-15^\\circ}\\text{ A}$ ; $V_s = 15\\angle{21,87^\\circ}\\text{ V}$<br><b>Forma Retangular:</b> $I_s = (2,90 - j0,78)\\text{ A}$ ; $V_s = (13,92 + j5,59)\\text{ V}$"
        },
        {
            "id": 19,
            "tipo": "Normal Engenharia Reversa (RLC)",
            "enunciado": "Um circuito paralelo possui ramos com $R = 30\\ \\Omega$, $X_L = 15\\ \\Omega$ e $X_C = 15\\ \\Omega$. A medição da corrente sobre o indutor revelou o valor $I_L = 10\\angle{-45^\\circ}\\text{ A}$. Determine, empregando conceitos de circuitos ressonantes, a tensão do barramento ($V_s$) e a corrente fornecida pela fonte principal ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $V_s = 150\\angle{45^\\circ}\\text{ V}$ ; $I_s = 5\\angle{45^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $V_s = (106,07 + j106,07)\\text{ V}$ ; $I_s = (3,54 + j3,54)\\text{ A}$"
        },
        {
            "id": 20,
            "tipo": "Normal Engenharia Reversa (Misto)",
            "enunciado": "Um circuito possui uma carga indutiva equivalente a $Z_L = 50\\angle{36,87^\\circ}\\ \\Omega$ conectada em paralelo com um capacitor de reatância $X_C = 50\\ \\Omega$ ($Z_C = 50\\angle{-90^\\circ}\\ \\Omega$). A corrente de ramo medida na carga indutiva é $I_{Z} = 2\\angle{0^\\circ}\\text{ A}$. Faça a engenharia reversa para encontrar a tensão de nó ($V_s$) e o fasor de corrente total ($I_s$).",
            "resposta": "<b>Forma Polar:</b> $V_s = 100\\angle{36,87^\\circ}\\text{ V}$ ; $I_s = 1,79\\angle{63,43^\\circ}\\text{ A}$<br><b>Forma Retangular:</b> $V_s = (80 + j60)\\text{ V}$ ; $I_s = (0,80 + j1,60)\\text{ A}$"
        }
    ]
};

// ==========================================
// === CONTROLE DO MENU LATERAL =============
// ==========================================
function toggleMenu(idMenu) {
    const menu = document.getElementById(idMenu);
    if(menu) menu.classList.toggle('ativo');
}

function carregarConteudo(modulo) {
    const painel = document.getElementById('painel-dinamico');
    if (!painel) return;

    if (modulo === 'inicio') {
        painel.innerHTML = `
            <div class="container-inicio">
                <img src="/static/imagens/capa.jpeg" alt="Página Inicial" class="imagem-inicio" style="max-width:100%; height:auto;">
            </div>
        `;
    }
    else if (modulo === 'exercicios') {
        painel.innerHTML = `
            <div style="max-width: 500px; margin: 40px auto; padding: 30px; border: 1px solid #ddd; border-radius: 8px; background: #fff; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <h3 style="text-align: center; margin-bottom: 25px; color: #2c3e50; font-family: Arial, sans-serif;">Gerador de Exercícios Customizado</h3>
                <div style="margin-bottom: 25px; font-family: Arial, sans-serif;">
                    <div style="margin-bottom: 20px; text-align: left;">
                        <label style="display: block; font-weight: bold; color: #34495e; margin-bottom: 8px; font-size: 14px;">Número de Questões (1 a 20):</label>
                        <input type="number" id="num-questoes" value="20" min="1" max="20" style="padding: 12px; border: 2px solid #bdc3c7; border-radius: 4px; font-size: 16px; width: 100%; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 20px; text-align: left;">
                        <label style="display: block; font-weight: bold; color: #34495e; margin-bottom: 8px; font-size: 14px;">Tipo de Circuito:</label>
                        <select id="tipo-circuito" style="padding: 12px; border: 2px solid #bdc3c7; border-radius: 4px; font-size: 16px; width: 100%; box-sizing: border-box;">
                            <option value="todos">Todos (Mesclado)</option>
                            <option value="reversa">Apenas Engenharia Reversa</option>
                            <option value="normal">Apenas Circuitos Clássicos</option>
                        </select>
                    </div>
                </div>
                <div style="text-align: center;">
                    <button onclick="enviarGerarExercicios()" style="background-color: #2980b9; color: white; border: none; padding: 14px 30px; font-size: 16px; font-weight: bold; border-radius: 4px; cursor: pointer; width: 100%;">
                        Gerar Lista de Exercícios
                    </button>
                </div>
            </div>
            <div id="conteudo-exercicios" style="margin-top: 20px;"></div>
        `;
    } else if (modulo === 'circuito-rl') {
        painel.innerHTML = `
            <h2>Análise de Circuitos RL</h2>
            <div class="grid-4-partes">
                <div class="quadrante">
                    <h3>RL - Série</h3>
                    <div class="container-imagem"><img src="/static/imagens/rl_serie.jpg" alt="Esquema Circuito RL Série" class="imagem-circuito"></div>
                </div>
                <div class="quadrante">
                    <h3>RL - Paralelo</h3>
                    <div class="container-imagem"><img src="/static/imagens/rl_paralelo.jpg" alt="Esquema Circuito RL Paralelo" class="imagem-circuito"></div>
                </div>
                <div class="quadrante">
                    <h4>Parâmetros da Fonte e Componentes</h4>
                    <div class="form-linha">
                        <div class="input-item"><label>V</label><input type="number" id="v-serie" step="0.1"></div>
                        <div class="input-item"><label>R (Ω)</label><input type="number" id="r-serie" step="0.1"></div>
                        <div class="input-item"><label>L (mH)</label><input type="number" id="l-serie" step="0.1"></div>
                        <div class="input-item"><label>f (Hz)</label><input type="number" id="f-serie" step="0.1"></div>
                    </div>
                    <div class="botoes-acao">
                        <button class="btn-calc" onclick="calcularSerie()">Calcular</button>
                        <button class="btn-graf" onclick="abrirGraficosSerie()">Exibir Gráficos</button>
                    </div>
                    <div class="resultados-linha">
                        <p><strong>X<sub>L</sub>:</strong> <span id="res-xl-serie">-</span> Ω</p>
                        <p><strong>I:</strong> <span id="res-i-serie">-</span> A</p>
                        <p><strong>V<sub>R</sub>:</strong> <span id="res-vr-serie">-</span> V</p>
                        <p><strong>V<sub>L</sub>:</strong> <span id="res-vl-serie">-</span> V</p>
                    </div>
                </div>
                <div class="quadrante">
                    <h4>Parâmetros da Fonte e Componentes</h4>
                    <div class="form-linha">
                        <div class="input-item"><label>V</label><input type="number" id="v-paralelo" step="0.1"></div>
                        <div class="input-item"><label>R (Ω)</label><input type="number" id="r-paralelo" step="0.1"></div>
                        <div class="input-item"><label>L (mH)</label><input type="number" id="l-paralelo" step="0.1"></div>
                        <div class="input-item"><label>f (Hz)</label><input type="number" id="f-paralelo" step="0.1"></div>
                    </div>
                    <div class="botoes-acao">
                        <button class="btn-calc" onclick="calcularParalelo()">Calcular</button>
                        <button class="btn-graf" onclick="abrirGraficosParalelo()">Exibir Gráficos</button>
                    </div>
                    <div class="resultados-linha">
                        <p><strong>X<sub>L</sub>:</strong> <span id="res-xl-paralelo">-</span> Ω</p>
                        <p><strong>I<sub>T</sub>:</strong> <span id="res-it-paralelo">-</span> A</p>
                        <p><strong>I<sub>R</sub>:</strong> <span id="res-ir-paralelo">-</span> A</p>
                        <p><strong>I<sub>L</sub>:</strong> <span id="res-il-paralelo">-</span> A</p>
                    </div>
                </div>
            </div>
        `;
    } else if (modulo === 'circuito-rc') {
        painel.innerHTML = `
            <h2>Análise de Circuitos RC</h2>
            <div class="grid-4-partes">
                <div class="quadrante">
                    <h3>RC - Série</h3>
                    <div class="container-imagem"><img src="/static/imagens/rc_serie.jpg" alt="Esquema Circuito RC Série" class="imagem-circuito"></div>
                </div>
                <div class="quadrante">
                    <h3>RC - Paralelo</h3>
                    <div class="container-imagem"><img src="/static/imagens/rc_paralelo.jpg" alt="Esquema Circuito RC Paralelo" class="imagem-circuito"></div>
                </div>
                <div class="quadrante">
                    <h4>Parâmetros da Fonte e Componentes</h4>
                    <div class="form-linha">
                        <div class="input-item"><label>V</label><input type="number" id="v-rc-serie" step="0.1"></div>
                        <div class="input-item"><label>R (Ω)</label><input type="number" id="r-rc-serie" step="0.1"></div>
                        <div class="input-item"><label>C (µF)</label><input type="number" id="c-rc-serie" step="0.1"></div>
                        <div class="input-item"><label>f (Hz)</label><input type="number" id="f-rc-serie" step="0.1"></div>
                    </div>
                    <div class="botoes-acao">
                        <button class="btn-calc" onclick="calcularSerieRC()">Calcular</button>
                        <button class="btn-graf" onclick="abrirGraficosSerieRC()">Exibir Gráficos</button>
                    </div>
                    <div class="resultados-linha">
                        <p><strong>X<sub>C</sub>:</strong> <span id="res-xc-serie">-</span> Ω</p>
                        <p><strong>I:</strong> <span id="res-i-rc-serie">-</span> A</p>
                        <p><strong>V<sub>R</sub>:</strong> <span id="res-vr-rc-serie">-</span> V</p>
                        <p><strong>V<sub>C</sub>:</strong> <span id="res-vc-serie">-</span> V</p>
                    </div>
                </div>
                <div class="quadrante">
                    <h4>Parâmetros da Fonte e Componentes</h4>
                    <div class="form-linha">
                        <div class="input-item"><label>V</label><input type="number" id="v-rc-paralelo" step="0.1"></div>
                        <div class="input-item"><label>R (Ω)</label><input type="number" id="r-rc-paralelo" step="0.1"></div>
                        <div class="input-item"><label>C (µF)</label><input type="number" id="c-rc-paralelo" step="0.1"></div>
                        <div class="input-item"><label>f (Hz)</label><input type="number" id="f-rc-paralelo" step="0.1"></div>
                    </div>
                    <div class="botoes-acao">
                        <button class="btn-calc" onclick="calcularParaleloRC()">Calcular</button>
                        <button class="btn-graf" onclick="abrirGraficosParaleloRC()">Exibir Gráficos</button>
                    </div>
                    <div class="resultados-linha">
                        <p><strong>X<sub>C</sub>:</strong> <span id="res-xc-paralelo">-</span> Ω</p>
                        <p><strong>I<sub>T</sub>:</strong> <span id="res-it-rc-paralelo">-</span> A</p>
                        <p><strong>I<sub>R</sub>:</strong> <span id="res-ir-rc-paralelo">-</span> A</p>
                        <p><strong>I<sub>C</sub>:</strong> <span id="res-ic-paralelo">-</span> A</p>
                    </div>
                </div>
            </div>
        `;
    } else if (modulo === 'circuito-rlc') {
        painel.innerHTML = `
            <h2>Análise de Circuitos RLC</h2>
            <div class="grid-4-partes">
                <div class="quadrante">
                    <h3>RLC - Série</h3>
                    <div class="container-imagem"><img src="/static/imagens/rlc_serie.jpg" alt="Esquema Circuito RLC Série" class="imagem-circuito"></div>
                </div>
                <div class="quadrante">
                    <h3>RLC - Paralelo</h3>
                    <div class="container-imagem"><img src="/static/imagens/rlc_paralelo.jpg" alt="Esquema Circuito RLC Paralelo" class="imagem-circuito"></div>
                </div>
                <div class="quadrante">
                    <h4>Parâmetros da Fonte e Componentes</h4>
                    <div class="form-linha-5">
                        <div class="input-item"><label>V</label><input type="number" id="v-rlc-serie" step="0.1"></div>
                        <div class="input-item"><label>R (Ω)</label><input type="number" id="r-rlc-serie" step="0.1"></div>
                        <div class="input-item"><label>L (mH)</label><input type="number" id="l-rlc-serie" step="0.1"></div>
                        <div class="input-item"><label>C (µF)</label><input type="number" id="c-rlc-serie" step="0.1"></div>
                        <div class="input-item"><label>f (Hz)</label><input type="number" id="f-rlc-serie" step="0.1"></div>
                    </div>
                    <div class="botoes-acao">
                        <button class="btn-calc" onclick="calcularSerieRLC()">Calcular</button>
                        <button class="btn-graf" onclick="abrirGraficosSerieRLC()">Exibir Gráficos</button>
                    </div>
                    <div class="resultados-linha">
                        <p><strong>Z:</strong> <span id="res-z-serie">-</span> Ω</p>
                        <p><strong>I:</strong> <span id="res-i-rlc-serie">-</span> A</p>
                        <p><strong>X<sub>L</sub>:</strong> <span id="res-xl-rlc-serie">-</span> Ω</p>
                        <p><strong>X<sub>C</sub>:</strong> <span id="res-xc-rlc-serie">-</span> Ω</p>
                    </div>
                </div>
                <div class="quadrante">
                    <h4>Parâmetros da Fonte e Componentes</h4>
                    <div class="form-linha-5">
                        <div class="input-item"><label>V</label><input type="number" id="v-rlc-paralelo" step="0.1"></div>
                        <div class="input-item"><label>R (Ω)</label><input type="number" id="r-rlc-paralelo" step="0.1"></div>
                        <div class="input-item"><label>L (mH)</label><input type="number" id="l-rlc-paralelo" step="0.1"></div>
                        <div class="input-item"><label>C (µF)</label><input type="number" id="c-rlc-paralelo" step="0.1"></div>
                        <div class="input-item"><label>f (Hz)</label><input type="number" id="f-rlc-paralelo" step="0.1"></div>
                    </div>
                    <div class="botoes-acao">
                        <button class="btn-calc" onclick="calcularParaleloRLC()">Calcular</button>
                        <button class="btn-graf" onclick="abrirGraficosParaleloRLC()">Exibir Gráficos</button>
                    </div>
                    <div class="resultados-linha">
                        <p><strong>Z:</strong> <span id="res-z-paralelo">-</span> Ω</p>
                        <p><strong>I<sub>T</sub>:</strong> <span id="res-it-rlc-paralelo">-</span> A</p>
                        <p><strong>I<sub>L</sub>:</strong> <span id="res-il-rlc-paralelo">-</span> A</p>
                        <p><strong>I<sub>C</sub>:</strong> <span id="res-ic-rlc-paralelo">-</span> A</p>
                    </div>
                </div>
            </div>
        `;
    }
    else if (modulo === 'trifasico-yy') {
        painel.innerHTML = `
            <h2>Circuitos Trifásicos - Y-Y Aterrado</h2>
            <div class="imagens-container" style="display: flex; gap: 20px; margin-bottom: 20px; justify-content: space-between;">
                <div style="width: 49%; border: 1px solid #ccc; text-align: center; padding: 5px; background:#fff;">
                    <img src="/static/imagens/circuito_yy.png" alt="Esquema do Circuito Y-Y" style="max-width: 100%; height: auto;">
                </div>
                <div style="width: 49%; border: 1px solid #ccc; text-align: center; padding: 5px; background:#fff;">
                    <img src="/static/imagens/formulas_yy.png" alt="Fórmulas do Sistema" style="max-width: 100%; height: auto;">
                </div>
            </div>

            <fieldset style="margin-bottom: 15px; padding: 15px; border: 1px solid #ccc; background:#fff;">
                <legend><strong>Parâmetros de Entrada (Use 'i' para complexos em impedâncias)</strong></legend>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                    <div>
                        <h4 style="margin-bottom:8px; color:#2980b9;">Tensões de Fase (Módulo / Ângulo°)</h4>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label>Van: </label><input type="number" id="in-van-mod" value="127" style="width:50%;">
                            <input type="number" id="in-van-ang" value="0" style="width:50%;">
                        </div>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label>Vbn: </label><input type="number" id="in-vbn-mod" value="127" style="width:50%;">
                            <input type="number" id="in-vbn-ang" value="-120" style="width:50%;">
                        </div>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label>Vcn: </label><input type="number" id="in-vcn-mod" value="127" style="width:50%;">
                            <input type="number" id="in-vcn-ang" value="120" style="width:50%;">
                        </div>
                    </div>
                    <div>
                        <h4 style="margin-bottom:8px; color:#2980b9;">Impedâncias (Fonte e Linha)</h4>
                        <label>Zfa: </label><input type="text" id="in-zfa" value="0" style="width:90%; margin-bottom:5px;">
                        <label>Zfb: </label><input type="text" id="in-zfb" value="0" style="width:90%; margin-bottom:5px;">
                        <label>Zfc: </label><input type="text" id="in-zfc" value="0" style="width:90%; margin-bottom:5px;">
                        <div style="margin-top:5px;">
                            <label>ZLa: </label><input type="text" id="in-zla" value="0" style="width:90%; margin-bottom:5px;">
                            <label>ZLb: </label><input type="text" id="in-zlb" value="0" style="width:90%; margin-bottom:5px;">
                            <label>ZLc: </label><input type="text" id="in-zlc" value="0" style="width:90%; margin-bottom:5px;">
                        </div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <h4 style="margin-bottom:8px; color:#2980b9;">Impedâncias de Carga e Neutro</h4>
                        <label>ZA: </label><input type="text" id="in-za" value="10+3i" style="width:90%; margin-bottom:5px;">
                        <label>ZB: </label><input type="text" id="in-zb" value="10+3i" style="width:90%; margin-bottom:5px;">
                        <label>ZC: </label><input type="text" id="in-zc" value="10+3i" style="width:90%; margin-bottom:5px;">
                        <label>Zo: </label><input type="text" id="in-zo" value="0+0i" style="width:90%; margin-bottom:5px;">
                    </div>
                </div>
            </fieldset>

            <fieldset style="padding: 15px; background-color: #f9f9f9; border: 1px solid #ccc;">
                <legend><strong>Painel de Resultados Otimizado</strong></legend>
                <div class="grid-resultados-trifasico">
                    <div class="col-resultado">
                        <h4>Correntes de Fase/Linha</h4>
                        <div id="out-correntes" class="res-bloco">Aguardando cálculo...</div>
                    </div>
                    <div class="col-resultado">
                        <h4>Tensões de Fase na Carga</h4>
                        <div id="out-tensoes-fase" class="res-bloco">Aguardando cálculo...</div>
                    </div>
                    <div class="col-resultado">
                        <h4>Tensões de Linha na Carga</h4>
                        <div id="out-tensoes-linha" class="res-bloco">Aguardando cálculo...</div>
                    </div>
                    <div class="col-resultado">
                        <h4>Potências Modais (Carga)</h4>
                        <div id="out-potencias" class="res-bloco">Aguardando cálculo...</div>
                    </div>
                </div>
            </fieldset>

            <div style="margin-top: 20px; display: flex; gap: 20px;">
                <button class="btn-calc" onclick="calcularTrifasicoYY()" style="padding: 10px 20px;">Calcular</button>
                <button class="btn-graf" onclick="abrirGraficosTrifasico()" style="padding: 10px 20px;">Exibir Gráficos</button>
            </div>
        `;
    } else if (modulo === 'trifasico-ydelta') {
        painel.innerHTML = `
            <h2>Circuitos Trifásicos - Y-Delta</h2>

            <div class="imagens-container" style="display: flex; gap: 20px; margin-bottom: 20px; justify-content: space-between;">
                <div style="width: 49%; border: 1px solid #ccc; text-align: center; padding: 5px; background:#fff;">
                    <img src="/static/imagens/circuito_ydelta.png" alt="Esquema Y-Delta" style="max-width: 100%; height: auto;">
                </div>
                <div style="width: 49%; border: 1px solid #ccc; text-align: center; padding: 5px; background:#fff;">
                    <img src="/static/imagens/formulas_ydelta.png" alt="Fórmulas Y-Delta" style="max-width: 100%; height: auto;">
                </div>
            </div>

            <fieldset style="margin-bottom: 15px; padding: 15px; border: 1px solid #ccc; background:#fff;">
                <legend><strong>Entrada de Dados</strong></legend>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                    <div>
                        <h4 style="margin-bottom:8px; color:#2980b9;">Tensões da Fonte (Mod / Âng°)</h4>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:40px;">Van:</label>
                            <input type="number" id="in-van-mod-yd" value="127" style="width:45%;">
                            <input type="number" id="in-van-ang-yd" value="0" style="width:45%;">
                        </div>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:40px;">Vbn:</label>
                            <input type="number" id="in-vbn-mod-yd" value="127" style="width:45%;">
                            <input type="number" id="in-vbn-ang-yd" value="-120" style="width:45%;">
                        </div>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:40px;">Vcn:</label>
                            <input type="number" id="in-vcn-mod-yd" value="127" style="width:45%;">
                            <input type="number" id="in-vcn-ang-yd" value="120" style="width:45%;">
                        </div>
                    </div>

                    <div>
                        <h4 style="margin-bottom:8px; color:#2980b9;">Impedâncias de Fonte e Linha (Ω)</h4>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:60px;">Fase A:</label>
                            <input type="text" id="in-zfa-yd" value="0" style="width:40%;" placeholder="Zfa">
                            <input type="text" id="in-zla-yd" value="1+1i" style="width:40%;" placeholder="ZLa">
                        </div>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:60px;">Fase B:</label>
                            <input type="text" id="in-zfb-yd" value="0" style="width:40%;" placeholder="Zfb">
                            <input type="text" id="in-zlb-yd" value="1+1i" style="width:40%;" placeholder="ZLb">
                        </div>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:60px;">Fase C:</label>
                            <input type="text" id="in-zfc-yd" value="0" style="width:40%;" placeholder="Zfc">
                            <input type="text" id="in-zlc-yd" value="1+1i" style="width:40%;" placeholder="ZLc">
                        </div>
                    </div>

                    <div>
                        <h4 style="margin-bottom:8px; color:#2980b9;">Impedâncias da Carga (Ω)</h4>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:40px;">ZAB:</label>
                            <input type="text" id="in-zab-yd" value="10+5i" style="width:80%;">
                        </div>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:40px;">ZBC:</label>
                            <input type="text" id="in-zbc-yd" value="10+5i" style="width:80%;">
                        </div>
                        <div style="display:flex; gap:5px; margin-bottom:5px;">
                            <label style="width:40px;">ZCA:</label>
                            <input type="text" id="in-zca-yd" value="10+5i" style="width:80%;">
                        </div>
                    </div>
                </div>
            </fieldset>

            <!-- Painel de Resultados Padronizado (5 Colunas) -->
            <fieldset style="padding: 15px; background-color: #f9f9f9; border: 1px solid #ccc;">
                <legend><strong>Painel de Resultados Otimizado</strong></legend>
                <div class="grid-resultados-trifasico-5col">
                    <div class="col-resultado">
                        <h4>Correntes de Linha</h4>
                        <div id="out-i-linha-yd" class="res-bloco">Aguardando...</div>
                    </div>
                    <div class="col-resultado">
                        <h4>Correntes de Fase</h4>
                        <div id="out-i-fase-yd" class="res-bloco">Aguardando...</div>
                    </div>
                    <div class="col-resultado">
                        <h4>Tensões de Linha</h4>
                        <div id="out-v-linha-yd" class="res-bloco">Aguardando...</div>
                    </div>
                    <div class="col-resultado">
                        <h4>Tensões de Fase</h4>
                        <div id="out-v-fase-yd" class="res-bloco">Aguardando...</div>
                    </div>
                    <div class="col-resultado">
                        <h4>Potências</h4>
                        <div id="out-potencias-yd" class="res-bloco">Aguardando...</div>
                    </div>
                </div>
            </fieldset>

            <div style="margin-top: 20px; display: flex; gap: 20px;">
                <button class="btn-calc" onclick="calcularTrifasicoYDelta()" style="padding: 10px 20px;">Calcular</button>
                <button class="btn-graf" onclick="abrirGraficosYDelta()" style="padding: 10px 20px;">Exibir Gráficos</button>
            </div>

            <!-- Div de Destino dos Gráficos -->
            <div id="container-graficos-trifasico-yd" style="margin-top: 20px;"></div>
        `;
    }
}

// ==========================================
// === FUNÇÃO DE CÁLCULO TRIFÁSICO YY =======
// ==========================================
function calcularTrifasicoYY() {
    const obterTexto = (id) => {
        const el = document.getElementById(id);
        return el ? el.value.trim() : "0";
    };

    const obterNumero = (id) => {
        const el = document.getElementById(id);
        return el ? Number(el.value) : 0;
    };

    const payload = {
        van_mod: obterNumero("in-van-mod"), van_ang: obterNumero("in-van-ang"),
        vbn_mod: obterNumero("in-vbn-mod"), vbn_ang: obterNumero("in-vbn-ang"),
        vcn_mod: obterNumero("in-vcn-mod"), vcn_ang: obterNumero("in-vcn-ang"),
        zfa: obterTexto("in-zfa"), zfb: obterTexto("in-zfb"), zfc: obterTexto("in-zfc"),
        zla: obterTexto("in-zla"), zlb: obterTexto("in-zlb"), zlc: obterTexto("in-zlc"),
        za: obterTexto("in-za"), zb: obterTexto("in-zb"), zc: obterTexto("in-zc"), zo: obterTexto("in-zo")
    };

    fetch('/calcular_trifasico_yy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.erro); });
        }
        return response.json();
    })
    .then(res => {
        const v = (val) => {
            if (val === undefined || val === null) return '-';
            if (typeof val === 'object') return val.polar || val.retangular || '-';
            return val;
        };

        const getPolar = (obj) => (obj && typeof obj === 'object') ? obj.polar : null;
        const getRet = (obj) => (obj && typeof obj === 'object') ? obj.retangular : null;

        document.getElementById("out-correntes").innerHTML = `
            <p><b>I<sub>AN</sub>:</b><br> P: ${v(getPolar(res.ian) || res.ian_pol || res.ian)}<br> R: ${v(getRet(res.ian) || res.ian_ret)}</p><br>
            <p><b>I<sub>BN</sub>:</b><br> P: ${v(getPolar(res.ibn) || res.ibn_pol || res.ibn)}<br> R: ${v(getRet(res.ibn) || res.ibn_ret)}</p><br>
            <p><b>I<sub>CN</sub>:</b><br> P: ${v(getPolar(res.icn) || res.icn_pol || res.icn)}<br> R: ${v(getRet(res.icn) || res.icn_ret)}</p><br>
            <p><b>I<sub>N</sub>:</b><br> P: ${v(getPolar(res.in_n) || getPolar(res.in) || res.in_pol || res.in)}<br> R: ${v(getRet(res.in_n) || getRet(res.in) || res.in_ret)}</p>
        `;

        document.getElementById("out-tensoes-fase").innerHTML = `
            <p><b>V<sub>AN</sub>:</b><br> P: ${v(getPolar(res.van_c) || res.van_c_pol || res.van)}<br> R: ${v(getRet(res.van_c) || res.van_c_ret)}</p><br>
            <p><b>V<sub>BN</sub>:</b><br> P: ${v(getPolar(res.vbn_c) || res.vbn_c_pol || res.vbn)}<br> R: ${v(getRet(res.vbn_c) || res.vbn_c_ret)}</p><br>
            <p><b>V<sub>CN</sub>:</b><br> P: ${v(getPolar(res.vcn_c) || res.vcn_c_pol || res.vcn)}<br> R: ${v(getRet(res.vcn_c) || res.vcn_c_ret)}</p>
        `;

        document.getElementById("out-tensoes-linha").innerHTML = `
            <p><b>V<sub>AB</sub>:</b><br> P: ${v(getPolar(res.vab) || res.vab_pol || res.vab)}<br> R: ${v(getRet(res.vab) || res.vab_ret)}</p><br>
            <p><b>V<sub>BC</sub>:</b><br> P: ${v(getPolar(res.vbc) || res.vbc_pol || res.vbc)}<br> R: ${v(getRet(res.vbc) || res.vbc_ret)}</p><br>
            <p><b>V<sub>CA</sub>:</b><br> P: ${v(getPolar(res.vca) || res.vca_pol || res.vca)}<br> R: ${v(getRet(res.vca) || res.vca_ret)}</p>
        `;

        document.getElementById("out-potencias").innerHTML = `
            <p><b>Fase A:</b><br> S: ${v(res.sa)} VA<br> P: ${v(res.pa)} W<br> Q: ${v(res.qa)} VAr</p><br>
            <p><b>Fase B:</b><br> S: ${v(res.sb)} VA<br> P: ${v(res.pb)} W<br> Q: ${v(res.qb)} VAr</p><br>
            <p><b>Fase C:</b><br> S: ${v(res.sc)} VA<br> P: ${v(res.pc)} W<br> Q: ${v(res.qc)} VAr</p><br>
            <p style="border-top: 1px solid #ccc; padding-top: 5px; margin-top: 5px;"><b>Total Trifásico:</b><br> S: ${v(res.stotal)} VA<br> P: ${v(res.ptotal)} W<br> Q: ${v(res.qtotal)} VAr</p>
        `;
    })
    .catch(error => alert("Erro ao calcular circuito trifásico: " + error.message));
}

// ==========================================
// === RENDERIZADOR INTERNO DE EXERCÍCIOS ====
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("conteudo-exercicios");
    if (container) {
        const urlParams = new URLSearchParams(window.location.search);
        const qtd = parseInt(urlParams.get('qtd')) || 20;
        const tipo = urlParams.get('tipo') || 'todos';
        gerarFolhaDeExercicios(container, qtd, tipo);
    }
});

function enviarGerarExercicios() {
    const campoQtd = document.getElementById('num-questoes');
    const qtd = (campoQtd && campoQtd.value) ? campoQtd.value : 20;
    const campoTipo = document.getElementById('tipo-circuito');
    const tipo = campoTipo ? campoTipo.value : 'todos';

    const container = document.getElementById("conteudo-exercicios");
    if (container) gerarFolhaDeExercicios(container, parseInt(qtd), tipo);
}

function gerarFolhaDeExercicios(container, quantidade, tipoFiltro) {
    container.innerHTML = "";
    let poolQuestoes = [];

    if (tipoFiltro === "normal") poolQuestoes = [...bancoDeExercicios.normal];
    else if (tipoFiltro === "reversa") poolQuestoes = [...bancoDeExercicios.engenharia_reversa];
    else poolQuestoes = [...bancoDeExercicios.normal, ...bancoDeExercicios.engenharia_reversa];

    poolQuestoes.sort(() => Math.random() - 0.5);
    const selecionados = poolQuestoes.slice(0, Math.min(quantidade, poolQuestoes.length));

    selecionados.forEach((exercicio, index) => {
        const card = document.createElement("div");
        card.style = "border: 1px solid #ddd; border-left: 5px solid #2980b9; padding: 15px; margin-bottom: 15px; background: #fff; border-radius: 4px; font-family: Arial, sans-serif;";
        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; margin-bottom: 10px; font-size:0.9rem; color:#555;">
                <span style="padding: 3px 8px; background: #34495e; color: white; border-radius:3px; font-weight:bold; text-transform:uppercase;">${exercicio.tipo}</span>
                <strong>Questão ${index + 1}</strong>
            </div>
            <p style="font-size: 1.05rem; line-height: 1.5; color:#2c3e50;">${exercicio.enunciado}</p>
            <hr style="border: 0; border-top: 1px dashed #eee; margin: 10px 0;">
            <div>
                <button onclick="toggleResposta(this)" style="padding: 5px 10px; cursor: pointer; border: 1px solid #7f8c8d; background: transparent; border-radius: 4px;">Mostrar Gabarito</button>
                <div style="display: none; margin-top: 10px; padding: 10px; background-color: #e8f8f5; color: #27ae60; border: 1px solid #2ecc71; border-radius: 4px; line-height: 1.6;">
                    <strong>Gabarito Oficial:</strong><br>${exercicio.resposta}
                </div>
            </div>
        `;
        container.appendChild(card);
    });

    if (typeof MathJax !== "undefined") MathJax.typesetPromise();
}

function toggleResposta(botao) {
    const containerResposta = botao.nextElementSibling;
    if (containerResposta.style.display === "none" || containerResposta.style.display === "") {
        containerResposta.style.display = "block";
        botao.innerText = "Ocultar Gabarito";
        botao.style.backgroundColor = "#7f8c8d";
        botao.style.color = "white";
    } else {
        containerResposta.style.display = "none";
        botao.innerText = "Mostrar Gabarito";
        botao.style.backgroundColor = "transparent";
        botao.style.color = "inherit";
    }
}

// ==========================================
// === CÁLCULOS DOS CIRCUITOS MONOFÁSICOS ===
// ==========================================
function calcularSerie() {
    const v = document.getElementById('v-serie').value;
    const r = document.getElementById('r-serie').value;
    const l = document.getElementById('l-serie').value;
    const f = document.getElementById('f-serie').value;
    if (!v || !r || !l || !f) { alert("Preencha todos os parâmetros."); return; }

    fetch('/calcular_serie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v, r, l, f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-xl-serie').innerText = data.xl;
            document.getElementById('res-i-serie').innerText = data.i;
            document.getElementById('res-vr-serie').innerText = data.vr;
            document.getElementById('res-vl-serie').innerText = data.vl;
        } else alert("Erro: " + data.erro);
    });
}

function calcularParalelo() {
    const v = document.getElementById('v-paralelo').value;
    const r = document.getElementById('r-paralelo').value;
    const l = document.getElementById('l-paralelo').value;
    const f = document.getElementById('f-paralelo').value;
    if (!v || !r || !l || !f) { alert("Preencha todos os parâmetros."); return; }

    fetch('/calcular_paralelo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v, r, l, f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-xl-paralelo').innerText = data.xl;
            document.getElementById('res-it-paralelo').innerText = data.it;
            document.getElementById('res-ir-paralelo').innerText = data.ir;
            document.getElementById('res-il-paralelo').innerText = data.il;
        } else alert("Erro: " + data.erro);
    });
}

function calcularSerieRC() {
    const v = document.getElementById('v-rc-serie').value;
    const r = document.getElementById('r-rc-serie').value;
    const c = document.getElementById('c-rc-serie').value;
    const f = document.getElementById('f-rc-serie').value;
    if (!v || !r || !c || !f) { alert("Preencha todos os parâmetros."); return; }

    fetch('/calcular_rc_serie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v, r, c, f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-xc-serie').innerText = data.xc;
            document.getElementById('res-i-rc-serie').innerText = data.i;
            document.getElementById('res-vr-rc-serie').innerText = data.vr;
            document.getElementById('res-vc-serie').innerText = data.vc;
        } else alert("Erro: " + data.erro);
    });
}

function calcularParaleloRC() {
    const v = document.getElementById('v-rc-paralelo').value;
    const r = document.getElementById('r-rc-paralelo').value;
    const c = document.getElementById('c-rc-paralelo').value;
    const f = document.getElementById('f-rc-paralelo').value;
    if (!v || !r || !c || !f) { alert("Preencha todos os parâmetros."); return; }

    fetch('/calcular_rc_paralelo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v, r, c, f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-xc-paralelo').innerText = data.xc;
            document.getElementById('res-it-rc-paralelo').innerText = data.it;
            document.getElementById('res-ir-rc-paralelo').innerText = data.ir;
            document.getElementById('res-ic-paralelo').innerText = data.ic;
        } else alert("Erro: " + data.erro);
    });
}

function calcularSerieRLC() {
    const v = document.getElementById('v-rlc-serie').value;
    const r = document.getElementById('r-rlc-serie').value;
    const l = document.getElementById('l-rlc-serie').value;
    const c = document.getElementById('c-rlc-serie').value;
    const f = document.getElementById('f-rlc-serie').value;
    if (!v || !r || !l || !c || !f) { alert("Preencha todos os parâmetros."); return; }

    fetch('/calcular_rlc_serie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v, r, l, c, f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-z-serie').innerText = data.z;
            document.getElementById('res-i-rlc-serie').innerText = data.i;
            document.getElementById('res-xl-rlc-serie').innerText = data.xl;
            document.getElementById('res-xc-rlc-serie').innerText = data.xc;
        } else alert("Erro: " + data.erro);
    });
}

function calcularParaleloRLC() {
    const v = document.getElementById('v-rlc-paralelo').value;
    const r = document.getElementById('r-rlc-paralelo').value;
    const l = document.getElementById('l-rlc-paralelo').value;
    const c = document.getElementById('c-rlc-paralelo').value;
    const f = document.getElementById('f-rlc-paralelo').value;
    if (!v || !r || !l || !c || !f) { alert("Preencha todos os parâmetros."); return; }

    fetch('/calcular_rlc_paralelo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v, r, l, c, f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-z-paralelo').innerText = data.z;
            document.getElementById('res-it-rlc-paralelo').innerText = data.it;
            document.getElementById('res-il-rlc-paralelo').innerText = data.il;
            document.getElementById('res-ic-rlc-paralelo').innerText = data.ic;
        } else alert("Erro: " + data.erro);
    });
}

// ==========================================
// === CONTROLE DE MÓDULOS DE GRÁFICOS ======
// ==========================================
function exibirGraficoGenerico(rota_url, dados_json) {
    const modal = document.getElementById('modal-graficos');
    const imgGrafico = document.getElementById('img-grafico');
    const msgCarregando = document.getElementById('msg-carregando');
    if (!modal || !imgGrafico || !msgCarregando) return;

    modal.style.display = "block";
    imgGrafico.style.display = "none";
    msgCarregando.style.display = "block";

    let containerCheckboxes = document.getElementById('container-chk-graficos');
    if (!containerCheckboxes) {
        containerCheckboxes = document.createElement('div');
        containerCheckboxes.id = 'container-chk-graficos';
        containerCheckboxes.style = "text-align: center; margin-top: 15px; font-family: Arial, sans-serif; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;";
        imgGrafico.parentNode.insertBefore(containerCheckboxes, imgGrafico.nextSibling);
    }

    let chhtml = `<label style="cursor:pointer; font-weight:bold; color:blue;"><input type="checkbox" id="chk_v" checked style="margin-right:5px;"> V (Fonte)</label>`;
    let checkIds = ['chk_v'];

    if (rota_url.includes('rlc_serie')) {
        chhtml += `
            <label style="cursor:pointer; font-weight:bold; color:green;"><input type="checkbox" id="chk_vr" checked style="margin-right:5px;"> VR</label>
            <label style="cursor:pointer; font-weight:bold; color:purple;"><input type="checkbox" id="chk_vl" checked style="margin-right:5px;"> VL</label>
            <label style="cursor:pointer; font-weight:bold; color:orange;"><input type="checkbox" id="chk_vc" checked style="margin-right:5px;"> VC</label>
            <label style="cursor:pointer; font-weight:bold; color:red;"><input type="checkbox" id="chk_i" checked style="margin-right:5px;"> I (Corrente)</label>
        `;
        checkIds.push('chk_vr', 'chk_vl', 'chk_vc', 'chk_i');
    } else if (rota_url.includes('rlc_paralelo')) {
        chhtml += `
            <label style="cursor:pointer; font-weight:bold; color:green;"><input type="checkbox" id="chk_ir" checked style="margin-right:5px;"> IR</label>
            <label style="cursor:pointer; font-weight:bold; color:purple;"><input type="checkbox" id="chk_il" checked style="margin-right:5px;"> IL</label>
            <label style="cursor:pointer; font-weight:bold; color:orange;"><input type="checkbox" id="chk_ic" checked style="margin-right:5px;"> IC</label>
            <label style="cursor:pointer; font-weight:bold; color:red;"><input type="checkbox" id="chk_i" checked style="margin-right:5px;"> IT (Total)</label>
        `;
        checkIds.push('chk_ir', 'chk_il', 'chk_ic', 'chk_i');
    } else if (rota_url.includes('rc_serie')) {
        chhtml += `
            <label style="cursor:pointer; font-weight:bold; color:green;"><input type="checkbox" id="chk_vr" checked style="margin-right:5px;"> VR</label>
            <label style="cursor:pointer; font-weight:bold; color:orange;"><input type="checkbox" id="chk_vc" checked style="margin-right:5px;"> VC</label>
            <label style="cursor:pointer; font-weight:bold; color:red;"><input type="checkbox" id="chk_i" checked style="margin-right:5px;"> I (Corrente)</label>
        `;
        checkIds.push('chk_vr', 'chk_vc', 'chk_i');
    } else if (rota_url.includes('rc_paralelo')) {
        chhtml += `
            <label style="cursor:pointer; font-weight:bold; color:green;"><input type="checkbox" id="chk_ir" checked style="margin-right:5px;"> IR</label>
            <label style="cursor:pointer; font-weight:bold; color:orange;"><input type="checkbox" id="chk_ic" checked style="margin-right:5px;"> IC</label>
            <label style="cursor:pointer; font-weight:bold; color:red;"><input type="checkbox" id="chk_i" checked style="margin-right:5px;"> IT (Total)</label>
        `;
        checkIds.push('chk_ir', 'chk_ic', 'chk_i');
    } else if (rota_url.includes('paralelo')) {
        chhtml += `
            <label style="cursor:pointer; font-weight:bold; color:green;"><input type="checkbox" id="chk_ir" checked style="margin-right:5px;"> IR</label>
            <label style="cursor:pointer; font-weight:bold; color:purple;"><input type="checkbox" id="chk_il" checked style="margin-right:5px;"> IL</label>
            <label style="cursor:pointer; font-weight:bold; color:red;"><input type="checkbox" id="chk_i" checked style="margin-right:5px;"> IT (Total)</label>
        `;
        checkIds.push('chk_ir', 'chk_il', 'chk_i');
    } else {
        chhtml += `
            <label style="cursor:pointer; font-weight:bold; color:green;"><input type="checkbox" id="chk_vr" checked style="margin-right:5px;"> VR</label>
            <label style="cursor:pointer; font-weight:bold; color:purple;"><input type="checkbox" id="chk_vl" checked style="margin-right:5px;"> VL</label>
            <label style="cursor:pointer; font-weight:bold; color:red;"><input type="checkbox" id="chk_i" checked style="margin-right:5px;"> I (Corrente)</label>
        `;
        checkIds.push('chk_vr', 'chk_vl', 'chk_i');
    }

    if (!containerCheckboxes.innerHTML || window.ultimaRotaGrafico !== rota_url) {
        containerCheckboxes.innerHTML = chhtml;
        checkIds.forEach(id => {
            const el = document.getElementById(id);
            if(el) {
                el.addEventListener('change', () => {
                    if (window.ultimosDadosGrafico) exibirGraficoGenerico(window.ultimaRotaGrafico, window.ultimosDadosGrafico);
                });
            }
        });
    }

    checkIds.forEach(id => {
        const el = document.getElementById(id);
        dados_json[id.replace('chk_', 'show_')] = el ? el.checked : true;
    });

    window.ultimaRotaGrafico = rota_url;
    window.ultimosDadosGrafico = dados_json;

    fetch(rota_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados_json)
    })
    .then(response => response.json())
    .then(data => {
        msgCarregando.style.display = "none";
        if (data.sucesso) {
            imgGrafico.src = "data:image/png;base64," + data.imagem;
            imgGrafico.style.display = "block";
        } else {
            alert("Erro ao gerar gráficos: " + data.erro);
            fecharModal();
        }
    })
    .catch(() => {
        msgCarregando.style.display = "none";
        alert("Erro de comunicação com o servidor.");
        fecharModal();
    });
}

function abrirGraficosSerie() {
    const v = document.getElementById('v-serie').value;
    const r = document.getElementById('r-serie').value;
    const l = document.getElementById('l-serie').value;
    const f = document.getElementById('f-serie').value;
    if (!v || !r || !l || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_serie', { v, r, l, f });
}

function abrirGraficosParalelo() {
    const v = document.getElementById('v-paralelo').value;
    const r = document.getElementById('r-paralelo').value;
    const l = document.getElementById('l-paralelo').value;
    const f = document.getElementById('f-paralelo').value;
    if (!v || !r || !l || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_paralelo', { v, r, l, f });
}

function abrirGraficosSerieRC() {
    const v = document.getElementById('v-rc-serie').value;
    const r = document.getElementById('r-rc-serie').value;
    const c = document.getElementById('c-rc-serie').value;
    const f = document.getElementById('f-rc-serie').value;
    if (!v || !r || !c || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_rc_serie', { v, r, c, f });
}

function abrirGraficosParaleloRC() {
    const v = document.getElementById('v-rc-paralelo').value;
    const r = document.getElementById('r-rc-paralelo').value;
    const c = document.getElementById('c-rc-paralelo').value;
    const f = document.getElementById('f-rc-paralelo').value;
    if (!v || !r || !c || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_rc_paralelo', { v, r, c, f });
}

function abrirGraficosSerieRLC() {
    const v = document.getElementById('v-rlc-serie').value;
    const r = document.getElementById('r-rlc-serie').value;
    const l = document.getElementById('l-rlc-serie').value;
    const c = document.getElementById('c-rlc-serie').value;
    const f = document.getElementById('f-rlc-serie').value;
    if (!v || !r || !l || !c || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_rlc_serie', { v, r, l, c, f });
}

function abrirGraficosParaleloRLC() {
    const v = document.getElementById('v-rlc-paralelo').value;
    const r = document.getElementById('r-rlc-paralelo').value;
    const l = document.getElementById('l-rlc-paralelo').value;
    const c = document.getElementById('c-rlc-paralelo').value;
    const f = document.getElementById('f-rlc-paralelo').value;
    if (!v || !r || !l || !c || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_rlc_paralelo', { v, r, l, c, f });
}

// ==========================================
// === GRÁFICOS TRIFÁSICOS (PLOTLY.JS) ======
// ==========================================
function abrirGraficosTrifasico() {
    const obterTexto = (id) => { const el = document.getElementById(id); return el ? el.value.trim() : "0"; };
    const obterNumero = (id) => { const el = document.getElementById(id); return el ? Number(el.value) : 0; };

    const payload = {
        van_mod: obterNumero("in-van-mod"), van_ang: obterNumero("in-van-ang"),
        vbn_mod: obterNumero("in-vbn-mod"), vbn_ang: obterNumero("in-vbn-ang"),
        vcn_mod: obterNumero("in-vcn-mod"), vcn_ang: obterNumero("in-vcn-ang"),
        zfa: obterTexto("in-zfa"), zfb: obterTexto("in-zfb"), zfc: obterTexto("in-zfc"),
        zla: obterTexto("in-zla"), zlb: obterTexto("in-zlb"), zlc: obterTexto("in-zlc"),
        za: obterTexto("in-za"), zb: obterTexto("in-zb"), zc: obterTexto("in-zc"), zo: obterTexto("in-zo")
    };

    fetch('/graficos_trifasico_yy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(dados => {
        if (!dados.sucesso) {
            alert("Erro ao calcular gráficos: " + dados.erro);
            return;
        }

        let container = document.getElementById("container-graficos-trifasico");
        if (!container) {
            container = document.createElement("div");
            container.id = "container-graficos-trifasico";
            container.style = "display: flex; flex-direction: column; align-items: center; gap: 15px; margin-top: 20px;";
            document.getElementById('painel-dinamico').appendChild(container);
        }

        container.innerHTML = `
            <!-- Painel Inteligente de Seleção de Visibilidade -->
            <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; background: #f8f9fa; padding: 12px; border-radius: 6px; border: 1px solid #ddd; font-family: Arial, sans-serif; font-size: 0.9rem; width: 100%; max-width: 1120px; box-sizing: border-box;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <strong style="color:#2c3e50;">Fases:</strong>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-van" checked> V<sub>AN</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vbn" checked> V<sub>BN</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vcn" checked> V<sub>CN</sub></label>
                </div>
                <span style="border-left: 1px solid #ccc; margin: 0 5px;"></span>
                <div style="display:flex; align-items:center; gap:8px;">
                    <strong style="color:#2c3e50;">Linhas:</strong>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vab"> V<sub>AB</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vbc"> V<sub>BC</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vca"> V<sub>CA</sub></label>
                </div>
                <span style="border-left: 1px solid #ccc; margin: 0 5px;"></span>
                <div style="display:flex; align-items:center; gap:8px;">
                    <strong style="color:#2c3e50;">Correntes:</strong>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-ia" checked> I<sub>A</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-ib" checked> I<sub>B</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-ic" checked> I<sub>C</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-in"> I<sub>N</sub></label>
                </div>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; width: 100%;">
                <div id="grafico-fasores" style="width: 550px; height: 500px; background:#fff; border:1px solid #ddd; border-radius: 4px;"></div>
                <div id="grafico-potencia" style="width: 550px; height: 500px; background:#fff; border:1px solid #ddd; border-radius: 4px;"></div>
            </div>
        `;

        // Garantia de fallback caso dados.fasores não exista ou as chaves sejam minúsculas
        const f = dados.fasores || {};

        const van = f.VAN || f.van || { mod: 0, ang: 0, real: 0, imag: 0 };
        const vbn = f.VBN || f.vbn || { mod: 0, ang: 0, real: 0, imag: 0 };
        const vcn = f.VCN || f.vcn || { mod: 0, ang: 0, real: 0, imag: 0 };

        const vab = f.VAB || f.vab || { mod: 0, ang: 0, real: 0, imag: 0 };
        const vbc = f.VBC || f.vbc || { mod: 0, ang: 0, real: 0, imag: 0 };
        const vca = f.VCA || f.vca || { mod: 0, ang: 0, real: 0, imag: 0 };

        const ia  = f.Ia  || f.ia  || f.ian || { mod: 0, ang: 0, real: 0, imag: 0 };
        const ib  = f.Ib  || f.ib  || f.ibn || { mod: 0, ang: 0, real: 0, imag: 0 };
        const ic  = f.Ic  || f.ic  || f.icn || { mod: 0, ang: 0, real: 0, imag: 0 };
        const in_ = f.In  || f.in  || f.in_n|| { mod: 0, ang: 0, real: 0, imag: 0 };

        // Reescalonamento Visual Automático das Correntes para exibição
        const maxV = Math.max(van.mod, vbn.mod, vcn.mod, vab.mod, vbc.mod, vca.mod, 1.0);
        const maxI = Math.max(ia.mod, ib.mod, ic.mod, in_.mod, 0.001);
        const fatorEscalaI = (0.5 * maxV) / maxI;
        const labelSufixoI = Math.abs(fatorEscalaI - 1.0) > 0.05 ? ` (x${fatorEscalaI.toFixed(1)})` : '';

        function renderizarTracos() {
            const vis = {
                van: document.getElementById('chk-van')?.checked ?? true,
                vbn: document.getElementById('chk-vbn')?.checked ?? true,
                vcn: document.getElementById('chk-vcn')?.checked ?? true,
                vab: document.getElementById('chk-vab')?.checked ?? false,
                vbc: document.getElementById('chk-vbc')?.checked ?? false,
                vca: document.getElementById('chk-vca')?.checked ?? false,
                ia:  document.getElementById('chk-ia')?.checked ?? true,
                ib:  document.getElementById('chk-ib')?.checked ?? true,
                ic:  document.getElementById('chk-ic')?.checked ?? true,
                in:  document.getElementById('chk-in')?.checked ?? false
            };

            function criarTracoVetor(fasor, nome, cor, sufixoUnidade, visivel, scale = 1.0, rotuloExtra = '') {
                if (!fasor || !visivel) return null;
                const rx = fasor.real * scale;
                const ry = fasor.imag * scale;
                return {
                    x: [0, rx],
                    y: [0, ry],
                    mode: 'lines+markers',
                    name: `${nome}: ${fasor.mod.toFixed(1)}${sufixoUnidade}${rotuloExtra} ∠${fasor.ang.toFixed(1)}°`,
                    line: { color: cor, width: 3 },
                    marker: { size: [0, 8], symbol: "arrow-bar-up", angleref: "previous" }
                };
            }

            const listaFasores = [
                criarTracoVetor(van, 'VAN', '#ff4d4d', 'V', vis.van),
                criarTracoVetor(vbn, 'VBN', '#2ecc71', 'V', vis.vbn),
                criarTracoVetor(vcn, 'VCN', '#3498db', 'V', vis.vcn),
                criarTracoVetor(vab, 'VAB', '#9b59b6', 'V', vis.vab),
                criarTracoVetor(vbc, 'VBC', '#f1c40f', 'V', vis.vbc),
                criarTracoVetor(vca, 'VCA', '#e67e22', 'V', vis.vca),
                criarTracoVetor(ia,  'Ia',  '#c0392b', 'A', vis.ia,  fatorEscalaI, labelSufixoI),
                criarTracoVetor(ib,  'Ib',  '#27ae60', 'A', vis.ib,  fatorEscalaI, labelSufixoI),
                criarTracoVetor(ic,  'Ic',  '#2980b9', 'A', vis.ic,  fatorEscalaI, labelSufixoI),
                criarTracoVetor(in_, 'In',  '#7f8c8d', 'A', vis.in,  fatorEscalaI, labelSufixoI)
            ].filter(t => t !== null);

            const maxVal = maxV * 1.25;

            const layoutFasores = {
                title: { text: '<b>Diagrama Fasorial de Tensões e Correntes</b>', font: { size: 16 } },
                xaxis: { range: [-maxVal, maxVal], title: 'Real (Re)', gridcolor: '#eee' },
                yaxis: { range: [-maxVal, maxVal], title: 'Imaginário (Im)', gridcolor: '#eee', scaleanchor: "x", scaleratio: 1 },
                showlegend: true,
                legend: { orientation: "h", y: -0.2 },
                margin: { l: 50, r: 50, t: 50, b: 100 }
            };

            Plotly.react('grafico-fasores', listaFasores, layoutFasores);
        }
        renderizarTracos();

        // Adiciona ouvintes de evento às checkboxes para redesenhar dinamicamente
        const idsCheckboxes = ['chk-van', 'chk-vbn', 'chk-vcn', 'chk-vab', 'chk-vbc', 'chk-vca', 'chk-ia', 'chk-ib', 'chk-ic', 'chk-in'];
        idsCheckboxes.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.addEventListener('change', renderizarTracos);
        });

        // Plota o Triângulo de Potências
        // Tratamento defensivo para evitar crash se dados.potencia vier undefined
        const pot = dados.potencia || dados.potencias || {};

        const p_ativa    = pot.P !== undefined ? pot.P : (pot.p !== undefined ? pot.p : (pot.ptotal || 0));
        const q_reativa  = pot.Q !== undefined ? pot.Q : (pot.q !== undefined ? pot.q : (pot.qtotal || 0));
        const s_aparente = pot.S_mod !== undefined ? pot.S_mod : (pot.s_mod !== undefined ? pot.s_mod : (pot.stotal || 0));

        // Plota o Triângulo de Potências
        const dadosPotencia = [
            {
                x: [0, p_ativa], y: [0, 0],
                mode: 'lines+markers',
                name: `Ativa (P): ${Number(p_ativa).toFixed(1)} W`,
                line: { color: '#27ae60', width: 4 }
            },
            {
                x: [p_ativa, p_ativa], y: [0, q_reativa],
                mode: 'lines+markers',
                name: `Reativa (Q): ${Number(q_reativa).toFixed(1)} var`,
                line: { color: '#e74c3c', width: 4 }
            },
            {
                x: [0, p_ativa], y: [0, q_reativa],
                mode: 'lines+markers',
                name: `Aparente (S): ${Number(s_aparente).toFixed(1)} VA`,
                line: { color: '#f1c40f', width: 4, dash: 'dash' }
            }
        ];

        const maxPot = Math.max(Math.abs(p_ativa), Math.abs(q_reativa), Math.abs(s_aparente), 1.0) * 1.2;

        const layoutPotencia = {
            title: { text: '<b>Triângulo de Potências Trifásico Total</b>', font: { size: 16 } },
            xaxis: { range: [p_ativa >= 0 ? -maxPot*0.1 : -maxPot, p_ativa >= 0 ? maxPot : maxPot*0.1], title: 'Potência Ativa (W)', gridcolor: '#eee' },
            yaxis: { range: [q_reativa >= 0 ? -maxPot*0.1 : -maxPot, q_reativa >= 0 ? maxPot : maxPot*0.1], title: 'Potência Reativa (var)', gridcolor: '#eee', scaleanchor: "x", scaleratio: 1 },
            showlegend: true,
            legend: { orientation: "h", y: -0.2 },
            margin: { l: 50, r: 50, t: 50, b: 100 }
        };

        Plotly.newPlot('grafico-potencia', dadosPotencia, layoutPotencia);
    })
    .catch(err => alert("Erro na requisição dos gráficos: " + err));
}

function calcularTrifasicoYDelta() {
    const dados = {
        van_mod: document.getElementById('in-van-mod-yd').value,
        van_ang: document.getElementById('in-van-ang-yd').value,
        vbn_mod: document.getElementById('in-vbn-mod-yd').value,
        vbn_ang: document.getElementById('in-vbn-ang-yd').value,
        vcn_mod: document.getElementById('in-vcn-mod-yd').value,
        vcn_ang: document.getElementById('in-vcn-ang-yd').value,

        zfa: document.getElementById('in-zfa-yd').value,
        zfb: document.getElementById('in-zfb-yd').value,
        zfc: document.getElementById('in-zfc-yd').value,

        zla: document.getElementById('in-zla-yd').value,
        zlb: document.getElementById('in-zlb-yd').value,
        zlc: document.getElementById('in-zlc-yd').value,

        zab: document.getElementById('in-zab-yd').value,
        zbc: document.getElementById('in-zbc-yd').value,
        zca: document.getElementById('in-zca-yd').value
    };

    fetch('/calcular_trifasico_ydelta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    })
    .then(r => r.json())
    .then(data => {
        if (data.erro) { alert(data.erro); return; }

        const pol = (obj) => (obj && typeof obj === 'object') ? obj.polar : (obj || '-');
        const ret = (obj) => (obj && typeof obj === 'object') ? obj.retangular : '-';

        // 1. Correntes de Linha
        document.getElementById('out-i-linha-yd').innerHTML = `
            <p><b>I<sub>a</sub>:</b><br>P: ${pol(data.ia)}<br>R: ${ret(data.ia)}</p><br>
            <p><b>I<sub>b</sub>:</b><br>P: ${pol(data.ib)}<br>R: ${ret(data.ib)}</p><br>
            <p><b>I<sub>c</sub>:</b><br>P: ${pol(data.ic)}<br>R: ${ret(data.ic)}</p>
        `;

        // 2. Correntes de Fase (Carga Δ)
        document.getElementById('out-i-fase-yd').innerHTML = `
            <p><b>I<sub>AB</sub>:</b><br>P: ${pol(data.iab)}<br>R: ${ret(data.iab)}</p><br>
            <p><b>I<sub>BC</sub>:</b><br>P: ${pol(data.ibc)}<br>R: ${ret(data.ibc)}</p><br>
            <p><b>I<sub>CA</sub>:</b><br>P: ${pol(data.ica)}<br>R: ${ret(data.ica)}</p>
        `;

        // 3. Tensões de Linha (Carga Δ)
        document.getElementById('out-v-linha-yd').innerHTML = `
            <p><b>V<sub>AB</sub>:</b><br>P: ${pol(data.vab)}<br>R: ${ret(data.vab)}</p><br>
            <p><b>V<sub>BC</sub>:</b><br>P: ${pol(data.vbc)}<br>R: ${ret(data.vbc)}</p><br>
            <p><b>V<sub>CA</sub>:</b><br>P: ${pol(data.vca)}<br>R: ${ret(data.vca)}</p>
        `;

        // 4. Tensões de Fase (Fonte Y)
        document.getElementById('out-v-fase-yd').innerHTML = `
            <p><b>V<sub>AN</sub>:</b><br>P: ${pol(data.van)}<br>R: ${ret(data.van)}</p><br>
            <p><b>V<sub>BN</sub>:</b><br>P: ${pol(data.vbn)}<br>R: ${ret(data.vbn)}</p><br>
            <p><b>V<sub>CN</sub>:</b><br>P: ${pol(data.vcn)}<br>R: ${ret(data.vcn)}</p>
        `;

        // 5. Potências
        document.getElementById('out-potencias-yd').innerHTML = `
            <p><b>Fase AB:</b><br>S: ${data.sa} VA<br>P: ${data.pa} W<br>Q: ${data.qa} VAr</p><br>
            <p><b>Fase BC:</b><br>S: ${data.sb} VA<br>P: ${data.pb} W<br>Q: ${data.qb} VAr</p><br>
            <p><b>Fase CA:</b><br>S: ${data.sc} VA<br>P: ${data.pc} W<br>Q: ${data.qc} VAr</p><br>
            <p style="border-top: 1px solid #ccc; padding-top: 4px; margin-top: 4px;"><b>Total:</b><br>S: ${data.stotal} VA<br>P: ${data.ptotal} W<br>Q: ${data.qtotal} VAr</p>
        `;
    })
    .catch(err => alert("Erro ao processar cálculo do Y-Delta: " + err));
}

// ==========================================
// === GRÁFICOS TRIFÁSICOS Y-DELTA (PLOTLY) ==
// ==========================================
function abrirGraficosYDelta() {
    const obterTexto = (id) => { const el = document.getElementById(id); return el ? el.value.trim() : "0"; };
    const obterNumero = (id) => { const el = document.getElementById(id); return el ? Number(el.value) : 0; };

    const payload = {
        van_mod: obterNumero("in-van-mod-yd"), van_ang: obterNumero("in-van-ang-yd"),
        vbn_mod: obterNumero("in-vbn-mod-yd"), vbn_ang: obterNumero("in-vbn-ang-yd"),
        vcn_mod: obterNumero("in-vcn-mod-yd"), vcn_ang: obterNumero("in-vcn-ang-yd"),
        zfa: obterTexto("in-zfa-yd"), zfb: obterTexto("in-zfb-yd"), zfc: obterTexto("in-zfc-yd"),
        zla: obterTexto("in-zla-yd"), zlb: obterTexto("in-zlb-yd"), zlc: obterTexto("in-zlc-yd"),
        zab: obterTexto("in-zab-yd"), zbc: obterTexto("in-zbc-yd"), zca: obterTexto("in-zca-yd")
    };

    fetch('/graficos_trifasico_ydelta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(dados => {
        if (!dados.sucesso) {
            alert("Erro ao calcular gráficos: " + dados.erro);
            return;
        }

        let container = document.getElementById("container-graficos-trifasico-yd");
        if (!container) {
            container = document.createElement("div");
            container.id = "container-graficos-trifasico-yd";
            container.style = "display: flex; flex-direction: column; align-items: center; gap: 15px; margin-top: 20px;";
            document.getElementById('painel-dinamico').appendChild(container);
        }

        container.innerHTML = `
            <!-- Painel Inteligente de Seleção de Visibilidade -->
            <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; background: #f8f9fa; padding: 12px; border-radius: 6px; border: 1px solid #ddd; font-family: Arial, sans-serif; font-size: 0.9rem; width: 100%; max-width: 1120px; box-sizing: border-box;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <strong style="color:#2c3e50;">Tensões Fase:</strong>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-van-yd" checked> V<sub>AN</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vbn-yd" checked> V<sub>BN</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vcn-yd" checked> V<sub>CN</sub></label>
                </div>
                <span style="border-left: 1px solid #ccc; margin: 0 5px;"></span>
                <div style="display:flex; align-items:center; gap:8px;">
                    <strong style="color:#2c3e50;">Tensões Linha:</strong>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vab-yd" checked> V<sub>AB</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vbc-yd" checked> V<sub>BC</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-vca-yd" checked> V<sub>CA</sub></label>
                </div>
                <span style="border-left: 1px solid #ccc; margin: 0 5px;"></span>
                <div style="display:flex; align-items:center; gap:8px;">
                    <strong style="color:#2c3e50;">Correntes Linha:</strong>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-ia-yd" checked> I<sub>A</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-ib-yd" checked> I<sub>B</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-ic-yd" checked> I<sub>C</sub></label>
                </div>
                <span style="border-left: 1px solid #ccc; margin: 0 5px;"></span>
                <div style="display:flex; align-items:center; gap:8px;">
                    <strong style="color:#2c3e50;">Correntes Carga ($\Delta$):</strong>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-iab-yd"> I<sub>AB</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-ibc-yd"> I<sub>BC</sub></label>
                    <label style="cursor:pointer;"><input type="checkbox" id="chk-ica-yd"> I<sub>CA</sub></label>
                </div>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; width: 100%;">
                <div id="grafico-fasores-yd" style="width: 550px; height: 500px; background:#fff; border:1px solid #ddd; border-radius: 4px;"></div>
                <div id="grafico-potencia-yd" style="width: 550px; height: 500px; background:#fff; border:1px solid #ddd; border-radius: 4px;"></div>
            </div>
        `;

        // Tratamento defensivo e mapeamento dos fasores
        const f = dados.fasores || {};

        const van = f.VAN || f.van || { mod: 0, ang: 0, real: 0, imag: 0 };
        const vbn = f.VBN || f.vbn || { mod: 0, ang: 0, real: 0, imag: 0 };
        const vcn = f.VCN || f.vcn || { mod: 0, ang: 0, real: 0, imag: 0 };

        const vab = f.VAB || f.vab || { mod: 0, ang: 0, real: 0, imag: 0 };
        const vbc = f.VBC || f.vbc || { mod: 0, ang: 0, real: 0, imag: 0 };
        const vca = f.VCA || f.vca || { mod: 0, ang: 0, real: 0, imag: 0 };

        const ia  = f.Ia  || f.ia  || { mod: 0, ang: 0, real: 0, imag: 0 };
        const ib  = f.Ib  || f.ib  || { mod: 0, ang: 0, real: 0, imag: 0 };
        const ic  = f.Ic  || f.ic  || { mod: 0, ang: 0, real: 0, imag: 0 };

        const iab = f.IAB || f.iab || { mod: 0, ang: 0, real: 0, imag: 0 };
        const ibc = f.IBC || f.ibc || { mod: 0, ang: 0, real: 0, imag: 0 };
        const ica = f.ICA || f.ica || { mod: 0, ang: 0, real: 0, imag: 0 };

        // Escalonamento Visual Automático das Correntes para exibição equilibrada no mesmo gráfico
        const maxV = Math.max(van.mod, vbn.mod, vcn.mod, vab.mod, vbc.mod, vca.mod, 1.0);
        const maxI = Math.max(ia.mod, ib.mod, ic.mod, iab.mod, ibc.mod, ica.mod, 0.001);
        const fatorEscalaI = (0.5 * maxV) / maxI;
        const labelSufixoI = Math.abs(fatorEscalaI - 1.0) > 0.05 ? ` (x${fatorEscalaI.toFixed(1)})` : '';

        function renderizarTracosYDelta() {
            const vis = {
                van: document.getElementById('chk-van-yd')?.checked ?? true,
                vbn: document.getElementById('chk-vbn-yd')?.checked ?? true,
                vcn: document.getElementById('chk-vcn-yd')?.checked ?? true,
                vab: document.getElementById('chk-vab-yd')?.checked ?? true,
                vbc: document.getElementById('chk-vbc-yd')?.checked ?? true,
                vca: document.getElementById('chk-vca-yd')?.checked ?? true,
                ia:  document.getElementById('chk-ia-yd')?.checked ?? true,
                ib:  document.getElementById('chk-ib-yd')?.checked ?? true,
                ic:  document.getElementById('chk-ic-yd')?.checked ?? true,
                iab: document.getElementById('chk-iab-yd')?.checked ?? false,
                ibc: document.getElementById('chk-ibc-yd')?.checked ?? false,
                ica: document.getElementById('chk-ica-yd')?.checked ?? false
            };

            function criarTracoVetor(fasor, nome, cor, sufixoUnidade, visivel, scale = 1.0, rotuloExtra = '') {
                if (!fasor || !visivel) return null;
                const rx = fasor.real !== undefined ? fasor.real * scale : fasor.mod * Math.cos(fasor.ang * Math.PI / 180) * scale;
                const ry = fasor.imag !== undefined ? fasor.imag * scale : fasor.mod * Math.sin(fasor.ang * Math.PI / 180) * scale;
                return {
                    x: [0, rx],
                    y: [0, ry],
                    mode: 'lines+markers',
                    name: `${nome}: ${fasor.mod.toFixed(1)}${sufixoUnidade}${rotuloExtra} ∠${fasor.ang.toFixed(1)}°`,
                    line: { color: cor, width: 3 },
                    marker: { size: [0, 8], symbol: "arrow-bar-up", angleref: "previous" }
                };
            }

            const listaFasores = [
                criarTracoVetor(van, 'VAN', '#ff4d4d', 'V', vis.van),
                criarTracoVetor(vbn, 'VBN', '#2ecc71', 'V', vis.vbn),
                criarTracoVetor(vcn, 'VCN', '#3498db', 'V', vis.vcn),
                criarTracoVetor(vab, 'VAB', '#9b59b6', 'V', vis.vab),
                criarTracoVetor(vbc, 'VBC', '#f1c40f', 'V', vis.vbc),
                criarTracoVetor(vca, 'VCA', '#e67e22', 'V', vis.vca),
                criarTracoVetor(ia,  'Ia',  '#c0392b', 'A', vis.ia,  fatorEscalaI, labelSufixoI),
                criarTracoVetor(ib,  'Ib',  '#27ae60', 'A', vis.ib,  fatorEscalaI, labelSufixoI),
                criarTracoVetor(ic,  'Ic',  '#2980b9', 'A', vis.ic,  fatorEscalaI, labelSufixoI),
                criarTracoVetor(iab, 'IAB', '#8e44ad', 'A', vis.iab, fatorEscalaI, labelSufixoI),
                criarTracoVetor(ibc, 'IBC', '#d35400', 'A', vis.ibc, fatorEscalaI, labelSufixoI),
                criarTracoVetor(ica, 'ICA', '#16a085', 'A', vis.ica, fatorEscalaI, labelSufixoI)
            ].filter(t => t !== null);

            const maxVal = maxV * 1.25;

            const layoutFasores = {
                title: { text: '<b>Diagrama Fasorial de Tensões e Correntes (Y-Δ)</b>', font: { size: 16 } },
                xaxis: { range: [-maxVal, maxVal], title: 'Real (Re)', gridcolor: '#eee' },
                yaxis: { range: [-maxVal, maxVal], title: 'Imaginário (Im)', gridcolor: '#eee', scaleanchor: "x", scaleratio: 1 },
                showlegend: true,
                legend: { orientation: "h", y: -0.2 },
                margin: { l: 50, r: 50, t: 50, b: 100 }
            };

            Plotly.react('grafico-fasores-yd', listaFasores, layoutFasores);
        }

        renderizarTracosYDelta();

        // Escutadores de eventos das checkboxes
        const idsCheckboxes = ['chk-van-yd', 'chk-vbn-yd', 'chk-vcn-yd', 'chk-vab-yd', 'chk-vbc-yd', 'chk-vca-yd', 'chk-ia-yd', 'chk-ib-yd', 'chk-ic-yd', 'chk-iab-yd', 'chk-ibc-yd', 'chk-ica-yd'];
        idsCheckboxes.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.addEventListener('change', renderizarTracosYDelta);
        });

        // Plota o Triângulo de Potências Total
        const pot = dados.potencia || dados.potencias || {};

        const p_ativa    = pot.P !== undefined ? pot.P : (pot.p !== undefined ? pot.p : (pot.ptotal || 0));
        const q_reativa  = pot.Q !== undefined ? pot.Q : (pot.q !== undefined ? pot.q : (pot.qtotal || 0));
        const s_aparente = pot.S_mod !== undefined ? pot.S_mod : (pot.s_mod !== undefined ? pot.s_mod : (pot.stotal || 0));

        const dadosPotencia = [
            {
                x: [0, p_ativa], y: [0, 0],
                mode: 'lines+markers',
                name: `Ativa (P): ${Number(p_ativa).toFixed(1)} W`,
                line: { color: '#27ae60', width: 4 }
            },
            {
                x: [p_ativa, p_ativa], y: [0, q_reativa],
                mode: 'lines+markers',
                name: `Reativa (Q): ${Number(q_reativa).toFixed(1)} var`,
                line: { color: '#e74c3c', width: 4 }
            },
            {
                x: [0, p_ativa], y: [0, q_reativa],
                mode: 'lines+markers',
                name: `Aparente (S): ${Number(s_aparente).toFixed(1)} VA`,
                line: { color: '#f1c40f', width: 4, dash: 'dash' }
            }
        ];

        const maxPot = Math.max(Math.abs(p_ativa), Math.abs(q_reativa), Math.abs(s_aparente), 1.0) * 1.2;

        const layoutPotencia = {
            title: { text: '<b>Triângulo de Potências Trifásico Total</b>', font: { size: 16 } },
            xaxis: { range: [p_ativa >= 0 ? -maxPot*0.1 : -maxPot, p_ativa >= 0 ? maxPot : maxPot*0.1], title: 'Potência Ativa (W)', gridcolor: '#eee' },
            yaxis: { range: [q_reativa >= 0 ? -maxPot*0.1 : -maxPot, q_reativa >= 0 ? maxPot : maxPot*0.1], title: 'Potência Reativa (var)', gridcolor: '#eee', scaleanchor: "x", scaleratio: 1 },
            showlegend: true,
            legend: { orientation: "h", y: -0.2 },
            margin: { l: 50, r: 50, t: 50, b: 100 }
        };

        Plotly.newPlot('grafico-potencia-yd', dadosPotencia, layoutPotencia);
    })
    .catch(err => alert("Erro na requisição dos gráficos Y-Delta: " + err));
}

// ==========================================
// === JANELA MODAL E INICIALIZAÇÃO =========
// ==========================================
function fecharModal() {
    const modal = document.getElementById('modal-graficos');
    if (modal) modal.style.display = "none";
    const containerCheckboxes = document.getElementById('container-chk-graficos');
    if (containerCheckboxes) containerCheckboxes.innerHTML = "";
}

window.onload = function() {
    carregarConteudo('inicio');
};

window.onclick = function(event) {
    const modal = document.getElementById('modal-graficos');
    if (event.target == modal) fecharModal();
};