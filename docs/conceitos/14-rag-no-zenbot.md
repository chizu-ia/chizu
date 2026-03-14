# RAG no Chizu

Este capítulo explica como o Chizu utiliza a técnica chamada **RAG (Retrieval Augmented Generation)** para gerar respostas baseadas nos textos carregados no sistema.

RAG combina duas capacidades:

- **recuperação de informação** (retrieval)
- **geração de texto** (generation)

Essa combinação permite que o modelo responda perguntas utilizando **conteúdo real armazenado no sistema**.

---

## 🧠 O que é RAG

**RAG** significa *Retrieval Augmented Generation*, que pode ser traduzido como:

> Geração de texto aumentada por recuperação de informações.

Em vez de responder apenas com base no conhecimento interno do modelo, o sistema primeiro **busca informações relevantes** e depois usa essas informações para gerar a resposta.

Isso torna as respostas:

- mais precisas
- mais contextualizadas
- baseadas nos textos fornecidos ao sistema

---

## 🔎 Como o RAG funciona

O processo geral do RAG segue três etapas principais:

1. **Receber a pergunta do usuário**
2. **Buscar trechos relevantes nos textos**
3. **Gerar a resposta usando esses trechos como contexto**

Esse processo permite que o modelo responda perguntas sobre conteúdos específicos, como livros ou documentos.

---

## ⚙️ Fluxo de funcionamento no Chizu

No Chizu, o fluxo funciona da seguinte forma:

1. O usuário faz uma pergunta
2. A pergunta é convertida em **embedding**
3. O sistema executa uma **busca semântica**
4. Os **chunks mais relevantes** são recuperados
5. Esses textos são enviados ao modelo de linguagem
6. O modelo gera a resposta usando esses trechos como base

Fluxo simplificado:

```text
Pergunta do usuário
        ↓
Embedding da pergunta
        ↓
Busca semântica
        ↓
Chunks relevantes
        ↓
Modelo de linguagem
        ↓
Resposta final
````
---

## 📚 Por que usar RAG

Sem RAG, o modelo responde apenas com base no **conhecimento aprendido durante o treinamento**.

Com RAG, o sistema pode responder utilizando:

- livros carregados
- documentos do projeto
- bases de conhecimento específicas

Isso permite que o Chizu funcione como um **assistente especializado nos textos fornecidos**.

---

## 📦 Exemplo simplificado

Usuário pergunta:

> O que é atenção plena?

O sistema realiza os seguintes passos:

1. converte a pergunta em embedding  
2. encontra chunks relacionados a **atenção, respiração e presença**  
3. envia esses trechos ao modelo  
4. o modelo gera uma resposta baseada nesses textos  

Exemplo de contexto enviado ao modelo:

```text
A atenção plena consiste em observar o momento presente sem julgamento.

Respirar conscientemente é uma das formas mais simples de retornar ao presente.
````
---

## 🧘 Analogia simples

Podemos imaginar o RAG como um **professor consultando um livro antes de responder uma pergunta**.

1. alguém faz uma pergunta  
2. o professor procura no livro os trechos relevantes  
3. ele lê rapidamente essas partes  
4. então formula a resposta  

O modelo de linguagem faz algo semelhante: ele **consulta os textos antes de responder**.

---

## 📌 Resumo

- **RAG** significa *Retrieval Augmented Generation*  
- Combina **busca de informação** com **geração de texto**  
- O sistema recupera trechos relevantes antes de responder  
- As respostas passam a ser baseadas nos **textos carregados**

Essa arquitetura permite que o Chizu funcione como um **assistente capaz de responder perguntas sobre os livros presentes no sistema**.
