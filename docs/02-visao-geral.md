# Visão Geral

O Chizu é um chatbot baseado em inteligência artificial capaz de responder perguntas a partir de uma base textual previamente organizada.

Ele combina técnicas modernas de processamento de linguagem natural com uma arquitetura simples, modular e escalável.

---

## O que o Chizu faz?

De forma resumida, o Chizu:

1. Recebe uma pergunta do usuário.
2. Analisa semanticamente essa pergunta.
3. Busca, em sua base de textos, os trechos mais relacionados.
4. Monta um contexto.
5. Envia esse contexto para um modelo de linguagem.
6. Retorna uma resposta clara e contextualizada.

---

## Componentes principais

- **Backend**, parte do sistema que roda no servidor e controla toda a lógica.
- **API**, interface que permite que aplicações externas façam perguntas.
- **Modelos de linguagem**, inteligências artificiais capazes de compreender texto.
- **Embeddings**, vetores numéricos que representam o significado das palavras.
- **Busca semântica**, mecanismo que encontra informações por similaridade de sentido.

---

## Por que usar embeddings?

Buscas tradicionais trabalham com palavras-chave.  
O Chizu trabalha com **significado**.

Isso permite que:

> Perguntas diferentes, mas com o mesmo sentido, produzam boas respostas.

Exemplo:

- "O que é mente zen?"
- "Explique o conceito de mente zen"

Mesmo usando palavras diferentes, o sistema encontra os textos corretos.

---

## Onde o Chizu roda?

O Chizu funciona como uma aplicação web hospedada em um servidor, utilizando:

- FastAPI, framework web moderno em Python.
- Render, plataforma de hospedagem.
- ngrok, ferramenta para testes locais de acesso remoto.