# Busca Semântica

Este capítulo explica o conceito de **busca semântica**, um dos mecanismos centrais utilizados pelo Chizu para encontrar informações relevantes nos textos.

Diferente de uma busca tradicional baseada apenas em palavras, a busca semântica tenta encontrar **significados relacionados**.

---

## 🔎 O que é Busca Semântica

A **busca semântica** é uma técnica que permite encontrar conteúdos com **significado semelhante**, mesmo que as palavras utilizadas sejam diferentes.

Em uma busca tradicional, o sistema procura **palavras exatas**.

Exemplo:

Consulta:

> Como acalmar a mente?

Uma busca tradicional procuraria apenas por palavras como:

- acalmar
- mente

Se essas palavras não estiverem no texto, o sistema não encontra nada.

Já a **busca semântica** procura ideias relacionadas, como:

- respirar
- atenção plena
- silêncio interior
- observar pensamentos

Mesmo sem repetir as mesmas palavras.

---

## 🧠 Como a Busca Semântica Funciona

A busca semântica funciona usando **embeddings**, que são representações numéricas do significado dos textos.

O processo funciona da seguinte forma:

1. O sistema possui vários **chunks** de texto armazenados
2. Cada chunk possui um **embedding**
3. Quando o usuário faz uma pergunta, ela também é convertida em embedding
4. O sistema compara esse vetor com os embeddings existentes
5. Os textos com **maior proximidade semântica** são selecionados

Essa proximidade normalmente é calculada usando **similaridade vetorial**.

---

## 📏 Similaridade entre Vetores

Embeddings podem ser comparados matematicamente.

Uma das técnicas mais comuns é a **similaridade de cosseno (cosine similarity)**.

Ela mede o **ângulo entre dois vetores**.

- vetores próximos → significados semelhantes  
- vetores distantes → significados diferentes  

Exemplo simplificado:

```text
Pergunta: "Como acalmar a mente?"
        ↓
Embedding da pergunta
        ↓
Comparação com embeddings dos textos
        ↓
Seleção dos chunks mais próximos
```
---

## ⚙️ Fluxo da Busca Semântica no Chizu

No Chizu, o fluxo básico funciona assim:

1. O usuário faz uma pergunta
2. A pergunta é convertida em embedding
3. O sistema procura os embeddings mais próximos
4. Os chunks correspondentes são recuperados
5. Esses textos são enviados ao modelo de linguagem
6. O modelo gera a resposta usando esse contexto

Esse processo permite que o sistema responda usando **informações presentes nos livros carregados**.

---

## 📚 Exemplo Prático

Suponha que exista um chunk no sistema:

> Observe sua respiração e permita que os pensamentos passem.

Usuário pergunta:

> Como posso acalmar minha mente?

Mesmo que as palavras sejam diferentes, o significado é semelhante.

A busca semântica identifica essa proximidade e recupera esse trecho como contexto para a resposta.

---

## 🧘 Analogia simples

Podemos imaginar a busca semântica como um **mapa de significados**.

- Cada texto é um ponto nesse mapa
- Textos com significados parecidos ficam próximos
- Textos muito diferentes ficam distantes

Quando surge uma pergunta, o sistema procura **os pontos mais próximos no mapa**.

---

## 📌 Resumo

- **Busca tradicional** → procura palavras exatas  
- **Busca semântica** → procura significados semelhantes  
- **Embeddings** permitem representar textos como vetores  
- **Similaridade vetorial** identifica conteúdos relacionados  

A busca semântica é o mecanismo que permite ao Chizu **encontrar conhecimento relevante dentro dos textos antes de gerar uma resposta**.
