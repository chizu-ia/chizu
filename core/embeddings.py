# core/embeddings.py
import json
import time
from pathlib import Path
from sentence_transformers import SentenceTransformer

# MESMO MODELO DO ENGINE.PY PARA MANTER A HARMONIA
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(MODEL_NAME)

def main():
    chunks_path = Path("textos/chunks.txt")
    # Usando o nome que o seu engine.py procura:
    out_path = Path("data/embeddings_bge.json") 

    if not chunks_path.exists():
        print(f"❌ Arquivo não encontrado: {chunks_path}")
        return

    blocos = chunks_path.read_text(encoding="utf-8").split("\n\n---\n\n")
    embeddings = []
    total = len(blocos)
    
    print(f"✨ Iniciando geração local para {total} blocos...")

    for i, bloco in enumerate(blocos, 1):
        bloco = bloco.strip()
        if not bloco: continue

        # Gera o vetor localmente
        vec = model.encode(bloco).tolist()

        embeddings.append({
            "id": i,
            "texto": bloco,
            "embedding": vec
        })
        
        if i % 10 == 0:
            print(f"Processed {i}/{total}...")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(embeddings, ensure_ascii=False, indent=2))
    print(f"✅ Sucesso! {out_path} gerado com o novo modelo local.")

if __name__ == "__main__":
    main()