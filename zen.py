import os
from dotenv import load_dotenv
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
    "A mente que pergunta já contém a resposta.",
    "A pergunta correta dissolve a necessidade da resposta.",
    "A resposta está no silêncio, não nas palavras.",
    "A resposta não está nas palavras, mas no silêncio entre elas.",
    "Não há palavras para isso, apenas prática.",
    "O caminho não se revela ao ser forçado.",
    "O vento levou a resposta... tente novamente mais tarde.",
    "Observe este instante antes de perguntar novamente.",
    "Observe sua própria mente enquanto pergunta.",
    "Quando nada surge, o vazio se revela.",
    "Talvez a pergunta seja mais importante que a resposta.",
    "Talvez não haja nada a buscar."
]

ERROS_ZEN = [
    "O silêncio de Chizu é mais profundo que o mar.",
    "O vento sopra forte e Chizu se cala por instantes. Tente novamente.",
    "Uma folha cai entre nós e a resposta se perde. Pergunte outra vez."
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

import random

def responder(pergunta, historico=None, temperature=0.45, max_tokens=500, top_p=0.9, frequency_penalty=0.45, presence_penalty=0.25):
    """
    Orquestra a resposta do Mestre Chizu com captura de silêncio e variação poética.
    """
    estilo = detectar_estilo(pergunta)
    pergunta_limpa = limpar_comando(pergunta)

    try:
        # 1. Monta o prompt (System + RAG + Pergunta)
        messages = montar_prompt(pergunta_limpa, estilo)
        
        # 2. Normaliza o histórico
        def normalizar_historico(hist, max_chars=300):
            if not hist: return []
            return [
                {
                    "role": m.get("role", "user"), 
                    "content": str(m.get("content", ""))[:max_chars]
                } for m in hist if isinstance(m, dict)
            ]

        memoria = normalizar_historico(historico)
        full_messages = [messages[0]] + memoria + [messages[-1]]

        # 3. MÁGICA DO FALLBACK: Chamada aos provedores
        resposta_llm, ia_nome = ai_provider.chat(
            full_messages, 
            temperature=temperature, 
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

        # 4. Polimento Zen na resposta
        if isinstance(resposta_llm, tuple):
            resposta_llm = resposta_llm[0]
            
        resposta_llm = str(resposta_llm).strip()
        
        # Remove tags de pensamento (modelos R1)
        if "</think>" in resposta_llm:
            resposta_llm = resposta_llm.split("</think>")[-1].strip() 

        # 5. O FILTRO DO SILÊNCIO: Captura erro de contexto ou erro de API (Fallback)
        gatilho_silencio = "Caminhante, o silêncio envolve essa questão"

        if gatilho_silencio in resposta_llm or ia_nome == "Fallback":
            import random
            # Sorteia uma das frases da sua lista RESPOSTAS_ZEN
            variacao = random.choice(RESPOSTAS_ZEN)
            
            # Formata a resposta final variada
            return f"Caminhante, {variacao.lower()}\n\nVá meditar!!!.", "Mestre Chizu"

        # Se houver resposta válida no contexto, retorna normalmente
        return resposta_llm, ia_nome

    except Exception as e:
        import traceback
        import random
        print(f"[LOG CHIZU] Falha total no sistema: {e}")
        traceback.print_exc()
        # Fallback extremo caso o código acima quebre por algum motivo
        return f"Caminhante, {random.choice(RESPOSTAS_ZEN).lower()}\n\nVá meditar!!!.", "Mestre Chizu"
    
    except Exception as e:
            print(f"[LOG CHIZU] Falha total no sistema: {e}")
            traceback.print_exc() # Isso vai te mostrar o erro real no terminal
            return random.choice(RESPOSTAS_ZEN), "Sistema (Fallback)" # Adicionei a vírgula e o nome
        
# =============================
# Inicialização e Verificação
# =============================

# IMPORTANTE: Chamar o load_dotenv fora de qualquer função garante 
# que as chaves fiquem disponíveis para todo o arquivo imediatamente.
load_dotenv(override=True)

def verificar_chave():
    """Valida se todas as APIs do Mestre Zen estão prontas"""
    chaves = [
        "GROQ_API_KEY", 
        "CEREBRAS_API_KEY", 
        "GEMINI_API_KEY", 
        "SAMBANOVA_API_KEY"
    ]
    
    erros = 0
    print("\n--- Verificando Chaves de API ---")
    for chave in chaves:
        valor = os.getenv(chave)
        if not valor:
            print(f"❌ {chave} não configurada.")
            erros += 1
        else:
            # Mostra apenas os 4 primeiros caracteres por segurança
            print(f"✅ {chave} carregada: {valor[:4]}...")
    
    if erros == 0:
        print("✅ Sistema pronto: Groq, Cerebras, Gemini e SambaNova online.\n")
    else:
        print(f"⚠️ Atenção: {erros} chaves ausentes. Algumas funções podem falhar.\n")

def aquecer_modelo():
    print(random.choice(AQUECIMENTO))