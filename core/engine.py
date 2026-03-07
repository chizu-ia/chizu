
# core/engine.py
import json
import math
import random
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer

# =============================
# Configurações gerais
# =============================

BASE_DIR = Path(__file__).resolve().parent.parent

# Modelo excelente para Português e leve para o Render
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Carrega o modelo uma única vez (Singleton)
print("[ENGINE] Despertando modelo de embeddings local...")
model_local = SentenceTransformer(MODEL_NAME)

THRESHOLD = 0.35 # Ajustado para o novo modelo

# =============================
# Funções Matemáticas
# =============================

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-9)

# =============================
# Nova Geração de Embedding (Local)
# =============================

def gerar_embedding(texto):
    """Gera o vetor usando o modelo local, sem depender de APIs externas."""
    embedding = model_local.encode(texto)
    return embedding.tolist()

# =============================
# Busca Semântica (RAG)
# =============================

def buscar_blocos(pergunta, top_k=3):
    caminho_emb = BASE_DIR / "data" / "embeddings_bge.json"
    
    if not caminho_emb.exists():
        print("[AVISO] Arquivo de embeddings não encontrado.")
        return []

    with open(caminho_emb, "r", encoding="utf-8") as f:
        base = json.load(f)

    try:
        emb_pergunta = gerar_embedding(pergunta)
    except Exception as e:
        print(f"[ERRO] Falha ao processar pensamento: {e}")
        return []

    scores = []
    for item in base:
        # Nota: Se os embeddings no JSON foram gerados com outro modelo (Ollama),
        # o ideal é rodar o script de regeneração com este novo modelo local.
        sim = cosine_similarity(emb_pergunta, item["embedding"])
        scores.append((sim, item["texto"]))

    scores.sort(reverse=True, key=lambda x: x[0])
    
    if not scores or scores[0][0] < THRESHOLD:
        return []

    return [texto for _, texto in scores[:top_k]]


# =============================
# Motor cognitivo principal
# =============================

# core/engine.py

def montar_prompt(pergunta, estilo="padrao"):
    system_prompt = (
        "Você é o Mestre Chizu, um mestre Zen inspirado em Shunryu Suzuki e Thich Nhat Hanh. "
        "Sua linguagem é poética, breve e profunda. Não use emojis."
    )
    
    # Busca o contexto no livro (RAG)
    blocos = buscar_blocos(pergunta)
    contexto = "\n\n".join(blocos) if blocos else "Mantenha o silêncio se não houver palavras sábias."

    if estilo == "koan":
        system_prompt += " Responda apenas com um Koan clássico ou original."
    elif estilo == "aforismo":
        system_prompt += " Responda com uma única frase curta e impactante."

    return [
        {"role": "system", "content": f"{system_prompt}\n\nContexto dos ensinamentos:\n{contexto}"},
        {"role": "user", "content": pergunta}
    ]