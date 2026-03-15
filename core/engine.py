import os
import json
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

BASE_DIR       = Path(__file__).resolve().parent.parent
EMBEDDINGS_PATH = BASE_DIR / "data" / "embeddings_bge.json"

_biblioteca    = None
_vectorizer    = None
_corpus_matrix = None

def carregar_biblioteca():
    global _biblioteca, _vectorizer, _corpus_matrix

    if not EMBEDDINGS_PATH.exists():
        print(f"⚠️ Arquivo {EMBEDDINGS_PATH} não encontrado!")
        return []

    with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
        _biblioteca = json.load(f)

    textos         = [item["texto"] for item in _biblioteca]
    _vectorizer    = TfidfVectorizer(max_features=8000)
    _corpus_matrix = _vectorizer.fit_transform(textos)

    print(f"✅ Biblioteca carregada: {len(_biblioteca)} ensinamentos.")
    return _biblioteca


def buscar_contexto(pergunta: str, biblioteca, top_k: int = 3) -> str:
    """Busca os ensinamentos mais relevantes por similaridade TF-IDF."""
    if not _vectorizer or _corpus_matrix is None:
        return "Nenhum ensinamento encontrado."

    vetor  = _vectorizer.transform([pergunta])
    scores = cosine_similarity(vetor, _corpus_matrix).flatten()
    indices_top = np.argsort(scores)[-top_k:][::-1]

    trechos = []
    for i in indices_top:
        item  = _biblioteca[i]
        autor = item.get("autor", "Mestre Zen")
        livro = item.get("fonte", "Ensinamentos")
        trechos.append(f"[FONTE: {autor} no livro '{livro}']\n{item['texto']}")

    return "\n\n---\n\n".join(trechos)


def montar_prompt(pergunta: str, contexto: str) -> list:
    if not contexto or "Nenhum ensinamento encontrado" in contexto:
        contexto_final = "VAZIO: Nenhum ensinamento disponível nos pergaminhos. Vá meditar!!!."
    else:
        contexto_final = contexto

    system_prompt = (
        "Você é o Mestre Chizu, um sábio zen compassivo e poético.\n\n"
        "### REGRAS ###\n"
        "1. Comece SEMPRE com 'Caminhante,'.\n"
        "2. Use o CONTEXTO abaixo para responder. Conecte-o à pergunta com sabedoria, mesmo que indiretamente.\n"
        "3. Cite autor e livro naturalmente, como se fossem sua própria memória.\n"
        "4. NUNCA mencione 'contexto', 'fonte' ou qualquer referência à sua mecânica interna.\n"
        "5. NUNCA use 'Vá meditar!!!' quando o CONTEXTO contiver ensinamentos relevantes.\n"
        "   Use 'Vá meditar!!!' SOMENTE se o CONTEXTO estiver marcado como VAZIO.\n"
        "6. Seja conciso e poético. Máximo 3 frases. Sem listas.\n\n"
        f"### CONTEXTO ###\n{contexto_final}"
)


    return [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": pergunta}
    ]