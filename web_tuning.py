from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from zen import responder
import os

router = APIRouter()

# Histórico em memória
MESSAGES = []

def get_last_messages(n: int):
    return MESSAGES[-n:]

def add_to_history(user_msg: str, assistant_msg: str):
    MESSAGES.append({"role": "user", "content": user_msg})
    MESSAGES.append({"role": "assistant", "content": assistant_msg})

# ============================================
# Página HTML do formulário de tuning
# ============================================

def render_form_html(resposta: str = "", historico_html: str = ""):
    return f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>ZenBot – Página de Testes</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f2f2f2; padding: 20px; }}
            .container {{ background: #fff; padding: 20px; border-radius: 10px; max-width: 700px; margin: auto; }}
            h2 {{ text-align: center; }}
            label {{ display: block; margin-top: 10px; font-weight: bold; }}
            input, select {{ width: 100%; padding: 5px; margin-top: 5px; }}
            button {{ margin-top: 15px; padding: 10px 20px; font-size: 16px; }}
            pre {{ background: #eee; padding: 10px; border-radius: 5px; }}
            .historico {{ margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>ZenBot – Página de Testes</h2>
            <form method="post">
                <label>Style:</label>
                <select name="style">
                    <option value="aforismo_zen.txt">Aforismos</option>
                    <option value="koans_classicos.txt">Koans</option>
                    <option value="meditacoes_guiadas.txt">Meditação</option>
                    <option value="system_prompt.txt">Prompt</option>
                </select>

                <label>Temperature:</label>
                <input type="number" step="0.05" name="temperature" value="0.5">

                <label>Max Tokens:</label>
                <input type="number" name="max_tokens" value="300">

                <label>Top P:</label>
                <input type="number" step="0.05" name="top_p" value="1.0">

                <label>Frequency Penalty:</label>
                <input type="number" step="0.1" name="frequency_penalty" value="0">

                <label>Presence Penalty:</label>
                <input type="number" step="0.1" name="presence_penalty" value="0">

                <label>Mensagens para lembrar:</label>
                <input type="number" name="context_count" value="5">

                <label>Pergunta:</label>
                <input type="text" name="question">

                <button type="submit">Enviar</button>
            </form>

            <h3>Última Resposta:</h3>
            <pre>{resposta}</pre>

            <div class="historico">
                <h3>Histórico:</h3>
                {historico_html}
            </div>
        </div>
    </body>
    </html>
    """

# ============================================
# GET: exibe formulário
# ============================================
@router.get("/")
async def tuning_page():
    historico_html = "".join([f"<pre><b>{msg['role']}:</b> {msg['content']}</pre>" for msg in MESSAGES[-10:]])
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
    try:
        # Lê o arquivo correspondente ao style
        style_content = ""
        style_path = os.path.join("src/styles", style)
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                style_content = f.read()
        else:
            style_content = f"Estilo selecionado: {style}"

        # Cria a pergunta final como string para o responder
        pergunta_final = f"{style_content}\nPergunta: {question}"

        # Pega histórico das últimas n mensagens como string concatenada
        historico_texto = "\n".join([m["content"] for m in get_last_messages(context_count)])

        # Chama o responder passando a string
        resposta = responder(pergunta_final, historico_texto)

        add_to_history(question, resposta)
    except Exception as e:
        resposta = f"O mestre medita. (Erro interno: {str(e)})"

    historico_html = "".join([f"<pre><b>{msg['role']}:</b> {msg['content']}</pre>" for msg in MESSAGES[-10:]])
    return HTMLResponse(render_form_html(resposta=resposta, historico_html=historico_html))