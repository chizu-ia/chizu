# Chunks e Embeddings

Este capítulo explica dois conceitos fundamentais usados pelo Chizu:

- **Chunks**
- **Embeddings**

Esses elementos formam a base da **busca semântica**, permitindo que o sistema encontre trechos relevantes dentro dos livros antes de gerar uma resposta.

---

## O que é um Chunk

Um **chunk** é um pequeno pedaço de texto retirado de um livro.

Em vez de consultar um livro inteiro, o sistema divide o conteúdo em partes menores.  
Cada fragmento é armazenado separadamente para facilitar a busca de informações.

Exemplo de chunk:

> A mente do principiante tem muitas possibilidades.

Outro exemplo:

> O silêncio não é ausência de som, mas presença de atenção.

Cada um desses fragmentos passa a ser uma **unidade de conhecimento** dentro do sistema.

---

##  O que é um Embedding

Um **embedding** é a representação numérica de um texto.

Como computadores trabalham melhor com números do que com palavras, o sistema transforma cada chunk em uma sequência de números que representa seu significado.

Exemplo simplificado:

Texto:

Respire e volte ao momento presente.

Embedding:
```text
[0.18, -0.33, 0.71, 0.04, -0.55, ...]
```

Esses números formam um **vetor**, que descreve o significado do texto.

---

## Por que Embeddings são importantes

Com embeddings, o sistema consegue comparar **significados**, não apenas palavras.

Por exemplo:

Pergunta do usuário:

> Como acalmar a mente?

O sistema transforma a pergunta em um embedding e compara com os embeddings dos chunks armazenados.

Assim ele consegue encontrar trechos relacionados, mesmo que as palavras utilizadas sejam diferentes.

---

##  Como o Chizu usa Chunks e Embeddings

O processo interno funciona da seguinte forma:

1. O usuário faz uma pergunta
2. A pergunta é convertida em um embedding
3. O sistema compara esse vetor com os embeddings dos chunks
4. Os trechos mais próximos em significado são selecionados
5. Esses trechos são enviados ao modelo de linguagem
6. O modelo gera a resposta com base nesses textos

Esse processo é conhecido como **busca semântica**.

---

##  Como isso aparece no projeto

No Chizu, os chunks e embeddings são armazenados em arquivos.

Um exemplo é:
```text
data/embeddings.json
```

Cada registro contém:

- o texto do chunk
- o vetor embedding correspondente

Exemplo simplificado:

```json
{
  "texto": "Respire e volte ao momento presente.",
  "embedding": [0.18, -0.33, 0.71, 0.04, -0.55]
}
```

##  Analogia simples

Podemos imaginar o sistema como uma biblioteca.

- **Chunks** são pequenos trechos de livros espalhados pelas estantes.
- **Embeddings** são coordenadas em um mapa que indicam o significado desses trechos.

Quando surge uma pergunta, o sistema procura no mapa os trechos **mais próximos daquele significado**.

---

##  Resumo

- **Chunk** → pequeno pedaço de texto  
- **Embedding** → representação numérica do significado do texto  
- **Busca semântica** → comparação entre embeddings para encontrar trechos relevantes

Esses dois elementos formam a base da **memória e da capacidade de busca do Chizu**.
