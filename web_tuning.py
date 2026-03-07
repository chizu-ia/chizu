from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from zen import responder
import os

router = APIRouter()

# ============================================
# Histórico em memória
# ============================================
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
        <title>ZenBot – Oficina de Tuning</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #e8ecef; padding: 20px; line-height: 1.6; }}
            .container {{ background: #fff; padding: 30px; border-radius: 12px; max-width: 800px; margin: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h2 {{ text-align: center; color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            label {{ display: block; margin-top: 15px; font-weight: bold; color: #34495e; }}
            input, select {{ width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
            button {{ margin-top: 20px; padding: 12px 25px; font-size: 16px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold; }}
            button:hover {{ background: #219150; }}
            
            /* Ajuste crucial para as quebras de linha */
            pre {{ 
                background: #f8f9fa; 
                padding: 15px; 
                border-left: 5px solid #27ae60; 
                border-radius: 4px; 
                white-space: pre-wrap;       /* Respeita quebras de linha originais */
                word-wrap: break-word;       /* Evita que o texto saia da caixa */
                color: #2c3e50; 
                font-family: 'Segoe UI', Arial, sans-serif; /* Voz do mestre sem fonte de código */
                font-size: 1.1em;
            }}
            
            .historico {{ margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }}
            .msg-box {{ margin-bottom: 15px; padding: 15px; border-radius: 8px; font-size: 0.95em; white-space: pre-wrap; }}
            .user {{ background: #d1ecf1; border-left: 4px solid #0c5460; color: #0c5460; }}
            .assistant {{ background: #d4edda; border-left: 4px solid #155724; color: #155724; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>ZenBot – Oficina de Tuning</h2>
            <form method="post">
                <label>Estilo (Personalidade):</label>
                <select name="style">
                    <option value="index.md" selected>Mestre Zen (Padrão)</option>
                    <option value="01-motivacao.md">Motivação</option>
                    <option value="09-metafora-zen.md">Metáfora Zen</option>
                    <option value="10-jornada-de-aprendizado.md">Jornada</option>
                </select>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div>
                        <label>Temperature:</label>
                        <input type="number" step="0.05" name="temperature" value="0.7">
                    </div>
                    <div>
                        <label>Max Tokens:</label>
                        <input type="number" name="max_tokens" value="400">
                    </div>
                </div>

                <label>Mensagens para Contexto:</label>
                <input type="number" name="context_count" value="5">

                <label>Sua Pergunta:</label>
                <input type="text" name="question" placeholder="O que é o aqui e agora?" required>

                <button type="submit">Enviar para o ZenBot</button>
            </form>

            <h3>Resposta do Mestre:</h3>
            <pre>{resposta if resposta else "O silêncio precede a sabedoria..."}</pre>

            <div class="historico">
                <h3>Diálogo Recente:</h3>
                {historico_html}
            </div>
        </div>
    </body>
    </html>
    """

@router.get("/")
async def tuning_page():
    historico_html = "".join([
        f"<div class='msg-box {msg['role']}'><b>{msg['role'].capitalize()}:</b> {msg['content']}</div>" 
        for msg in MESSAGES[-10:]
    ])
    return HTMLResponse(render_form_html(historico_html=historico_html))

@router.post("/")
async def tuning_submit(
    style: str = Form(...),
    temperature: float = Form(...),
    max_tokens: int = Form(...),
    context_count: int = Form(...),
    question: str = Form(...)
):
    try:
        # Busca o conteúdo do estilo na pasta docs/ (conforme suas capturas)
        style_path = os.path.join("docs", style)
        
        style_content = ""
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                style_content = f.read()

        pergunta_com_estilo = f"Estilo: {style_content}\n\nPergunta: {question}"
        historico_list = get_last_messages(context_count)
        mensagens_para_responder = historico_list + [{"role": "user", "content": pergunta_com_estilo}]

        # TRATAMENTO DA RESPOSTA DO ZEN.PY
        resposta_final = responder(question, mensagens_para_responder)

        # 1. Remove parênteses se for uma Tupla
        if isinstance(resposta_final, tuple):
            resposta_final = resposta_final[0]

        # 2. Limpa aspas extras se existirem
        resposta_final = str(resposta_final).strip("()").strip("'").strip('"')

        # Salva no histórico (sem as tags HTML para não poluir)
        add_to_history(question, resposta_final)
        
        resposta = resposta_final

    except Exception as e:
        resposta = f"Ocorreu uma distração na meditação: {str(e)}"

    historico_html = "".join([
        f"<div class='msg-box {msg['role']}'><b>{msg['role'].capitalize()}:</b> {msg['content']}</div>" 
        for msg in MESSAGES[-10:]
    ])
    
    return HTMLResponse(render_form_html(resposta=resposta, historico_html=historico_html))