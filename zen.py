import os
import time
import random
import requests
import traceback
from core.engine import montar_prompt
from core.ai_provider import FreeAIProvider

# =============================
# Configurações da API
# =============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
TIMEOUT = 30

# =============================
# Mensagens zen
# =============================

RESPOSTAS_ZEN = [
    "A resposta não está nas palavras, mas no silêncio entre elas.",
    "A mente que pergunta já contém a resposta.",
    "Quando nada surge, o vazio se revela.",
    "Talvez não haja nada a buscar.",
    "Observe este instante antes de perguntar novamente.",
    "O caminho não se revela ao ser forçado.",
    "A pergunta correta dissolve a necessidade da resposta.",
    "A resposta está no silêncio, não nas palavras.",
    "Observe sua própria mente enquanto pergunta.",
    "Talvez a pergunta seja mais importante que a resposta.",
    "O vento levou a resposta... tente novamente mais tarde.",
    "Não há palavras para isso, apenas prática."
]

ERROS_ZEN = [
    "O vento sopra forte e Chizu se cala por instantes. Tente novamente.",
    "Uma folha cai entre nós e a resposta se perde. Pergunte outra vez.",
    "O silêncio de Chizu é mais profundo que o mar."
]

AQUECIMENTO = [
    "(Chizu prepara o incenso...)",
    "(O mestre ajusta a postura de zazen...)"
]

# =============================
# Estilo
# =============================

def detectar_estilo(pergunta: str) -> str:
    p = pergunta.lower().strip()

    if p.startswith("/aforismo"):
        return "aforismo"
    if p.startswith("/koan"):
        return "koan"
    if p.startswith("/meditacao"):
        return "meditacao"

    return "padrao"


def limpar_comando(pergunta: str) -> str:
    if pergunta.startswith("/"):
        partes = pergunta.split(" ", 1)
        if len(partes) == 2:
            return partes[1]
        return ""
    return pergunta


# =============================
# Motor de resposta
# =============================


ai_provider = FreeAIProvider()

def responder(pergunta, historico=None, temperature=0.4, max_tokens=180):
    """
    Orquestra a resposta do Mestre Chizu, 
    garantindo resiliência através de múltiplos provedores.
    """
    estilo = detectar_estilo(pergunta)
    pergunta_limpa = limpar_comando(pergunta)

    try:
        # 1. Monta o prompt (System + RAG + Pergunta) usando o engine.py
        messages = montar_prompt(pergunta_limpa, estilo)
        
        # 2. Normaliza o histórico para manter a fluidez da conversa
        def normalizar_historico(hist, limite_pares=2, max_chars=300):
            if not hist: return []
            ultimos = hist[-limite_pares*2:]
            return [
                {
                    "role": m.get("role", "user"), 
                    "content": str(m.get("content", ""))[:max_chars]
                } for m in ultimos
            ]

        memoria = normalizar_historico(historico)
        
        # Insere a memória entre o System Prompt e a pergunta atual
        # messages[0] é o System, messages[1] é o User
        full_messages = [messages[0]] + memoria + [messages[-1]]

        # 3. MÁGICA DO FALLBACK: Tenta Groq -> Gemini -> SambaNova -> Cerebras
        resposta_llm = ai_provider.chat(full_messages, temperature, max_tokens)
        
        # 4. Polimento Zen na resposta
        resposta_llm = resposta_llm.strip()
        
        # Remove marcas de pensamento se a IA as gerar (como no DeepSeek ou similares)
        if "</think>" in resposta_llm:
            resposta_llm = resposta_llm.split("</think>")[-1].strip()

        if not resposta_llm.endswith((".", "。", "!", "?", "...", "—")):
            resposta_llm += "..."

        return resposta_llm, resposta_llm

    except Exception as e:
        # Se o "tremor na montanha digital" derrubar todas as APIs
        print(f"[LOG CHIZU] Falha total no sistema: {e}")
        
        # O mestre recorre à sua sabedoria interior (estática)
        sabedoria_silenciosa = random.choice(RESPOSTAS_ZEN)
        
        return sabedoria_silenciosa, sabedoria_silenciosa
    
# =============================
# Inicialização
# =============================

def verificar_chave():
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY não configurada.")
        exit(1)


def aquecer_modelo():
    print(random.choice(AQUECIMENTO))
    