const PALAVRAS_SAIDA = ['sair', 'exit', 'quit', 'gassho', 'obrigado', 'ok'];

// Mapa de @ para nome exato do autor no JSON
const AUTORES_MAP = {
    'dogen':   'Eihei Dogen',
    'osho':    'Osho',
    'haemin':  'Haemin Sunim',
    'sunim':   'Haemin Sunim',
    'masuno':  'Shunmyo Masuno',
    'suzuki':  'Shunryu Suzuki',
    'thich':   'Thich Nhat Hanh',
    'hanh':    'Thich Nhat Hanh',
};

const input = document.getElementById('pergunta');
const respostaDiv = document.getElementById('resposta');

function randomMsg(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

// Extrai autor e pergunta limpa quando usuário usa @
function parsearPergunta(texto) {
    const match = texto.match(/^@(\w+)\s+(.*)/);
    if (match) {
        const chave = match[1].toLowerCase();
        const autor = AUTORES_MAP[chave] || null;
        const pergunta = match[2].trim();
        return { pergunta, autor };
    }
    return { pergunta: texto, autor: null };
}

window.addEventListener('DOMContentLoaded', () => {
    respostaDiv.innerHTML = `<em>O silêncio precede a resposta...</em>`;
});

async function fazerPergunta() {
    const textoRaw = input.value.trim();
    if (!textoRaw) return;

    if (PALAVRAS_SAIDA.includes(textoRaw.toLowerCase())) {
        respostaDiv.innerHTML = ` ${randomMsg(window.DESPEDIDA_JS)}`;
        input.value = '';
        input.disabled = true;
        return;
    }

    const { pergunta, autor } = parsearPergunta(textoRaw);

    input.disabled = true;
    input.placeholder = autor
        ? `Consultando ${autor}...`
        : "Chizu medita...";
    respostaDiv.innerHTML = `<em>${randomMsg(window.AGUARDANDO_JS)}</em>`;

    try {
        // Monta payload — inclui autor só se foi informado via @
        const payload = { pergunta };
        if (autor) payload.autor = autor;

        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const resposta = data.resposta;

        const respostaHTML = resposta
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^\* (.+)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/\. ([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÀÇ])/g, '.</p><p>$1');

        respostaDiv.innerHTML = `
            <p>${respostaHTML}</p>
            <div class="share-buttons">
                <button id="btn-whatsapp">WhatsApp</button>
                <button id="btn-email">Email</button>
            </div>
        `;

        document.getElementById('btn-whatsapp').addEventListener('click', () => compartilharWhatsApp(resposta));
        document.getElementById('btn-email').addEventListener('click', () => compartilharEmail(resposta));

    } catch (error) {
        respostaDiv.innerHTML = '<em>(o vento levou sua pergunta...)</em>';
    } finally {
        input.disabled = false;
        input.value = '';
        input.placeholder = "Fale com Chizu...";
        input.focus();
    }
}

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