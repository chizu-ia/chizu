from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from zen import responder  # sua função que envia o payload para o modelo

router = APIRouter()

# ============================================
# Histórico em memória (persistente enquanto o servidor roda)
# ============================================
MESSAGES = []

def get_last_messages(n: int):
    """Retorna as últimas n mensagens do histórico"""
    return MESSAGES[-n:]

def add_to_history(user_msg: str, assistant_msg: str):
    """Adiciona interação ao histórico"""
    MESSAGES.append({"role": "user", "content": user_msg})
    MESSAGES.append({"role": "assistant", "content": assistant_msg})

# ============================================
# Página HTML do formulário de tuning
# ============================================
def render_form_html(resposta: str = "", historico_html: str = ""):
    return f"""
    <html>
    <head>
        <title>ZenBot – Página de Testes</title>
    </head>
    <body>
        <h2>ZenBot – Página de Testes</h2>
        <form method="post">
            Style: <input name="style" type="text" value="zen"><br>
            Temperature: <input name="temperature" type="number" step="0.05" value="0.5"><br>
            Max Tokens: <input name="max_tokens" type="number" value="300"><br>
            Top P: <input name="top_p" type="number" step="0.05" value="1.0"><br>
            Frequency Penalty: <input name="frequency_penalty" type="number" step="0.1" value="0"><br>
            Presence Penalty: <input name="presence_penalty" type="number" step="0.1" value="0"><br>
            Mensagens para lembrar: <input name="context_count" type="number" value="5"><br>
            Pergunta: <input name="question" type="text"><br>
            <button type="submit">Enviar</button>
        </form>

        <h3>Última Resposta:</h3>
        <pre>{resposta}</pre>

        {historico_html}
    </body>
    </html>
    """

# ============================================
# GET: exibe formulário
# ============================================
@router.get("/")
async def tuning_page():
    # monta histórico em HTML
    historico_html = "<h3>Histórico:</h3><ul>"
    for msg in MESSAGES[-10:]:  # mostra últimas 10 interações
        historico_html += f"<li><b>{msg['role']}:</b> {msg['content']}</li>"
    historico_html += "</ul>"
    return HTMLResponse(render_form_html(historico_html=historico_html))

# ============================================
# POST: processa formulário e responde
# ============================================
@router.post("/")
async def tuning_submit(
    style: str = Form(...),
    temperature: float = Form(...),
    max_tokens: int = Form(...),
    top_p: float = Form(...),
    frequency_penalty: float = Form(...),
    presence_penalty: float = Form(...),
    context_count: int = Form(...),
    question: str = Form(...)
):
    # monta payload dinâmico
    payload = {
        "model": "gpt-5-mini",
        "messages": get_last_messages(context_count) + [
            {"role": "user", "content": f"Style:{style} Pergunta:{question}"}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
    }

    # chama o modelo
    resposta = responder(payload)

    # adiciona ao histórico
    add_to_history(question, resposta)

    # monta histórico em HTML
    historico_html = "<h3>Histórico:</h3><ul>"
    for msg in MESSAGES[-10:]:
        historico_html += f"<li><b>{msg['role']}:</b> {msg['content']}</li>"
    historico_html += "</ul>"

    return HTMLResponse(render_form_html(resposta=resposta, historico_html=historico_html))