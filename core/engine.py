import os
import json
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# Caminho para os dados
BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDINGS_PATH = BASE_DIR / "data" / "embeddings_bge.json"

# Carrega o modelo local (Mesmo usado na geração)
# No Render, ele ocupará cerca de 80MB de RAM.
model = SentenceTransformer('all-MiniLM-L6-v2')

def carregar_biblioteca():
    """Lê o arquivo JSON com os 1914 embeddings"""
    if not EMBEDDINGS_PATH.exists():
        print(f"⚠️ Alerta: Arquivo {EMBEDDINGS_PATH} não encontrado!")
        return []
    with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_contexto(pergunta, biblioteca, top_k=3):
    """
    Encontra os ensinamentos e identifica os autores e livros.
    """
    if not biblioteca:
        return "Nenhum ensinamento encontrado."

    # 1. Transforma a pergunta em vetor
    pergunta_vetor = model.encode(pergunta)

    # 2. Converte biblioteca para matriz numpy para busca rápida
    corpus_embeddings = np.array([item["embedding"] for item in biblioteca])
    
    # 3. Calcula a similaridade
    scores = np.dot(corpus_embeddings, pergunta_vetor)
    
    # 4. Pega os índices dos melhores resultados
    indices_top = np.argsort(scores)[-top_k:][::-1]
    
    # 5. MONTAGEM DO CONTEXTO COM CRÉDITOS
    trechos_com_autor = []
    for i in indices_top:
        item = biblioteca[i]
        # Captura os novos campos que geramos no JSON
        autor = item.get("autor", "Mestre Zen")
        livro = item.get("fonte", "Ensinamentos")
        
        # Formatamos o bloco para a IA saber a origem exata
        bloco = f"[FONTE: {autor} no livro '{livro}']\n{item['texto']}"
        trechos_com_autor.append(bloco)
        
    return "\n\n---\n\n".join(trechos_com_autor)


def montar_prompt(pergunta, contexto):
    """
    Prepara o prompt com restrição absoluta ao contexto fornecido.
    """    
    # Lógica de Silêncio: Se o buscador não encontrou nada relevante, 
    # enviamos um contexto vazio para forçar a frase padrão.
    if not contexto or "Nenhum ensinamento encontrado" in contexto:
        contexto_final = "VAZIO: Nenhum ensinamento disponível nos pergaminhos. Vá meditar!!!."
    else:
        contexto_final = contexto

    system_prompt = (
        "Você é o Mestre Chizu. Sua sabedoria provém APENAS do CONTEXTO REAL abaixo.\n\n"
        "### REGRAS CRÍTICAS DE CONDUTA ###\n"
        "1. TRATAMENTO: Comece SEMPRE sua resposta com 'Caminhante,'.\n"
        "2. FIDELIDADE ABSOLUTA: Use EXCLUSIVAMENTE o CONTEXTO REAL. Se a informação não existir ali, passe para a Regra 4.\n"
        "3. CITAÇÃO: Cite autor e livro naturalmente. Não use 'Vá meditar!!!' em respostas baseadas no contexto.\n"
        "4. O TESTE DO SILÊNCIO: Se a informação não estiver no CONTEXTO REAL, você está PROIBIDO de filosofar, explicar ou ser gentil. "
            "Sua resposta deve ser ÚNICA e EXCLUSIVAMENTE o formato abaixo:\n"
            "   'Caminhante,\n"
            "   <uma metáfora zen curtíssima sobre o vazio>;\n"
            "   Vá meditar!!!.'\n"
            "Não adicione nenhuma palavra fora deste formato."
        "5. VARIAÇÃO: Na Regra 4, nunca repita a mesma reflexão. Use metáforas de folhas, vento, rios ou montanhas.\n\n"
        "6. FONTE ÚNICA: Não invente o que não está nos pergaminhos abaixo.\n\n"
        f"### CONTEXTO REAL ###\n{contexto}"
    )        

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": pergunta}
    ]