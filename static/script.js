const PALAVRAS_SAIDA = ['sair', 'exit', 'quit', 'gassho', 'obrigado', 'ok'];

const input = document.getElementById('pergunta');
const respostaDiv = document.getElementById('resposta');

function randomMsg(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

window.addEventListener('DOMContentLoaded', () => {
    respostaDiv.innerHTML = `<em>O silêncio precede a resposta...</em>`;
});

async function fazerPergunta() {
    const pergunta = input.value.trim();
    if (!pergunta) return;

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