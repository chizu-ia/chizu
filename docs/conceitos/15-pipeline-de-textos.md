# Pipeline de Textos

Este capítulo descreve o **pipeline de processamento de textos** utilizado pelo ZenBot.

Antes que o sistema consiga responder perguntas sobre um livro ou documento, o conteúdo precisa passar por uma série de etapas de processamento.

Esse fluxo transforma textos brutos em **informações pesquisáveis por significado**.

---

## 🧭 Visão geral do pipeline

O pipeline do ZenBot segue estas etapas principais:

1. Entrada do texto
2. Divisão em chunks
3. Geração de embeddings
4. Armazenamento dos dados
5. Busca semântica durante as consultas

Fluxo simplificado:

```text
Livro / Documento
        ↓
Divisão em Chunks
        ↓
Geração de Embeddings
        ↓
Armazenamento
        ↓
Busca Semântica
        ↓
RAG
        ↓
Resposta ao usuário
```

---

## 📥 1. Entrada do texto

O processo começa com um **livro ou documento** que será utilizado como fonte de conhecimento.

Esses textos podem vir de:

- livros
- arquivos de texto
- documentos convertidos
- conteúdos preparados manualmente

O objetivo dessa etapa é disponibilizar o conteúdo que será processado pelo sistema.

---

## 🧩 2. Divisão em Chunks

O texto completo é dividido em **pequenos fragmentos**, chamados de **chunks**.

Isso é necessário porque:

- modelos de linguagem têm limites de contexto
- pedaços menores facilitam a busca
- cada fragmento pode ser indexado separadamente

Exemplo:

Texto original:

> A mente do principiante tem muitas possibilidades.

Chunk gerado:

> A mente do principiante tem muitas possibilidades.

Cada chunk passa a ser tratado como uma **unidade independente de conhecimento**.

---

## 🔢 3. Geração de Embeddings

Depois que os chunks são criados, cada um deles é convertido em um **embedding**.

Embeddings são vetores numéricos que representam o **significado do texto**.

Exemplo simplificado:

```text
Texto:
Respire e volte ao momento presente.

Embedding:
[0.18, -0.33, 0.71, 0.04, -0.55, ...]
```

Esses vetores permitem que o sistema compare **significados entre textos**.

---

## 💾 4. Armazenamento

Após a geração dos embeddings, os dados são armazenados para consulta futura.

Cada registro normalmente contém:

- o texto do chunk
- o embedding correspondente

Exemplo simplificado:

```json
{
  "texto": "Respire e volte ao momento presente.",
  "embedding": [0.18, -0.33, 0.71, 0.04, -0.55]
}
```

Esse conjunto forma a **base de conhecimento do ZenBot**.

---

## 🔎 5. Busca durante perguntas

Quando um usuário faz uma pergunta, ocorre o seguinte processo:

1. a pergunta é convertida em embedding
2. o sistema compara esse vetor com os embeddings armazenados
3. os chunks mais próximos são encontrados
4. esses trechos são enviados ao modelo de linguagem

Esse mecanismo utiliza **busca semântica**.

---

## 🤖 6. Geração da resposta (RAG)

Após recuperar os trechos relevantes, o sistema utiliza a técnica **RAG (Retrieval Augmented Generation)**.

O modelo recebe:

- a pergunta do usuário
- os chunks recuperados

E então gera uma resposta baseada nesse contexto.

---

## 🧘 Analogia simples

Podemos imaginar o pipeline como o trabalho de um **bibliotecário**.

1. os livros chegam à biblioteca  
2. eles são organizados em pequenos trechos  
3. cada trecho é catalogado por significado  
4. quando alguém faz uma pergunta, o bibliotecário encontra os trechos relevantes  
5. esses trechos ajudam a formular a resposta  

---

## 📌 Resumo

O pipeline de textos do ZenBot segue esta sequência:

- **Entrada de textos**
- **Divisão em chunks**
- **Geração de embeddings**
- **Armazenamento dos dados**
- **Busca semântica**
- **RAG para geração de respostas**

Esse processo transforma textos comuns em uma **base de conhecimento consultável por significado**.
