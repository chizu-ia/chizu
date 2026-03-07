from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from zen import responder
import os

router = APIRouter()

MESSAGES = []

def get_last_messages(n: int):
    return MESSAGES[-n:]

def add_to_history(user_msg: str, assistant_msg: str):
    MESSAGES.append({"role": "user", "content": user_msg})
    MESSAGES.append({"role": "assistant", "content": assistant_msg})

def render_form_html(resposta: str = "", historico_html: str = ""):
    # Usei aspas triplas para evitar conflitos com as aspas do CSS/HTML
    return f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>ZenBot – Oficina de Tuning</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #f0f2f5; padding: 20px; }}
            .container {{ background: #fff; padding: 30px; border-radius: 15px; max-width: 850px; margin: auto; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
            h2 {{ text-align: center; color: #1a5928; }}
            label {{ display: block; margin-top: 15px; font-weight: bold; }}
            input, select {{ width: 100%; padding: 12px; margin-top: 8px; border-radius: 8px; border: 1px solid #ccc; }}
            button {{ margin-top: 25px; padding: 15px; background: #27ae60; color: white; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; }}
            pre {{ background: #fdfdfd; padding: 20px; border-left: 6px solid #27ae60; border-radius: 8px; white-space: pre-wrap; }}
            .historico {{ margin-top: 40px; border-top: 2px solid #eee; }}
            .msg-box {{ margin-bottom: 15px; padding: 15px; border-radius: 10px; }}
            .user {{ background: #e3f2fd; text-align: right; }}
            .assistant {{ background: #f1f8e9; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>ZenBot – Oficina de Tuning</h2>
            <form method="post">
                <label>Estilo:</label>
                <select name="style">
                    <option value="system_prompt.txt">Base</option>
                    <option value="koans_classicos.txt">Koans</option>
                    <option value="aforismos_zen.txt">Aforismos</option>
                </select>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <label>Temp:</label><input type="number" step="0.05" name="temperature" value="0.4">
                        <label>Top P:</label><input type="number" step="0.05" name="top_p" value="0.9">
                        <label>Context:</label><input type="number" name="context_count" value="4">
                    </div>
                    <div>
                        <label>Max Tokens:</label><input type="number" name="max_tokens" value="180">
                        <label>Freq Penalty:</label><input type="number" step="0.1" name="frequency_penalty" value="0.0">
                        <label>Pres Penalty:</label><input type="number" step="0.1" name="presence_penalty" value="0.0">
                    </div>
                </div>
                <label>Pergunta:</label>
                <input type="text" name="question" required>
                <button type="submit">Calibrar e Perguntar</button>
            </form>
            <h3>Resposta:</h3>
            <pre>{resposta if resposta else "Aguardando..."}</pre>
            <div class="historico"><h3>Diálogo Recente:</h3>{historico_html}</div>
        </div>
    </body>
    </html>
    """

@router.get("/", response_class=HTMLResponse)
async def tuning_page():
    # Renderização segura do histórico
    hist_html = ""
    for msg in MESSAGES[-10:]:
        role_class = "user" if msg["role"] == "user" else "assistant"
        hist_html += f"<div class='msg-box {role_class}'><b>{msg['role']}:</b> {msg['content']}</div>"
    return HTMLResponse(render_form_html(historico_html=hist_html))

@router.post("/")
async def tuning_submit(
    style: str = Form(...), temperature: float = Form(...), top_p: float = Form(...),
    max_tokens: int = Form(...), frequency_penalty: float = Form(...),
    presence_penalty: float = Form(...), context_count: int = Form(...), question: str = Form(...)
):
    try:
        # Busca estilo
        style_path = os.path.join("styles", style)
        style_content = "Aja como o Mestre Chizu."
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                style_content = f.read()

        hist_sel = get_last_messages(context_count)
        pergunta_com_estilo = f"Estilo: {style_content}\n\nPergunta: {question}"

        # Chamada ao zen.py
        resposta = responder(
            pergunta_com_estilo, historico=hist_sel, temperature=temperature,
            max_tokens=max_tokens, top_p=top_p, frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        
        # Limpeza simples
        if isinstance(resposta, tuple): resposta = resposta[0]
        resposta_final = str(resposta).replace("\\n", "\n")
        
        add_to_history(question, resposta_final)
        res_display = resposta_final

    except Exception as e:
        res_display = f"Erro: {str(e)}"

    # Reconstroi o histórico para exibir
    hist_html = ""
    for msg in MESSAGES[-10:]:
        role_class = "user" if msg["role"] == "user" else "assistant"
        hist_html += f"<div class='msg-box {role_class}'><b>{msg['role']}:</b> {msg['content']}</div>"
    
    return HTMLResponse(render_form_html(resposta=res_display, historico_html=hist_html))