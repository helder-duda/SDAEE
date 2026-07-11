function carregarConteudo(modulo) {
    const painel = document.getElementById('painel-dinamico');

    if (modulo === 'circuito-rl') {
        painel.innerHTML = `
            <h2>Análise de Circuitos RL</h2>

            <div class="grid-4-partes">
                <!-- QUADRANTE 1: Imagem (Série) -->
                <div class="quadrante">
                    <h3>Circuito RL - Série</h3>
                    <div class="container-imagem">
                        <img src="/static/imagens/rl_serie.jpg" alt="Esquema Circuito RL Série" class="imagem-circuito">
                    </div>
                </div>

                <!-- QUADRANTE 2: Imagem (Paralelo) -->
                <div class="quadrante">
                    <h3>Circuito RL - Paralelo</h3>
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
    }
}

// === CÁLCULOS DO CIRCUITO SÉRIE ===
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

// === CÁLCULOS DO CIRCUITO PARALELO ===
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

// === GRÁFICOS SÉRIE ===
function abrirGraficosSerie() {
    const v = document.getElementById('v-serie').value;
    const r = document.getElementById('r-serie').value;
    const l = document.getElementById('l-serie').value;
    const f = document.getElementById('f-serie').value;

    if (!v || !r || !l || !f) {
        alert("Calcule os parâmetros primeiro (Preencha V, R, L e f).");
        return;
    }

    const modal = document.getElementById('modal-graficos');
    const imgGrafico = document.getElementById('img-grafico');
    const msgCarregando = document.getElementById('msg-carregando');

    modal.style.display = "block";
    imgGrafico.style.display = "none";
    msgCarregando.style.display = "block";

    fetch('/graficos_serie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v: v, r: r, l: l, f: f })
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

function abrirGraficosParalelo() {
    const v = document.getElementById('v-paralelo').value;
    const r = document.getElementById('r-paralelo').value;
    const l = document.getElementById('l-paralelo').value;
    const f = document.getElementById('f-paralelo').value;

    if (!v || !r || !l || !f) {
        alert("Calcule os parâmetros primeiro (Preencha V, R, L e f do Paralelo).");
        return;
    }

    const modal = document.getElementById('modal-graficos');
    const imgGrafico = document.getElementById('img-grafico');
    const msgCarregando = document.getElementById('msg-carregando');

    modal.style.display = "block";
    imgGrafico.style.display = "none";
    msgCarregando.style.display = "block";

    fetch('/graficos_paralelo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ v: v, r: r, l: l, f: f })
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

// === CONTROLES DA JANELA MODAL ===
function fecharModal() {
    document.getElementById('modal-graficos').style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById('modal-graficos');
    if (event.target == modal) {
        fecharModal();
    }
}