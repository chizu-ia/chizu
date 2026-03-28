"""
corrigir_links.py
Corrige links quebrados nos documentos mkdocs do Chizu.

Dois tipos de problema:
1. Links com prefixo 'conceitos/' duplicado (dentro de docs/conceitos/)
   conceitos/08-pipeline.md  →  08-pipeline.md

2. Links para arquivos na raiz docs/ sem o '../'
   00-por-que-chizu.md  →  ../00-por-que-chizu.md

Uso:
  python corrigir_links.py --dry-run   # só mostra o que seria corrigido
  python corrigir_links.py             # corrige de verdade
"""

import re
import sys
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv
DOCS_DIR = Path("docs")

LINK_CONCEITOS_RE = re.compile(r'\[([^\]]*)\]\(conceitos/([^)]+\.md)\)')
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^/)][^)]*\.md)\)')


def arquivos_raiz(docs_dir: Path) -> set:
    return {f.name for f in docs_dir.glob("*.md")}


def corrigir_arquivo(path: Path, raiz: set) -> int:
    texto = path.read_text(encoding="utf-8")
    novo = texto
    substituicoes = []

    # Tipo 1: conceitos/ duplicado
    for m in LINK_CONCEITOS_RE.finditer(texto):
        antigo = m.group(0)
        correto = f'[{m.group(1)}]({m.group(2)})'
        substituicoes.append((antigo, correto))

    # Tipo 2: links para raiz sem ../
    texto_tipo1 = LINK_CONCEITOS_RE.sub(lambda m: f'[{m.group(1)}]({m.group(2)})', texto)
    for m in LINK_RE.finditer(texto_tipo1):
        nome = m.group(2)
        if nome.startswith(('..', 'http', '#')):
            continue
        if nome in raiz:
            antigo = m.group(0)
            correto = f'[{m.group(1)}](../{nome})'
            substituicoes.append((antigo, correto))

    if substituicoes:
        print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}📄 {path}")
        for antigo, correto in substituicoes:
            print(f"  ❌  {antigo}")
            print(f"  ✅  {correto}")
            novo = novo.replace(antigo, correto, 1)
        if not DRY_RUN:
            path.write_text(novo, encoding="utf-8")

    return len(substituicoes)


def main():
    conceitos_dir = DOCS_DIR / "conceitos"
    if not conceitos_dir.exists():
        print(f"Pasta não encontrada: {conceitos_dir}")
        sys.exit(1)

    raiz = arquivos_raiz(DOCS_DIR)
    arquivos = sorted(conceitos_dir.glob("*.md"))

    total = 0
    for arq in arquivos:
        total += corrigir_arquivo(arq, raiz)

    print(f"\n{'─'*50}")
    if total == 0:
        print("✅ Nenhum link para corrigir.")
    elif DRY_RUN:
        print(f"🔍 {total} link(s) seriam corrigidos. Rode sem --dry-run para aplicar.")
    else:
        print(f"✅ {total} link(s) corrigidos.")


if __name__ == "__main__":
    main()
