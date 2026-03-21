const PALAVRAS_SAIDA = ['sair', 'exit', 'quit', 'gassho', 'obrigado', 'ok'];

const input = document.getElementById('pergunta');
const respostaDiv = document.getElementById('resposta');

function randomMsg(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

// Mensagem inicial ao carregar a página
window.addEventListener('DOMContentLoaded', () => {
    respostaDiv.innerHTML = `<em>O silêncio precede a resposta...</em>`;
});

async function fazerPergunta() {
    const pergunta = input.value.trim();
    if (!pergunta) return;

    // Lógica de encerramento
    if (PALAVRAS_SAIDA.includes(pergunta.toLowerCase())) {
        respostaDiv.innerHTML = ` ${randomMsg(window.DESPEDIDA_JS)}`;
        input.value = '';
        input.disabled = true;
        return;
    }

    input.disabled = true;
    input.placeholder = "Chizu medita...";
    respostaDiv.innerHTML = `<em>${randomMsg(window.AGUARDANDO_JS)}</em>`;

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pergunta })
        });
        const data = await response.json();


        const resposta = data.resposta;
        const respostaEscapada = resposta.replace(/'/g, "\\'").replace(/\n/g, "\\n");
        respostaDiv.innerHTML = `
            <p>${resposta}</p>
            <div class="share-buttons">
                <button onclick="compartilharWhatsApp('${respostaEscapada}')">WhatsApp</button>
                <button onclick="compartilharEmail('${respostaEscapada}')">Email</button>
            </div>
        `;


    } catch (error) {
        respostaDiv.innerHTML = '<em>(o vento levou sua pergunta...)</em>';
    } finally {
        input.disabled = false;
        input.value = '';
        input.placeholder = "Fale com Chizu...";
        input.focus();
    }
}

// Escuta a tecla Enter
input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') fazerPergunta();
});

function compartilharWhatsApp(texto) {
    const msg = encodeURIComponent("Mestre Chizu:\n\n" + texto + "\n\nhttp://chizu.ia.br");
    window.open(`https://wa.me/?text=${msg}`, '_blank');
}

function compartilharEmail(texto) {
    const assunto = encodeURIComponent("Um ensinamento do Mestre Chizu");
    const corpo = encodeURIComponent("Mestre Chizu:\n\n" + texto + "\n\nhttp://chizu.ia.br");
    window.open(`mailto:?subject=${assunto}&body=${corpo}`, '_blank');
}