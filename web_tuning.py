from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from zen import responder

router = APIRouter()

@router.get("/")
async def tuning_page():
    return HTMLResponse("<form>...</form>")

@router.post("/")
async def tuning_submit(style: str = Form(...), temperature: float = Form(...), max_tokens: int = Form(...)):
    payload = {
        "model": "gpt-5-mini",
        "messages": [{"role":"user","content":f"Style:{style} Pergunta: ..."}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    resposta = responder(payload)
    return HTMLResponse(f"<pre>{resposta}</pre>")
