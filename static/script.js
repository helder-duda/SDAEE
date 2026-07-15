// ==========================================
// === CONTROLE DO MENU LATERAL =============
// ==========================================
function toggleMenu(idMenu) {
    const menu = document.getElementById(idMenu);
    // O toggle liga a classe se estiver desligada, e desliga se estiver ligada
    menu.classList.toggle('ativo');
}

function carregarConteudo(modulo) {
    const painel = document.getElementById('painel-dinamico');

    // NOVO: Condição para a página inicial
    if (modulo === 'inicio') {
        painel.innerHTML = `
            <div class="container-inicio">
                <!-- Lembre-se de colocar uma imagem chamada capa.jpg na sua pasta static/imagens -->
                <img src="/static/imagens/capa.jpeg" alt="Página Inicial" class="imagem-inicio">
            </div>
        `;
    }
    // NOVO: Módulo do Gerador Customizado de Exercícios (com inputs de quantidade e tipo)
    else if (modulo === 'exercicios') {
        painel.innerHTML = `
            <div class="quadrante" style="max-width: 500px; margin: 40px auto; padding: 30px; border: 1px solid #ddd; border-radius: 8px; background: #fff; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <h3 style="text-align: center; margin-bottom: 25px; color: #2c3e50; font-family: Arial, sans-serif;">Gerador de Exercícios Customizado</h3>

                <div style="display: flex; flex-direction: column; gap: 20px; margin-bottom: 30px; font-family: Arial, sans-serif;">
                    <!-- Campo para digitar o número de questões -->
                    <div class="input-item" style="display: flex; flex-direction: column; gap: 8px;">
                        <label style="font-weight: bold; color: #34495e;">Número de Questões (1 a 30):</label>
                        <input type="number" id="num-questoes" value="10" min="1" max="30" style="padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; width: 100%; box-sizing: border-box;">
                    </div>

                    <!-- Campo para selecionar o tipo de circuito -->
                    <div class="input-item" style="display: flex; flex-direction: column; gap: 8px;">
                        <label style="font-weight: bold; color: #34495e;">Tipo de Circuito:</label>
                        <select id="tipo-circuito" style="padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; background-color: white; width: 100%; box-sizing: border-box;">
                            <option value="todos">Todos (Mesclado)</option>
                            <option value="RL">Apenas RL</option>
                            <option value="RC">Apenas RC</option>
                            <option value="RLC">Apenas RLC</option>
                        </select>
                    </div>
                </div>

                <!-- Botão que envia a requisição e abre a nova aba -->
                <div style="text-align: center;">
                    <button class="btn-calc" onclick="enviarGerarExercicios()" style="background-color: #2980b9; color: white; border: none; padding: 12px 30px; font-size: 16px; font-weight: bold; border-radius: 4px; cursor: pointer; transition: background 0.2s;">
                        Gerar Lista de Exercícios
                    </button>
                </div>
            </div>
        `;
    } else if (modulo === 'circuito-rl') {
        painel.innerHTML = `
            <h2>Análise de Circuitos RL</h2>

            <div class="grid-4-partes">
                <!-- QUADRANTE 1: Imagem (Série) -->
                <div class="quadrante">
                    <h3>RL - Série</h3>
                    <div class="container-imagem">
                        <img src="/static/imagens/rl_serie.jpg" alt="Esquema Circuito RL Série" class="imagem-circuito">
                    </div>
                </div>

                <!-- QUADRANTE 2: Imagem (Paralelo) -->
                <div class="quadrante">
                    <h3>RL - Paralelo</h3>
                    <div class="container-imagem">
                        <img src="/static/imagens/rl_paralelo.jpg" alt="Esquema Circuito RL Paralelo" class="imagem-circuito">
                    </div>
                </div>

                <!-- QUADRANTE 3: Controles Série -->
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

                <!-- QUADRANTE 4: Controles Paralelo -->
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
                <!-- QUADRANTE 1: Imagem (Série) -->
                <div class="quadrante">
                    <h3>RC - Série</h3>
                    <div class="container-imagem">
                        <img src="/static/imagens/rc_serie.jpg" alt="Esquema Circuito RC Série" class="imagem-circuito">
                    </div>
                </div>

                <!-- QUADRANTE 2: Imagem (Paralelo) -->
                <div class="quadrante">
                    <h3>RC - Paralelo</h3>
                    <div class="container-imagem">
                        <img src="/static/imagens/rc_paralelo.jpg" alt="Esquema Circuito RC Paralelo" class="imagem-circuito">
                    </div>
                </div>

                <!-- QUADRANTE 3: Controles Série RC -->
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

                <!-- QUADRANTE 4: Controles Paralelo RC -->
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
                <!-- QUADRANTE 1: Imagem (Série) -->
                <div class="quadrante">
                    <h3>RLC - Série</h3>
                    <div class="container-imagem">
                        <img src="/static/imagens/rlc_serie.jpg" alt="Esquema Circuito RLC Série" class="imagem-circuito">
                    </div>
                </div>

                <!-- QUADRANTE 2: Imagem (Paralelo) -->
                <div class="quadrante">
                    <h3>RLC - Paralelo</h3>
                    <div class="container-imagem">
                        <img src="/static/imagens/rlc_paralelo.jpg" alt="Esquema Circuito RLC Paralelo" class="imagem-circuito">
                    </div>
                </div>

                <!-- QUADRANTE 3: Controles Série RLC -->
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

                <!-- QUADRANTE 4: Controles Paralelo RLC -->
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
}

// ==========================================
// === AUXILIAR DE GERAÇÃO EXERCÍCIOS =======
// ==========================================
function enviarGerarExercicios() {
    const qtd = document.getElementById('num-questoes').value;
    const tipo = document.getElementById('tipo-circuito').value;

    if (!qtd || qtd <= 0) {
        alert("Por favor, digite uma quantidade de questões válida.");
        return;
    }

    // Abre a folha em uma NOVA ABA passando as variáveis digitadas/escolhidas por parâmetro
    window.open(`/gerar_exercicios?qtd=${qtd}&tipo=${tipo}`, '_blank');
}

// ==========================================
// === CÁLCULOS DO CIRCUITO RL =============
// ==========================================
function calcularSerie() {
    const v = document.getElementById('v-serie').value;
    const r = document.getElementById('r-serie').value;
    const l = document.getElementById('l-serie').value;
    const f = document.getElementById('f-serie').value;

    if (!v || !r || !l || !f) {
        alert("Preencha todos os parâmetros (V, R, L e f) da Série.");
        return;
    }

    fetch('/calcular_serie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v: v, r: r, l: l, f: f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-xl-serie').innerText = data.xl;
            document.getElementById('res-i-serie').innerText = data.i;
            document.getElementById('res-vr-serie').innerText = data.vr;
            document.getElementById('res-vl-serie').innerText = data.vl;
        } else {
            alert("Erro: " + data.erro);
        }
    })
    .catch(error => console.error('Erro:', error));
}

function calcularParalelo() {
    const v = document.getElementById('v-paralelo').value;
    const r = document.getElementById('r-paralelo').value;
    const l = document.getElementById('l-paralelo').value;
    const f = document.getElementById('f-paralelo').value;

    if (!v || !r || !l || !f) {
        alert("Preencha todos os parâmetros (V, R, L e f) do Paralelo.");
        return;
    }

    fetch('/calcular_paralelo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v: v, r: r, l: l, f: f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-xl-paralelo').innerText = data.xl;
            document.getElementById('res-it-paralelo').innerText = data.it;
            document.getElementById('res-ir-paralelo').innerText = data.ir;
            document.getElementById('res-il-paralelo').innerText = data.il;
        } else {
            alert("Erro: " + data.erro);
        }
    })
    .catch(error => console.error('Erro:', error));
}

// ==========================================
// === CÁLCULOS DO CIRCUITO RC =============
// ==========================================
function calcularSerieRC() {
    const v = document.getElementById('v-rc-serie').value;
    const r = document.getElementById('r-rc-serie').value;
    const c = document.getElementById('c-rc-serie').value;
    const f = document.getElementById('f-rc-serie').value;

    if (!v || !r || !c || !f) {
        alert("Preencha todos os parâmetros (V, R, C e f) da Série RC.");
        return;
    }

    fetch('/calcular_rc_serie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v: v, r: r, c: c, f: f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-xc-serie').innerText = data.xc;
            document.getElementById('res-i-rc-serie').innerText = data.i;
            document.getElementById('res-vr-rc-serie').innerText = data.vr;
            document.getElementById('res-vc-serie').innerText = data.vc;
        } else {
            alert("Erro: " + data.erro);
        }
    })
    .catch(error => console.error('Erro:', error));
}

function calcularParaleloRC() {
    const v = document.getElementById('v-rc-paralelo').value;
    const r = document.getElementById('r-rc-paralelo').value;
    const c = document.getElementById('c-rc-paralelo').value;
    const f = document.getElementById('f-rc-paralelo').value;

    if (!v || !r || !c || !f) {
        alert("Preencha todos os parâmetros (V, R, C e f) do Paralelo RC.");
        return;
    }

    fetch('/calcular_rc_paralelo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v: v, r: r, c: c, f: f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-xc-paralelo').innerText = data.xc;
            document.getElementById('res-it-rc-paralelo').innerText = data.it;
            document.getElementById('res-ir-rc-paralelo').innerText = data.ir;
            document.getElementById('res-ic-paralelo').innerText = data.ic;
        } else {
            alert("Erro: " + data.erro);
        }
    })
    .catch(error => console.error('Erro:', error));
}

// ==========================================
// === GRÁFICOS (GERAL E JANELAS MODAIS) ====
// ==========================================
function exibirGraficoGenerico(rota_url, dados_json) {
    const modal = document.getElementById('modal-graficos');
    const imgGrafico = document.getElementById('img-grafico');
    const msgCarregando = document.getElementById('msg-carregando');

    modal.style.display = "block";
    imgGrafico.style.display = "none";
    msgCarregando.style.display = "block";

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
    .catch(error => {
        msgCarregando.style.display = "none";
        alert("Erro de comunicação com o servidor.");
        fecharModal();
    });
}

// Gráficos RL
function abrirGraficosSerie() {
    const v = document.getElementById('v-serie').value;
    const r = document.getElementById('r-serie').value;
    const l = document.getElementById('l-serie').value;
    const f = document.getElementById('f-serie').value;
    if (!v || !r || !l || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_serie', { v: v, r: r, l: l, f: f });
}

// Gráficos RC
function abrirGraficosSerieRC() {
    const v = document.getElementById('v-rc-serie').value;
    const r = document.getElementById('r-rc-serie').value;
    const c = document.getElementById('c-rc-serie').value;
    const f = document.getElementById('f-rc-serie').value;
    if (!v || !r || !c || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_rc_serie', { v: v, r: r, c: c, f: f });
}

function abrirGraficosParaleloRC() {
    const v = document.getElementById('v-rc-paralelo').value;
    const r = document.getElementById('r-rc-paralelo').value;
    const c = document.getElementById('c-rc-paralelo').value;
    const f = document.getElementById('f-rc-paralelo').value;
    if (!v || !r || !c || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_rc_paralelo', { v: v, r: r, c: c, f: f });
}

// ==========================================
// === CÁLCULOS DO CIRCUITO RLC =============
// ==========================================
function calcularSerieRLC() {
    const v = document.getElementById('v-rlc-serie').value;
    const r = document.getElementById('r-rlc-serie').value;
    const l = document.getElementById('l-rlc-serie').value;
    const c = document.getElementById('c-rlc-serie').value;
    const f = document.getElementById('f-rlc-serie').value;

    if (!v || !r || !l || !c || !f) {
        alert("Preencha todos os 5 parâmetros da Série RLC.");
        return;
    }

    fetch('/calcular_rlc_serie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v: v, r: r, l: l, c: c, f: f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-z-serie').innerText = data.z;
            document.getElementById('res-i-rlc-serie').innerText = data.i;
            document.getElementById('res-xl-rlc-serie').innerText = data.xl;
            document.getElementById('res-xc-rlc-serie').innerText = data.xc;
        } else {
            alert("Erro: " + data.erro);
        }
    })
    .catch(error => console.error('Erro:', error));
}

function calcularParaleloRLC() {
    const v = document.getElementById('v-rlc-paralelo').value;
    const r = document.getElementById('r-rlc-paralelo').value;
    const l = document.getElementById('l-rlc-paralelo').value;
    const c = document.getElementById('c-rlc-paralelo').value;
    const f = document.getElementById('f-rlc-paralelo').value;

    if (!v || !r || !l || !c || !f) {
        alert("Preencha todos os 5 parâmetros do Paralelo RLC.");
        return;
    }

    fetch('/calcular_rlc_paralelo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v: v, r: r, l: l, c: c, f: f })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('res-z-paralelo').innerText = data.z;
            document.getElementById('res-it-rlc-paralelo').innerText = data.it;
            document.getElementById('res-il-rlc-paralelo').innerText = data.il;
            document.getElementById('res-ic-rlc-paralelo').innerText = data.ic;
        } else {
            alert("Erro: " + data.erro);
        }
    })
    .catch(error => console.error('Erro:', error));
}

// ==========================================
// === GRÁFICOS RLC =========================
// ==========================================
function abrirGraficosSerieRLC() {
    const v = document.getElementById('v-rlc-serie').value;
    const r = document.getElementById('r-rlc-serie').value;
    const l = document.getElementById('l-rlc-serie').value;
    const c = document.getElementById('c-rlc-serie').value;
    const f = document.getElementById('f-rlc-serie').value;
    if (!v || !r || !l || !c || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_rlc_serie', { v: v, r: r, l: l, c: c, f: f });
}

function abrirGraficosParaleloRLC() {
    const v = document.getElementById('v-rlc-paralelo').value;
    const r = document.getElementById('r-rlc-paralelo').value;
    const l = document.getElementById('l-rlc-paralelo').value;
    const c = document.getElementById('c-rlc-paralelo').value;
    const f = document.getElementById('f-rlc-paralelo').value;
    if (!v || !r || !l || !c || !f) { alert("Calcule os parâmetros primeiro."); return; }
    exibirGraficoGenerico('/graficos_rlc_paralelo', { v: v, r: r, l: l, c: c, f: f });
}
// ==========================================
// === CONTROLES DA JANELA MODAL ============
// ==========================================
function fecharModal() {
    document.getElementById('modal-graficos').style.display = "none";
}

// ==========================================
// === INICIALIZAÇÃO DA PÁGINA ==============
// ==========================================
window.onload = function() {
    carregarConteudo('inicio');
};

window.onclick = function(event) {
    const modal = document.getElementById('modal-graficos');
    if (event.target == modal) {
        fecharModal();
    }
}